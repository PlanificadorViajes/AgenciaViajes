# Flight & Accommodation Search System - Implementation Plan

## Project Transformation
From: Travel itinerary generator
To: Flight + Accommodation search system with web scraping

---

## Architecture Overview

```
Frontend (React + TypeScript)
    ↓
FastAPI Backend
    ↓
Orchestrator
    ↓
Agents:
  - FlightPlanner (scraping)
  - FlightAnalyst (top 5)
  - HousePlanner (scraping)
  - HouseAnalyst (top 5)
  - Documentalist (formatting)
    ↓
WebScraper Tool (Playwright/httpx)
```

---

## Backend Structure

```
backend/
├── main.py
├── api/
│   └── routes.py
├── orchestrator/
│   └── flow.py
├── agents/
│   ├── flight_planner.py
│   ├── flight_analyst.py
│   ├── house_planner.py
│   ├── house_analyst.py
│   └── documentalist.py
├── tools/
│   └── web_scraper.py
├── models/
│   ├── flight_models.py
│   └── house_models.py
├── persistence/
└── requirements.txt
```

---

## Frontend Structure

```
frontend/
├── pages/
│   ├── index.tsx
│   └── results.tsx
├── components/
│   ├── FlightForm.tsx
│   ├── FlightList.tsx
│   ├── HouseList.tsx
│   ├── OfferCard.tsx
│   └── ApprovalPanel.tsx
├── services/
│   └── api.ts
└── styles/
```

---

## Implementation Steps

### Phase 1: Backend Models & Tools
- [ ] Create flight models (FlightRequest, FlightOffer)
- [ ] Create house models (HouseRequest, HouseOffer)
- [ ] Implement WebScraper tool

### Phase 2: Backend Agents
- [ ] FlightPlannerAgent (scraping)
- [ ] FlightAnalystAgent (top 5 selection)
- [ ] HousePlannerAgent (scraping)
- [ ] HouseAnalystAgent (top 5 selection)
- [ ] DocumentalistAgent (formatting)

### Phase 3: Backend Orchestrator & API
- [ ] Implement orchestrator flow
- [ ] Create API routes
- [ ] Update main.py

### Phase 4: Frontend
- [ ] FlightForm component (structured form)
- [ ] OfferCard component
- [ ] FlightList component
- [ ] HouseList component
- [ ] ApprovalPanel component
- [ ] API service
- [ ] Main page integration

### Phase 5: Integration & Testing
- [ ] End-to-end flow test
- [ ] Error handling
- [ ] HITL implementation
- [ ] "No offers" flow validation

---

## Critical Rules

1. **No flights found → Show exact message + stop**
   - Message: "No hemos encontrado ofertas con tus requisitos"
   - Do NOT execute house search

2. **HITL points:**
   - After showing top 5 flights
   - After showing top 5 houses

3. **Structured input (no free text):**
   - origin_airport
   - destination_country
   - departure_date
   - return_date
   - passengers
   - max_budget

4. **Real scraping targets:**
   - Flights: Skyscanner, Google Flights, Kayak, Kiwi, Expedia
   - Houses: Airbnb, Booking

5. **Maintain existing:**
   - LLM client infrastructure
   - API keys configuration
   - Environment variables
