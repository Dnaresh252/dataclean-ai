"""
Verify the cleaning actually worked
"""

import pandas as pd

# Load original and cleaned
original = pd.read_csv('data/synthetic/messy/messy_001_titanic_v0.csv')
cleaned = pd.read_csv('data/processed/test_cleaned.csv')

print("=" * 60)
print("CLEANING VERIFICATION")
print("=" * 60)

print(f"\n📊 FILE SIZE:")
print(f"   Original: {original.shape}")
print(f"   Cleaned:  {cleaned.shape}")
print(f"   Removed:  {original.shape[0] - cleaned.shape[0]} rows")

print(f"\n📊 DUPLICATES:")
orig_dupes = original.duplicated().sum()
clean_dupes = cleaned.duplicated().sum()
print(f"   Original: {orig_dupes} duplicates")
print(f"   Cleaned:  {clean_dupes} duplicates")
print(f"   ✅ Removed: {orig_dupes - clean_dupes}")

print(f"\n📊 MISSING VALUES:")
orig_missing = original.isna().sum().sum()
clean_missing = cleaned.isna().sum().sum()
print(f"   Original: {orig_missing} missing cells")
print(f"   Cleaned:  {clean_missing} missing cells")
print(f"   ✅ Fixed: {orig_missing - clean_missing}")

print(f"\n📊 SAMPLE DATA:")
print("\nOriginal (first 3 rows):")
print(original.head(3))
print("\nCleaned (first 3 rows):")
print(cleaned.head(3))

print("\n" + "=" * 60)
print("✅ CLEANING VERIFICATION COMPLETE!")
print("=" * 60)