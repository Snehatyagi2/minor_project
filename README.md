# 🌍 Advanced AQI Intelligence System

A Streamlit-based web application that predicts and forecasts the **Air Quality Index (AQI)** using live pollution data, real-time weather data, and a trained machine learning model. The system provides comprehensive AQI reports, 7-day forecasts, pollution source analysis, and satellite-based downscaling simulations.

Recently updated with a **Modern SaaS Dashboard** UI inspired by Vercel and Linear, featuring a deep slate radial gradient theme, glassmorphism cards, split-view interactive mapping, and dynamic visual components.

---

## 📑 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Setup & Installation](#-setup--installation)
- [Running the Application](#-running-the-application)
- [Usage Guide](#-usage-guide)
- [Module Documentation](#-module-documentation)
- [External APIs Used](#-external-apis-used)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

| Feature | Description |
|---|---|
| **Modern SaaS Dashboard** | A highly polished, responsive split-view UI featuring deep slate gradients, glassmorphism cards, and interactive hover states. |
| **Live AQI Report** | Fetches real-time PM2.5, PM10, and NO2 data from multiple sensor locations in any city |
| **ML-Based AQI Prediction** | Uses a trained Random Forest Regressor model to predict AQI from pollutant and weather inputs |
| **7-Day AQI Forecast** | Generates a forward-looking 7-day AQI forecast using historical NO2 trends, temperature, and humidity adjustments |
| **Pollution Score** | Calculates a weighted pollution score combining PM2.5 (50%), PM10 (30%), and NO2 (20%) |
| **Area Classification** | Automatically categorizes monitoring locations as Industrial, Traffic, Residential, or Mixed |
| **Pollution Source Analysis** | Provides contextual explanations for high AQI readings based on area type and pollutant levels |
| **Satellite Downscaling** | Simulates a geographical AQI grid over Delhi using randomized satellite NO2 readings and the ML model |

---

## 📁 Project Structure

```
minor_project/
├── app.py                  # Main Streamlit web application (entry point)
├── README.md               # Project documentation (this file)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (Create this using .env.example)
├── .env.example            # Template for environment variables
│
├── .streamlit/
│   └── config.toml         # Global theme configuration for Streamlit
│
├── model/
│   └── model.pkl           # Trained RandomForestRegressor model (binary)
│
└── src/
    ├── __init__.py          # Makes src/ a Python package
    ├── api_pollution.py     # OpenAQ API integration for pollution data
    ├── api_weather.py       # OpenWeatherMap API integration for weather data
    ├── logic.py             # Helper functions: scoring, classification, reasoning
    ├── predict.py           # Core prediction pipeline & report generation
    ├── satellite.py         # Simulated satellite grid data generation
    └── train.py             # Script to train and save the ML model
```

---

## 🔄 How It Works

The application follows a pipeline architecture:

```
┌─────────────┐     ┌───────────────────┐     ┌──────────────────┐     ┌────────────────┐
│  User Input │────>│  Fetch Live Data  │────>│  ML Prediction   │────>│  Display Report │
│  (City Name)│     │  (APIs: Pollution │     │  (RandomForest   │     │  (Streamlit UI) │
│             │     │   + Weather)      │     │   Model)         │     │                │
└─────────────┘     └───────────────────┘     └──────────────────┘     └────────────────┘
```

### Step-by-Step Flow

1. **User enters a city name** in the top navigation bar (defaults to "Delhi").
2. **"Run Analysis" button (Full AQI Report):**
   - Fetches real-time pollution data (PM2.5, PM10, NO2) from OpenAQ API for all sensor locations in the city.
   - Fetches current temperature and humidity from OpenWeatherMap API.
   - For each sensor location:
     - Computes a **Pollution Score** using weighted formula.
     - Predicts **AQI** using the trained Random Forest model.
     - Classifies the **area type** (Industrial / Traffic / Residential / Mixed).
     - Generates a **7-day AQI forecast** using trend analysis.
     - Provides a **reason** for the current pollution level.
   - Displays the full report in a stacked, clean list format alongside a 7-day city-wide forecast graph.
3. **"Run Analysis" button (Satellite Downscaling):**
   - Fetches current weather (temperature, humidity).
   - Generates 20 random geo-points within Delhi's bounding box with simulated NO2 values.
   - Predicts AQI for each point using the ML model.
   - Activates the Split View Dashboard: Displays an interactive heatmap on the left, and an AI Insights panel on the right (showing health advisories, top polluted zones, and cleanest zones).

---

## 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.8+** | Programming language |
| **Streamlit** | Web application framework for the interactive dashboard |
| **Pandas** | Data manipulation and tabular display |
| **NumPy** | Numerical computations for prediction arrays |
| **Scikit-learn** | Machine learning (RandomForestRegressor) |
| **Plotly & Folium** | Interactive charting and mapping |
| **Requests / python-dotenv** | HTTP client for API calls and environment variable management |
| **Pickle** | Model serialization/deserialization |

---

## 📋 Prerequisites

Before setting up the project, make sure you have:

1. **Python 3.8 or higher** installed on your system.
   - Verify by running: `python --version`
2. **pip** (Python package manager) — usually bundled with Python.
3. **An OpenWeatherMap API Key** (free tier is sufficient).
   - Sign up at: [https://openweathermap.org/api](https://openweathermap.org/api)
   - Navigate to your API Keys section and copy your key.

---

## 🚀 Setup & Installation

Follow these steps precisely to get the application up and running.

### Step 1: Clone or Download the Project

```bash
# If using Git
git clone <repository-url>
cd minor_project
```

Or simply download and extract the project folder, then open a terminal inside `minor_project/`.

### Step 2: Install Python Dependencies

Install all required packages using pip:

```bash
pip install -r requirements.txt
```

### Step 3: Train the Machine Learning Model

The model must be trained before running the application for the first time. This script creates the `model/model.pkl` file.

```bash
python src/train.py
```

You should see the output:
```
Model Ready
```
> **Note:** A pre-trained `model.pkl` is already included in the `model/` directory. You only need to re-run this step if you modify the training data or delete the model file.

### Step 4: Configure Environment Variables

The application relies on API keys to fetch live weather and pollution data.

1. In the root directory (`minor_project/`), you will find a file named `.env.example`.
2. **Create a copy** of this file and rename it to `.env` (note the dot at the beginning).
3. Open `.env` in a text editor and replace the placeholder text with your actual API keys:

```env
OPENWEATHER_API_KEY=your_actual_api_key_here
OPENAQ_API_KEY=your_openaq_api_key_here
```
> ⚠️ **Important:** Without the `OPENWEATHER_API_KEY`, the weather-dependent features will show "Weather not available" or "Data not available" errors. OpenAQ currently works without a key for basic limits, but providing one ensures stability.

---

## ▶️ Running the Application

Once your `.env` file is set up and dependencies are installed, start the Streamlit app with:

```bash
python -m streamlit run app.py
```

The terminal will display:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open the **Local URL** (`http://localhost:8501`) in your web browser to view the interactive dashboard.

To stop the application, press `Ctrl + C` in the terminal.

---

## 📖 Usage Guide

### Generating a Full AQI Report

1. Open the app in your browser.
2. In the top navigation bar, use the **"City"** dropdown to select or type the name of a city (e.g., `Delhi`, `Mumbai`, `London`).
3. Ensure the Analysis Mode is set to **"Full AQI Report"**.
4. Click the blue gradient **"Run"** button.
5. The dashboard will populate with:
   - A unified 7-day AQI forecast graph for the city.
   - A stacked list of monitoring stations displaying live AQI scores and area classifications.

### Viewing Satellite AQI (Downscaled)

1. Enter a city name in the top navbar.
2. Toggle the Analysis Mode to **"Satellite Downscaling"**.
3. Click the **"Run"** button.
4. The dashboard will transform into a Split View layout:
   - **Left Panel:** An interactive Map showing pollution hotspots and an AQI distribution graph.
   - **Right Panel (Insights):** A dynamically generated Health Advisory, alongside the exact coordinates of the top 3 most polluted and top 3 cleanest zones.

---

## 📚 Module Documentation

### `app.py` — Main Application
The entry point of the Streamlit web application. Contains all UI logic, HTML/CSS for the SaaS dashboard design, split views, and controls.

### `src/train.py` — Model Training
Trains a **Random Forest Regressor** on a built-in dataset to predict AQI from NO2, Temperature, and Humidity. Saves the model to `model/model.pkl`.

### `src/predict.py` — Prediction Pipeline
Contains the core prediction logic, including `smart_forecast` for generating 7-day predictions and `generate_report` for orchestrating data retrieval and ML inference.

### `src/api_pollution.py` — Pollution Data API
Interfaces with the **OpenAQ v2 API** to fetch real-time and historical NO2, PM2.5, and PM10 pollution data.

### `src/api_weather.py` — Weather Data API
Interfaces with the **OpenWeatherMap API** to fetch current weather conditions.

### `src/logic.py` — Helper Logic
Utility functions for scoring, classification (Industrial/Traffic/Residential), and generating contextual reasoning text.

### `src/satellite.py` — Satellite Grid Simulation
Generates random geographic coordinates within Delhi's bounding box and simulates NO2 values for downscaled analysis.

---

## ❓ Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `"Data not available"` when generating report | Weather API key not set, or pollution API returned no data for the city | Ensure `.env` is configured correctly. Try a major city like "Delhi" or "London". |
| `"Weather not available"` on satellite downscaling | Missing or invalid OpenWeatherMap API key | Verify your API key is correct inside your `.env` file. |
| `FileNotFoundError: model/model.pkl` | Model has not been trained yet | Run `python src/train.py` to generate the model file. |
| `ModuleNotFoundError: No module named 'src'` | Missing `__init__.py` in the `src/` folder | Ensure `src/__init__.py` exists (even if empty). |
| `ModuleNotFoundError: No module named 'streamlit'` | Dependencies not installed | Run `pip install -r requirements.txt`. |
| App opens but buttons do nothing | Streamlit re-runs the entire script on each interaction | Click a button and wait — data is being fetched from external APIs. |

---

## 📄 License

This project is developed for academic/educational purposes as a Minor Project.
