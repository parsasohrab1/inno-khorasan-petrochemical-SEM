"""
پارامترهای پیکربندی سامانه: محدودیت‌های عملیاتی، اختلالات، قیمت‌ها و فضای اقدام.
مقادیر برگرفته از سند الزامات نرم‌افزاری (SRS) بخش‌های ۱، ۲-۳ و ۲-۴.
"""

from __future__ import annotations

# طول هر گام تصمیم کنترلی. نمونه‌برداری SCADA واقعی هر ۱ ثانیه است اما آموزش
# عامل RL روی آن بازه غیرعملی است؛ بنابراین هر گام محیط معادل یک بازه تصمیم
# ۱۵ دقیقه‌ای در نظر گرفته می‌شود (فرکانس تصمیم کنترلی، نه فرکانس پایش).
DECISION_STEP_MINUTES = 15
STEPS_PER_EPISODE = 96  # یک روز کامل عملیاتی (۹۶ × ۱۵ دقیقه = ۲۴ ساعت)

# محدودیت‌های عملیاتی متغیرهای حالت/اختلال (بخش ۱ و ۲-۳ SRS)
OPERATING_LIMITS = {
    "T_primary_reformer": (750.0, 850.0),      # °C
    "T_secondary_reformer": (950.0, 1050.0),   # °C
    "P_ammonia_reactor": (120.0, 250.0),       # bar
    "S_C_ratio": (2.5, 4.0),                   # mol/mol
    "feed_gas_flow": (80_000.0, 120_000.0),    # Nm3/h
    "air_flow": (40_000.0, 60_000.0),          # Nm3/h
    "steam_flow": (120.0, 200.0),              # ton/h
    "compressor_power": (15.0, 35.0),          # MW
    "cooling_water_temp": (25.0, 40.0),        # °C
    "cooling_water_flow": (8_000.0, 15_000.0), # m3/h
    "ambient_temp": (-5.0, 45.0),              # °C
    "ammonia_production": (30.0, 45.0),        # ton/h
    "urea_production": (45.0, 65.0),           # ton/h
    "melamine_production": (1.5, 3.0),         # ton/h
}

# متغیرهای غیرقابل کنترل (اختلالات فرآیندی)
DISTURBANCE_RANGES = {
    "feed_composition_CH4": (0.85, 0.95),
    "feed_composition_C2H6": (0.02, 0.08),
    "feed_composition_C3H8": (0.01, 0.04),
    "feed_composition_N2": (0.01, 0.03),
    "feed_composition_CO2": (0.005, 0.02),
    "coking_factor": (0.0, 0.3),  # ضریب کاهش راندمان بر اثر کک‌زدگی کویل‌های ریفرمر
}

# بازه قیمت‌ها (ریال) - بخش ۲-۳-۲ SRS
PRICE_RANGES = {
    "gas_price": (5_000.0, 8_000.0),          # IRR/Nm3
    "electricity_price": (800.0, 1_500.0),    # IRR/kWh
    "ammonia_price": (18_000.0, 25_000.0),    # IRR/ton
    "urea_price": (12_000.0, 18_000.0),       # IRR/ton
    "melamine_price": (45_000.0, 60_000.0),   # IRR/ton
    "carbon_credit_price": (500.0, 1_500.0),  # IRR/ton CO2
}

# فضای اقدام کنترلی (بخش ۲-۴-۱ SRS) - ۱۱ اقدام پیوسته.
# نام‌های *_APPROX یعنی اثر این اقدام بر مدل فیزیکی به‌صورت ساده‌شده مدل شده
# است (مدل تفصیلی این تجهیزات در دامنه این ریپو نیست)؛ نگاه کنید به
# simulator.py برای جزئیات.
ACTION_SPACE = {
    "S_C_ratio": (2.5, 4.0),                  # mol/mol
    "T_primary_reformer": (750.0, 850.0),     # °C  (COT)
    "T_secondary_reformer": (950.0, 1050.0),  # °C
    "P_ammonia_reactor": (120.0, 250.0),      # bar
    "secondary_air_pct": (50.0, 100.0),       # % ظرفیت دبی هوا به ریفرمر ثانویه
    "cooling_water_temp_target": (25.0, 40.0),# °C
    "cooling_water_flow_pct": (50.0, 100.0),  # % ظرفیت گردش آب خنک‌کننده
    "compressor_speed_pct": (60.0, 100.0),    # % توان کمپرسورهای اصلی
    "heat_recovery_ratio_pct": (50.0, 90.0),  # % APPROX - نسبت بازیابی حرارت
    "aux_fuel_pct": (0.0, 100.0),             # % APPROX - دبی سوخت کمکی
    "control_valve_pct": (0.0, 100.0),        # % APPROX - گشودگی شیرهای کنترلی کلیدی
}
ACTION_KEYS = list(ACTION_SPACE.keys())

# شاخص مصرف ویژه انرژی هدف (SEC) - بخش ۱-۲ SRS، مبنای تشخیص ناکارآمدی
SEC_TARGET_AMMONIA_GJ_PER_TON = 62.61
SEC_TARGET_UREA_GJ_PER_TON = 4.52
SEC_ALERT_DEVIATION_PCT = 5.0  # انحراف بیش از این درصد از هدف → هشدار پیشگیرانه

RANDOM_SEED = 42
