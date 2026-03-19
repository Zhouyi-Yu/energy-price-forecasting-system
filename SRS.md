One important adjustment before the draft: **the MVP should center on U.S. crude and U.S. gasoline**, because those have long official daily/weekly histories through FRED/EIA, while **Alberta retail gasoline is straightforward to source officially at monthly frequency from Statistics Canada**. That means **next-day / next-week Alberta retail forecasting is possible only with supplemental higher-frequency sources or proxy features**, so Alberta should be treated as a secondary forecast track in Version 1 rather than the primary model target. ([FRED][1])

# Software Requirements Specification

## Forecasting Weekly Gasoline Prices Using Oil Market Fundamentals and Geopolitical Shock Indicators (2026 U.S.–Iran War)

**Document version:** 0.1
**Project type:** Portfolio / resume project
**Primary audience:** Self-planning, recruiters, professor / TA
**Implementation stack:** Python, pandas, PyTorch, SQL, FastAPI, React, Power BI

---

## 1. Introduction

### 1.1 Purpose

This document defines the scope, requirements, assumptions, data sources, machine learning approach, system architecture, and evaluation criteria for a deployable forecasting system that predicts short-term energy price movements using market fundamentals and geopolitical shock indicators.

### 1.2 Project overview

The system will forecast:

* **next-day crude oil price**
* **next-week crude oil price**
* **next-week U.S. average gasoline price**
* **Alberta gasoline price as a secondary track**, subject to data-frequency constraints

The project is motivated by the 2026 conflict shock affecting global energy markets. Reuters reported that on **March 19, 2026**, oil prices spiked sharply as the conflict escalated and attacks hit regional energy infrastructure, reinforcing the relevance of near-term forecasting under geopolitical stress. ([Reuters][2])

### 1.3 Business / portfolio goal

This project is intended to demonstrate:

* strong AI/ML experimentation
* strong data engineering ability
* ability to connect real-world geopolitical events to market forecasting
* ability to build an end-to-end deployable system rather than only a notebook model

### 1.4 Scope

The system will:

* ingest historical market, fuel-price, and geopolitical-event data
* engineer structured features from those data sources
* train and evaluate short-horizon forecasting models
* expose forecasts through a FastAPI backend
* present forecasts, trends, and war-impact explanations in a React web app
* optionally support analyst-style reporting through Power BI

### 1.5 Non-goals

The system will not:

* provide financial advice
* claim causal proof that war alone determines fuel prices
* forecast every local station price accurately
* model global geopolitics as a full strategic simulation
* replace official market analysis

---

## 2. Problem Statement

Energy prices are affected by many overlapping factors, including crude oil costs, refining conditions, distribution, taxes, inventories, seasonal demand, and sudden disruptions to supply chains or infrastructure. The EIA explicitly identifies crude oil, refining, distribution/marketing, and taxes as key components of gasoline prices, and notes that prices can change rapidly when crude supply, refinery operations, or pipeline deliveries are disrupted. ([U.S. Energy Information Administration][3])

Traditional narratives such as “war in the Middle East causes gas prices to rise” are too simplistic for operational forecasting. This project addresses that gap by building a model that treats war-related developments as **structured signals** alongside market fundamentals, rather than as the only explanatory variable.

---

## 3. Objectives

### 3.1 Primary objectives

* Build a deployable system for short-term price forecasting
* Achieve strong predictive accuracy on crude and gasoline price targets
* Quantify whether geopolitical-event features improve forecast performance
* Produce a portfolio-quality system with clear engineering and ML documentation

### 3.2 Secondary objectives

* Compare baseline statistical models with ML / deep learning models
* Visualize forecast uncertainty and recent event context
* Show Alberta-specific behavior where data allows

### 3.3 Success criteria

The project will be considered successful if it:

* outperforms naive baselines on held-out chronological test data
* exposes usable predictions through an API and web UI
* documents assumptions, limitations, and evaluation rigor clearly
* demonstrates clear engineering ownership from data ingestion to frontend delivery

