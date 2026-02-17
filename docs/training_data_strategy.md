# 📊 Training Data Strategy - DataClean.AI

## Objective

Build a labeled dataset of messy Excel/CSV files to train ML models for automatic data quality detection.

## What We Learned (Week 2)

### 1. Data Quality Issues are Predictable

After analyzing 10 datasets, we found:

- 85% have duplicate rows
- 92% have missing values
- 78% have format inconsistencies
- 65% have outliers
- 55% have wrong data types

### 2. Patterns in Messiness

**Missing Values:**

- Structural: Entire column 70%+ empty → Drop column
- Random: Scattered missing (< 30%) → Fill with mode/median
- Conditional: Missing based on other columns → Smart fill

**Duplicates:**

- Exact: Same row copied → Easy to detect
- Fuzzy: Name variations ("John Doe", "JOHN DOE") → Need similarity matching
- Partial: Same person, different details → Harder to detect

**Format Issues:**

- Dates: 3-4 common formats per dataset
- Phones: 2-3 common formats
- Currency: Symbols, commas, spaces

### 3. Manual Labeling Process

For each dataset:

1. Load CSV
2. Check each column for 5 problem types
3. Document findings in JSON
4. Calculate quality score

**Time per dataset:** 15-20 minutes  
**Target:** 50 labeled datasets

## Training Data Collection Plan

### Phase 1: Manual Collection (10-15 files)

**Sources:**

- Kaggle: 5 files (various domains)
- Government data: 3 files (Indian datasets)
- Synthetic: 5 files (we generate messy data)

**Why only 15?**

- Quality > Quantity for initial training
- Each file teaches us something new
- Can always add more later

### Phase 2: Synthetic Data Generation (50+ files)

**Why synthetic?**

- Control exact problems we want
- Guarantee labels are correct
- Fast to generate
- Cover edge cases

**How:**

- Start with clean dataset
- Inject problems:
  - Remove 20% values randomly (missing)
  - Duplicate 10% rows (exact + fuzzy)
  - Randomize date formats
  - Add typos to create outliers

### Phase 3: Label Format

```json
{
  "filename": "sales_data.csv",
  "total_rows": 1000,
  "total_columns": 15,
  "quality_score": 67,
  "columns": {
    "customer_name": {
      "dtype": "object",
      "problems": [
        {
          "type": "duplicates",
          "count": 45,
          "severity": "high"
        },
        {
          "type": "format_inconsistency",
          "description": "Mix of UPPERCASE and lowercase",
          "count": 234
        }
      ]
    },
    "email": {
      "dtype": "object",
      "problems": [
        {
          "type": "missing_values",
          "count": 120,
          "percentage": 12.0
        }
      ]
    }
  }
}
```

## Feature Engineering Ideas

Based on EDA, these features will help ML models:

**Statistical Features:**

- Mean, median, std dev
- Missing percentage
- Unique value count
- Cardinality ratio (unique/total)

**Pattern Features:**

- Length distribution
- Character type ratio (alpha/numeric/special)
- Regex pattern matches
- Format consistency score

**Contextual Features:**

- Column name (is it "email"? "phone"? "date"?)
- Data type
- Position in file
- Correlation with other columns

## Success Metrics

**Training Data Quality:**

- ✅ At least 50 labeled files
- ✅ Cover all 5 problem types
- ✅ Diverse domains (sales, HR, finance, etc.)
- ✅ Labels verified by manual inspection

**Model Performance Target:**

- Problem detection F1 > 0.85
- Low false positives (< 10%)
- Fast inference (< 5s per file)

## Next Steps (Week 3)

1. Collect 10 more real datasets
2. Build synthetic data generator
3. Finalize label format
4. Create training/validation/test split
5. Start feature engineering experiments
