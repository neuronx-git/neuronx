"""
Demo Data Seeding
POST /demo/seed  — Populate database with realistic demo data for presentations
POST /demo/clear — Remove all demo data
"""

from fastapi import APIRouter
from datetime import datetime, timezone, timedelta
import logging

router = APIRouter()
logger = logging.getLogger("neuronx.demo")


DEMO_CONTACTS = [
    {"id": "demo-001", "first_name": "Priya", "last_name": "Sharma", "email": "priya@example.com", "phone": "+14165551001", "tags": ["nx:score:high", "nx:contacted", "nx:retainer:signed"], "source": "Website", "program_interest": "Express Entry", "readiness_score": 82, "readiness_outcome": "ready_standard"},
    {"id": "demo-002", "first_name": "Ahmed", "last_name": "Hassan", "email": "ahmed@example.com", "phone": "+14165551002", "tags": ["nx:score:high", "nx:retainer:signed"], "source": "Referral", "program_interest": "Spousal Sponsorship", "readiness_score": 91, "readiness_outcome": "ready_standard"},
    {"id": "demo-003", "first_name": "Wei", "last_name": "Chen", "email": "wei@example.com", "phone": "+14165551003", "tags": ["nx:score:med"], "source": "Google Ads", "program_interest": "Work Permit", "readiness_score": 55, "readiness_outcome": "ready_standard"},
    {"id": "demo-004", "first_name": "Maria", "last_name": "Santos", "email": "maria@example.com", "phone": "+14165551004", "tags": ["nx:score:high", "nx:booking:confirmed"], "source": "Website", "program_interest": "Express Entry", "readiness_score": 78, "readiness_outcome": "ready_standard"},
    {"id": "demo-005", "first_name": "James", "last_name": "Park", "email": "james@example.com", "phone": "+14165551005", "tags": ["nx:score:low"], "source": "Facebook", "program_interest": "Study Permit", "readiness_score": 28, "readiness_outcome": "not_ready"},
    {"id": "demo-006", "first_name": "Fatima", "last_name": "Al-Rashid", "email": "fatima@example.com", "phone": "+14165551006", "tags": ["nx:score:high", "nx:retainer:signed"], "source": "Referral", "program_interest": "Express Entry", "readiness_score": 88, "readiness_outcome": "ready_standard"},
    {"id": "demo-007", "first_name": "Raj", "last_name": "Patel", "email": "raj@example.com", "phone": "+14165551007", "tags": ["nx:score:med", "nx:human_escalation"], "source": "Website", "program_interest": "LMIA", "readiness_score": 45, "readiness_outcome": "ready_complex"},
    {"id": "demo-008", "first_name": "Yuki", "last_name": "Tanaka", "email": "yuki@example.com", "phone": "+14165551008", "tags": ["nx:score:high"], "source": "Google Ads", "program_interest": "Work Permit", "readiness_score": 75, "readiness_outcome": "ready_standard"},
    {"id": "demo-009", "first_name": "Carlos", "last_name": "Rivera", "email": "carlos@example.com", "phone": "+14165551009", "tags": ["nx:score:high", "nx:retainer:signed"], "source": "Website", "program_interest": "Spousal Sponsorship", "readiness_score": 85, "readiness_outcome": "ready_standard"},
    {"id": "demo-010", "first_name": "Sophie", "last_name": "Martin", "email": "sophie@example.com", "phone": "+14165551010", "tags": ["nx:score:high", "nx:booking:confirmed"], "source": "Referral", "program_interest": "Express Entry", "readiness_score": 79, "readiness_outcome": "ready_standard"},
    {"id": "demo-011", "first_name": "David", "last_name": "Kim", "email": "david@example.com", "phone": "+14165551011", "tags": ["nx:score:high", "nx:retainer:signed"], "source": "Google Ads", "program_interest": "Express Entry", "readiness_score": 86, "readiness_outcome": "ready_standard"},
    {"id": "demo-012", "first_name": "Anita", "last_name": "Desai", "email": "anita@example.com", "phone": "+14165551012", "tags": ["nx:score:med"], "source": "Website", "program_interest": "PR Renewal", "readiness_score": 52, "readiness_outcome": "ready_standard"},
]


