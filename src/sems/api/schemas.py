"""مدل‌های Pydantic ورودی/خروجی API - منطبق با جداول بخش ۲-۳ و ۲-۴ سند SRS."""

from __future__ import annotations

from pydantic import BaseModel, Field

from sems.config import ACTION_SPACE, OPERATING_LIMITS


class ProcessInputs(BaseModel):
    """داده‌های عملیاتی و اقتصادی لحظه‌ای (بخش ۲-۳-۱ و ۲-۳-۲ SRS)."""

    feed_flow: float = Field(
        default=100_000.0, description="دبی خوراک گاز طبیعی ورودی (Nm3/h)",
        ge=OPERATING_LIMITS["feed_gas_flow"][0] * 0.5,
        le=OPERATING_LIMITS["feed_gas_flow"][1] * 1.5,
    )
    feed_CH4: float = Field(default=0.90, ge=0, le=1)
    feed_C2H6: float = Field(default=0.05, ge=0, le=1)
    feed_C3H8: float = Field(default=0.02, ge=0, le=1)
    feed_N2: float = Field(default=0.02, ge=0, le=1)
    feed_CO2: float = Field(default=0.01, ge=0, le=1)
    coking_factor: float = Field(default=0.1, ge=0, le=0.3, description="ضریب کک‌زدگی کویل ریفرمر")
    ambient_temp: float = Field(default=25.0, description="دمای محیط (°C)")

    gas_price: float = Field(default=6_500.0, description="قیمت گاز طبیعی خوراک (IRR/Nm3)")
    electricity_price: float = Field(default=1_100.0, description="قیمت برق مصرفی (IRR/kWh)")
    ammonia_price: float = Field(default=21_000.0, description="قیمت فروش آمونیاک (IRR/ton)")
    urea_price: float = Field(default=15_000.0, description="قیمت فروش اوره (IRR/ton)")
    melamine_price: float = Field(default=52_000.0, description="قیمت فروش ملامین (IRR/ton)")
    carbon_price: float = Field(default=1_000.0, description="قیمت گواهی کاهش انتشار کربن (IRR/ton CO2)")

    previous_action: dict[str, float] | None = Field(
        default=None,
        description="اقدام کنترلی قبلی (برای ساخت مشاهده کامل عامل)؛ در نبود آن مقدار میانی بازه استفاده می‌شود.",
    )


class RecommendResponse(BaseModel):
    recommended_action: dict[str, float]
    predicted_profit_IRR: float
    predicted_SEC_ammonia: float
    predicted_SEC_urea: float
    predicted_total_emissions_ton: float
    alerts: list[dict]
    model_status: str


class ForecastResponse(BaseModel):
    decision_interval_minutes: int
    horizon_steps: int
    total_predicted_energy_GJ: float
    total_predicted_emissions_ton: float
    total_predicted_profit_IRR: float
    predicted_energy_GJ_per_step: list[float]
    predicted_emissions_ton_per_step: list[float]
    method: str
    model_status: str


class AlertsResponse(BaseModel):
    alerts: list[dict]


class ReportResponse(BaseModel):
    period: str
    steps: int
    agent: dict
    baseline_fixed_action: dict
    profit_uplift_pct_vs_baseline: float
    emissions_reduction_pct_vs_baseline: float
    note: str


class ActionSpaceInfo(BaseModel):
    action_space: dict[str, tuple[float, float]] = Field(default_factory=lambda: dict(ACTION_SPACE))


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
