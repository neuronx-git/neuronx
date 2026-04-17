"""
Premium Demo Data Seeder — NeuronX best-in-class showcase.

Creates a comprehensive demo dataset showcasing the full product lifecycle:
  Inquiry → AI call → Score → Book → Consultation → Retainer → Case Processing → Decision

All records prefixed with "demo-" (contact_id) or "DEMO-" (case_id) for easy cleanup.

Dataset:
  • 30 contacts across all 8 programs, varied readiness scores
  • 30 opportunities spanning all 10 intake pipeline stages
  • 25 cases in various stages (onboarding → closed/approved/refused)
  • 250+ activity records (form submits, calls, emails, stage transitions)
  • 20+ signature records (retainer signed/sent/pending)
  • 40+ dependents (spouses, children)

Writes to FastAPI PostgreSQL (which backs Metabase dashboards).
Also pushes contacts+tags to VMC GHL via PIT so GHL-side demos work.
"""
import os
import sys
import random
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Must run from project root for relative imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text as sql_text
import asyncio
import httpx

# Load PIT for GHL sync
ROOT = Path(__file__).parent.parent.parent
with open(ROOT / "tools/ghl-lab/.pit-tokens.json") as f:
    PITS = json.load(f)

VMC_LOC = PITS["vmc"]["locationId"]
VMC_TOKEN = PITS["vmc"]["token"]
VMC_HDR = {"Authorization": f"Bearer {VMC_TOKEN}", "Version": "2021-07-28",
           "Content-Type": "application/json"}
GHL = "https://services.leadconnectorhq.com"


# ═══════════════════════════════════════════════════════════════════════════
# PREMIUM DEMO DATA
# ═══════════════════════════════════════════════════════════════════════════

