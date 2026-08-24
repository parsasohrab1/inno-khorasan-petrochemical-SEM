import numpy as np
from gymnasium.utils.env_checker import check_env

from sems.config import ACTION_SPACE, STEPS_PER_EPISODE
from sems.env import KhorasanEnergyEnv


def test_env_passes_gymnasium_checker():
    env = KhorasanEnergyEnv(seed=0, steps_per_episode=5)
    check_env(env, skip_render_check=True)


def test_reset_returns_valid_observation():
    env = KhorasanEnergyEnv(seed=0)
    obs, info = env.reset()
    assert obs.shape == env.observation_space.shape
    assert np.all(np.isfinite(obs))
    assert "profit" in info


def test_episode_truncates_after_configured_steps():
    steps = 10
    env = KhorasanEnergyEnv(seed=0, steps_per_episode=steps)
    env.reset()
    mid_action = np.array([(lo + hi) / 2 for lo, hi in ACTION_SPACE.values()], dtype=np.float32)

    truncated = False
    count = 0
    for _ in range(steps):
        _obs, _reward, terminated, truncated, _info = env.step(mid_action)
        count += 1
        if terminated or truncated:
            break

    assert truncated is True
    assert count == steps


def test_step_reward_and_info_are_sane():
    env = KhorasanEnergyEnv(seed=1)
    env.reset()
    mid_action = np.array([(lo + hi) / 2 for lo, hi in ACTION_SPACE.values()], dtype=np.float32)

    obs, reward, terminated, truncated, info = env.step(mid_action)

    assert np.all(np.isfinite(obs))
    assert np.isfinite(reward)
    assert info["violations"] == 0
    assert terminated is False
