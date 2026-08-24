"""
بک‌تست عامل آموزش‌دیده در برابر یک baseline ثابت (اقدام میانی بازه مجاز)،
و محاسبه واقعی متریک‌ها (سود، SEC، انتشار) — بدون هیچ عدد از پیش‌فرض یا ادعای
دقتی که محاسبه نشده باشد.

مثال اجرا:
    python -m sems.evaluate --model-path models/ppo_khorasan.zip --episodes 20
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from stable_baselines3 import PPO

from sems.config import ACTION_KEYS, ACTION_SPACE, RANDOM_SEED
from sems.env import KhorasanEnergyEnv


def _rollout_episode(env: KhorasanEnergyEnv, policy) -> dict:
    obs, _ = env.reset()
    total_profit = 0.0
    total_emissions = 0.0
    sec_ammonia_values = []
    sec_urea_values = []
    violations = 0
    done = False
    truncated = False

    while not (done or truncated):
        action = policy(obs)
        obs, _reward, done, truncated, info = env.step(action)
        total_profit += info["profit"]
        total_emissions += info["total_emissions"]
        sec_ammonia_values.append(info["SEC_ammonia"])
        sec_urea_values.append(info["SEC_urea"])
        violations += info["violations"]

    return {
        "total_profit_IRR": total_profit,
        "total_emissions_ton": total_emissions,
        "mean_SEC_ammonia": float(np.mean(sec_ammonia_values)),
        "mean_SEC_urea": float(np.mean(sec_urea_values)),
        "constraint_violations": violations,
    }


def baseline_policy(_obs: np.ndarray) -> np.ndarray:
    """اقدام ثابت میانی بازه مجاز (بدون کنترل هوشمند) - نقطه مرجع مقایسه."""
    return np.array([(lo + hi) / 2 for lo, hi in ACTION_SPACE.values()], dtype=np.float32)


def make_agent_policy(model: PPO):
    def _policy(obs: np.ndarray) -> np.ndarray:
        action, _ = model.predict(obs, deterministic=True)
        return action

    return _policy


def evaluate_with_model(
    model: PPO | None,
    episodes: int,
    seed: int = RANDOM_SEED,
    steps_per_episode: int | None = None,
) -> dict:
    """هسته ارزیابی؛ مدل از پیش بارگذاری‌شده می‌پذیرد تا از بارگذاری مکرر دیسک در API جلوگیری شود."""
    env_kwargs = {"seed": seed}
    if steps_per_episode is not None:
        env_kwargs["steps_per_episode"] = steps_per_episode

    agent_env = KhorasanEnergyEnv(**env_kwargs)
    baseline_env = KhorasanEnergyEnv(**env_kwargs)

    agent_policy = make_agent_policy(model) if model is not None else baseline_policy

    agent_results = [_rollout_episode(agent_env, agent_policy) for _ in range(episodes)]
    baseline_results = [_rollout_episode(baseline_env, baseline_policy) for _ in range(episodes)]

    def _aggregate(results: list[dict]) -> dict:
        keys = results[0].keys()
        return {k: float(np.mean([r[k] for r in results])) for k in keys}

    agent_agg = _aggregate(agent_results)
    baseline_agg = _aggregate(baseline_results)

    profit_uplift_pct = (
        (agent_agg["total_profit_IRR"] - baseline_agg["total_profit_IRR"])
        / abs(baseline_agg["total_profit_IRR"])
        * 100.0
        if baseline_agg["total_profit_IRR"] != 0
        else float("nan")
    )
    emissions_reduction_pct = (
        (baseline_agg["total_emissions_ton"] - agent_agg["total_emissions_ton"])
        / abs(baseline_agg["total_emissions_ton"])
        * 100.0
        if baseline_agg["total_emissions_ton"] != 0
        else float("nan")
    )

    report = {
        "episodes": episodes,
        "agent": agent_agg,
        "baseline_fixed_action": baseline_agg,
        "profit_uplift_pct_vs_baseline": profit_uplift_pct,
        "emissions_reduction_pct_vs_baseline": emissions_reduction_pct,
        "note": (
            "این اعداد از بک‌تست شبیه‌ساز فیزیک-آگاه محاسبه شده‌اند، نه از داده‌های "
            "عملیاتی واقعی کارخانه؛ برای اعتبارسنجی صنعتی به کالیبراسیون با داده‌های "
            "واقعی SCADA نیاز است."
        ),
    }
    return report


def evaluate(model_path: str, episodes: int, seed: int = RANDOM_SEED) -> dict:
    """بارگذاری مدل از دیسک و اجرای ارزیابی (برای استفاده CLI)."""
    model = PPO.load(model_path)
    return evaluate_with_model(model, episodes, seed)


def main() -> None:
    parser = argparse.ArgumentParser(description="ارزیابی عامل RL در برابر baseline")
    parser.add_argument("--model-path", type=str, default="models/ppo_khorasan.zip")
    parser.add_argument("--episodes", type=int, default=20)
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--report-path", type=str, default="reports/evaluation_report.json")
    args = parser.parse_args()

    report = evaluate(args.model_path, args.episodes, args.seed)

    report_path = Path(args.report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"\n✅ گزارش در {report_path} ذخیره شد.")


if __name__ == "__main__":
    main()
