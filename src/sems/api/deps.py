"""Shared API dependencies: lazy loading of the trained model and building an observation from user input."""

from __future__ import annotations

import os
from functools import lru_cache

import numpy as np
from stable_baselines3 import PPO

from sems.api.schemas import ProcessInputs
from sems.config import ACTION_KEYS, ACTION_SPACE, RANDOM_SEED
from sems.env import OBS_KEYS
from sems.simulator import StepResult, simulate_step

MODEL_PATH = os.environ.get("SEMS_MODEL_PATH", "models/ppo_khorasan.zip")

_rng = np.random.default_rng(RANDOM_SEED)


@lru_cache(maxsize=1)
def get_model() -> PPO | None:
    """Lazy loading of the PPO model; returns None if there is no model file (baseline fallback)."""
    if not os.path.exists(MODEL_PATH):
        return None
    return PPO.load(MODEL_PATH)


def model_status() -> str:
    return "trained_ppo_model" if get_model() is not None else "fallback_baseline_no_trained_model"


def inputs_to_disturbances_prices(inputs: ProcessInputs) -> tuple[dict, dict]:
    """Convert the API request input into the disturbances/prices dictionaries required by the simulator."""
    disturbances = {
        "feed_flow": inputs.feed_flow,
        "feed_composition": {
            "CH4": inputs.feed_CH4,
            "C2H6": inputs.feed_C2H6,
            "C3H8": inputs.feed_C3H8,
            "N2": inputs.feed_N2,
            "CO2": inputs.feed_CO2,
        },
        "coking_factor": inputs.coking_factor,
        "ambient_temp": inputs.ambient_temp,
    }
    prices = {
        "gas": inputs.gas_price,
        "electricity": inputs.electricity_price,
        "ammonia": inputs.ammonia_price,
        "urea": inputs.urea_price,
        "melamine": inputs.melamine_price,
        "carbon": inputs.carbon_price,
    }
    return disturbances, prices


def build_observation(inputs: ProcessInputs) -> tuple[np.ndarray, dict, dict]:
    """Build the observation vector per OBS_KEYS from user input + previous/mid-range action."""
    disturbances, prices = inputs_to_disturbances_prices(inputs)
    previous_action = inputs.previous_action or {
        key: (lo + hi) / 2 for key, (lo, hi) in ACTION_SPACE.items()
    }

    result = simulate_step(previous_action, disturbances, prices, _rng, add_noise=False)
    obs_array = np.array([result.observation[k] for k in OBS_KEYS], dtype=np.float32)
    return obs_array, disturbances, prices


def recommend_action(inputs: ProcessInputs) -> tuple[dict[str, float], str]:
    """Suggest the next control action based on the trained model (or baseline if there is no model)."""
    model = get_model()
    obs_array, _disturbances, _prices = build_observation(inputs)

    if model is not None:
        raw_action, _ = model.predict(obs_array, deterministic=True)
        action = {k: float(v) for k, v in zip(ACTION_KEYS, raw_action)}
    else:
        action = {key: (lo + hi) / 2 for key, (lo, hi) in ACTION_SPACE.items()}

    return action, model_status()


def evaluate_recommendation(inputs: ProcessInputs) -> tuple[dict[str, float], StepResult, str]:
    """Suggest an action + simulate the result of applying it to current conditions (for /recommend and /alerts)."""
    action, status_str = recommend_action(inputs)
    disturbances, prices = inputs_to_disturbances_prices(inputs)
    result = simulate_step(action, disturbances, prices, _rng, add_noise=False)
    return action, result, status_str