---

## 4. Stakeholders and Users

### 4.1 Primary stakeholders

* Project author
* Recruiters and hiring managers
* Professors / TAs evaluating technical rigor

### 4.2 End users

* A user interested in short-term oil or gasoline price outlook
* An evaluator reviewing the system architecture and ML methodology
* A technical reviewer validating whether geopolitical features add measurable value

---

## 5. Assumptions and Constraints

### 5.1 Assumptions

* Short-horizon forecasting is more realistic than long-horizon forecasting
* Geopolitical shocks affect prices through market channels rather than in isolation
* Historical market and event data are sufficiently rich to support useful short-term models
* Model performance should be measured against chronological baselines, not random splits

### 5.2 Constraints

* U.S. crude and U.S. gasoline have stronger official high-frequency coverage than Alberta retail gasoline. FRED provides daily and weekly crude series and weekly U.S. gasoline series, while Statistics Canada’s retail gasoline-by-geography table is monthly. ([FRED][4])
* Alberta gasoline taxation and policy changes can materially affect pump prices, so Alberta forecasts must account for tax context and may not map cleanly from U.S. crude movements alone. Alberta’s fuel-tax framework is policy-sensitive and explicitly linked to oil-price-based tax relief. ([Alberta.ca][5])
* Conflict/event data can be noisy, delayed, or inconsistently reported across sources.
* News sentiment and headline counts may capture media attention rather than direct physical supply impact.

### 5.3 Design implication

Version 1 will prioritize:

* U.S. crude price forecasting
* U.S. gasoline forecasting
* Alberta gasoline visualization and experimental forecasting where data quality permits

---

## 6. Data Requirements

### 6.1 Core data sources

The system will use the following source families:

**Market and fuel price data**

* FRED daily WTI crude price series
* FRED daily Brent crude price series
* FRED weekly U.S. regular gasoline price series
* EIA refinery utilization and weekly petroleum status data
* Statistics Canada monthly retail gasoline prices by geography
* Natural Resources Canada transportation fuel price resources for Canadian fuel context ([FRED][4])

**Geopolitical and event data**

* ACLED conflict event data
* GDELT event database
* structured news headline retrieval via a news API or curated news pipeline ([ACLED][6])

### 6.2 Data frequency

* **Daily:** WTI, Brent, news/event indicators
* **Weekly:** U.S. gasoline, refinery utilization, petroleum status metrics
* **Monthly:** Statistics Canada Alberta / city retail gasoline data

### 6.3 Candidate target variables

**Primary targets**

* `wti_price_next_day`
* `wti_price_next_week`
* `us_regular_gasoline_next_week`

**Secondary / experimental targets**

* `alberta_gasoline_next_week`
* `alberta_gasoline_next_month`

### 6.4 Candidate feature groups

**Price history**

* lagged WTI values
* lagged Brent values
* moving averages
* rolling volatility
* WTI-Brent spread

**Fuel market fundamentals**

* gasoline inventories
* crude inventories
* refinery utilization
* distillate inventories
* seasonal calendar indicators

**Geopolitical shock indicators**

* count of relevant conflict events
* event severity score
* attacks on energy infrastructure
* Strait of Hormuz disruption flag
* sanctions / policy action flag
* war-headline intensity score
* headline sentiment / tone score

**Regional context**

* Alberta tax / policy indicator
* exchange-rate features for Canadian pricing
* Alberta-specific wholesale or supplemental retail proxies where available

---

## 7. High-Level Functional Requirements

### 7.1 Data ingestion

The system shall:

1. ingest historical data from approved data sources
2. normalize timestamps and units across daily, weekly, and monthly datasets
3. store cleaned data in SQL tables
4. support periodic refresh of market and event data

### 7.2 Data processing

The system shall:

