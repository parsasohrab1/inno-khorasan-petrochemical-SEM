"""
Reinforcement learning environment (Gymnasium) for dynamic optimization of energy consumption at
Khorasan Petrochemical, per the state space (section 2-3) and action space (section 2-4-1) of the SRS.

Each environment step is equivalent to a 15-minute decision interval (see ``config.DECISION_STEP_MINUTES``)
and each episode simulates one complete operating day (``config.STEPS_PER_EPISODE`` steps).
.
"""

from __future__ import annotations

from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium import spaces

from sems.config import (
    ACTION_KEYS,
    ACTION_SPACE,
    OPERATING_LIMITS,
    RANDOM_SEED,
    STEPS_PER_EPISODE,
)
from sems.simulator import sample_disturbances, sample_prices, simulate_step

# Reward scaling: raw profit in millions of rials (for numerical stability of RL training).
REWARD_SCALE = 1.0e-6

# Fixed order of observation variables (state section) - all members of the output of simulate_step except
# duplicate action keys, which are returned in the observation with the prefix action_ and
# count as part of the "previous state" and not the prediction target.
OBS_KEYS = [
    "feed_flow", "feed_CH4", "feed_C2H6", "feed_C3H8", "feed_N2", "feed_CO2",
    "coking_factor", "ambient_temp",
    "syngas_flow", "H2_fraction", "N2_fraction", "CH4_fraction", "Ar_fraction",
    "steam_flow", "reformer_efficiency", "reformer_energy",
    "T_ammonia_reactor", "ammonia_flow", "ammonia_conversion", "compressor_power",
    "H2_N2_ratio", "urea_flow", "melamine_flow", "total_emissions",
    "SEC_ammonia", "SEC_urea",
    "gas_price", "electricity_price", "ammonia_price", "urea_price",
    "melamine_price", "carbon_price",
] + [f"action_{k}" for k in ACTION_KEYS]


class KhorasanEnergyEnv(gym.Env):
    """RL environment for optimizing the Khorasan Petrochemical ammonia-urea-melamine chain."""

    metadata = {"render_modes": []}

    def __init__(self, seed: int = RANDOM_SEED, steps_per_episode: int = STEPS_PER_EPISODE):
        super().__init__()
        self.steps_per_episode = steps_per_episode
        self._rng = np.random.default_rng(seed)

        low = np.array([ACTION_SPACE[k][0] for k in ACTION_KEYS], dtype=np.float32)
        high = np.array([ACTION_SPACE[k][1] for k in ACTION_KEYS], dtype=np.float32)
        self.action_space = spaces.Box(low=low, high=high, dtype=np.float32)

        # The observation range is defined as unbounded (±infinity) because some variables
        # (such as prices or emissions) have no strict physical bound in this simple model;
        # normalization, if needed, should be done in the training layer.
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(len(OBS_KEYS),), dtype=np.float32
        )

        self._disturbances: dict[str, Any] | None = None
        self._prices: dict[str, float] | None = None
        self._step_idx = 0
        self._last_obs_dict: dict[str, float] = {}

    @property
    def last_observation(self) -> dict[str, float]:
        """The latest complete observation as a dictionary (for reporting/API)."""
        return dict(self._last_obs_dict)

    def _obs_dict_to_array(self, obs_dict: dict[str, float]) -> np.ndarray:
        return np.array([obs_dict[k] for k in OBS_KEYS], dtype=np.float32)

    def _drift_disturbances(self) -> None:
        """Gradual update of slowly changing disturbances during one operating day."""
        assert self._disturbances is not None
        d = self._disturbances

        d["coking_factor"] = float(
            np.clip(d["coking_factor"] + self._rng.normal(0, 0.005), 0.0, 0.3)
        )
        feed_lo, feed_hi = OPERATING_LIMITS["feed_gas_flow"]
        d["feed_flow"] = float(
            np.clip(d["feed_flow"] + self._rng.normal(0, 1000), feed_lo, feed_hi)
        )

        # Diurnal ambient temperature fluctuation around the episode's initial value
        amb_lo, amb_hi = OPERATING_LIMITS["ambient_temp"]
        phase = 2 * np.pi * self._step_idx / self.steps_per_episode
        diurnal = 5.0 * np.sin(phase)
        d["ambient_temp"] = float(np.clip(d["_ambient_base"] + diurnal, amb_lo, amb_hi))

    def reset(
        self, *, seed: int | None = None, options: dict | None = None
    ) -> tuple[np.ndarray, dict]:
        super().reset(seed=seed)
        if seed is not None:
            self._rng = np.random.default_rng(seed)

        self._step_idx = 0
        self._disturbances = sample_disturbances(self._rng)
        self._disturbances["_ambient_base"] = self._disturbances["ambient_temp"]
        self._prices = sample_prices(self._rng)

        # The mid-range action as the initial action for building the first observation
        mid_action = {k: (lo + hi) / 2 for k, (lo, hi) in ACTION_SPACE.items()}
        result = simulate_step(mid_action, self._disturbances, self._prices, self._rng)
        self._last_obs_dict = result.observation

        return self._obs_dict_to_array(result.observation), {"profit": result.profit}

    def step(self, action: np.ndarray) -> tuple[np.ndarray, float, bool, bool, dict]:
        assert self._disturbances is not None and self._prices is not None
        action_dict = {k: float(v) for k, v in zip(ACTION_KEYS, action)}

        self._drift_disturbances()
        result = simulate_step(action_dict, self._disturbances, self._prices, self._rng)
        self._last_obs_dict = result.observation

        self._step_idx += 1
        terminated = False
        truncated = self._step_idx >= self.steps_per_episode

        reward = result.profit * REWARD_SCALE

        info = {
            "profit": result.profit,
            "revenue": result.revenue,
            "energy_cost": result.energy_cost,
            "carbon_cost": result.carbon_cost,
            "violations": result.violations,
            "SEC_ammonia": result.observation["SEC_ammonia"],
            "SEC_urea": result.observation["SEC_urea"],
            "total_emissions": result.observation["total_emissions"],
            "reformer_energy": result.observation["reformer_energy"],
        }

        return (
            self._obs_dict_to_array(result.observation),
            float(reward),
            terminated,
            truncated,
            info,
        )
