"""
Metabase Dashboard Setup Script

Creates 3 investor-demo dashboards with SQL-based cards:
1. Pipeline Health — conversion funnel, lead sources, pipeline stages
2. Case Status — stage distribution, RCIC workload, doc progress, revenue
3. Activity Timeline — daily volume, recent activities, stage transitions

Usage:
  python scripts/setup_metabase.py

Requires: METABASE_URL, METABASE_USER, METABASE_PASS env vars (or uses defaults).
"""

import os
import sys
import json
import requests

MB_URL = os.getenv("METABASE_URL", "https://metabase-production-1846.up.railway.app")
MB_USER = os.getenv("METABASE_USER", "ranjan@neuronx.co")
MB_PASS = os.getenv("METABASE_PASS", "NeuronX2026!Secure")
DB_ID = 2  # NeuronX Production
COLLECTION_ID = 5  # NeuronX Dashboards


def get_session():
    r = requests.post(f"{MB_URL}/api/session", json={"username": MB_USER, "password": MB_PASS})
    r.raise_for_status()
    return r.json()["id"]


def api(method, path, token, json_data=None):
    headers = {"X-Metabase-Session": token}
    r = getattr(requests, method)(f"{MB_URL}/api{path}", headers=headers, json=json_data)
    r.raise_for_status()
    return r.json()


def create_card(token, name, sql, display="table", viz_settings=None):
    """Create a native SQL question card."""
    payload = {
        "name": name,
        "dataset_query": {
            "type": "native",
            "native": {"query": sql},
            "database": DB_ID,
        },
        "display": display,
        "visualization_settings": viz_settings or {},
        "collection_id": COLLECTION_ID,
    }
    return api("post", "/card", token, payload)


def create_dashboard(token, name, description):
    payload = {
        "name": name,
        "description": description,
        "collection_id": COLLECTION_ID,
    }
    return api("post", "/dashboard", token, payload)


def set_dashboard_cards(token, dashboard_id, cards_layout):
    """Update dashboard with all cards at once via PUT."""
    dashcards = []
    for i, (card_id, row, col, size_x, size_y) in enumerate(cards_layout):
        dashcards.append({
            "id": -(i + 1),  # temporary negative ID for new cards
            "card_id": card_id,
            "row": row,
            "col": col,
            "size_x": size_x,
            "size_y": size_y,
        })
    return api("put", f"/dashboard/{dashboard_id}", token, {"dashcards": dashcards})


def main():
    print("Authenticating with Metabase...")
    token = get_session()
    print(f"Session: {token[:8]}...")

    # ── Dashboard 1: Pipeline Health ──────────────────────────────────
    print("\n--- Creating Pipeline Health dashboard ---")
    d1 = create_dashboard(token, "Pipeline Health", "Intake funnel metrics, lead sources, conversion rates")
    d1_id = d1["id"]
    print(f"Dashboard created: ID {d1_id}")

    cards_d1 = [
        ("Conversion Funnel", "SELECT * FROM v_conversion_funnel ORDER BY stage_order", "bar",
         {"graph.dimensions": ["stage"], "graph.metrics": ["count"]}),
        ("Pipeline by Stage & Status", "SELECT * FROM v_pipeline_funnel", "bar",
         {"graph.dimensions": ["stage_name"], "graph.metrics": ["count", "total_value"]}),
        ("Lead Source Performance", "SELECT * FROM v_lead_sources", "table", {}),
    ]

    d1_layout = []
    for i, (name, sql, display, viz) in enumerate(cards_d1):
        card = create_card(token, name, sql, display, viz)
        row = (i // 2) * 4
        col = (i % 2) * 9
        size_x = 18 if i == 0 else 9
        d1_layout.append((card["id"], row, col, size_x, 4))
        print(f"  Card: {name} (ID {card['id']})")
    set_dashboard_cards(token, d1_id, d1_layout)

    # ── Dashboard 2: Case Status ──────────────────────────────────────
    print("\n--- Creating Case Status dashboard ---")
    d2 = create_dashboard(token, "Case Status", "Case stage distribution, RCIC workload, document progress, revenue")
    d2_id = d2["id"]
    print(f"Dashboard created: ID {d2_id}")

    cards_d2 = [
        ("Case Stage Distribution", "SELECT stage, SUM(count) as cases, SUM(total_value) as revenue FROM v_case_stages GROUP BY stage ORDER BY cases DESC", "bar",
         {"graph.dimensions": ["stage"], "graph.metrics": ["cases"]}),
        ("RCIC Workload", "SELECT * FROM v_rcic_workload", "table", {}),
        ("Revenue by Program", "SELECT * FROM v_revenue", "table", {}),
        ("Document Collection Progress", "SELECT case_id, client_name, program_type, docs_received || '/' || docs_required as docs, pct_complete || '%' as progress, stage FROM v_doc_progress", "table", {}),
    ]

    d2_layout = []
    for i, (name, sql, display, viz) in enumerate(cards_d2):
        card = create_card(token, name, sql, display, viz)
        row = (i // 2) * 4
        col = (i % 2) * 9
        d2_layout.append((card["id"], row, col, 9, 4))
        print(f"  Card: {name} (ID {card['id']})")
    set_dashboard_cards(token, d2_id, d2_layout)

    # ── Dashboard 3: Activity Timeline ────────────────────────────────
    print("\n--- Creating Activity Timeline dashboard ---")
    d3 = create_dashboard(token, "Activity Timeline", "Daily activity volume, recent activities, case stage transitions")
    d3_id = d3["id"]
    print(f"Dashboard created: ID {d3_id}")

    cards_d3 = [
        ("Daily Activity Volume (Last 30d)", "SELECT activity_date, activity_type, count FROM v_daily_activity WHERE activity_date > CURRENT_DATE - 30 ORDER BY activity_date", "line",
         {"graph.dimensions": ["activity_date"], "graph.metrics": ["count"]}),
        ("Recent Activities", "SELECT created_at, activity_type, client_name, detail FROM v_recent_activities LIMIT 50", "table", {}),
        ("Case Stage Transitions", "SELECT transition_date, case_id, client_name, from_stage || ' → ' || to_stage as transition, updated_by FROM v_stage_transitions LIMIT 50", "table", {}),
    ]

    d3_layout = []
    for i, (name, sql, display, viz) in enumerate(cards_d3):
        card = create_card(token, name, sql, display, viz)
        row = (i // 2) * 4
        col = (i % 2) * 9
        size_x = 18 if i == 0 else 9
        d3_layout.append((card["id"], row, col, size_x, 4))
        print(f"  Card: {name} (ID {card['id']})")
    set_dashboard_cards(token, d3_id, d3_layout)

    print(f"\n{'='*60}")
    print(f"3 dashboards created in NeuronX Dashboards collection:")
    print(f"  1. Pipeline Health:    {MB_URL}/dashboard/{d1_id}")
    print(f"  2. Case Status:        {MB_URL}/dashboard/{d2_id}")
    print(f"  3. Activity Timeline:  {MB_URL}/dashboard/{d3_id}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
