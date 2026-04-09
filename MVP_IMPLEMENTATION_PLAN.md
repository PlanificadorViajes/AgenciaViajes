# MVP Target Architecture Implementation Plan

## Target Architecture

Frontend  
↓  
FastAPI  
↓  
Orchestrator  
↓  
Analyst → Planner → Critic  
↓  
HITL  
↓  
PostgreSQL (with versioning)

---

## Implementation Roadmap

### 1. Backend Foundation
- Create FastAPI application
- Define REST endpoints:
  - POST /travel-request
  - GET /travel-plan/{id}
  - PUT /travel-plan/{id}
  - POST /travel-plan/{id}/refine
  - POST /travel-plan/{id}/human-review
- Integrate existing Orchestrator into API layer

### 2. Domain Model (Clean Architecture Layer)
- Create domain models:
  - TravelRequest
  - StructuredTravelSpec
  - TravelPlan
  - DayPlan
  - Activity
  - ValidationReport
  - PlanVersion
- Replace raw dict usage with structured models

### 3. Analyst Agent
- Create AnalystAgent
- Extract:
  - destination
  - duration
  - budget
  - preferences
  - constraints
- Output StructuredTravelSpec

### 4. Planner Agent
- Refactor GeneratorAgent into PlannerAgent
- Accept StructuredTravelSpec
- Produce TravelPlanDraft (typed model)

### 5. Critic Agent
- Adapt CriticAgent to evaluate TravelPlan model
- Produce ValidationReport model
- Add status:
  - approved
  - requires_refinement
  - requires_human_review

### 6. HITL Module
- Add HumanReviewService
- Store pending plans
- Allow:
  - approve
  - reject
  - edit
- Integrate into orchestrator flow

### 7. PostgreSQL Integration
- Add SQLAlchemy
- Create tables:
  - users
  - travel_requests
  - structured_specs
  - travel_plans
  - validation_reports
  - plan_versions
- Implement versioning strategy

### 8. Orchestrator Refactor
Flow:
TravelRequest  
→ Analyst  
→ Planner  
→ Critic  
→ If refinement → Planner  
→ If human_review → HITL  
→ Persist final version  

### 9. Frontend (MVP-level)
- Minimal React or simple HTML frontend
- Form submission
- Plan visualization
- Human review interface

---

## Final Deliverable Characteristics

- Fully modular multi-agent architecture
- REST API
- PostgreSQL persistence with versioning
- Human-in-the-loop capability
- Production-ready backend structure
- MVP frontend
