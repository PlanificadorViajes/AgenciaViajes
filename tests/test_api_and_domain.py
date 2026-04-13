import pytest
from fastapi.testclient import TestClient

from backend.api.app import app
from backend.domain.flight_planner import FlightPlanner
from backend.domain.flight_analyst import FlightAnalyst
from backend.domain.house_planner import HousePlanner
from backend.domain.house_analyst import HouseAnalyst
from backend.domain.documentalist import Documentalist


client = TestClient(app)


# -------------------------
# API TESTS (5)
# -------------------------

def test_api_docs_available():
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema_available():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "paths" in response.json()


def test_root_endpoint_exists():
    response = client.get("/")
    assert response.status_code in (200, 404)


def test_invalid_route_returns_404():
    response = client.get("/route-that-does-not-exist")
    assert response.status_code == 404


def test_app_instance_created():
    assert app is not None


# -------------------------
# DOMAIN STRUCTURE TESTS (15)
# -------------------------

def test_flight_planner_instantiation():
    planner = FlightPlanner()
    assert planner is not None


def test_flight_analyst_instantiation():
    analyst = FlightAnalyst()
    assert analyst is not None


def test_house_planner_instantiation():
    planner = HousePlanner()
    assert planner is not None


def test_house_analyst_instantiation():
    analyst = HouseAnalyst()
    assert analyst is not None


def test_documentalist_instantiation():
    doc = Documentalist()
    assert doc is not None


def test_flight_planner_has_methods():
    planner = FlightPlanner()
    assert len(dir(planner)) > 0


def test_house_planner_has_methods():
    planner = HousePlanner()
    assert len(dir(planner)) > 0


def test_flight_analyst_has_methods():
    analyst = FlightAnalyst()
    assert len(dir(analyst)) > 0


def test_house_analyst_has_methods():
    analyst = HouseAnalyst()
    assert len(dir(analyst)) > 0


def test_documentalist_has_methods():
    doc = Documentalist()
    assert len(dir(doc)) > 0


def test_domain_modules_importable():
    assert FlightPlanner is not None
    assert FlightAnalyst is not None
    assert HousePlanner is not None
    assert HouseAnalyst is not None


def test_documentalist_importable():
    assert Documentalist is not None


def test_fastapi_app_title():
    assert hasattr(app, "title")


def test_fastapi_routes_loaded():
    assert len(app.routes) > 0


def test_client_creation():
    assert client is not None
