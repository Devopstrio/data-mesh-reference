import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("mesh-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="Data Mesh Reference API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/domains")
def get_domains():
    return [
        {"id": "dom-sales", "name": "Sales Domain", "products_count": 12, "maturity": "Level 4"},
        {"id": "dom-finance", "name": "Finance Domain", "products_count": 8, "maturity": "Level 5"},
        {"id": "dom-hr", "name": "HR Domain", "products_count": 4, "maturity": "Level 2"}
    ]

@app.get("/products")
def get_products():
    return [
        {"id": "prod-sales-rev", "name": "Revenue Attribution", "domain": "Sales", "quality": 0.98, "freshness": "5m"},
        {"id": "prod-fin-ledger", "name": "General Ledger", "domain": "Finance", "quality": 0.99, "freshness": "1h"},
        {"id": "prod-hr-talent", "name": "Talent Pipeline", "domain": "HR", "quality": 0.85, "freshness": "24h"}
    ]

@app.get("/governance/summary")
def get_governance_summary():
    return {
        "global_mesh_maturity": 0.78,
        "federated_council_status": "ALIGNED",
        "total_active_contracts": 142,
        "policy_violations": 2
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_data_products": 42,
        "active_consumers": 850,
        "avg_product_quality": "94.2%",
        "monthly_mesh_cost": "$62,800"
    }

@app.post("/domains/register")
def register_domain(name: str):
    logger.info(f"Registering new mesh domain: {name}")
    return {"status": "Domain Pending Approval", "id": "dom_new_123"}
