

# 📊 Energy Price Forecasting System

**Forecasting crude oil and gasoline prices using market fundamentals and geopolitical signals**

---

## 🚀 Overview

This project is an end-to-end machine learning system that forecasts short-term **crude oil and gasoline prices** by combining:

* Oil market fundamentals (WTI, inventories, refinery utilization)
* Time-series signals (lags, trends, volatility)
* Geopolitical shock indicators (conflict events, energy disruptions, news signals)

The system is designed as a **deployable full-stack application**, demonstrating both **ML experimentation** and **production-oriented engineering**.

---

## 📄 Documentation

* 📘 **Software Requirements Specification (SRS)**
  See [`docs/SRS.md`](docs/SRS.md) for full system design, requirements, data schema, and assumptions.

* 📝 **Changelog**
  See [`CHANGELOG.md`](CHANGELOG.md) for version history and major updates.

---

## 🎯 Objectives

* Predict:

  * **Next-day crude oil price (WTI)**
  * **Next-week crude oil price**
  * **Next-week U.S. gasoline price**
* Evaluate impact of **geopolitical events** on forecasting accuracy
* Build a **deployable ML system (API + dashboard)**
* Demonstrate strong **data engineering + ML + system design**

---

## 🧠 Key Features

* 📈 Time-series forecasting (short horizon)
* 🌍 Geopolitical event feature integration
* 🔄 ETL pipeline across multiple data sources
* ⚙️ Model comparison (baseline → ML → deep learning)
* 🌐 FastAPI backend for predictions
* 💻 React dashboard for visualization
* 🗄️ SQL-based data storage
* 🐳 Dockerized environment for reproducibility

---

## 🏗️ System Architecture

```text
Data Sources (FRED, EIA, StatCan, Events, News)
        ↓
ETL Pipeline (Python, pandas)
        ↓
Feature Engineering
        ↓
Model Training (scikit-learn, PyTorch)
        ↓
Model Storage + SQL Database
        ↓
FastAPI Backend
        ↓
React Frontend Dashboard
        ↓
(Optional) Power BI Analytics
```

---

## 📦 Tech Stack

### Data & ML

* Python
* pandas, NumPy
* scikit-learn
* PyTorch

### Backend

* FastAPI
* SQLAlchemy
* PostgreSQL

### Frontend

* React

### DevOps

* Docker
* Docker Compose

### Analytics

* Power BI (optional)

---

## 📊 Data Sources

* FRED (Federal Reserve Economic Data)
* EIA (U.S. Energy Information Administration)
* Statistics Canada
* Conflict/event datasets (ACLED, GDELT)
* News APIs (headline-based features)

---

## ⚙️ Setup Instructions

### Run with Docker (Recommended)

```bash
docker-compose up --build
```

Backend:

```
http://localhost:8000
```

---

### Run locally

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

---

## 🔌 API Endpoints

* `GET /forecast/wti?horizon=1d`
* `GET /forecast/wti?horizon=1w`
* `GET /forecast/us-gasoline?horizon=1w`
* `GET /history/wti`
* `GET /events/recent`

---

## 📈 Modeling Approach

### Baselines

* Naive (last value)
* Moving average

### ML Models

* Linear regression
* Gradient boosting

### Deep Learning

* LSTM (PyTorch)

### Evaluation

* Chronological split
* Backtesting
* Metrics: MAE, RMSE, MAPE

---

## ⚠️ Limitations

* Geopolitical events are sparse and noisy
* Correlation ≠ causation
* Non-stationary market conditions
* Alberta gasoline data has lower frequency
* Model performance may degrade during extreme shocks

---

## 🔐 Disclaimer

This project is for **educational and research purposes only**.
It does **not** constitute financial advice.

---

## 📝 Changelog (Summary)

> Full version: [`CHANGELOG.md`](CHANGELOG.md)

### v0.1.0 — Project Initialization

* Defined SRS and system architecture
* Selected data sources (FRED, EIA, StatCan, event datasets)
* Designed ML pipeline (baseline → ML → DL)
* Set up repository structure and documentation

### v0.2.0 — Data Pipeline (Planned)

* Implement ETL for crude oil and gasoline data
* Integrate geopolitical event datasets
* Create feature engineering pipeline

### v0.3.0 — Modeling (Planned)

* Implement baseline and ML models
* Add PyTorch LSTM model
* Conduct backtesting and evaluation

### v0.4.0 — Backend API (Planned)

* Build FastAPI endpoints
* Serve model predictions
* Integrate database layer

### v0.5.0 — Frontend Dashboard (Planned)

* Build React UI
* Add visualization for forecasts and events

### v1.0.0 — Full System Release (Planned)

* End-to-end deployable system
* Dockerized services
* Final evaluation and documentation

---

## 📌 Future Improvements

* Transformer-based models
* Real-time data streaming
* NLP-based event embeddings
* Improved Alberta modeling
* Prediction uncertainty intervals

---

## 💼 Resume Highlights

* Built end-to-end ML forecasting system using **market + geopolitical data**
* Designed ETL pipelines across multiple real-world datasets
* Compared statistical, ML, and deep learning approaches
* Deployed full-stack system using **FastAPI, React, SQL, Docker**

---

## 📜 License

MIT License

---

## ⭐ Final Note

This project is designed to reflect **real-world ML system design**, not just model training — bridging:

* data engineering
* machine learning
* backend systems
* and user-facing applications

---


