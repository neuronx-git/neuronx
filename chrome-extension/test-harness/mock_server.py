"""
Mock NeuronX API server for Chrome extension testing.

Run:
    cd chrome-extension/test-harness
    pip install fastapi uvicorn
    python mock_server.py

The extension (after setting API URL to http://127.0.0.1:8000 in settings)
can then search clients, fetch form data, validate, etc. against this mock.

Mock clients:
    contact_123 — John Smith (Express Entry, India)
    contact_456 — Maria Garcia (Spousal, Mexico)
    contact_789 — Raj Patel (Work Permit, India)
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="NeuronX API Mock (for Chrome extension testing)")

# Permissive CORS for extension testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOCK_CLIENTS = {
    "contact_123": {
        "id": "contact_123",
        "firstName": "John",
        "lastName": "Smith",
        "email": "john.smith@demo.neuronx.co",
        "phone": "+14165550100",
        "tags": ["nx:case:form_prep", "Express Entry", "demo-data"],
        "fields": {
            "date_of_birth": "1990-05-15",
            "country_of_citizenship": "India",
            "passport_number": "K1234567",
            "education_level": "Bachelor's Degree",
            "work_experience": "5",
            "marital_status": "married",
            "noc_code": "2173",
            "settlement_funds": "25000",
            "sponsor_name": "",
        },
    },
    "contact_456": {
        "id": "contact_456",
        "firstName": "Maria",
        "lastName": "Garcia",
        "email": "maria.garcia@demo.neuronx.co",
        "phone": "+14165550200",
        "tags": ["nx:case:under_review", "Spousal Sponsorship", "demo-data"],
        "fields": {
            "date_of_birth": "1988-11-22",
            "country_of_citizenship": "Mexico",
            "passport_number": "M9876543",
            "marital_status": "married",
            "marriage_date": "2015-06-10",
            "sponsor_name": "Carlos Garcia",
        },
    },
    "contact_789": {
        "id": "contact_789",
        "firstName": "Raj",
        "lastName": "Patel",
        "email": "raj.patel@demo.neuronx.co",
        "phone": "+14165550300",
        "tags": ["nx:case:docs_pending", "Work Permit", "demo-data"],
        "fields": {
            "date_of_birth": "1985-03-08",
            "country_of_citizenship": "India",
            "passport_number": "P7654321",
            "employer_name": "Acme Corp Canada",
            "job_title": "Software Engineer",
        },
    },
}

FIRM_DEFAULTS = {
    "rep_family_name": "Mehta",
    "rep_given_name": "Rajiv",
    "rep_organization": "Visa Master Canada",
    "rep_member_id": "R123456",
    "rep_email": "rajiv.mehta@demo.visamasters.ca",
    "rep_phone": "+14165559001",
}


@app.get("/health")
async def health():
    return {"status": "ok", "service": "mock", "clients": len(MOCK_CLIENTS)}


@app.get("/clients/search")
async def search_clients(q: str = Query(..., min_length=2)):
    q_lower = q.lower()
    results = [
        c
        for c in MOCK_CLIENTS.values()
        if q_lower in c["firstName"].lower()
        or q_lower in c["lastName"].lower()
        or q_lower in c["email"].lower()
        or q_lower in c["phone"]
    ]
    return {
        "query": q,
        "results": [
            {
                "id": c["id"],
                "name": f"{c['firstName']} {c['lastName']}",
                "email": c["email"],
                "phone": c["phone"],
                "tags": c["tags"],
            }
            for c in results
        ],
        "total": len(results),
    }


@app.get("/clients/{contact_id}/form-data")
async def get_form_data(contact_id: str):
    if contact_id not in MOCK_CLIENTS:
        raise HTTPException(status_code=404, detail="Contact not found")
    c = MOCK_CLIENTS[contact_id]
    return {
        "contact_id": contact_id,
        "given_name": c["firstName"],
        "full_name": c["lastName"],
        "email": c["email"],
        "phone": c["phone"],
        **c["fields"],
        "firm_defaults": FIRM_DEFAULTS,
    }


@app.get("/clients/{contact_id}/data-sheet")
async def data_sheet(contact_id: str):
    if contact_id not in MOCK_CLIENTS:
        raise HTTPException(status_code=404, detail="Contact not found")
    c = MOCK_CLIENTS[contact_id]
    return {
        "contact_id": contact_id,
        "sections": {
            "personal": {
                "name": f"{c['firstName']} {c['lastName']}",
                "dob": c["fields"].get("date_of_birth"),
                "citizenship": c["fields"].get("country_of_citizenship"),
            },
            "contact": {"email": c["email"], "phone": c["phone"]},
            "program_specific": c["fields"],
            "representative": FIRM_DEFAULTS,
        },
    }


@app.get("/clients/{contact_id}/validate")
async def validate(contact_id: str):
    if contact_id not in MOCK_CLIENTS:
        raise HTTPException(status_code=404, detail="Contact not found")
    c = MOCK_CLIENTS[contact_id]
    required = ["date_of_birth", "country_of_citizenship", "passport_number", "marital_status"]
    missing = [k for k in required if not c["fields"].get(k)]
    total = len(c["fields"]) + 4  # + name/email/phone/dob implicit
    return {
        "contact_id": contact_id,
        "is_complete": len(missing) == 0,
        "total_fields": total,
        "filled_fields": total - len(missing),
        "missing_count": len(missing),
        "missing_fields": missing,
        "ready_for_submission": len(missing) == 0,
    }


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("NeuronX Mock API — Chrome extension test harness")
    print("=" * 60)
    print(f"Clients: {list(MOCK_CLIENTS.keys())}")
    print(f"Endpoints:")
    print("  GET  /health")
    print("  GET  /clients/search?q={name}")
    print("  GET  /clients/{id}/form-data")
    print("  GET  /clients/{id}/data-sheet")
    print("  GET  /clients/{id}/validate")
    print("=" * 60)
    print("In Chrome extension settings → API URL: http://127.0.0.1:8000")
    print("=" * 60)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
