import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app.main import app
from fastapi.testclient import TestClient

def main():
    with TestClient(app) as client:
        root_res = client.get("/")
        health_res = client.get("/api/v1/health")
        print("ROOT RESPONSE:", root_res.json())
        print("HEALTH RESPONSE:", health_res.json())

if __name__ == "__main__":
    main()