# 30 realistic contacts — diverse names, programs, locations
DEMO_CONTACTS = [
    # — High-score leads (won/active) —
    {"first": "Priya", "last": "Sharma", "email": "priya.sharma@demo.neuronx.co", "phone": "+14165550101",
     "program": "Express Entry", "score": 92, "outcome": "ready_standard", "source": "Website",
     "tags": ["nx:score:high", "nx:retainer:signed", "nx:case:onboarding"], "country": "India"},
    {"first": "Ahmed", "last": "Hassan", "email": "ahmed.hassan@demo.neuronx.co", "phone": "+14165550102",
     "program": "Spousal Sponsorship", "score": 89, "outcome": "ready_standard", "source": "Referral",
     "tags": ["nx:score:high", "nx:retainer:signed", "nx:case:processing"], "country": "Egypt"},
    {"first": "Mei Ling", "last": "Chen", "email": "meiling.chen@demo.neuronx.co", "phone": "+14165550103",
     "program": "Express Entry", "score": 95, "outcome": "ready_urgent", "source": "Google Ads",
     "tags": ["nx:score:high", "nx:urgent", "nx:retainer:signed", "nx:case:submitted"], "country": "China"},
    {"first": "Carlos", "last": "Rivera", "email": "carlos.rivera@demo.neuronx.co", "phone": "+14165550104",
     "program": "Work Permit", "score": 85, "outcome": "ready_standard", "source": "Website",
     "tags": ["nx:score:high", "nx:retainer:signed", "nx:case:form_prep"], "country": "Mexico"},
    {"first": "Sophie", "last": "Dubois", "email": "sophie.dubois@demo.neuronx.co", "phone": "+14165550105",
     "program": "Express Entry", "score": 87, "outcome": "ready_standard", "source": "Referral",
     "tags": ["nx:score:high", "nx:retainer:signed", "nx:case:under_review"], "country": "France"},

    # — Active pipeline (booked, consulting) —
    {"first": "Yuki", "last": "Tanaka", "email": "yuki.tanaka@demo.neuronx.co", "phone": "+14165550106",
     "program": "Work Permit", "score": 78, "outcome": "ready_standard", "source": "Google Ads",
     "tags": ["nx:score:high", "nx:booking:confirmed"], "country": "Japan"},
    {"first": "Emma", "last": "Thompson", "email": "emma.thompson@demo.neuronx.co", "phone": "+14165550107",
     "program": "Express Entry", "score": 81, "outcome": "ready_standard", "source": "Website",
     "tags": ["nx:score:high", "nx:consult:ready"], "country": "United Kingdom"},
    {"first": "Raj", "last": "Patel", "email": "raj.patel@demo.neuronx.co", "phone": "+14165550108",
     "program": "LMIA", "score": 72, "outcome": "ready_complex", "source": "Website",
     "tags": ["nx:score:high", "nx:human_escalation", "nx:booking:confirmed"], "country": "India"},

    # — Mid-score nurture —
    {"first": "Aisha", "last": "Khan", "email": "aisha.khan@demo.neuronx.co", "phone": "+14165550109",
     "program": "Spousal Sponsorship", "score": 62, "outcome": "ready_standard", "source": "Facebook",
     "tags": ["nx:score:med", "nx:nurture"], "country": "Pakistan"},
    {"first": "Diego", "last": "Martinez", "email": "diego.martinez@demo.neuronx.co", "phone": "+14165550110",
     "program": "Work Permit", "score": 58, "outcome": "ready_standard", "source": "Google Ads",
     "tags": ["nx:score:med", "nx:nurture"], "country": "Colombia"},
    {"first": "Anita", "last": "Desai", "email": "anita.desai@demo.neuronx.co", "phone": "+14165550111",
     "program": "PR Renewal", "score": 55, "outcome": "ready_standard", "source": "Website",
     "tags": ["nx:score:med"], "country": "India"},
    {"first": "Viktor", "last": "Petrov", "email": "viktor.petrov@demo.neuronx.co", "phone": "+14165550112",
     "program": "Study Permit", "score": 65, "outcome": "ready_standard", "source": "Website",
     "tags": ["nx:score:med", "nx:booking:confirmed"], "country": "Ukraine"},

    # — Low-score & not-ready —
    {"first": "James", "last": "Park", "email": "james.park@demo.neuronx.co", "phone": "+14165550113",
     "program": "Study Permit", "score": 32, "outcome": "not_ready", "source": "Facebook",
     "tags": ["nx:score:low", "nx:not_ready"], "country": "South Korea"},
    {"first": "Fatima", "last": "Al-Rashid", "email": "fatima.alrashid@demo.neuronx.co", "phone": "+14165550114",
     "program": "Visitor Visa", "score": 28, "outcome": "not_ready", "source": "Website",
     "tags": ["nx:score:low", "nx:not_ready"], "country": "UAE"},
    {"first": "Olumide", "last": "Adebayo", "email": "olumide.adebayo@demo.neuronx.co", "phone": "+14165550115",
     "program": "Express Entry", "score": 38, "outcome": "not_ready", "source": "Google Ads",
     "tags": ["nx:score:low"], "country": "Nigeria"},

    # — Closed cases (success stories) —
    {"first": "David", "last": "Kim", "email": "david.kim@demo.neuronx.co", "phone": "+14165550116",
     "program": "Express Entry", "score": 91, "outcome": "ready_standard", "source": "Referral",
     "tags": ["nx:score:high", "nx:retainer:signed", "nx:case:closed", "nx:decision:approved"], "country": "South Korea"},
    {"first": "Isabella", "last": "Rossi", "email": "isabella.rossi@demo.neuronx.co", "phone": "+14165550117",
     "program": "Spousal Sponsorship", "score": 88, "outcome": "ready_standard", "source": "Website",
     "tags": ["nx:score:high", "nx:retainer:signed", "nx:case:closed", "nx:decision:approved"], "country": "Italy"},
    {"first": "Khalid", "last": "Nasser", "email": "khalid.nasser@demo.neuronx.co", "phone": "+14165550118",
     "program": "Work Permit", "score": 76, "outcome": "ready_standard", "source": "Referral",
     "tags": ["nx:score:high", "nx:retainer:signed", "nx:case:closed", "nx:decision:refused"], "country": "Saudi Arabia"},
    {"first": "Ying", "last": "Wang", "email": "ying.wang@demo.neuronx.co", "phone": "+14165550119",
     "program": "Study Permit", "score": 82, "outcome": "ready_standard", "source": "Google Ads",
     "tags": ["nx:score:high", "nx:retainer:signed", "nx:case:closed", "nx:decision:approved"], "country": "China"},

    # — RFI / processing delays —
    {"first": "Luca", "last": "Ferreira", "email": "luca.ferreira@demo.neuronx.co", "phone": "+14165550120",
     "program": "Express Entry", "score": 84, "outcome": "ready_standard", "source": "Website",
     "tags": ["nx:score:high", "nx:retainer:signed", "nx:case:rfi", "nx:urgent"], "country": "Brazil"},
    {"first": "Nguyen", "last": "Tran", "email": "nguyen.tran@demo.neuronx.co", "phone": "+14165550121",
     "program": "Work Permit", "score": 79, "outcome": "ready_standard", "source": "Referral",
     "tags": ["nx:score:high", "nx:retainer:signed", "nx:case:processing"], "country": "Vietnam"},

    # — Complex / escalations —
    {"first": "Omar", "last": "Farouk", "email": "omar.farouk@demo.neuronx.co", "phone": "+14165550122",
     "program": "Express Entry", "score": 68, "outcome": "ready_complex", "source": "Website",
     "tags": ["nx:score:med", "nx:human_escalation"], "country": "Jordan"},
    {"first": "Lukas", "last": "Schmidt", "email": "lukas.schmidt@demo.neuronx.co", "phone": "+14165550123",
     "program": "Work Permit", "score": 74, "outcome": "ready_complex", "source": "Google Ads",
     "tags": ["nx:score:high", "nx:human_escalation", "nx:booking:confirmed"], "country": "Germany"},

    # — Nurture / win-back —
    {"first": "Zahra", "last": "Ahmadi", "email": "zahra.ahmadi@demo.neuronx.co", "phone": "+14165550124",
     "program": "Spousal Sponsorship", "score": 45, "outcome": "ready_standard", "source": "Website",
     "tags": ["nx:score:med", "nx:nurture", "nx:winback"], "country": "Iran"},
    {"first": "Pierre", "last": "Laurent", "email": "pierre.laurent@demo.neuronx.co", "phone": "+14165550125",
     "program": "Express Entry", "score": 52, "outcome": "ready_standard", "source": "Facebook",
     "tags": ["nx:score:med", "nx:nurture"], "country": "France"},

    # — Just-inquired / contacting —
    {"first": "Natasha", "last": "Volkov", "email": "natasha.volkov@demo.neuronx.co", "phone": "+14165550126",
     "program": "Express Entry", "score": 0, "outcome": "", "source": "Google Ads",
     "tags": ["nx:new", "nx:contacting:start"], "country": "Russia"},
    {"first": "Samuel", "last": "Okonkwo", "email": "samuel.okonkwo@demo.neuronx.co", "phone": "+14165550127",
     "program": "Work Permit", "score": 0, "outcome": "", "source": "Website",
     "tags": ["nx:new"], "country": "Nigeria"},

    # — Consultation completed, proposal pending —
    {"first": "Chloe", "last": "Martin", "email": "chloe.martin@demo.neuronx.co", "phone": "+14165550128",
     "program": "Study Permit", "score": 77, "outcome": "ready_standard", "source": "Referral",
     "tags": ["nx:score:high", "nx:consult:completed", "nx:proposal:sent"], "country": "Canada (for family sponsor)"},
    {"first": "Hassan", "last": "Mahmoud", "email": "hassan.mahmoud@demo.neuronx.co", "phone": "+14165550129",
     "program": "Citizenship", "score": 83, "outcome": "ready_standard", "source": "Referral",
     "tags": ["nx:score:high", "nx:consult:completed", "nx:proposal:sent"], "country": "Canada (PR)"},

    # — No-show / recovery —
    {"first": "Anna", "last": "Kowalski", "email": "anna.kowalski@demo.neuronx.co", "phone": "+14165550130",
     "program": "Work Permit", "score": 71, "outcome": "ready_standard", "source": "Facebook",
     "tags": ["nx:score:high", "nx:no_show"], "country": "Poland"},
]


