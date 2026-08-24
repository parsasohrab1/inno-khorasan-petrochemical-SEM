import math

import numpy as np
import pytest

from sems.config import ACTION_SPACE
from sems.simulator import (
    clip_action,
    count_violations,
    sample_action,
    sample_disturbances,
    sample_prices,
    simulate_step,
)


@pytest.fixture
def rng() -> np.random.Generator:
    return np.random.default_rng(0)


def test_sample_action_within_bounds(rng):
    action = sample_action(rng)
    for key, (lo, hi) in ACTION_SPACE.items():
        assert lo <= action[key] <= hi


def test_clip_action_clamps_out_of_range_values():
    action = {key: hi + 1000 for key, (_lo, hi) in ACTION_SPACE.items()}
    clipped = clip_action(action)
    for key, (_lo, hi) in ACTION_SPACE.items():
        assert clipped[key] == pytest.approx(hi)


def test_count_violations_detects_out_of_range():
    action = {key: hi + 1000 for key, (_lo, hi) in ACTION_SPACE.items()}
    assert count_violations(action) == len(ACTION_SPACE)

    ok_action = {key: (lo + hi) / 2 for key, (lo, hi) in ACTION_SPACE.items()}
    assert count_violations(ok_action) == 0


def test_simulate_step_produces_finite_sane_outputs(rng):
    disturbances = sample_disturbances(rng)
    prices = sample_prices(rng)
    action = {key: (lo + hi) / 2 for key, (lo, hi) in ACTION_SPACE.items()}

    result = simulate_step(action, disturbances, prices, rng)

    for key, value in result.observation.items():
        assert math.isfinite(value), f"{key} is not finite: {value}"

    assert 0 < result.observation["ammonia_flow"] < 100
    assert 0 < result.observation["urea_flow"] < 100
    assert result.observation["total_emissions"] >= 0
    assert result.violations == 0


def test_simulate_step_penalizes_violations(rng):
    disturbances = sample_disturbances(rng)
    prices = sample_prices(rng)
    ok_action = {key: (lo + hi) / 2 for key, (lo, hi) in ACTION_SPACE.items()}
    bad_action = {key: hi + 1000 for key, (_lo, hi) in ACTION_SPACE.items()}

    ok_result = simulate_step(ok_action, disturbances, prices, np.random.default_rng(1), add_noise=False)
    bad_result = simulate_step(bad_action, disturbances, prices, np.random.default_rng(1), add_noise=False)

    assert bad_result.violations == len(ACTION_SPACE)
    assert bad_result.profit < ok_result.profit