@router.post("/seed")
async def seed_demo_data():
    """Populate database with realistic demo data for sales presentations and investor demos."""
    from app import database
    if not database.async_session_factory:
        return {"error": "Database not configured"}

    from app.models.db_models import Contact, Opportunity, Case, Activity, Signature
    from sqlalchemy import select, delete

    now = datetime.now(timezone.utc)

    async with database.async_session_factory() as session:
        # Clear existing demo data (delete children first due to FK constraints)
        await session.execute(delete(Activity).where(Activity.contact_id.like("demo-%")))
        await session.execute(delete(Signature).where(Signature.contact_id.like("demo-%")))
        await session.execute(delete(Case).where(Case.contact_id.like("demo-%")))
        await session.execute(delete(Opportunity).where(Opportunity.contact_id.like("demo-%")))
        await session.execute(delete(Contact).where(Contact.id.like("demo-%")))

        # Insert contacts
        for c in DEMO_CONTACTS:
            session.add(Contact(**c, synced_at=now))

        # Insert opportunities
        opps = [
            {"id": "opp-001", "contact_id": "demo-001", "pipeline_name": "Immigration Intake", "stage_name": "RETAINED", "status": "won", "monetary_value": 3500},
            {"id": "opp-002", "contact_id": "demo-002", "pipeline_name": "Immigration Intake", "stage_name": "RETAINED", "status": "won", "monetary_value": 4500},
            {"id": "opp-003", "contact_id": "demo-003", "pipeline_name": "Immigration Intake", "stage_name": "CONSULT COMPLETED", "status": "lost", "monetary_value": 2500},
            {"id": "opp-004", "contact_id": "demo-004", "pipeline_name": "Immigration Intake", "stage_name": "BOOKED", "status": "open", "monetary_value": 3500},
            {"id": "opp-005", "contact_id": "demo-005", "pipeline_name": "Immigration Intake", "stage_name": "NURTURE", "status": "open", "monetary_value": 0},
            {"id": "opp-006", "contact_id": "demo-006", "pipeline_name": "Immigration Intake", "stage_name": "RETAINED", "status": "won", "monetary_value": 3500},
            {"id": "opp-007", "contact_id": "demo-007", "pipeline_name": "Immigration Intake", "stage_name": "CONTACTING", "status": "open", "monetary_value": 0},
            {"id": "opp-008", "contact_id": "demo-008", "pipeline_name": "Immigration Intake", "stage_name": "RETAINED", "status": "won", "monetary_value": 2500},
            {"id": "opp-009", "contact_id": "demo-009", "pipeline_name": "Immigration Intake", "stage_name": "RETAINED", "status": "won", "monetary_value": 4500},
            {"id": "opp-010", "contact_id": "demo-010", "pipeline_name": "Immigration Intake", "stage_name": "CONSULT READY", "status": "open", "monetary_value": 3500},
            {"id": "opp-011", "contact_id": "demo-011", "pipeline_name": "Immigration Intake", "stage_name": "RETAINED", "status": "won", "monetary_value": 3500},
            {"id": "opp-012", "contact_id": "demo-012", "pipeline_name": "Immigration Intake", "stage_name": "CONTACTING", "status": "open", "monetary_value": 0},
        ]
        for o in opps:
            session.add(Opportunity(**o, pipeline_id="intake", synced_at=now))

        # Insert cases
        cases = [
            {"case_id": "NX-20260301-DEMO01", "contact_id": "demo-001", "program_type": "Express Entry", "assigned_rcic": "Rajiv Mehta", "stage": "closed", "ircc_receipt_number": "E000778899", "ircc_decision": "Approved", "retainer_value": 3500, "docs_required": 8, "docs_received": 8, "created_at": now - timedelta(days=90), "closed_at": now - timedelta(days=15)},
            {"case_id": "NX-20260310-DEMO02", "contact_id": "demo-002", "program_type": "Spousal Sponsorship", "assigned_rcic": "Rajiv Mehta", "stage": "processing", "ircc_receipt_number": "F000112233", "ircc_decision": "Pending", "retainer_value": 4500, "docs_required": 12, "docs_received": 12, "created_at": now - timedelta(days=45)},
            {"case_id": "NX-20260315-DEMO03", "contact_id": "demo-009", "program_type": "Spousal Sponsorship", "assigned_rcic": "Nina Patel", "stage": "doc_collection", "ircc_receipt_number": "", "ircc_decision": "Pending", "retainer_value": 4500, "docs_required": 12, "docs_received": 5, "created_at": now - timedelta(days=20)},
            {"case_id": "NX-20260320-DEMO04", "contact_id": "demo-004", "program_type": "Express Entry", "assigned_rcic": "Rajiv Mehta", "stage": "onboarding", "ircc_receipt_number": "", "ircc_decision": "Pending", "retainer_value": 3500, "docs_required": 8, "docs_received": 0, "created_at": now - timedelta(days=10)},
            {"case_id": "NX-20260101-DEMO05", "contact_id": "demo-006", "program_type": "Express Entry", "assigned_rcic": "Rajiv Mehta", "stage": "submitted", "ircc_receipt_number": "E000445566", "ircc_decision": "Pending", "retainer_value": 3500, "docs_required": 8, "docs_received": 8, "created_at": now - timedelta(days=30)},
            {"case_id": "NX-20260115-DEMO06", "contact_id": "demo-008", "program_type": "Work Permit", "assigned_rcic": "Nina Patel", "stage": "closed", "ircc_receipt_number": "W000334455", "ircc_decision": "Approved", "retainer_value": 2500, "docs_required": 6, "docs_received": 6, "created_at": now - timedelta(days=75), "closed_at": now - timedelta(days=10)},
            {"case_id": "NX-20260201-DEMO07", "contact_id": "demo-003", "program_type": "Work Permit", "assigned_rcic": "Nina Patel", "stage": "closed", "ircc_receipt_number": "W000667788", "ircc_decision": "Refused", "retainer_value": 2500, "docs_required": 6, "docs_received": 6, "created_at": now - timedelta(days=60), "closed_at": now - timedelta(days=5)},
            {"case_id": "NX-20260325-DEMO08", "contact_id": "demo-011", "program_type": "Express Entry", "assigned_rcic": "Rajiv Mehta", "stage": "form_prep", "ircc_receipt_number": "", "ircc_decision": "Pending", "retainer_value": 3500, "docs_required": 8, "docs_received": 8, "created_at": now - timedelta(days=15)},
        ]
        for c in cases:
            session.add(Case(**c))

        # Insert activities
        activities = [
            ("demo-001", "form_submitted", "Immigration inquiry", 95),
            ("demo-001", "call_completed", "VAPI call — Express Entry, score 82", 95),
            ("demo-001", "appointment_booked", "Free assessment booked", 93),
            ("demo-001", "retainer_signed", "Signed via Documenso", 91),
            ("demo-001", "case_closed", "IRCC Approved", 15),
            ("demo-002", "form_submitted", "Immigration inquiry", 50),
            ("demo-002", "call_completed", "VAPI call — Spousal, score 91", 50),
            ("demo-002", "retainer_signed", "Signed via Documenso", 46),
            ("demo-003", "form_submitted", "Work permit inquiry", 65),
            ("demo-003", "call_completed", "VAPI call — score 55", 64),
            ("demo-004", "form_submitted", "Express Entry inquiry", 12),
            ("demo-004", "call_completed", "VAPI call — score 78", 12),
            ("demo-004", "appointment_booked", "Consultation booked", 10),
            ("demo-005", "form_submitted", "Study permit inquiry", 8),
            ("demo-005", "nurture_entered", "Low score — nurture campaign", 7),
            ("demo-006", "form_submitted", "Express Entry inquiry", 35),
            ("demo-006", "retainer_signed", "Signed via Documenso", 32),
            ("demo-007", "form_submitted", "LMIA inquiry", 20),
            ("demo-007", "human_escalation", "Complex case — senior RCIC", 19),
            ("demo-008", "form_submitted", "Work permit inquiry", 80),
            ("demo-008", "retainer_signed", "Signed", 76),
            ("demo-009", "form_submitted", "Spousal inquiry", 22),
            ("demo-009", "retainer_signed", "Signed via Documenso", 20),
            ("demo-010", "form_submitted", "Express Entry inquiry", 5),
            ("demo-010", "appointment_booked", "Consultation booked", 3),
            ("demo-011", "form_submitted", "Express Entry inquiry", 18),
            ("demo-011", "retainer_signed", "Signed", 16),
            ("demo-012", "form_submitted", "PR Renewal inquiry", 4),
        ]
        for contact_id, atype, detail, days_ago in activities:
            session.add(Activity(
                contact_id=contact_id,
                activity_type=atype,
                detail=detail,
                created_at=now - timedelta(days=days_ago),
            ))

        # Insert signatures
        sigs = [
            ("demo-001", "retainer", "signed", "priya@example.com", 92, 91),
            ("demo-002", "retainer", "signed", "ahmed@example.com", 47, 46),
            ("demo-006", "retainer", "signed", "fatima@example.com", 33, 32),
            ("demo-009", "retainer", "signed", "carlos@example.com", 21, 20),
            ("demo-008", "retainer", "signed", "yuki@example.com", 77, 76),
            ("demo-011", "retainer", "signed", "david@example.com", 17, 16),
            ("demo-004", "retainer", "sent", "maria@example.com", 2, None),
            ("demo-010", "retainer", "pending", "sophie@example.com", None, None),
        ]
        for contact_id, doc_type, status, email, sent_days, signed_days in sigs:
            session.add(Signature(
                contact_id=contact_id,
                document_type=doc_type,
                status=status,
                signer_email=email,
                sent_at=(now - timedelta(days=sent_days)) if sent_days else None,
                signed_at=(now - timedelta(days=signed_days)) if signed_days else None,
            ))

        # Insert case stage change activities (for Metabase timeline)
        stage_changes = [
            ("demo-001", "stage_changed", "onboarding → doc_collection", 88, {"case_id": "NX-20260301-DEMO01", "old_stage": "onboarding", "new_stage": "doc_collection"}),
            ("demo-001", "stage_changed", "doc_collection → docs_complete", 75, {"case_id": "NX-20260301-DEMO01", "old_stage": "doc_collection", "new_stage": "docs_complete"}),
            ("demo-001", "stage_changed", "docs_complete → form_prep", 72, {"case_id": "NX-20260301-DEMO01", "old_stage": "docs_complete", "new_stage": "form_prep"}),
            ("demo-001", "stage_changed", "form_prep → under_review", 65, {"case_id": "NX-20260301-DEMO01", "old_stage": "form_prep", "new_stage": "under_review"}),
            ("demo-001", "stage_changed", "under_review → submitted", 60, {"case_id": "NX-20260301-DEMO01", "old_stage": "under_review", "new_stage": "submitted"}),
            ("demo-001", "stage_changed", "submitted → processing", 55, {"case_id": "NX-20260301-DEMO01", "old_stage": "submitted", "new_stage": "processing"}),
            ("demo-001", "stage_changed", "processing → decision", 20, {"case_id": "NX-20260301-DEMO01", "old_stage": "processing", "new_stage": "decision"}),
            ("demo-001", "stage_changed", "decision → closed", 15, {"case_id": "NX-20260301-DEMO01", "old_stage": "decision", "new_stage": "closed"}),
            ("demo-002", "stage_changed", "onboarding → doc_collection", 43, {"case_id": "NX-20260310-DEMO02", "old_stage": "onboarding", "new_stage": "doc_collection"}),
            ("demo-002", "stage_changed", "doc_collection → docs_complete", 35, {"case_id": "NX-20260310-DEMO02", "old_stage": "doc_collection", "new_stage": "docs_complete"}),
            ("demo-002", "stage_changed", "docs_complete → form_prep", 30, {"case_id": "NX-20260310-DEMO02", "old_stage": "docs_complete", "new_stage": "form_prep"}),
            ("demo-002", "stage_changed", "form_prep → under_review", 25, {"case_id": "NX-20260310-DEMO02", "old_stage": "form_prep", "new_stage": "under_review"}),
            ("demo-002", "stage_changed", "under_review → submitted", 20, {"case_id": "NX-20260310-DEMO02", "old_stage": "under_review", "new_stage": "submitted"}),
            ("demo-002", "stage_changed", "submitted → processing", 15, {"case_id": "NX-20260310-DEMO02", "old_stage": "submitted", "new_stage": "processing"}),
            ("demo-009", "stage_changed", "onboarding → doc_collection", 18, {"case_id": "NX-20260315-DEMO03", "old_stage": "onboarding", "new_stage": "doc_collection"}),
            ("demo-011", "stage_changed", "onboarding → doc_collection", 13, {"case_id": "NX-20260325-DEMO08", "old_stage": "onboarding", "new_stage": "doc_collection"}),
            ("demo-011", "stage_changed", "doc_collection → docs_complete", 10, {"case_id": "NX-20260325-DEMO08", "old_stage": "doc_collection", "new_stage": "docs_complete"}),
            ("demo-011", "stage_changed", "docs_complete → form_prep", 7, {"case_id": "NX-20260325-DEMO08", "old_stage": "docs_complete", "new_stage": "form_prep"}),
        ]
        for contact_id, atype, detail, days_ago, meta in stage_changes:
            session.add(Activity(
                contact_id=contact_id,
                activity_type=atype,
                detail=detail,
                metadata_json=meta,
                created_at=now - timedelta(days=days_ago),
            ))

        await session.commit()

    return {
        "status": "demo data seeded",
        "contacts": len(DEMO_CONTACTS),
        "opportunities": len(opps),
        "cases": len(cases),
        "activities": len(activities) + len(stage_changes),
        "signatures": len(sigs),
        "note": "Realistic immigration consulting data for investor demo. Run POST /demo/clear to remove.",
    }