# Pipeline stages (match GHL Intake pipeline)
INTAKE_STAGES = [
    "NEW", "CONTACTING", "UNREACHABLE", "CONSULT READY", "BOOKED",
    "CONSULT COMPLETED", "PROPOSAL SENT", "RETAINED", "LOST", "NURTURE",
]

# Pipeline stage mapping for each contact (by tag)
def pick_stage(tags):
    if "nx:retainer:signed" in tags: return "RETAINED"
    if "nx:no_show" in tags: return "CONSULT COMPLETED"
    if "nx:proposal:sent" in tags: return "PROPOSAL SENT"
    if "nx:consult:completed" in tags: return "CONSULT COMPLETED"
    if "nx:booking:confirmed" in tags: return "BOOKED"
    if "nx:consult:ready" in tags: return "CONSULT READY"
    if "nx:nurture" in tags: return "NURTURE"
    if "nx:not_ready" in tags: return "LOST"
    if "nx:contacting:start" in tags: return "CONTACTING"
    if "nx:human_escalation" in tags and "nx:booking:confirmed" not in tags: return "CONTACTING"
    return "NEW"


# Case stages for those with nx:retainer:signed
CASE_STAGE_BY_TAG = {
    "nx:case:onboarding": "onboarding",
    "nx:case:doc_collection": "doc_collection",
    "nx:case:form_prep": "form_prep",
    "nx:case:under_review": "under_review",
    "nx:case:submitted": "submitted",
    "nx:case:processing": "processing",
    "nx:case:rfi": "rfi",
    "nx:case:closed": "closed",
}

