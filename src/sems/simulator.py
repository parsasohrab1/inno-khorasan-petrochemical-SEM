"""
هسته شبیه‌سازی فیزیک-آگاه فرآیندهای پتروشیمی خراسان.

این ماژول منطق ریاضی مشترکی را در بر می‌گیرد که هم برای تولید دیتاست سنتتیک
(``data_generator.py``) و هم برای محیط یادگیری تقویتی گام‌به‌گام (``env.py``)
استفاده می‌شود، تا فیزیک شبیه‌سازی فقط یک‌بار نوشته و نگهداری شود.

مدل‌ها ساده‌شده و تقریبی‌اند (موازنه جرم/انرژی درجه‌یک، نه شبیه‌سازی فرآیندی
دقیق CFD/ترمودینامیکی)؛ هدف تولید رفتاری فیزیکاً معقول و پاسخگو به اقدامات
کنترلی برای آموزش عامل RL است، نه جایگزینی برای شبیه‌سازهای فرآیندی صنعتی
(مثل Aspen HYSYS/Plus).

سه اقدام «control_valve_pct»، «heat_recovery_ratio_pct» و «aux_fuel_pct» در
سند SRS (بخش ۲-۴-۱) وجود دارند اما تجهیزات متناظرشان در منابع اولیه پروژه
مدل فیزیکی تفصیلی نداشتند؛ این‌جا با ضرایب ساده و مستندشده به مدل انرژی/بازده
متصل شده‌اند (به کامنت‌های APPROX در کد مراجعه کنید).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from sems.config import (
    ACTION_SPACE,
    DISTURBANCE_RANGES,
    OPERATING_LIMITS,
    PRICE_RANGES,
)


def _add_noise(
    rng: np.random.Generator,
    value: float,
    noise_std: float = 0.01,
    min_val: float | None = None,
    max_val: float | None = None,
) -> float:
    """افزودن نویز گاوسی نسبی با محدودسازی اختیاری."""
    noisy = value + rng.normal(0.0, noise_std * abs(value) + 1e-9)
    if min_val is not None:
        noisy = max(noisy, min_val)
    if max_val is not None:
        noisy = min(noisy, max_val)
    return noisy


def sample_feed_composition(rng: np.random.Generator) -> dict[str, float]:
    composition = {
        "CH4": rng.uniform(*DISTURBANCE_RANGES["feed_composition_CH4"]),
        "C2H6": rng.uniform(*DISTURBANCE_RANGES["feed_composition_C2H6"]),
        "C3H8": rng.uniform(*DISTURBANCE_RANGES["feed_composition_C3H8"]),
        "N2": rng.uniform(*DISTURBANCE_RANGES["feed_composition_N2"]),
        "CO2": rng.uniform(*DISTURBANCE_RANGES["feed_composition_CO2"]),
    }
    total = sum(composition.values())
    return {k: v / total for k, v in composition.items()}


def sample_disturbances(rng: np.random.Generator) -> dict[str, Any]:
    """نمونه‌برداری کامل اختلالات غیرقابل‌کنترل یک گام/روز."""
    return {
        "feed_composition": sample_feed_composition(rng),
        "coking_factor": rng.uniform(*DISTURBANCE_RANGES["coking_factor"]),
        "ambient_temp": rng.uniform(*OPERATING_LIMITS["ambient_temp"]),
        "feed_flow": rng.uniform(*OPERATING_LIMITS["feed_gas_flow"]),
    }


def sample_prices(rng: np.random.Generator) -> dict[str, float]:
    return {
        "gas": rng.uniform(*PRICE_RANGES["gas_price"]),
        "electricity": rng.uniform(*PRICE_RANGES["electricity_price"]),
        "ammonia": rng.uniform(*PRICE_RANGES["ammonia_price"]),
        "urea": rng.uniform(*PRICE_RANGES["urea_price"]),
        "melamine": rng.uniform(*PRICE_RANGES["melamine_price"]),
        "carbon": rng.uniform(*PRICE_RANGES["carbon_credit_price"]),
    }


def sample_action(rng: np.random.Generator) -> dict[str, float]:
    """نمونه‌برداری تصادفی از فضای اقدام (برای دیتاست سنتتیک یا baseline)."""
    return {key: rng.uniform(lo, hi) for key, (lo, hi) in ACTION_SPACE.items()}


def clip_action(action: dict[str, float]) -> dict[str, float]:
    """اطمینان از قرارگیری هر بعد اقدام درون بازه مجاز فضای اقدام."""
    clipped = {}
    for key, (lo, hi) in ACTION_SPACE.items():
        clipped[key] = float(np.clip(action.get(key, (lo + hi) / 2), lo, hi))
    return clipped


def count_violations(action: dict[str, float], tol: float = 1e-6) -> int:
    """شمارش ابعادی از اقدام خام که پیش از کلیپ‌شدن خارج از محدوده بوده‌اند."""
    violations = 0
    for key, (lo, hi) in ACTION_SPACE.items():
        value = action.get(key)
        if value is None:
            continue
        if value < lo - tol or value > hi + tol:
            violations += 1
    return violations


def _simulate_reformer(
    feed_flow: float,
    action: dict[str, float],
    feed_composition: dict[str, float],
    coking_factor: float,
) -> dict[str, float]:
    """شبیه‌سازی ریفرمر بر اساس موازنه جرم و انرژی ساده‌شده."""
    S_C_ratio = action["S_C_ratio"]
    T_primary = action["T_primary_reformer"]
    T_secondary = action["T_secondary_reformer"]
    secondary_air_pct = action["secondary_air_pct"]
    heat_recovery_ratio_pct = action["heat_recovery_ratio_pct"]
    aux_fuel_pct = action["aux_fuel_pct"]
    control_valve_pct = action["control_valve_pct"]

    steam_flow = feed_flow * S_C_ratio * 0.012

    # اثر کک‌زدگی بر راندمان
    efficiency_factor = 1.0 - coking_factor * 0.3
    # APPROX: شیرهای کنترلی کاملاً باز (100%) بهینه فرض می‌شوند؛ بسته‌بودن جزئی
    # افت فشار/راندمان کوچکی ایجاد می‌کند.
    efficiency_factor *= 0.95 + 0.05 * (control_valve_pct / 100.0)

    # بازده تبدیل متان بر اساس دما (مدل ساده آرنیوس)
    k_primary = 0.85 * (1 + 0.003 * (T_primary - 800)) * efficiency_factor
    # APPROX: دبی هوای ریفرمر ثانویه حول یک مقدار اسمی نوسان می‌کند؛ کمبود هوا
    # نسبت به اسمی، تبدیل ثانویه را کاهش می‌دهد.
    air_ratio = secondary_air_pct / 75.0  # 75% ≈ نقطه اسمی
    k_secondary = (
        0.92 * (1 + 0.002 * (T_secondary - 1000)) * efficiency_factor
        * (0.9 + 0.1 * np.clip(air_ratio, 0.5, 1.5))
    )

    # ترکیب گاز سنتز
    H2_fraction = 0.60 + 0.02 * (T_primary - 800) / 50 + 0.01 * (1 - coking_factor)
    N2_fraction = 0.20 + 0.01 * (feed_composition["N2"] - 0.02) / 0.01
    CH4_fraction = 0.15 - 0.02 * (T_primary - 800) / 50 - 0.01 * k_primary
    Ar_fraction = 0.02 + 0.01 * (feed_composition["N2"] - 0.02) / 0.01

    total = H2_fraction + N2_fraction + CH4_fraction + Ar_fraction
    H2_fraction /= total
    N2_fraction /= total
    CH4_fraction /= total
    Ar_fraction /= total

    # APPROX: سوخت کمکی، ظرفیت تبدیل گاز سنتز را افزایش می‌دهد اما مصرف
    # انرژی و انتشار را نیز بالا می‌برد (رجوع کنید به _calculate_emissions).
    aux_boost = 1.0 + 0.05 * (aux_fuel_pct / 100.0)

    energy_consumption = feed_flow * 2.5 * (1 - 0.1 * coking_factor)
    # APPROX: بازیابی حرارت بخشی از انرژی مصرفی خالص را جبران می‌کند.
    heat_recovery_savings = 0.15 * (heat_recovery_ratio_pct - 50) / 40
    energy_consumption *= (1 - np.clip(heat_recovery_savings, 0.0, 0.15))
    energy_consumption += aux_fuel_pct / 100.0 * 0.05 * feed_flow / 1000.0

    return {
        "syngas_flow": feed_flow * 1.8 * efficiency_factor * aux_boost,
        "H2_fraction": H2_fraction,
        "N2_fraction": N2_fraction,
        "CH4_fraction": CH4_fraction,
        "Ar_fraction": Ar_fraction,
        "steam_flow": steam_flow,
        "energy_consumption": energy_consumption,
        "efficiency": k_primary * k_secondary,
    }


def _compute_reactor_temp(rng: np.random.Generator, T_secondary: float) -> float:
    T_reactor = 400 + 0.5 * (T_secondary - 950) + rng.normal(0, 5)
    return float(np.clip(T_reactor, 380, 500))


def _simulate_ammonia_synthesis(
    syngas_flow: float,
    H2_fraction: float,
    N2_fraction: float,
    P_reactor: float,
    T_reactor: float,
    compressor_speed_pct: float,
) -> dict[str, float]:
    """شبیه‌سازی سنتز آمونیاک با سینتیک واکنش ساده‌شده."""
    H2_N2_ratio = H2_fraction / N2_fraction if N2_fraction > 0 else 3.0

    conversion = 0.85 * (1 + 0.005 * (P_reactor - 180) / 10) * (
        1 - 0.008 * (T_reactor - 450) / 10
    )
    conversion = float(np.clip(conversion, 0.4, 0.98))

    ammonia_flow = syngas_flow * 0.15 * conversion * (H2_N2_ratio / 3.0) * 0.8
    compressor_power = (
        20 * (P_reactor / 180) * (syngas_flow / 100_000) * (compressor_speed_pct / 100.0)
    )

    return {
        "ammonia_flow": float(np.clip(ammonia_flow, 20, 55)),
        "conversion": conversion,
        "compressor_power": compressor_power,
        "H2_N2_ratio": H2_N2_ratio,
    }


def _simulate_urea_production(ammonia_flow: float, co2_availability: float) -> float:
    urea_flow = ammonia_flow * 0.75 * co2_availability * 0.92
    return float(np.clip(urea_flow, 35, 70))


def _simulate_melamine_production(ammonia_flow: float, urea_flow: float) -> float:
    urea_for_melamine = min(urea_flow * 0.15, 3.5)
    melamine_flow = urea_for_melamine * 0.28
    return float(np.clip(melamine_flow, 0.5, 3.5))


def _calculate_emissions(
    feed_flow: float, energy_consumption: float, efficiency: float, aux_fuel_pct: float
) -> float:
    combustion_co2 = feed_flow * 0.002 * (1 - efficiency * 0.1)
    process_co2 = feed_flow * 0.0005
    # APPROX: سوخت کمکی احتراق اضافه‌ای تولید می‌کند.
    aux_co2 = aux_fuel_pct / 100.0 * feed_flow * 0.0003
    return combustion_co2 + process_co2 + aux_co2


@dataclass
class StepResult:
    """خروجی کامل یک گام شبیه‌سازی، شامل حالت، اقتصاد و پاداش."""

    observation: dict[str, float]
    profit: float
    revenue: float
    energy_cost: float
    carbon_cost: float
    violations: int
    raw: dict[str, float] = field(default_factory=dict)


def simulate_step(
    action: dict[str, float],
    disturbances: dict[str, Any],
    prices: dict[str, float],
    rng: np.random.Generator,
    add_noise: bool = True,
) -> StepResult:
    """
    اجرای یک گام کامل شبیه‌سازی زنجیره تولید: ریفرمر → سنتز آمونیاک → اوره →
    ملامین → انتشار → اقتصاد. ``action`` باید شامل تمام کلیدهای
    ``config.ACTION_SPACE`` باشد (خام، قبل یا بعد از کلیپ).
    """
    raw_action = dict(action)
    violations = count_violations(raw_action)
    clipped_action = clip_action(raw_action)

    feed_flow = disturbances["feed_flow"]
    feed_composition = disturbances["feed_composition"]
    coking_factor = disturbances["coking_factor"]

    reformer = _simulate_reformer(feed_flow, clipped_action, feed_composition, coking_factor)

    T_reactor = _compute_reactor_temp(rng, clipped_action["T_secondary_reformer"])
    ammonia = _simulate_ammonia_synthesis(
        reformer["syngas_flow"],
        reformer["H2_fraction"],
        reformer["N2_fraction"],
        clipped_action["P_ammonia_reactor"],
        T_reactor,
        clipped_action["compressor_speed_pct"],
    )
    ammonia_flow = ammonia["ammonia_flow"]

    co2_availability = 0.85 + 0.1 * (feed_composition["CO2"] / 0.02)
    urea_flow = _simulate_urea_production(ammonia_flow, co2_availability)
    melamine_flow = _simulate_melamine_production(ammonia_flow, urea_flow)

    total_emissions = _calculate_emissions(
        feed_flow, reformer["energy_consumption"], reformer["efficiency"],
        clipped_action["aux_fuel_pct"],
    )

    sec_ammonia = reformer["energy_consumption"] / max(ammonia_flow, 1e-6)
    sec_urea = (reformer["energy_consumption"] * 0.4) / max(urea_flow, 1e-6)

    revenue = (
        ammonia_flow * prices["ammonia"]
        + urea_flow * prices["urea"]
        + melamine_flow * prices["melamine"]
    )
    energy_cost = (
        feed_flow * prices["gas"] * 0.001
        + ammonia["compressor_power"] * 1000 * prices["electricity"] * 0.001
    )
    carbon_cost = total_emissions * prices["carbon"]
    profit = revenue - energy_cost - carbon_cost - violations * 5_000_000.0

    observation = {
        "feed_flow": feed_flow,
        "feed_CH4": feed_composition["CH4"],
        "feed_C2H6": feed_composition["C2H6"],
        "feed_C3H8": feed_composition["C3H8"],
        "feed_N2": feed_composition["N2"],
        "feed_CO2": feed_composition["CO2"],
        "coking_factor": coking_factor,
        "ambient_temp": disturbances["ambient_temp"],
        **{f"action_{k}": v for k, v in clipped_action.items()},
        "syngas_flow": reformer["syngas_flow"],
        "H2_fraction": reformer["H2_fraction"],
        "N2_fraction": reformer["N2_fraction"],
        "CH4_fraction": reformer["CH4_fraction"],
        "Ar_fraction": reformer["Ar_fraction"],
        "steam_flow": reformer["steam_flow"],
        "reformer_efficiency": reformer["efficiency"],
        "reformer_energy": reformer["energy_consumption"],
        "T_ammonia_reactor": T_reactor,
        "ammonia_flow": ammonia_flow,
        "ammonia_conversion": ammonia["conversion"],
        "compressor_power": ammonia["compressor_power"],
        "H2_N2_ratio": ammonia["H2_N2_ratio"],
        "urea_flow": urea_flow,
        "melamine_flow": melamine_flow,
        "total_emissions": total_emissions,
        "SEC_ammonia": sec_ammonia,
        "SEC_urea": sec_urea,
        "gas_price": prices["gas"],
        "electricity_price": prices["electricity"],
        "ammonia_price": prices["ammonia"],
        "urea_price": prices["urea"],
        "melamine_price": prices["melamine"],
        "carbon_price": prices["carbon"],
    }

    if add_noise:
        for key, value in list(observation.items()):
            if isinstance(value, (int, float)):
                observation[key] = _add_noise(rng, float(value), noise_std=0.01)

    return StepResult(
        observation=observation,
        profit=float(profit),
        revenue=float(revenue),
        energy_cost=float(energy_cost),
        carbon_cost=float(carbon_cost),
        violations=violations,
        raw=raw_action,
    )
