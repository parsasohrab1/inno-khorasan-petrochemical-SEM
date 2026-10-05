"""
Train the reinforcement learning agent (PPO) on the KhorasanEnergyEnv environment.

Example run:
    python -m sems.train --timesteps 100000 --model-path models/ppo_khorasan.zip
"""

from __future__ import annotations

import argparse
from pathlib import Path

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.monitor import Monitor

from sems.config import RANDOM_SEED
from sems.env import KhorasanEnergyEnv


def build_env(seed: int = RANDOM_SEED) -> Monitor:
    return Monitor(KhorasanEnergyEnv(seed=seed))


def train(timesteps: int, model_path: str, seed: int = RANDOM_SEED, n_envs: int = 1) -> PPO:
    vec_env = make_vec_env(lambda: KhorasanEnergyEnv(seed=seed), n_envs=n_envs)

    model = PPO(
        "MlpPolicy",
        vec_env,
        verbose=1,
        seed=seed,
        n_steps=256,
        batch_size=64,
    )
    model.learn(total_timesteps=timesteps, progress_bar=False)

    out_path = Path(model_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(out_path))
    print(f"\n✅ The trained model was saved in {out_path}.")
    return model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the PPO agent for SEMS")
    parser.add_argument("--timesteps", type=int, default=50_000)
    parser.add_argument("--model-path", type=str, default="models/ppo_khorasan.zip")
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--n-envs", type=int, default=1)
    args = parser.parse_args()

    train(args.timesteps, args.model_path, args.seed, args.n_envs)


if __name__ == "__main__":
    main()
