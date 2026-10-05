"""
24-hour horizon forecasting of energy consumption/CO₂ emissions, inefficiency detection and preventive alerting
(section 2-4-2 of the SRS, rows 12 to 15).

Forecasting method: Monte-Carlo rollout of the physics-informed simulator with the agent policy (or
the baseline policy in the absence of a trained model) over the desired horizon. This is a forecast based on the
simulation model, not a statistical regression on real historical data; its accuracy depends on how well
the simulator matches the real plant process.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from stable_baselines3 import PPO

from sems.config import (
    DECISION_STEP_MINUTES,
    RANDOM_SEED,
    SEC_ALERT_DEVIATION_PCT,
    SEC_TARGET_AMMONIA_GJ_PER_TON,
    SEC_TARGET_UREA_GJ_PER_TON,
    STEPS_PER_EPISODE,
)
from sems.env import KhorasanEnergyEnv


def _policy_from_model(model: PPO | None):
    if model is None:
        from sems.evaluate import baseline_policy

        return baseline_policy

    def _policy(obs: np.ndarray) -> np.ndarray:
        action, _ = model.predict(obs, deterministic=True)
        return action

    return _policy


def forecast_horizon(
    model: PPO | None = None,
    steps: int = STEPS_PER_EPISODE,
    seed: int | None = None,
) -> dict[str, Any]:
    """Forecast energy consumption and CO₂ emissions for ``steps`` future decision steps."""
    env = KhorasanEnergyEnv(seed=seed if seed is not None else RANDOM_SEED, steps_per_episode=steps)
    policy = _policy_from_model(model)

    obs, _ = env.reset()
    energy_series: list[float] = []
    emissions_series: list[float] = []
    profit_series: list[float] = []

    done = truncated = False
    while not (done or truncated):
        action = policy(obs)
        obs, _reward, done, truncated, info = env.step(action)
        energy_series.append(info["reformer_energy"])
        emissions_series.append(info["total_emissions"])
        profit_series.append(info["profit"])

    return {
        "decision_interval_minutes": DECISION_STEP_MINUTES,
        "horizon_steps": len(energy_series),
        "predicted_energy_GJ_per_step": energy_series,
        "predicted_emissions_ton_per_step": emissions_series,
        "predicted_profit_IRR_per_step": profit_series,
        "total_predicted_energy_GJ": float(np.sum(energy_series)),
        "total_predicted_emissions_ton": float(np.sum(emissions_series)),
        "total_predicted_profit_IRR": float(np.sum(profit_series)),
        "method": "physics_informed_monte_carlo_rollout",
    }


def detect_inefficiency(sec_ammonia: float, sec_urea: float) -> list[dict[str, Any]]:
    """Detect energy inefficiency by comparing instantaneous SEC with the target indicator (section 1-2 of the SRS)."""
    alerts = []

    dev_ammonia_pct = (sec_ammonia - SEC_TARGET_AMMONIA_GJ_PER_TON) / SEC_TARGET_AMMONIA_GJ_PER_TON * 100.0
    if dev_ammonia_pct > SEC_ALERT_DEVIATION_PCT:
        alerts.append(
            {
                "unit": "Ammonia",
                "metric": "SEC_ammonia",
                "current": sec_ammonia,
                "target": SEC_TARGET_AMMONIA_GJ_PER_TON,
                "deviation_pct": dev_ammonia_pct,
                "severity": "High" if dev_ammonia_pct > 2 * SEC_ALERT_DEVIATION_PCT else "Medium",
                "message": f"The ammonia unit's specific energy consumption is {dev_ammonia_pct:.1f}% above the target.",
            }
        )

    dev_urea_pct = (sec_urea - SEC_TARGET_UREA_GJ_PER_TON) / SEC_TARGET_UREA_GJ_PER_TON * 100.0
    if dev_urea_pct > SEC_ALERT_DEVIATION_PCT:
        alerts.append(
            {
                "unit": "Urea",
                "metric": "SEC_urea",
                "current": sec_urea,
                "target": SEC_TARGET_UREA_GJ_PER_TON,
                "deviation_pct": dev_urea_pct,
                "severity": "High" if dev_urea_pct > 2 * SEC_ALERT_DEVIATION_PCT else "Medium",
                "message": f"The urea unit's specific energy consumption is {dev_urea_pct:.1f}% above the target.",
            }
        )

    return alerts