@router.get("/summary")
async def demo_summary():
    """
    Investor demo summary — key metrics at a glance.
    Shows pipeline health, case status distribution, revenue, activity timeline.
    """
    from app import database
    if not database.async_session_factory:
        return {"error": "Database not configured"}

    from sqlalchemy import text

    async with database.async_session_factory() as session:
        # Pipeline metrics
        opp_stats = await session.execute(text("""
            SELECT status, COUNT(*) as cnt, COALESCE(SUM(monetary_value), 0) as total_value
            FROM opportunities GROUP BY status
        """))
        pipeline = {row.status: {"count": row.cnt, "value": row.total_value} for row in opp_stats}

        # Case stage distribution
        case_stats = await session.execute(text("""
            SELECT stage, COUNT(*) as cnt FROM cases GROUP BY stage ORDER BY cnt DESC
        """))
        stages = {row.stage: row.cnt for row in case_stats}

        # Activity volume (last 30 days)
        activity_stats = await session.execute(text("""
            SELECT activity_type, COUNT(*) as cnt FROM activities
            WHERE created_at > NOW() - INTERVAL '30 days'
            GROUP BY activity_type ORDER BY cnt DESC
        """))
        recent_activities = {row.activity_type: row.cnt for row in activity_stats}

        # Revenue
        revenue = await session.execute(text("""
            SELECT COUNT(*) as total_cases,
                   COALESCE(SUM(retainer_value), 0) as total_revenue,
                   COALESCE(AVG(retainer_value), 0) as avg_retainer
            FROM cases WHERE retainer_value > 0
        """))
        rev_row = revenue.first()

        # Contacts by readiness
        score_dist = await session.execute(text("""
            SELECT readiness_outcome, COUNT(*) as cnt FROM contacts
            WHERE readiness_outcome != '' GROUP BY readiness_outcome
        """))
        readiness = {row.readiness_outcome: row.cnt for row in score_dist}

    return {
        "pipeline": pipeline,
        "case_stages": stages,
        "recent_activities": recent_activities,
        "revenue": {
            "total_cases": rev_row.total_cases if rev_row else 0,
            "total_revenue": float(rev_row.total_revenue) if rev_row else 0,
            "avg_retainer": round(float(rev_row.avg_retainer), 2) if rev_row else 0,
        },
        "readiness_distribution": readiness,
    }


@router.post("/clear")
async def clear_demo_data():
    """Remove all demo data (contacts with demo- prefix)."""
    from app import database
    if not database.async_session_factory:
        return {"error": "Database not configured"}

    from app.models.db_models import Contact, Opportunity, Case, Activity, Signature
    from sqlalchemy import delete

    async with database.async_session_factory() as session:
        for model in [Activity, Signature, Case, Opportunity]:
            await session.execute(delete(model).where(model.__table__.c.contact_id.like("demo-%")))
        await session.execute(delete(Contact).where(Contact.id.like("demo-%")))
        await session.commit()

    return {"status": "demo data cleared"}
