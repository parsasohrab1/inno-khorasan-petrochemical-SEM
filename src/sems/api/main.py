"""
API سامانه مدیریت انرژی هوشمند (SEMS) پتروشیمی خراسان.

پیاده‌سازی خروجی‌های بخش ۲-۴-۲ SRS: توصیه کنترلی، پیش‌بینی مصرف انرژی/انتشار،
هشدار پیشگیرانه و گزارش دوره‌ای. توجه: این API یک نمونه نرم‌افزاری برای دمو و
توسعه است، نه یک استقرار صنعتی با تضمین ۹۹.۹۹٪ در دسترس‌بودن یا اتصال واقعی
SCADA/OPC UA (به README برای ماتریس ردیابی الزامات مراجعه کنید).
"""

from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sems.api import deps, security
from sems.api.schemas import (
    ActionSpaceInfo,
    AlertsResponse,
    ForecastResponse,
    ProcessInputs,
    RecommendResponse,
    ReportResponse,
    TokenResponse,
)
from sems.config import STEPS_PER_EPISODE
from sems.evaluate import evaluate_with_model
from sems.forecasting import detect_inefficiency, forecast_horizon

app = FastAPI(
    title="SEMS پتروشیمی خراسان",
    description="سامانه مدیریت انرژی هوشمند مبتنی بر یادگیری تقویتی",
    version="0.1.0",
)

REPORT_PERIOD_STEPS = {
    "daily": STEPS_PER_EPISODE,
    "weekly": STEPS_PER_EPISODE * 7,
    "monthly": STEPS_PER_EPISODE * 30,
}


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_status": deps.model_status()}


@app.post("/auth/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    if not security.authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="نام کاربری یا رمز عبور نادرست است")
    token = security.create_access_token(subject=form_data.username)
    return TokenResponse(access_token=token)


@app.get("/action-space", response_model=ActionSpaceInfo)
def action_space(_user: str = Depends(security.get_current_user)) -> ActionSpaceInfo:
    return ActionSpaceInfo()


@app.post("/recommend", response_model=RecommendResponse)
def recommend(
    inputs: ProcessInputs, _user: str = Depends(security.get_current_user)
) -> RecommendResponse:
    action, result, status_str = deps.evaluate_recommendation(inputs)
    alerts = detect_inefficiency(result.observation["SEC_ammonia"], result.observation["SEC_urea"])

    return RecommendResponse(
        recommended_action=action,
        predicted_profit_IRR=result.profit,
        predicted_SEC_ammonia=result.observation["SEC_ammonia"],
        predicted_SEC_urea=result.observation["SEC_urea"],
        predicted_total_emissions_ton=result.observation["total_emissions"],
        alerts=alerts,
        model_status=status_str,
    )


@app.get("/forecast/energy", response_model=ForecastResponse)
def forecast_energy(
    horizon_steps: int = STEPS_PER_EPISODE, _user: str = Depends(security.get_current_user)
) -> ForecastResponse:
    model = deps.get_model()
    result = forecast_horizon(model=model, steps=horizon_steps)
    return ForecastResponse(**result, model_status=deps.model_status())


@app.get("/forecast/emissions", response_model=ForecastResponse)
def forecast_emissions(
    horizon_steps: int = STEPS_PER_EPISODE, _user: str = Depends(security.get_current_user)
) -> ForecastResponse:
    # از همان rollout پیش‌بینی انرژی استفاده می‌شود چون هر دو خروجی یک شبیه‌سازی مشترک‌اند.
    model = deps.get_model()
    result = forecast_horizon(model=model, steps=horizon_steps)
    return ForecastResponse(**result, model_status=deps.model_status())


@app.post("/alerts", response_model=AlertsResponse)
def alerts(inputs: ProcessInputs, _user: str = Depends(security.get_current_user)) -> AlertsResponse:
    _action, result, _status_str = deps.evaluate_recommendation(inputs)
    return AlertsResponse(
        alerts=detect_inefficiency(result.observation["SEC_ammonia"], result.observation["SEC_urea"])
    )


@app.get("/report/{period}", response_model=ReportResponse)
def report(period: str, _user: str = Depends(security.get_current_user)) -> ReportResponse:
    if period not in REPORT_PERIOD_STEPS:
        raise HTTPException(
            status_code=400,
            detail=f"دوره نامعتبر. یکی از {list(REPORT_PERIOD_STEPS.keys())} را انتخاب کنید.",
        )
    steps = REPORT_PERIOD_STEPS[period]
    model = deps.get_model()
    result = evaluate_with_model(model, episodes=1, steps_per_episode=steps)
    return ReportResponse(period=period, steps=steps, **{k: v for k, v in result.items() if k != "episodes"})