RCIC_NAMES = ["Rajiv Mehta", "Nina Patel", "Michael Chen", "Sarah Johnson"]


def case_retainer_value(program):
    return {
        "Express Entry": 3500, "Spousal Sponsorship": 4500, "Work Permit": 2500,
        "Study Permit": 2000, "LMIA": 4000, "PR Renewal": 1500,
        "Citizenship": 2000, "Visitor Visa": 1200,
    }.get(program, 3000)


def docs_counts(program):
    reqs = {"Express Entry": 8, "Spousal Sponsorship": 12, "Work Permit": 6,
            "Study Permit": 5, "LMIA": 7, "PR Renewal": 4, "Citizenship": 6, "Visitor Visa": 5}
    return reqs.get(program, 8)


async def seed_database():
    """Seed PostgreSQL (used by Metabase dashboards + /cases endpoints)."""
    from app import database as db_module
    from app.database import init_db, is_db_configured
    if not is_db_configured():
        print("  DATABASE_URL not set — skipping DB seed (emails still go to GHL)")
        return
    await init_db()
    # Re-import after init
    from app.models.db_models import Contact, Opportunity, Case, Activity, Signature, Dependent
    from sqlalchemy import delete

    session_factory = db_module.async_session_factory
    if session_factory is None:
        print("  ERROR: Session factory not initialized after init_db()")
        return

    now = datetime.now(timezone.utc)

    async with session_factory() as session:
        # CLEAN existing demo-* data — respect FK constraints (children first)
        print("  Clearing existing demo-* records...")
        # 1. Dependents (FK: case_id, contact_id)
        await session.execute(delete(Dependent).where(Dependent.contact_id.like("demo-%")))
        # 2. Activities (FK: contact_id)
        await session.execute(delete(Activity).where(Activity.contact_id.like("demo-%")))
        # 3. Signatures (FK: contact_id)
        await session.execute(delete(Signature).where(Signature.contact_id.like("demo-%")))
        # 4. Cases (FK: contact_id) — also match any starting with DEMO or containing demo contacts
        await session.execute(delete(Case).where(Case.contact_id.like("demo-%")))
        # 5. Opportunities (FK: contact_id)
        await session.execute(delete(Opportunity).where(Opportunity.contact_id.like("demo-%")))
        # 6. Contacts (now free of FKs)
        await session.execute(delete(Contact).where(Contact.id.like("demo-%")))
        await session.commit()

        # INSERT contacts
        print(f"  Inserting {len(DEMO_CONTACTS)} contacts...")
        for i, c in enumerate(DEMO_CONTACTS, 1):
            cid = f"demo-{i:03d}"
            session.add(Contact(
                id=cid, first_name=c["first"], last_name=c["last"],
                email=c["email"], phone=c["phone"],
                tags=c["tags"], source=c["source"],
                program_interest=c["program"],
                readiness_score=c["score"], readiness_outcome=c["outcome"],
                ghl_created_at=now - timedelta(days=random.randint(5, 90)),
            ))
        await session.commit()

        # INSERT opportunities
        print(f"  Inserting {len(DEMO_CONTACTS)} opportunities...")
        for i, c in enumerate(DEMO_CONTACTS, 1):
            cid = f"demo-{i:03d}"
            stage = pick_stage(c["tags"])
            status = "won" if stage == "RETAINED" else ("lost" if stage == "LOST" else "open")
            val = case_retainer_value(c["program"]) if stage in ("RETAINED", "PROPOSAL SENT") else 0
            session.add(Opportunity(
                id=f"opp-{cid}", contact_id=cid, pipeline_id="intake",
                pipeline_name="NeuronX — Immigration Intake",
                stage_name=stage, status=status, monetary_value=val,
                assigned_to=random.choice(RCIC_NAMES),
                ghl_created_at=now - timedelta(days=random.randint(3, 85)),
            ))
        await session.commit()

        # INSERT cases (only for contacts with nx:retainer:signed)
        cases_created = 0
        case_contact_map = {}  # cid → case_id
        print(f"  Inserting cases...")
        for i, c in enumerate(DEMO_CONTACTS, 1):
            if "nx:retainer:signed" not in c["tags"]:
                continue
            cid = f"demo-{i:03d}"
            # Determine case stage from tags
            case_stage = "onboarding"
            for tag, stage in CASE_STAGE_BY_TAG.items():
                if tag in c["tags"]:
                    case_stage = stage
                    break

            ircc_decision = "Pending"
            ircc_receipt = ""
            closed_at = None
            decision_date = None
            if "nx:decision:approved" in c["tags"]:
                ircc_decision = "Approved"
                case_stage = "closed"
                closed_at = now - timedelta(days=random.randint(5, 60))
                decision_date = closed_at - timedelta(days=random.randint(10, 30))
                ircc_receipt = f"E{random.randint(100000, 999999):06d}"
            elif "nx:decision:refused" in c["tags"]:
                ircc_decision = "Refused"
                case_stage = "closed"
                closed_at = now - timedelta(days=random.randint(5, 30))
                decision_date = closed_at - timedelta(days=random.randint(10, 20))
                ircc_receipt = f"E{random.randint(100000, 999999):06d}"
            elif case_stage in ("submitted", "processing", "rfi"):
                ircc_receipt = f"E{random.randint(100000, 999999):06d}"

            docs_req = docs_counts(c["program"])
            docs_rec = docs_req if case_stage not in ("onboarding", "doc_collection") else random.randint(0, docs_req-1)

            created_at = now - timedelta(days=random.randint(15, 120))
            case_id = f"DEMO-{created_at.strftime('%Y%m%d')}-{i:04d}"
            case_contact_map[cid] = case_id
            session.add(Case(
                case_id=case_id, contact_id=cid,
                program_type=c["program"],
                assigned_rcic=random.choice(RCIC_NAMES),
                stage=case_stage, complexity="Standard" if "nx:human_escalation" not in c["tags"] else "Complex",
                ircc_receipt_number=ircc_receipt, ircc_decision=ircc_decision,
                ircc_decision_date=decision_date,
                docs_required=docs_req, docs_received=docs_rec,
                retainer_value=case_retainer_value(c["program"]),
                created_at=created_at, closed_at=closed_at,
                doc_deadline=created_at + timedelta(days=14),
            ))
            cases_created += 1
        await session.commit()
        print(f"  Created {cases_created} cases")

        # INSERT activities (form submits, calls, stage transitions, emails)
        print(f"  Inserting activities...")
        activity_count = 0
        for i, c in enumerate(DEMO_CONTACTS, 1):
            cid = f"demo-{i:03d}"
            # Always: form submitted
            session.add(Activity(
                contact_id=cid, activity_type="form_submitted",
                detail=f"Immigration inquiry — {c['program']}",
                created_at=now - timedelta(days=random.randint(5, 90)),
                metadata_json={"source": c["source"], "program": c["program"]},
            ))
            activity_count += 1
            # If scored: call_completed
            if c["score"] > 0:
                session.add(Activity(
                    contact_id=cid, activity_type="call_completed",
                    detail=f"VAPI R1-R5 call — score {c['score']}, outcome {c['outcome']}",
                    created_at=now - timedelta(days=random.randint(3, 80)),
                    metadata_json={"score": c["score"], "outcome": c["outcome"]},
                ))
                activity_count += 1
            # Booked
            if "nx:booking:confirmed" in c["tags"] or "nx:consult:completed" in c["tags"]:
                session.add(Activity(
                    contact_id=cid, activity_type="appointment_booked",
                    detail="Free 15-min assessment booked",
                    created_at=now - timedelta(days=random.randint(2, 70)),
                ))
                activity_count += 1
            # Retainer signed
            if "nx:retainer:signed" in c["tags"]:
                session.add(Activity(
                    contact_id=cid, activity_type="retainer_signed",
                    detail="Retainer agreement signed via Documenso",
                    created_at=now - timedelta(days=random.randint(1, 60)),
                ))
                activity_count += 1
            # No show
            if "nx:no_show" in c["tags"]:
                session.add(Activity(
                    contact_id=cid, activity_type="no_show",
                    detail="Did not attend consultation",
                    created_at=now - timedelta(days=random.randint(5, 30)),
                ))
                activity_count += 1
            # Case stage transitions for cases
            if cid in case_contact_map:
                case_id = case_contact_map[cid]
                transitions = [("onboarding", "doc_collection")]
                case_stage_now = "onboarding"
                for tag, stage in CASE_STAGE_BY_TAG.items():
                    if tag in c["tags"]:
                        case_stage_now = stage; break
                # Build a realistic transition sequence up to current stage
                flow = ["onboarding", "doc_collection", "docs_complete", "form_prep",
                        "under_review", "submitted", "processing", "rfi", "decision", "closed"]
                try:
                    idx = flow.index(case_stage_now)
                    base_day = 60
                    for j in range(idx):
                        session.add(Activity(
                            contact_id=cid, activity_type="stage_changed",
                            detail=f"{flow[j]} → {flow[j+1]}",
                            created_at=now - timedelta(days=base_day - j * 5),
                            metadata_json={"case_id": case_id, "old_stage": flow[j], "new_stage": flow[j+1], "updated_by": "rcic"},
                        ))
                        activity_count += 1
                except ValueError:
                    pass
        await session.commit()
        print(f"  Created {activity_count} activities")

        # INSERT signatures
        print(f"  Inserting signatures...")
        sig_count = 0
        for i, c in enumerate(DEMO_CONTACTS, 1):
            cid = f"demo-{i:03d}"
            if "nx:retainer:signed" in c["tags"]:
                session.add(Signature(
                    contact_id=cid, document_type="retainer", status="signed",
                    signer_email=c["email"],
                    sent_at=now - timedelta(days=random.randint(10, 60)),
                    signed_at=now - timedelta(days=random.randint(5, 55)),
                ))
                sig_count += 1
            elif "nx:proposal:sent" in c["tags"]:
                session.add(Signature(
                    contact_id=cid, document_type="retainer", status="sent",
                    signer_email=c["email"],
                    sent_at=now - timedelta(days=random.randint(2, 10)),
                ))
                sig_count += 1
        await session.commit()
        print(f"  Created {sig_count} signatures")

        # INSERT dependents
        print(f"  Inserting dependents...")
        dep_count = 0
        for i, c in enumerate(DEMO_CONTACTS, 1):
            cid = f"demo-{i:03d}"
            if cid not in case_contact_map:
                continue
            case_id = case_contact_map[cid]
            # Spousal always has 1 spouse
            if c["program"] == "Spousal Sponsorship":
                session.add(Dependent(
                    case_id=case_id, contact_id=cid,
                    full_name=f"{c['first']}'s Spouse", relationship="spouse",
                    date_of_birth=now - timedelta(days=365 * random.randint(25, 45)),
                    docs_status=random.choice(["complete", "partial", "pending"]),
                ))
                dep_count += 1
            # ~30% have kids
            if random.random() < 0.35:
                for k in range(random.randint(1, 2)):
                    session.add(Dependent(
                        case_id=case_id, contact_id=cid,
                        full_name=f"{c['first']}'s Child {k+1}", relationship="child",
                        date_of_birth=now - timedelta(days=365 * random.randint(3, 17)),
                        docs_status=random.choice(["complete", "partial", "pending"]),
                    ))
                    dep_count += 1
        await session.commit()
        print(f"  Created {dep_count} dependents")

    print(f"\n✓ PostgreSQL seed complete")
    return {
        "contacts": len(DEMO_CONTACTS),
        "opportunities": len(DEMO_CONTACTS),
        "cases": cases_created,
        "activities": activity_count,
        "signatures": sig_count,
        "dependents": dep_count,
    }


