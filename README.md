# ** 🔗Supply Chain Optimization App**

In the digital age, where supply chains are the backbone of global commerce, the ability to **predict, optimize, and react** in real time has become a competitive superpower. This project is a modern, AI-powered command center designed to tackle the complex challenges of supply chain management with intelligence and style.

With an interactive interface built using **React, TypeScript, and Tailwind CSS**, and multiple machine learning models serving as the brains behind the operation, this project bridges the gap between **human decision-making and AI-driven insights**. 

An intelligent, modern dashboard designed to optimize supply chain operations through smart routing, demand forecasting, real-time monitoring, and data-driven decision making.



[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.2.0-blue)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)](https://fastapi.tiangolo.com/)

> An AI-powered command center for modern supply chain management, combining machine learning predictions with real-time optimization algorithms.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview
![Uploading Screenshot 2025-12-08 000627.png…]()


This project presents a comprehensive supply chain management system designed to optimize logistics operations, inventory tracking, and supply chain visibility. The system addresses critical challenges in modern supply chain operations including real-time tracking, inventory optimization, and data-driven decision making.

### Key Capabilities

- **🤖 AI-Powered Predictions** - Machine learning models for supplier reliability, shipment delays, and demand forecasting
- **📊 Real-Time Optimization** - EOQ calculations, safety stock optimization, and vehicle routing
- **🗄️ Data Persistence** - CSV-based database for easy data management and portability
- **📈 Interactive Dashboard** - Modern React interface with real-time visualizations
- **⚡ Parallel Processing** - Multi-threaded batch operations for large-scale analysis
- **🗺️ Route Optimization** - Advanced VRP algorithms with interactive map visualization

---

## ✨ Features

### Machine Learning & Predictions

- **Supplier Reliability Predictor**
  - Random Forest classifier
  - Confidence intervals and feature importance
  - Historical performance tracking

- **Shipment Delay Predictor**
  - Logistic regression model
  - Risk level classification
  - Probability estimates

- **Inventory Forecasting**
  - ARIMA time series model
  - Multi-step ahead predictions
  - Confidence intervals

### Optimization Algorithms

- **Inventory Optimization**
  - Economic Order Quantity (EOQ)
  - Safety stock calculations
  - Reorder point optimization
  - Service level analysis

- **Vehicle Routing Problem (VRP)**
  - Clarke-Wright Savings Algorithm
  - Nearest Neighbor heuristic
  - Interactive route visualization
  - Distance matrix optimization

- **Parallel Processing**
  - Batch supplier evaluation
  - Multi-threaded computations
  - Progress tracking

### Data Management

- **CSV Database**
  - Suppliers management
  - Shipments tracking
  - Inventory monitoring
  - Predictions logging
  - Routes history

- **Real-Time Statistics**
  - Total predictions made
  - Suppliers registered
  - Shipments tracked
  - Performance rankings

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │Dashboard │ │Predictor │ │Optimizer │ │  Viewer  │  │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │
│       └────────────┴────────────┴────────────┘         │
│                        │                                │
│                   API Service                           │
└───────────────────────┼─────────────────────────────────┘
                        │ REST API
┌───────────────────────┼─────────────────────────────────┐
│                   Backend (FastAPI)                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Prediction Service                  │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │   │
│  │  │ Supplier │ │ Shipment │ │Inventory │        │   │
│  │  │  Model   │ │  Model   │ │  Model   │        │   │
│  │  └──────────┘ └──────────┘ └──────────┘        │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │          Optimization Algorithms                 │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │   │
│  │  │   EOQ    │ │   VRP    │ │ Parallel │        │   │
│  │  └──────────┘ └──────────┘ └──────────┘        │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │              CSV Database Layer                  │   │
│  │  suppliers.csv | shipments.csv | inventory.csv  │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend
- **Framework:** FastAPI 0.104.1
- **ML Libraries:** scikit-learn 1.3.2, statsmodels 0.14.0
- **Optimization:** NetworkX 3.2.1, SciPy 1.11.4
- **Data Processing:** Pandas 2.1.3, NumPy 1.26.2
- **Server:** Uvicorn (ASGI)

### Frontend
- **Framework:** React 18.2.0 + Vite
- **Language:** JavaScript/TypeScript
- **Styling:** Tailwind CSS
- **Visualization:** Recharts, Leaflet
- **HTTP Client:** Fetch API

### Database
- **Type:** CSV-based file storage
- **Handler:** Pandas DataFrame operations

---

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Clone repository
git clone https://github.com/SyuzannE/Supply-Chain-Management-project.git
cd Supply-Chain-Management-project

# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app:app --reload
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend (from root directory)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## 📖 Usage

### 1. Start the Application

**Backend:**
```bash
cd backend
uvicorn app:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### 2. Access the Dashboard

Open your browser and navigate to `http://localhost:5173`

### 3. Explore Features

#### **Supplier Prediction**
1. Navigate to "🏭 Supplier Predictor"
2. Enter supplier details (lead time, cost, past orders)
3. Click "Predict Reliability"
4. View reliability score, confidence interval, and recommendations

#### **Inventory Optimization**
1. Navigate to "📦 Inventory Optimizer"
2. Input annual demand, unit cost, demand std, lead time
3. Click "Optimize Inventory"
4. Review EOQ, reorder point, safety stock, and cost analysis

#### **Vehicle Routing**
1. Navigate to "🗺️ Vehicle Routing"
2. Set depot location and add customer locations
3. Select algorithm (Clarke-Wright or Nearest Neighbor)
4. Click "Optimize Routes"
5. View optimized routes on interactive map

#### **Database Viewer**
1. Navigate to "💾 Database"
2. Switch between views:
   - 📊 Statistics - Overall system metrics
   - 🏭 Suppliers - Supplier records with CRUD operations
   - 🚚 Shipments - Shipment tracking history
   - 📦 Inventory - Inventory items
   - 🎯 Predictions - ML prediction logs
   - 📈 Performance - Supplier performance rankings

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### **Health Check**
```http
GET /
GET /health
```

#### **Predictions**
```http
POST /api/v1/predict/supplier
POST /api/v1/predict/shipment
GET  /api/v1/predict/inventory?steps=5&confidence_level=0.95
```

#### **Optimization**
```http
POST /api/v1/optimize/inventory
POST /api/v1/optimize/routing
```

#### **Database Operations**
```http
GET    /api/v1/suppliers
POST   /api/v1/suppliers
GET    /api/v1/suppliers/{id}
DELETE /api/v1/suppliers/{id}
GET    /api/v1/shipments
GET    /api/v1/inventory
GET    /api/v1/predictions/history
GET    /api/v1/statistics
GET    /api/v1/suppliers/performance/ranking
```

#### **Batch Processing**
```http
POST /api/v1/batch/suppliers
```

#### **Model Management**
```http
GET  /api/v1/models/info
POST /api/v1/models/reload
```

### Example Request

**Predict Supplier Reliability:**
```bash
curl -X POST "http://localhost:8000/api/v1/predict/supplier" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_time": 7,
    "cost": 50.0,
    "past_orders": 100
  }'
```

**Response:**
```json
{
  "reliability_score": 0.85,
  "confidence_interval": {
    "lower": 0.78,
    "upper": 0.92
  },
  "feature_importance": {
    "lead_time": 0.45,
    "cost": 0.30,
    "past_orders": 0.25
  },
  "model": "RandomForest",
  "prediction_time": "0.02ms"
}
```

---

## 🗄️ Database Schema

### Suppliers Table
```csv
supplier_id, name, lead_time, cost, past_orders, reliability_score, created_at
```

### Shipments Table
```csv
shipment_id, delivery_time, quantity, delay_time, status, created_at
```

### Inventory Table
```csv
inventory_id, item_name, quantity, reorder_point, safety_stock, created_at
```

### Predictions Table
```csv
prediction_id, prediction_type, input_data, result, model_used, created_at
```

### Routes Table
```csv
route_id, depot, customers, total_distance, algorithm, created_at
```

---

## 📁 Project Structure

```
Supply-Chain-Management-project/
├── backend/
│   ├── src/
│   │   ├── core/              # Config, logger, exceptions
│   │   ├── services/          # ML prediction services
│   │   ├── optimization/      # Optimization algorithms
│   │   └── models/            # Data models
│   ├── data/                  # CSV database files
│   ├── ml_models/             # Trained ML models
│   ├── app.py                 # FastAPI application
│   ├── csv_database.py        # Database handler
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API service layer
│   │   ├── styles/            # CSS styling
│   │   ├── App.jsx            # Main app component
│   │   └── main.jsx           # Entry point
│   ├── package.json           # NPM dependencies
│   └── vite.config.ts         # Vite configuration
│
├── docs/                      # Documentation
├── LICENSE                    # Apache 2.0 License
└── README.md                  # This file
```

---

## 🎯 Key Algorithms

### Economic Order Quantity (EOQ)
```
EOQ = √((2 × D × S) / H)

Where:
- D = Annual demand
- S = Ordering cost
- H = Holding cost per unit
```

### Safety Stock Calculation
```
Safety Stock = Z × σ × √L

Where:
- Z = Service level factor (e.g., 1.65 for 95%)
- σ = Demand standard deviation
- L = Lead time
```

### Clarke-Wright Savings Algorithm
```
Savings(i,j) = d(0,i) + d(0,j) - d(i,j)

Where:
- d(0,i) = Distance from depot to customer i
- d(i,j) = Distance between customers i and j
```

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📊 Performance Metrics

- **API Response Time:** < 100ms (average)
- **ML Prediction Time:** < 50ms
- **Route Optimization:** < 2s for 20 locations
- **Batch Processing:** 100 suppliers/second

---

## 🔐 Security

- CORS enabled for cross-origin requests
- Input validation with Pydantic
- Error handling and logging
- No sensitive data in repository

---

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

---

## 📧 Contact

**Project Maintainer:** [@SyuzannE](https://github.com/SyuzannE)

**Repository:** [Supply-Chain-Management-project](https://github.com/SyuzannE/Supply-Chain-Management-project)

---

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- scikit-learn for ML capabilities
- React team for the frontend library
- Leaflet for interactive maps
- All contributors and supporters

---

## 📈 Roadmap

- [ ] PostgreSQL database integration
- [ ] User authentication and authorization
- [ ] Real-time WebSocket updates
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Cloud deployment (AWS/Azure)

---

<div align="center">

**Built for Supply Chain Optimization**

⭐ Star this repository if you find it helpful!

</div>





