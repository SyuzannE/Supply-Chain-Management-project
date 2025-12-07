"""
CSV Database Handler
Simple CSV-based data persistence for Supply Chain System
"""

import pandas as pd
import os
from datetime import datetime
from typing import List, Dict, Optional
import json
import uuid

class CSVDatabase:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # CSV file paths
        self.suppliers_file = os.path.join(data_dir, "suppliers.csv")
        self.shipments_file = os.path.join(data_dir, "shipments.csv")
        self.inventory_file = os.path.join(data_dir, "inventory.csv")
        self.predictions_file = os.path.join(data_dir, "predictions.csv")
        self.routes_file = os.path.join(data_dir, "routes.csv")
        
        # Initialize CSV files
        self._initialize_files()
    
    def _initialize_files(self):
        """Create CSV files with headers if they don't exist"""
        
        # Suppliers
        if not os.path.exists(self.suppliers_file):
            df = pd.DataFrame(columns=[
                'supplier_id', 'name', 'lead_time', 'cost', 
                'past_orders', 'reliability_score', 'created_at'
            ])
            df.to_csv(self.suppliers_file, index=False)
        
        # Shipments
        if not os.path.exists(self.shipments_file):
            df = pd.DataFrame(columns=[
                'shipment_id', 'delivery_time', 'quantity', 
                'delay_time', 'status', 'created_at'
            ])
            df.to_csv(self.shipments_file, index=False)
        
        # Inventory
        if not os.path.exists(self.inventory_file):
            df = pd.DataFrame(columns=[
                'inventory_id', 'item_name', 'quantity', 
                'reorder_point', 'safety_stock', 'created_at'
            ])
            df.to_csv(self.inventory_file, index=False)
        
        # Predictions
        if not os.path.exists(self.predictions_file):
            df = pd.DataFrame(columns=[
                'prediction_id', 'prediction_type', 'input_data', 
                'result', 'model_used', 'created_at'
            ])
            df.to_csv(self.predictions_file, index=False)
        
        # Routes
        if not os.path.exists(self.routes_file):
            df = pd.DataFrame(columns=[
                'route_id', 'depot', 'customers', 'total_distance', 
                'algorithm', 'created_at'
            ])
            df.to_csv(self.routes_file, index=False)
    
    # ==================== SUPPLIERS ====================
    
    def save_supplier(self, supplier_data: Dict) -> bool:
        """Save or update supplier"""
        try:
            df = pd.read_csv(self.suppliers_file)
            
            # Generate ID if not provided
            if 'supplier_id' not in supplier_data or not supplier_data['supplier_id']:
                supplier_data['supplier_id'] = str(uuid.uuid4())
            
            supplier_data['created_at'] = datetime.now().isoformat()
            
            # Append new row
            new_row = pd.DataFrame([supplier_data])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(self.suppliers_file, index=False)
            
            return True
        except Exception as e:
            print(f"Error saving supplier: {e}")
            return False
    
    def get_suppliers(self, limit: int = 100) -> List[Dict]:
        """Get all suppliers"""
        try:
            df = pd.read_csv(self.suppliers_file)
            df = df.head(limit)
            return df.to_dict('records')
        except Exception as e:
            print(f"Error reading suppliers: {e}")
            return []
    
    def get_supplier(self, supplier_id: str) -> Optional[Dict]:
        """Get single supplier by ID"""
        try:
            df = pd.read_csv(self.suppliers_file)
            supplier = df[df['supplier_id'] == supplier_id]
            if len(supplier) > 0:
                return supplier.iloc[0].to_dict()
            return None
        except Exception as e:
            print(f"Error getting supplier: {e}")
            return None
    
    def delete_supplier(self, supplier_id: str) -> bool:
        """Delete supplier by ID"""
        try:
            df = pd.read_csv(self.suppliers_file)
            df = df[df['supplier_id'] != supplier_id]
            df.to_csv(self.suppliers_file, index=False)
            return True
        except Exception as e:
            print(f"Error deleting supplier: {e}")
            return False
    
    def get_supplier_performance(self) -> List[Dict]:
        """Get supplier performance ranking"""
        try:
            df = pd.read_csv(self.suppliers_file)
            if len(df) == 0:
                return []
            
            # Sort by reliability score (descending) and cost (ascending)
            df['reliability_score'] = pd.to_numeric(df['reliability_score'], errors='coerce')
            df['cost'] = pd.to_numeric(df['cost'], errors='coerce')
            df = df.sort_values(['reliability_score', 'cost'], 
                               ascending=[False, True])
            
            return df.to_dict('records')
        except Exception as e:
            print(f"Error getting supplier performance: {e}")
            return []
    
    # ==================== SHIPMENTS ====================
    
    def save_shipment(self, shipment_data: Dict) -> bool:
        """Save shipment record"""
        try:
            df = pd.read_csv(self.shipments_file)
            
            shipment_data['shipment_id'] = str(uuid.uuid4())
            shipment_data['created_at'] = datetime.now().isoformat()
            
            new_row = pd.DataFrame([shipment_data])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(self.shipments_file, index=False)
            
            return True
        except Exception as e:
            print(f"Error saving shipment: {e}")
            return False
    
    def get_shipments(self, limit: int = 100) -> List[Dict]:
        """Get all shipments"""
        try:
            df = pd.read_csv(self.shipments_file)
            df = df.head(limit)
            return df.to_dict('records')
        except Exception as e:
            print(f"Error reading shipments: {e}")
            return []
    
    # ==================== INVENTORY ====================
    
    def save_inventory(self, inventory_data: Dict) -> bool:
        """Save inventory record"""
        try:
            df = pd.read_csv(self.inventory_file)
            
            inventory_data['inventory_id'] = str(uuid.uuid4())
            inventory_data['created_at'] = datetime.now().isoformat()
            
            new_row = pd.DataFrame([inventory_data])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(self.inventory_file, index=False)
            
            return True
        except Exception as e:
            print(f"Error saving inventory: {e}")
            return False
    
    def get_inventory(self, limit: int = 100) -> List[Dict]:
        """Get all inventory items"""
        try:
            df = pd.read_csv(self.inventory_file)
            df = df.head(limit)
            return df.to_dict('records')
        except Exception as e:
            print(f"Error reading inventory: {e}")
            return []
    
    # ==================== PREDICTIONS ====================
    
    def log_prediction(self, prediction_type: str, input_data: Dict, 
                      result: Dict, model_used: str) -> bool:
        """Log prediction to CSV"""
        try:
            df = pd.read_csv(self.predictions_file)
            
            prediction_record = {
                'prediction_id': str(uuid.uuid4()),
                'prediction_type': prediction_type,
                'input_data': json.dumps(input_data),
                'result': json.dumps(result),
                'model_used': model_used,
                'created_at': datetime.now().isoformat()
            }
            
            new_row = pd.DataFrame([prediction_record])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(self.predictions_file, index=False)
            
            return True
        except Exception as e:
            print(f"Error logging prediction: {e}")
            return False
    
    def get_predictions(self, limit: int = 100, 
                       prediction_type: Optional[str] = None) -> List[Dict]:
        """Get prediction history"""
        try:
            df = pd.read_csv(self.predictions_file)
            
            if prediction_type:
                df = df[df['prediction_type'] == prediction_type]
            
            df = df.head(limit)
            predictions = df.to_dict('records')
            
            # Parse JSON strings back to dicts
            for pred in predictions:
                try:
                    pred['input_data'] = json.loads(pred['input_data'])
                    pred['result'] = json.loads(pred['result'])
                except:
                    pass
            
            return predictions
        except Exception as e:
            print(f"Error reading predictions: {e}")
            return []
    
    # ==================== ROUTES ====================
    
    def save_route(self, route_data: Dict) -> bool:
        """Save route optimization result"""
        try:
            df = pd.read_csv(self.routes_file)
            
            route_record = {
                'route_id': str(uuid.uuid4()),
                'depot': json.dumps(route_data.get('depot', {})),
                'customers': json.dumps(route_data.get('customers', [])),
                'total_distance': route_data.get('total_distance', 0),
                'algorithm': route_data.get('algorithm', 'unknown'),
                'created_at': datetime.now().isoformat()
            }
            
            new_row = pd.DataFrame([route_record])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(self.routes_file, index=False)
            
            return True
        except Exception as e:
            print(f"Error saving route: {e}")
            return False
    
    def get_routes(self, limit: int = 100) -> List[Dict]:
        """Get route history"""
        try:
            df = pd.read_csv(self.routes_file)
            df = df.head(limit)
            routes = df.to_dict('records')
            
            # Parse JSON strings
            for route in routes:
                try:
                    route['depot'] = json.loads(route['depot'])
                    route['customers'] = json.loads(route['customers'])
                except:
                    pass
            
            return routes
        except Exception as e:
            print(f"Error reading routes: {e}")
            return []
    
    # ==================== STATISTICS ====================
    
    def get_statistics(self) -> Dict:
        """Get overall system statistics"""
        try:
            stats = {
                'total_suppliers': 0,
                'total_shipments': 0,
                'total_inventory_items': 0,
                'total_predictions': 0,
                'total_routes': 0,
                'last_updated': datetime.now().isoformat()
            }
            
            try:
                df = pd.read_csv(self.suppliers_file)
                stats['total_suppliers'] = len(df)
            except:
                pass
            
            try:
                df = pd.read_csv(self.shipments_file)
                stats['total_shipments'] = len(df)
            except:
                pass
            
            try:
                df = pd.read_csv(self.inventory_file)
                stats['total_inventory_items'] = len(df)
            except:
                pass
            
            try:
                df = pd.read_csv(self.predictions_file)
                stats['total_predictions'] = len(df)
            except:
                pass
            
            try:
                df = pd.read_csv(self.routes_file)
                stats['total_routes'] = len(df)
            except:
                pass
            
            return stats
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {
                'total_suppliers': 0,
                'total_shipments': 0,
                'total_inventory_items': 0,
                'total_predictions': 0,
                'total_routes': 0,
                'error': str(e)
            }

# Create global instance
db = CSVDatabase()