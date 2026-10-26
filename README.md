# 🚇 AI Public Transport Assistant - Chennai

An intelligent, multi-modal journey planner for Chennai, supporting Bus, Metro, and Suburban Rail. This application leverages real-world GTFS (General Transit Feed Specification) data and AI to provide the fastest and most accurate transit routes across the city.

![App Dashboard](docs/demo_dashboard.png)

## ✨ Features

- **⚡ High-Performance Routing**: A custom-built Dijkstra-based routing engine optimized for large-scale GTFS datasets, providing millisecond-level pathfinding.
- **🤖 AI-Powered Interface**: Natural language parsing of travel requests, converting "Go from Anna Nagar to Central" into precise routing parameters.
- **🗺️ Interactive Spatial Search**: PostGIS-powered stop search with fuzzy text matching and spatial proximity.
- **🌙 Modern Dark UI**: A premium, high-fidelity interface designed for clarity and ease of use, featuring a visual journey timeline.
- **📅 Real-time Schedules**: Accurate journey planning based on actual transit schedules, including arrival and departure times.

## 📸 Demo

### 1. Search & Discovery
Users can easily search for origin and destination stops with a responsive autocomplete system.
![Search Interface](docs/demo_search.png)

### 2. Intelligent Suggestions
The system provides the best route options, displaying clear transfer points and total duration.
![Journey Results](docs/demo_results.png)

### 3. Seamless Experience
From searching to calculating the best route, the app provides a smooth, intuitive flow.
![Calculation Process](docs/demo_calculating.png)

## 🛠️ Technical Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | Next.js 15, TypeScript, Tailwind CSS | Modern, responsive user interface |
| **Backend** | FastAPI, Python 3.10+ | High-performance asynchronous API |
| **Database** | PostgreSQL 16 + PostGIS | Spatial data storage and GTFS management |
| **AI Engine** | Claude AI | Natural Language Processing (NLP) |
| **Routing** | Custom Dijkstra Implementation | Deterministic fastest-path calculation |

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 16 with PostGIS extension

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-public-transport-assistant.git
   cd ai-public-transport-assistant
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Configure your .env file with DATABASE_URL and ANTHROPIC_API_KEY
   python main.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📐 Architecture
The system uses a decoupled architecture:
- **Frontend** $\rightarrow$ sends requests to **FastAPI**.
- **FastAPI** $\rightarrow$ queries **PostGIS** for spatial stops and **GTFS** for schedules.
- **Routing Engine** $\rightarrow$ computes the optimal path using a time-expanded graph.
- **AI Layer** $\rightarrow$ handles natural language intent extraction.

## 📄 License
This project is licensed under the MIT License.
