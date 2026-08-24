"""
پیش‌بینی افق ۲۴ساعته مصرف انرژی/انتشار CO₂، تشخیص ناکارآمدی و هشدار پیشگیرانه
(بخش ۲-۴-۲ SRS، ردیف‌های ۱۲ تا ۱۵).

روش پیش‌بینی: rollout مونت‌کارلوی شبیه‌ساز فیزیک-آگاه با سیاست عامل (یا سیاست
baseline در نبود مدل آموزش‌دیده) برای افق موردنظر. این یک پیش‌بینی مبتنی بر
مدل شبیه‌سازی است، نه رگرسیون آماری روی داده تاریخی واقعی؛ دقت آن به میزان
مطابقت شبیه‌ساز با فرآیند واقعی کارخانه وابسته است.
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
    """پیش‌بینی مصرف انرژی و انتشار CO₂ برای ``steps`` گام تصمیم آینده."""
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
    """تشخیص ناکارآمدی انرژی با مقایسه SEC لحظه‌ای با شاخص هدف (بخش ۱-۲ SRS)."""
    alerts = []

    dev_ammonia_pct = (sec_ammonia - SEC_TARGET_AMMONIA_GJ_PER_TON) / SEC_TARGET_AMMONIA_GJ_PER_TON * 100.0
    if dev_ammonia_pct > SEC_ALERT_DEVIATION_PCT:
        alerts.append(
            {
                "unit": "آمونیاک",
                "metric": "SEC_ammonia",
                "current": sec_ammonia,
                "target": SEC_TARGET_AMMONIA_GJ_PER_TON,
                "deviation_pct": dev_ammonia_pct,
                "severity": "بالا" if dev_ammonia_pct > 2 * SEC_ALERT_DEVIATION_PCT else "متوسط",
                "message": f"مصرف ویژه انرژی واحد آمونیاک {dev_ammonia_pct:.1f}٪ بالاتر از هدف است.",
            }
        )

    dev_urea_pct = (sec_urea - SEC_TARGET_UREA_GJ_PER_TON) / SEC_TARGET_UREA_GJ_PER_TON * 100.0
    if dev_urea_pct > SEC_ALERT_DEVIATION_PCT:
        alerts.append(
            {
                "unit": "اوره",
                "metric": "SEC_urea",
                "current": sec_urea,
                "target": SEC_TARGET_UREA_GJ_PER_TON,
                "deviation_pct": dev_urea_pct,
                "severity": "بالا" if dev_urea_pct > 2 * SEC_ALERT_DEVIATION_PCT else "متوسط",
                "message": f"مصرف ویژه انرژی واحد اوره {dev_urea_pct:.1f}٪ بالاتر از هدف است.",
            }
        )

    return alerts