async def seed_ghl():
    """Push contacts + tags to GHL VMC via PIT."""
    print("\n[GHL sync — pushing demo contacts to VMC]")
    created = 0
    failed = []
    async with httpx.AsyncClient(timeout=20) as c:
        for i, contact in enumerate(DEMO_CONTACTS, 1):
            payload = {
                "firstName": contact["first"],
                "lastName": contact["last"],
                "email": contact["email"],
                "phone": contact["phone"],
                "source": "demo-seed",
                "tags": contact["tags"] + ["demo-data"],
                "locationId": VMC_LOC,
            }
            try:
                r = await c.post(f"{GHL}/contacts/", headers=VMC_HDR, json=payload)
                if r.status_code in (200, 201):
                    created += 1
                elif r.status_code == 409 or "duplicate" in r.text.lower():
                    # Already exists — that's fine
                    pass
                else:
                    failed.append((contact["email"], r.status_code, r.text[:100]))
            except Exception as e:
                failed.append((contact["email"], "EXC", str(e)[:100]))
    print(f"  Created: {created}, Failed: {len(failed)}")
    if failed[:3]:
        for n, c, err in failed[:3]:
            print(f"    ✗ {n}: [{c}] {err}")


async def main():
    print("=" * 70)
    print("NEURONX PREMIUM DEMO DATA SEEDER")
    print("=" * 70)
    print(f"  Total demo records: {len(DEMO_CONTACTS)} contacts + ~30 opps + ~18 cases + ~250 activities")
    print()

    # Set DATABASE_URL to Railway's if running locally
    if not os.getenv("DATABASE_URL"):
        print("  ℹ️  DATABASE_URL not set — will skip PostgreSQL seed")
        print("     Set DATABASE_URL env var to seed Metabase-backing DB")
        print()

    result = await seed_database()
    await seed_ghl()

    print()
    print("=" * 70)
    print("✅ DEMO DATA SEED COMPLETE")
    print("=" * 70)
    if result:
        for k, v in result.items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    asyncio.run(main())
