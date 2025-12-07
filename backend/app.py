"""
Enhanced FastAPI Application with CSV Database Support
Integrates:
- Computer Networks: RESTful API design
- Software Engineering: Layered architecture
- All optimization services
- CSV Database persistence
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn

from src.services.prediction_service import get_prediction_service
from src.optimization.inventory_optimizer import InventoryOptimizer
from src.optimization.vehicle_routing import VehicleRoutingOptimizer
from src.optimization.parallel_optimizer import ParallelOptimizer
from src.core.logger import get_logger
from src.core.config import settings
from src.core.exceptions import SupplyChainException

# Import CSV database
from csv_database import db

logger = get_logger(__name__)

app = FastAPI(
    title="Supply Chain Optimization API",
    description="Advanced supply chain optimization with ML, graph algorithms, and CSV database",
    version="2.0.0"
)

# ==================== CORS CONFIG ====================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.security.get("cors_origins", ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODELS ====================

class SupplierInput(BaseModel):
    lead_time: int = Field(..., ge=1, le=365)
    cost: float = Field(..., gt=0)
    past_orders: int = Field(..., ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "lead_time": 7,
                "cost": 50.0,
                "past_orders": 100
            }
        }


class SupplierData(BaseModel):
    supplier_id: Optional[str] = None
    name: str
    lead_time: float
    cost: float
    past_orders: int
    reliability_score: Optional[float] = None


class ShipmentInput(BaseModel):
    delivery_time: int = Field(..., ge=1)
    quantity: int = Field(..., ge=1)
    delay_time: int = Field(..., ge=0)


class InventoryOptimizationInput(BaseModel):
    annual_demand: float = Field(..., gt=0)
    unit_cost: float = Field(..., gt=0)
    demand_std: float = Field(..., ge=0)
    lead_time_days: int = Field(..., ge=1)


class LocationInput(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    name: Optional[str] = "Location"
    demand: Optional[float] = 0.0


class RoutingInput(BaseModel):
    depot: LocationInput
    customers: List[LocationInput]
    algorithm: Optional[str] = "clarke_wright"

# ==================== STARTUP/SHUTDOWN ====================

@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("SUPPLY CHAIN OPTIMIZATION API STARTING")
    logger.info("=" * 60)

    try:
        prediction_service = get_prediction_service()
        logger.info("Prediction service initialized")

        logger.info("CSV Database ready")
        logger.info("=" * 60)
        logger.info("API READY")
        logger.info(f"Environment: {settings.app.get('environment', 'development')}")
        logger.info(f"Version: {settings.app.get('version', '2.0.0')}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("API shutting down...")

# ==================== HEALTH ENDPOINTS ====================

@app.get("/", tags=["Health"])
async def root():
    prediction_service = get_prediction_service()
    model_info = prediction_service.get_model_info()
    stats = db.get_statistics()

    return {
        "status": "online",
        "message": "Supply Chain Optimization API v2.0 with CSV Database",
        "environment": settings.app.get("environment"),
        "models_loaded": model_info.get("loaded_models") 
                          or model_info.get("loaded_models", []),
        "database": {
            "type": "CSV",
            "statistics": stats
        },
        "features": {
            "predictions": True,
            "inventory_optimization": True,
            "vehicle_routing": True,
            "parallel_processing": True,
            "csv_persistence": True
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    prediction_service = get_prediction_service()
    stats = db.get_statistics()

    return {
        "status": "healthy",
        "models": prediction_service.get_model_info(),
        "database": stats,
        "config": {
            "parallel_workers": settings.optimization.parallel.get('max_workers', 4),
            "vehicle_capacity": settings.optimization.routing.get('vehicle_capacity', 1000)
        }
    }

# ==================== PREDICTIONS ====================

@app.post("/api/v1/predict/supplier", tags=["Predictions"])
async def predict_supplier_reliability(data: SupplierInput):
    try:
        prediction_service = get_prediction_service()
        result = prediction_service.predict_supplier_reliability(
            lead_time=data.lead_time,
            cost=data.cost,
            past_orders=data.past_orders
        )
        
        # Log prediction to CSV database
        db.log_prediction(
            prediction_type="supplier",
            input_data=data.dict(),
            result=result,
            model_used=result.get("model", "RandomForest")
        )
        
        return result
        
    except SupplyChainException as e:
        raise HTTPException(status_code=400, detail=e.to_dict())
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/predict/inventory", tags=["Predictions"])
async def forecast_inventory(steps: int = 5, confidence_level: float = 0.95):
    try:
        prediction_service = get_prediction_service()
        result = prediction_service.forecast_inventory(steps, confidence_level)
        
        # Log forecast to CSV database
        db.log_prediction(
            prediction_type="inventory_forecast",
            input_data={"steps": steps, "confidence_level": confidence_level},
            result=result,
            model_used="ARIMA"
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Forecast error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/predict/shipment", tags=["Predictions"])
async def predict_shipment_delay(data: ShipmentInput):
    try:
        prediction_service = get_prediction_service()
        result = prediction_service.predict_shipment_delay(
            delivery_time=data.delivery_time,
            quantity=data.quantity,
            delay_time=data.delay_time
        )
        
        # Log prediction to CSV database
        db.log_prediction(
            prediction_type="shipment",
            input_data=data.dict(),
            result=result,
            model_used=result.get("model", "LogisticRegression")
        )
        
        # Save shipment record to CSV
        db.save_shipment({
            "delivery_time": data.delivery_time,
            "quantity": data.quantity,
            "delay_time": data.delay_time,
            "status": result.get("status", "Unknown")
        })
        
        return result
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== OPTIMIZATION ====================

@app.post("/api/v1/optimize/inventory", tags=["Optimization"])
async def optimize_inventory(data: InventoryOptimizationInput):
    try:
        optimizer = InventoryOptimizer()
        policy = optimizer.optimize_inventory_policy(
            annual_demand=data.annual_demand,
            unit_cost=data.unit_cost,
            demand_std=data.demand_std,
            lead_time_days=data.lead_time_days
        )

        result = {
            "economic_order_quantity": policy.economic_order_quantity,
            "reorder_point": policy.reorder_point,
            "safety_stock": policy.safety_stock,
            "average_inventory": policy.average_inventory,
            "total_annual_cost": policy.total_annual_cost,
            "service_level": policy.service_level,
            "number_of_orders": policy.number_of_orders
        }
        
        # Log optimization to CSV database
        db.log_prediction(
            prediction_type="inventory",
            input_data=data.dict(),
            result=result,
            model_used="EOQ_Model"
        )

        return result

    except Exception as e:
        logger.error(f"Inventory optimization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/optimize/routing", tags=["Optimization"])
async def optimize_vehicle_routes(data: RoutingInput):
    try:
        optimizer = VehicleRoutingOptimizer()

        depot_dict = {
            "lat": data.depot.lat,
            "lon": data.depot.lon,
            "name": data.depot.name,
        }

        customers = [
            {
                "lat": c.lat,
                "lon": c.lon,
                "name": c.name,
                "demand": c.demand,
            }
            for c in data.customers
        ]

        result = optimizer.optimize_routes(
            depot=depot_dict,
            customers=customers,
            algorithm=data.algorithm
        )
        
        # Log routing optimization to CSV
        db.log_prediction(
            prediction_type="routing",
            input_data={
                "depot": depot_dict,
                "customers": customers,
                "algorithm": data.algorithm
            },
            result=result,
            model_used=f"VRP_{data.algorithm}"
        )

        return result

    except Exception as e:
        logger.error(f"Routing optimization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== BATCH PROCESSING ====================

@app.post("/api/v1/batch/suppliers", tags=["Batch Processing"])
async def batch_evaluate_suppliers(suppliers: List[SupplierInput]):
    try:
        prediction_service = get_prediction_service()
        parallel_optimizer = ParallelOptimizer(max_workers=4)

        supplier_dicts = [s.dict() for s in suppliers]

        results = parallel_optimizer.parallel_map(
            lambda s: prediction_service.predict_supplier_reliability(
                lead_time=s["lead_time"],
                cost=s["cost"],
                past_orders=s["past_orders"]
            ),
            supplier_dicts
        )
        
        # Log batch prediction
        db.log_prediction(
            prediction_type="batch_supplier",
            input_data={"suppliers": supplier_dicts},
            result={"results": results, "total": len(suppliers)},
            model_used="RandomForest_Batch"
        )

        return {
            "total_suppliers": len(suppliers),
            "results": results
        }

    except Exception as e:
        logger.error(f"Batch evaluation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== CSV DATABASE ENDPOINTS ====================

@app.post("/api/v1/suppliers", tags=["Database"])
async def create_supplier(supplier: SupplierData):
    """Create or update supplier in CSV database"""
    try:
        success = db.save_supplier(supplier.dict())
        if success:
            return {"message": "Supplier saved successfully", "supplier": supplier}
        else:
            raise HTTPException(status_code=500, detail="Failed to save supplier")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/suppliers", tags=["Database"])
async def get_suppliers(limit: int = 100):
    """Get all suppliers from CSV database"""
    try:
        suppliers = db.get_suppliers(limit=limit)
        return {
            "suppliers": suppliers,
            "count": len(suppliers)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/suppliers/{supplier_id}", tags=["Database"])
async def get_supplier(supplier_id: str):
    """Get single supplier by ID"""
    try:
        supplier = db.get_supplier(supplier_id)
        if supplier:
            return supplier
        else:
            raise HTTPException(status_code=404, detail="Supplier not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/v1/suppliers/{supplier_id}", tags=["Database"])
async def delete_supplier(supplier_id: str):
    """Delete supplier from CSV database"""
    try:
        success = db.delete_supplier(supplier_id)
        if success:
            return {"message": "Supplier deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Supplier not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/shipments", tags=["Database"])
async def get_shipments(limit: int = 100):
    """Get all shipments from CSV database"""
    try:
        shipments = db.get_shipments(limit=limit)
        return {
            "shipments": shipments,
            "count": len(shipments)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/inventory", tags=["Database"])
async def get_inventory(limit: int = 100):
    """Get all inventory items from CSV database"""
    try:
        inventory = db.get_inventory(limit=limit)
        return {
            "inventory": inventory,
            "count": len(inventory)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/predictions/history", tags=["Database"])
async def get_prediction_history(
    limit: int = 100, 
    prediction_type: Optional[str] = None
):
    """Get prediction history from CSV database"""
    try:
        predictions = db.get_predictions(limit=limit, prediction_type=prediction_type)
        return {
            "predictions": predictions,
            "count": len(predictions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/statistics", tags=["Database"])
async def get_statistics():
    """Get overall system statistics"""
    try:
        stats = db.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/suppliers/performance/ranking", tags=["Database"])
async def get_supplier_performance():
    """Get supplier performance ranking"""
    try:
        performance = db.get_supplier_performance()
        return {
            "suppliers": performance,
            "count": len(performance)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== MODEL MANAGEMENT ====================

@app.get("/api/v1/models/info", tags=["Models"])
async def get_models_info():
    prediction_service = get_prediction_service()
    return prediction_service.get_model_info()


@app.post("/api/v1/models/reload", tags=["Models"])
async def reload_models():
    try:
        prediction_service = get_prediction_service()
        prediction_service.reload_models()
        return {"status": "success", "message": "Models reloaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== MAIN ====================

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload,
        log_level="info"
    )