# Agentic AI Based Trip Planner

An end-to-end agentic AI application that generates personalized travel itineraries using LLM reasoning, real-time tool integrations, and a production-grade LLMOps deployment pipeline on AWS.

---

## Table of Contents

- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [CI/CD Workflow Configuration](#cicd-workflow-configuration)
- [Application Interface](#application-interface)
- [Sample Outputs](#sample-outputs)
- [AWS Infrastructure](#aws-infrastructure)
- [CI/CD Pipeline Result](#cicd-pipeline-result)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)

---

## System Architecture

Documents/1 SYSTEM ARCHI.png

The architecture is divided into two primary layers.

The **Agent Layer** forms the core of the application. It consists of an LLM reasoning engine powered by Groq, an agentic workflow graph built using LangGraph, and a suite of real-time tools including weather, currency conversion, place search, and expense calculation. The agent follows a perceive-reason-act-learn cycle to handle complex multi-step travel planning queries.

The **LLMOps Layer** sits above the agent layer and handles productionization. The Streamlit frontend communicates with a FastAPI backend, both containerized via Docker. The entire deployment is managed through a GitHub Actions CI/CD pipeline that builds Docker images, pushes them to Amazon ECR, and deploys them to an Amazon EC2 instance automatically on every push to the main branch.

---

## Project Structure

```
Agentic_Ai_Based_Trip_Planner/
│
├── .github/
│   └── workflows/
│       └── deploy.yml                  # GitHub Actions CI/CD pipeline
│
├── agents/
│   └── agentic_workflow.py             # LangGraph agent graph definition
│
├── config/
│   └── config.yaml                     # Application configuration
│
├── exception/
│   └── exceptionhandling.py            # Custom exception classes
│
├── logger/
│   └── logging.py                      # Logging setup
│
├── notebooks/
│   └── experiments.ipynb               # Development and experimentation
│
├── prompt_library/
│   └── prompt.py                       # Prompt templates for the agent
│
├── tools/
│   ├── arthamatic_tool.py              # Arithmetic / expense calculator tool
│   ├── currency_conversion_tool.py     # Real-time currency conversion tool
│   ├── expense_calculator_tool.py      # Trip expense breakdown tool
│   ├── place_search_tool.py            # Place and POI search tool
│   └── weather_info_tool.py            # Weather information tool
│
├── utils/
│   ├── config_loader.py                # Config file loader
│   ├── currency_converter.py           # Currency utility
│   ├── expense_calculator.py           # Expense calculation utility
│   ├── model_loader.py                 # LLM model initialization
│   ├── place_info_search.py            # Place search utility
│   └── weather_info.py                 # Weather data utility
│
├── .env                                # Environment variables (not committed)
├── .gitignore
├── .python-version
├── Dockerfile.api                      # Dockerfile for FastAPI backend
├── Dockerfile.streamlit                # Dockerfile for Streamlit frontend
├── docker-compose.yml                  # Multi-container orchestration
├── main.py                             # FastAPI application entry point
├── streamlit_app.py                    # Streamlit UI entry point
├── requirements.txt
├── setup.py
└── pyproject.toml
```

---

## CI/CD Workflow Configuration


The `deploy.yml` file under `.github/workflows/` defines a two-job pipeline triggered on every push to the `main` branch.

**Continuous-Integration** runs on a GitHub-hosted `ubuntu-latest` runner. It checks out the code, configures AWS credentials from GitHub Secrets, logs in to Amazon ECR, and builds and pushes two Docker images — one for the FastAPI backend (`Dockerfile.api`) and one for the Streamlit frontend (`Dockerfile.streamlit`) — tagged as `api-latest` and `streamlit-latest` respectively.

**Continuous-Deployment** runs on the self-hosted runner installed on the EC2 instance. It pulls the latest images from ECR, copies the `.env` file from a persistent location on the EC2 host into the workspace, brings down any running containers, and starts the updated stack using `docker-compose up -d`.

---

## Application Interface

e:\Agentic_Ai_Based_Trip_Planner\Documents\2 UIUX.png

The frontend is built with Streamlit and served on port 8501. Users enter a natural language travel query such as "Plan a 7-day trip to Kyoto in spring" into the destination input field. Quick-select destination chips are provided for common destinations including Kyoto, Santorini, Bali, Paris, and Patagonia. Submitting the query triggers the agentic workflow via the FastAPI backend.

---

## Sample Outputs

### New York City Trip Plan

e:\Agentic_Ai_Based_Trip_Planner\Documents\3 in-op ex -a.png

The agent generates a structured day-by-day itinerary. For a New York City trip, the output includes a morning-to-evening schedule with landmark recommendations, dining suggestions, accommodation options across different budget tiers, transportation guidance, and a detailed budget breakdown covering accommodation, food, transport, and attractions.

### London 2-Day Travel Plan

e:\Agentic_Ai_Based_Trip_Planner\Documents\4 in-op ex 2a.png



e:\Agentic_Ai_Based_Trip_Planner\Documents\5 in-op ex 2b.png

For a London trip, the agent produces a two-day plan with timed activity slots, restaurant recommendations, West End entertainment suggestions, transportation advice including the Oyster Card, accommodation recommendations, a full budget breakdown totalling approximately $820, current weather conditions, and practical travel tips.

---

## AWS Infrastructure

### EC2 Instance

e:\Agentic_Ai_Based_Trip_Planner\Documents\6 EC2 initiated.png

The application is deployed on an Amazon EC2 `t2.medium` instance named `ai-trip-planner` in the `us-east-1` region. The instance runs Ubuntu and hosts the self-hosted GitHub Actions runner as a systemd service, ensuring the deployment step executes directly on the target machine without requiring SSH from the pipeline.

### Amazon ECR Repository

e:\Agentic_Ai_Based_Trip_Planner\Documents\7 ecr initiated.png

A private Amazon ECR repository named `ai-trip-planner` is provisioned under account `107564013511` in `us-east-1`. The repository stores both Docker images — `api-latest` and `streamlit-latest` — with mutable tags and AES-256 encryption. Images are pushed here during the CI phase and pulled during the CD phase.

---

## CI/CD Pipeline Result

e:\Agentic_Ai_Based_Trip_Planner\Documents\8 cicd done.png

The GitHub Actions pipeline run #5 completed with a status of **Success** in 1 minute 52 seconds. The Continuous-Integration job finished in 1 minute 20 seconds and the Continuous-Deployment job completed in 28 seconds. Both jobs passed without errors, confirming that the Docker images were built, pushed to ECR, and deployed to the EC2 instance successfully.

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq (LLaMA 3) |
| Agent Framework | LangGraph |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Containerization | Docker, Docker Compose |
| Container Registry | Amazon ECR |
| Cloud Compute | Amazon EC2 (t2.medium) |
| CI/CD | GitHub Actions |
| External APIs | OpenWeatherMap, Tavily, Foursquare, Google Places, Exchange Rate API |

---

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
GPLACES_API_KEY=your_google_places_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
FOURSQUARE_API_KEY=your_foursquare_api_key
```

These variables are stored as GitHub Secrets for the CI/CD pipeline and as a persistent `.env` file on the EC2 instance for the deployment step.

---

## GitHub Actions Secrets Required

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `AWS_DEFAULT_REGION` | AWS region (e.g. us-east-1) |
| `ECR_REPO` | ECR repository name (e.g. ai-trip-planner) |