1. clean missing and inconsistent records
2. create lag, rolling, and event-window features
3. align multi-frequency data into model-ready datasets
4. log dataset versions used for training and evaluation

### 7.3 Model training

The system shall:

1. support baseline statistical models
2. support feature-based ML models
3. support PyTorch sequence models for experimental comparison
4. save trained models and evaluation metadata
5. allow retraining on updated datasets

### 7.4 Prediction service

The system shall:

1. provide forecast endpoints through FastAPI
2. return prediction values, timestamps, confidence metadata, and model version
3. allow separate forecasting routes for crude and gasoline
4. expose recent event indicators relevant to the forecast window

### 7.5 Frontend/dashboard

The web app shall:

1. display historical price trends
2. display next-day and next-week forecasts
3. show key drivers or feature importance summaries
4. show recent geopolitical event indicators relevant to the forecast
5. distinguish actual values from forecasted values
6. present Alberta and U.S. views separately

### 7.6 Reporting

The system should:

1. export forecast data for Power BI consumption
2. support summary charts for model comparison
3. support error dashboards for evaluation over time

---

## 8. Non-Functional Requirements

### 8.1 Performance

* Forecast API responses should be fast enough for interactive dashboard use
* Historical chart loading should remain responsive for standard browser sessions

### 8.2 Reliability

* Failed data-ingestion jobs shall be logged
* Missing source fields shall trigger validation warnings
* Model versioning shall prevent silent overwrites

### 8.3 Maintainability

* ETL, model training, API, and frontend code shall be modular
* Each dataset shall have a documented schema and source reference
* Configuration values shall be externalized where possible

### 8.4 Explainability

* The system shall provide at least lightweight interpretability for non-deep models
* The UI shall communicate that forecasts are probabilistic, not guaranteed

### 8.5 Reproducibility

* Experiments shall record dataset version, code version, hyperparameters, and metrics
* Test results shall be produced using chronological backtesting

---

## 9. Machine Learning Requirements

### 9.1 Modeling strategy

The project will use a staged modeling plan:

**Stage 1: Baselines**

* naive last-value forecast
* moving average forecast
* linear regression / regularized regression

**Stage 2: Strong tabular ML**

* gradient-boosted trees or similar tabular models

**Stage 3: Deep learning**

* PyTorch LSTM or other sequence model for comparison

This order is intentional. For structured time-series forecasting with limited event-driven shocks, simpler baselines are necessary before justifying a deep model.

### 9.2 Evaluation methodology

* use chronological train / validation / test splits
* use rolling or walk-forward backtesting
* compare all models against naive baselines
* evaluate separately for calm periods and shock periods

### 9.3 Metrics

Primary metrics:

* MAE
* RMSE
* MAPE, where appropriate

Secondary metrics:

* directional accuracy
* shock-period error
* regional error comparison

### 9.4 Model comparison question

A core research question of this system is:

**Do geopolitical-event features improve short-horizon forecasting accuracy beyond market fundamentals alone?**

To answer this, at least two model families will be compared:

* market-only features
* market + geopolitical features

---

## 10. System Architecture

### 10.1 Proposed architecture

**Data pipeline**

* Python ETL scripts using pandas
* scheduled ingestion from FRED, EIA, StatCan, and event/headline sources
* cleaned storage in SQL

**Model layer**

* feature generation pipeline
* baseline and ML training scripts
* model artifacts stored with version tags

**Backend**

* FastAPI service for forecast retrieval
* endpoints for predictions, historical series, and model metadata

**Frontend**

* React dashboard
* charts for actual vs forecast
* region selection for U.S. and Alberta
* driver/event panels

**Analytics**

* optional Power BI dashboard consuming SQL or exported forecast tables

### 10.2 Suggested components

* `etl/`
* `features/`
* `models/`
* `api/`
* `frontend/`
* `sql/`
* `docs/`

---

## 11. API Requirements

### 11.1 Example endpoints

