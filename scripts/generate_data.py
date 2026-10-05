#!/usr/bin/env python
"""CLI for generating the synthetic training/test dataset. Example:

    python scripts/generate_data.py --n-samples 100000 --out-dir data
"""

from __future__ import annotations

import argparse
from pathlib import Path

from sems.config import RANDOM_SEED
from sems.data_generator import KhorasanPetrochemicalDataGenerator


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the SEMS synthetic dataset")
    parser.add_argument("--n-samples", type=int, default=100_000)
    parser.add_argument("--out-dir", type=str, default="data")
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--train-frac", type=float, default=0.8)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    generator = KhorasanPetrochemicalDataGenerator(seed=args.seed)
    df = generator.generate_dataset(
        n_samples=args.n_samples, save_path=str(out_dir / "khorasan_petrochem_data.csv")
    )
    generator.validate_dataset(df)

    train_df = df.sample(frac=args.train_frac, random_state=args.seed)
    test_df = df.drop(train_df.index)

    train_df.to_csv(out_dir / "khorasan_petrochem_train.csv", index=False)
    test_df.to_csv(out_dir / "khorasan_petrochem_test.csv", index=False)

    print(f"\n✅ Training data: {len(train_df)} samples")
    print(f"✅ Test data: {len(test_df)} samples")


if __name__ == "__main__":
    main()
