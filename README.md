# 🧹 DataClean.AI

> AI-powered data cleaning platform for messy Excel/CSV files

## 🎯 What It Does

Automatically detects and fixes data quality issues in Excel/CSV files using machine learning.

**Problem:** Data analysts spend 60-80% of time cleaning data manually.  
**Solution:** Upload messy file → AI analyzes → Download clean file (in 30 seconds).

## 🚀 Features

- ✅ Duplicate detection (exact + fuzzy matching)
- ✅ Missing value imputation
- ✅ Format standardization
- ✅ Outlier detection
- ✅ Before/after preview
- ✅ Detailed cleaning reports

## 🏗️ Architecture

```
Frontend (React) → Backend (FastAPI) → ML Pipeline (XGBoost, Isolation Forest)
                      ↓
                 PostgreSQL + Redis
```

## 🤖 ML Models

1. **Problem Classifier**: XGBoost (89% F1 score)
2. **Duplicate Detector**: Levenshtein distance + blocking
3. **Outlier Detector**: Isolation Forest
4. **Type Inference**: Hybrid rule-based + ML

## 🛠️ Tech Stack

**Backend:**

- Python 3.11, FastAPI, SQLAlchemy
- PostgreSQL, Redis, Celery
- scikit-learn, XGBoost, ONNX

**Frontend:**

- React, TypeScript, TailwindCSS
- Axios, React Query

**DevOps:**

- Docker, GitHub Actions
- AWS S3, Railway/Render

## 📊 Performance

- Processing time: <30s for 5,000 rows
- ML accuracy: 89% F1 score
- API response: <500ms (p95)

## 🎓 Learning Outcomes

Built this to learn:

- Production ML pipelines
- MLOps (MLflow, DVC, ONNX)
- Backend development (FastAPI, async)
- Frontend (React, TypeScript)
- DevOps (Docker, CI/CD)

## 🚧 Status

Currently in development (Week X/13)

## 📄 License

MIT