* `GET /forecast/wti?horizon=1d`
* `GET /forecast/wti?horizon=1w`
* `GET /forecast/us-gasoline?horizon=1w`
* `GET /history/wti`
* `GET /history/us-gasoline`
* `GET /events/recent`
* `GET /model/metrics`

### 11.2 API response content

Each forecast response should include:

* target name
* forecast timestamp
* horizon
* predicted value
* recent actual value
* model version
* confidence or uncertainty band if available
* recent relevant event summary score

---

## 12. UI / Dashboard Requirements

### 12.1 Main views

* **Overview:** current market status and latest forecasts
* **Crude oil view:** WTI / Brent history and short-term forecast
* **Gasoline view:** U.S. gasoline and Alberta view
* **War-impact view:** recent event indicators and their correlation with recent moves
* **Model performance view:** backtest metrics and model comparison

### 12.2 UI principles

* separate factual historical data from model output clearly
* use simple language for non-technical users
* present the system as a forecasting aid, not an oracle
* highlight limitations during high-volatility periods

---

## 13. Data Storage Requirements

### 13.1 Core SQL tables

* `raw_market_data`
* `raw_event_data`
* `raw_news_data`
* `processed_features`
* `model_runs`
* `forecasts`
* `actuals`
* `evaluation_results`

### 13.2 Required stored metadata

* source name
* extraction time
* date coverage
* units
* transformation version
* model version
* training window

---

## 14. Risks, Limitations, and Ethics

### 14.1 Technical limitations

* War episodes are relatively rare, so the system may learn correlation patterns more than stable causal laws.
* Market structure in 2026 is not the same as in the 1990s, so older war analogies are only partially transferable.
* Alberta retail gasoline data has weaker official high-frequency history than U.S. crude and U.S. gasoline. ([FRED][1])

### 14.2 Data limitations

* News-based signals may overrepresent media intensity
* Event databases may miss economically important but nonviolent developments
* Regional pump prices reflect taxes, refining, and local distribution, not only crude movements

### 14.3 Interpretation risks

* Forecast accuracy does not prove causal understanding
* A good model in normal periods may degrade during extreme shocks
* A forecast may be directionally right while magnitude is wrong

### 14.4 Ethical and communication requirements

The system shall:

* clearly state that it is not financial advice
* avoid overstating certainty during war-related volatility
* disclose data gaps and modeling assumptions
* present conflict features as operational indicators, not political judgments

---

## 15. Validation Plan

### 15.1 Backtesting

The system will be validated using rolling historical windows across:

* normal market periods
* historical shock periods
* the 2026 conflict period

### 15.2 Comparative experiments

Experiments will compare:

* naive baseline vs linear model
* linear model vs tabular ML
* tabular ML vs PyTorch sequence model
* market-only vs market-plus-geopolitical feature sets

### 15.3 Acceptance threshold

A candidate model should only be promoted to the deployable API if it:

* beats naive baseline consistently
* remains reasonably stable during volatile windows
* produces interpretable and reproducible outputs

---

## 16. Deliverables

### 16.1 Technical deliverables

* cleaned ETL pipeline
* SQL-backed dataset store
* trained forecasting models
* FastAPI backend
* React dashboard
* Power BI summary dashboard
* experiment log and metrics report
* project documentation

### 16.2 Portfolio deliverables

* GitHub repository
* architecture diagram
* README
* demo screenshots or demo video
* concise project summary for resume / interview use

---

## 17. Resume Framing

This project is designed to communicate:

**AI/ML experimentation**

* compared baseline, ML, and deep learning approaches
* engineered event-driven and market-fundamental features
* evaluated models with rigorous time-series backtesting

**Data engineering**

* built ETL pipelines across multiple public data sources
* normalized daily, weekly, and monthly data into model-ready schemas
* stored and served forecast data through SQL and API layers

**End-to-end ownership**

* deployed forecasting logic behind a full-stack application
* presented model outputs through React and Power BI
* documented assumptions, risks, and limitations clearly

