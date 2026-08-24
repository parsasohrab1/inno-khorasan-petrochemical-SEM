"""
تولید دیتاست سنتتیک برای آموزش/ارزیابی عامل یادگیری تقویتی (بخش ۳ SRS).

این ماژول بر پایه ``simulator.py`` بنا شده تا فیزیک شبیه‌سازی تکرار نشود؛
تنها مسئولیت آن، نمونه‌برداری متغیرهای تصمیم/اختلال به‌صورت مستقل و تصادفی
(رویکرد Physics-Informed مطابق سند اصلی) و ساخت دیتافریم خروجی است.
"""

from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from sems.config import ACTION_SPACE, OPERATING_LIMITS, RANDOM_SEED
from sems.simulator import (
    sample_action,
    sample_disturbances,
    sample_prices,
    simulate_step,
)


class KhorasanPetrochemicalDataGenerator:
    """داده‌ساز سنتتیک پتروشیمی خراسان بر پایه هسته فیزیکی مشترک simulator.py."""

    def __init__(self, seed: int = RANDOM_SEED):
        self.rng = np.random.default_rng(seed)

    def generate_sample(self, t: datetime) -> dict:
        """تولید یک نمونه داده کامل (یک ردیف دیتاست)."""
        disturbances = sample_disturbances(self.rng)
        action = sample_action(self.rng)
        prices = sample_prices(self.rng)

        result = simulate_step(action, disturbances, prices, self.rng, add_noise=True)

        sample = {"timestamp": t, **result.observation}
        sample["profit"] = result.profit
        sample["revenue"] = result.revenue
        sample["energy_cost"] = result.energy_cost
        sample["carbon_cost"] = result.carbon_cost
        return sample

    def generate_dataset(self, n_samples: int = 100_000, save_path: str | None = None) -> pd.DataFrame:
        """تولید مجموعه داده کامل با فاصله زمانی ۱ ثانیه (مطابق نرخ نمونه‌برداری SCADA)."""
        print(f"تولید {n_samples} نمونه داده...")
        start_time = datetime.now() - timedelta(days=30)

        rows = []
        for i in range(n_samples):
            if i % 10_000 == 0:
                print(f"پیشرفت: {i}/{n_samples} نمونه")
            t = start_time + timedelta(seconds=i)
            rows.append(self.generate_sample(t))

        df = pd.DataFrame(rows)

        print("\nآمار توصیفی مجموعه داده:")
        print(df.describe())

        if save_path:
            df.to_csv(save_path, index=False)
            print(f"\nداده‌ها در {save_path} ذخیره شدند.")

        return df

    def validate_dataset(self, df: pd.DataFrame) -> bool:
        """اعتبارسنجی مجموعه داده بر اساس محدودیت‌های فیزیکی و همبستگی‌های مورد انتظار."""
        print("\n=== اعتبارسنجی مجموعه داده ===")

        violations = 0
        checked_limits = {**OPERATING_LIMITS, **{f"action_{k}": v for k, v in ACTION_SPACE.items()}}
        for var, (min_val, max_val) in checked_limits.items():
            if var in df.columns:
                outside = ((df[var] < min_val * 0.9) | (df[var] > max_val * 1.1)).sum()
                if outside > 0:
                    violations += int(outside)
                    print(f"⚠ {var}: {outside} نمونه خارج از محدوده [{min_val}, {max_val}] (با ۱۰٪ رواداری نویز)")

        correlations = {
            ("feed_flow", "syngas_flow"): 0.5,
            ("action_S_C_ratio", "steam_flow"): 0.5,
        }

        corr_violations = 0
        for (var1, var2), expected_corr in correlations.items():
            if var1 in df.columns and var2 in df.columns:
                actual_corr = df[var1].corr(df[var2])
                if abs(actual_corr - expected_corr) > 0.4:
                    corr_violations += 1
                    print(
                        f"⚠ همبستگی {var1}-{var2}: انتظار {expected_corr:.2f}, دریافت {actual_corr:.2f}"
                    )

        if violations == 0 and corr_violations == 0:
            print("✅ مجموعه داده معتبر است.")
        else:
            print(f"⚠ {violations + corr_violations} مورد نقض شناسایی شد.")

        return violations == 0 and corr_violations == 0


if __name__ == "__main__":
    generator = KhorasanPetrochemicalDataGenerator(seed=RANDOM_SEED)

    df = generator.generate_dataset(n_samples=100_000, save_path="data/khorasan_petrochem_data.csv")
    generator.validate_dataset(df)

    print("\nنمونه داده تولید شده:")
    print(df.iloc[0].to_dict())

    train_df = df.sample(frac=0.8, random_state=RANDOM_SEED)
    test_df = df.drop(train_df.index)

    train_df.to_csv("data/khorasan_petrochem_train.csv", index=False)
    test_df.to_csv("data/khorasan_petrochem_test.csv", index=False)

    print(f"\n✅ داده‌های آموزشی: {len(train_df)} نمونه")
    print(f"✅ داده‌های آزمون: {len(test_df)} نمونه")