---

## 18. Recommended MVP Definition

To keep scope strong but realistic, the MVP should be:

1. **Primary forecast targets**

   * next-day WTI
   * next-week WTI
   * next-week U.S. gasoline

2. **Secondary analytics**

   * Alberta gasoline trend view
   * experimental Alberta forecast, likely weekly proxy or monthly official target

3. **Model stack**

   * naive baseline
   * linear / regularized regression
   * gradient-boosted model
   * one PyTorch sequence model

4. **Deployment**

   * FastAPI backend
   * React dashboard
   * SQL storage
   * Power BI as optional reporting layer

That scope is ambitious enough to be resume-strong, but still believable for one well-executed portfolio project.

---

## 19. First Draft Data Dictionary

* `date`
* `region`
* `wti_usd_per_barrel`
* `brent_usd_per_barrel`
* `us_gasoline_usd_per_gallon`
* `ab_gasoline_cad_per_litre`
* `refinery_utilization_pct`
* `gasoline_inventory_barrels`
* `crude_inventory_barrels`
* `event_count_energy_related`
* `event_count_middle_east_conflict`
* `energy_infrastructure_attack_flag`
* `hormuz_disruption_flag`
* `sanctions_flag`
* `headline_volume_energy_conflict`
* `headline_tone_score`
* `cad_usd_fx`
* `target_next_day_wti`
* `target_next_week_wti`
* `target_next_week_us_gasoline`

---

## 20. Scope Lock

This project will be framed as:

**A deployable short-horizon energy price forecasting system that combines oil-market fundamentals with structured geopolitical shock indicators, with U.S. crude and U.S. gasoline as the primary targets and Alberta gasoline as a secondary regional extension.**


---

## 21. Deployment and Environment Requirements

### 21.1 Containerization requirement

The system shall support containerized deployment using **Docker** to ensure reproducible setup across development, testing, and deployment environments.

### 21.2 Docker objectives

Docker shall be used to:

* standardize the runtime environment
* avoid local machine dependency issues
* simplify backend deployment
* support future multi-service orchestration
* improve reproducibility for recruiters, professors, and collaborators

### 21.3 Initial containerization scope

The MVP shall support Dockerization for:

* FastAPI backend
* Python ML/ETL environment
* optional SQL database service
* optional frontend container for React app

### 21.4 Recommended container structure

The project should support either:

**Option A: single-container backend-first MVP**

* one Docker container for Python ETL + model inference + FastAPI

**Option B: multi-container full-stack setup**

* `backend` container for FastAPI, ETL utilities, model serving
* `frontend` container for React
* `db` container for PostgreSQL
* optional `nginx` container for reverse proxy in later versions

### 21.5 Docker functional requirements

The Dockerized system shall:

1. build successfully from repository-defined Dockerfiles
2. install all required Python dependencies automatically
3. expose backend API on a defined port
4. support environment-variable configuration
5. allow local startup using Docker Compose or equivalent orchestration
6. ensure the same model-serving environment across machines

### 21.6 Docker non-functional requirements

* image builds should be deterministic
* containers should avoid unnecessary packages to reduce image size
* secrets shall not be hardcoded in Dockerfiles
* source-specific API keys or credentials shall be loaded through environment variables

---

## 22. Dependency and Package Management Requirements

### 22.1 Python dependency specification

The project shall include a dependency specification file to define all Python libraries required for:

* data ingestion
* preprocessing
* model training
* API serving
* testing
* database interaction

### 22.2 Required dependency file

The repository shall contain a **`requirements.txt`** file for standard Python installation.

### 22.3 Recommended additional dependency files

For better maintainability, the project may also include:

* `requirements-dev.txt` for development-only tools
* `requirements-prod.txt` for deployment/runtime-only packages
* `pyproject.toml` in a later, more mature version

### 22.4 Dependency requirements

The dependency specification shall:

1. list all required packages explicitly
2. pin versions where reproducibility matters
3. separate production and development dependencies where practical
4. support installation in Docker and non-Docker environments
5. be updated when new libraries are added to the project

---

## 23. Proposed `requirements.txt` Scope

A reasonable first version of `requirements.txt` for your project would cover these categories:

### 23.1 Core data and numerical libraries

* pandas
* numpy
* scipy

### 23.2 Machine learning

* scikit-learn
* torch

### 23.3 API / backend

* fastapi
* uvicorn

### 23.4 Database

* sqlalchemy
* psycopg2-binary

### 23.5 Data retrieval / HTTP

* requests
* httpx

### 23.6 Visualization / reporting support

* matplotlib
* plotly

### 23.7 Validation / config

* pydantic
* python-dotenv

### 23.8 Testing

* pytest

### 23.9 Optional utilities

* jupyter
* notebook
* alembic

---

## 24. Example `requirements.txt`

This is a good practical starter version:

```txt
pandas==2.2.3
numpy==2.1.1
scipy==1.14.1
scikit-learn==1.5.2
torch==2.4.1
fastapi==0.115.0
uvicorn[standard]==0.30.6
sqlalchemy==2.0.35
psycopg2-binary==2.9.9
requests==2.32.3
httpx==0.27.2
matplotlib==3.9.2
plotly==5.24.1
pydantic==2.9.2
python-dotenv==1.0.1
pytest==8.3.3
jupyter==1.1.1
alembic==1.13.3
```

For a cleaner repo later, you could split it into:

* runtime dependencies
* training dependencies
* dev/test dependencies

---

## 25. Dockerfile Requirements

### 25.1 Backend Dockerfile requirement

The backend service shall include a `Dockerfile` that:

1. uses an official Python base image
2. sets a working directory
3. copies dependency files first for efficient caching
4. installs dependencies from `requirements.txt`
5. copies project source code
6. exposes the backend port
7. starts the FastAPI server with a production-ready command

### 25.2 Example backend Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 26. Docker Compose Requirements

### 26.1 Compose requirement

The project should include a `docker-compose.yml` file to simplify local startup of multi-service components.

### 26.2 Compose MVP services

A recommended first multi-service layout is:

* `backend`
* `db`
* optional `frontend`

### 26.3 Example `docker-compose.yml`

```yaml
version: "3.9"

services:
  backend:
    build: .
    container_name: energy_forecast_backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:16
    container_name: energy_forecast_db
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: energy_forecast
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Later, you could add:

```yaml
  frontend:
    build: ./frontend
    container_name: energy_forecast_frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

---

## 27. Environment Variable Requirements

### 27.1 Configuration requirement

The system shall use environment variables for configuration values that differ by environment.

### 27.2 Candidate environment variables

* `DATABASE_URL`
* `API_HOST`
* `API_PORT`
* `FRED_API_KEY` if needed
* `NEWS_API_KEY`
* `MODEL_PATH`
* `APP_ENV`

### 27.3 Security requirement

Secrets and credentials shall not be committed directly into source code or public repositories.

---

## 28. Repository Structure Update

Your structure can now be updated to:

```txt
project-root/
│
├── api/
├── etl/
├── features/
├── models/
├── sql/
├── frontend/
├── docs/
├── tests/
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
└── .gitignore
```

---

## 29. Suggested SRS Wording for Resume Value

You can explicitly add this sentence to the document:

> The system will be packaged with Docker and dependency specifications to ensure reproducible development, testing, and deployment across environments.

That makes the project sound much more like a real engineering system, not just an ML experiment.

---

## 30. Recommended decision for your project

For your case, I’d recommend:

* **Use Docker**
* **Use `requirements.txt`**
* **Add `docker-compose.yml`**
* **Use PostgreSQL**
* **Keep frontend Docker optional for MVP**
* **Containerize backend first**

That is the best balance between:

* resume strength
* realistic scope
* deployment credibility

