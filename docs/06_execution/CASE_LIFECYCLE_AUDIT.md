# Case Lifecycle + Document Processing Audit

**Last updated:** 2026-04-18
**Verdict:** Case lifecycle state machine is solid. **Document flow has critical gaps** that need fixing before a real pilot.

## Critical gaps (production-blocking)

### 1. No document storage mechanism
- Typebot uploads get OCR'd then **the file is lost** — no MinIO/S3/SeaweedFS config in `app/config.py`
- `/extract/upload` returns extracted fields only, doesn't persist
- RCIC cannot retrieve original documents

### 2. Documents not linked to cases
- `Case.docs_received` is a counter, not a foreign-key relation
- No `documents` table exists
- RCIC cannot query "show me all documents for case NX-..."
- Metabase `v_doc_progress` shows percentages but can't list missing docs

### 3. No document-type tracking per case
- Checklists live in `programs.yaml`, not linked to actual uploads
- Case never marks "passport: received" or "police_clearance: pending"
- RCIC must manually track in spreadsheet

## High-impact gaps

### 4. RCIC cannot view case documents in one place
- GHL shows custom fields (extracted data) but no document folder link
- No `case_documents_url` or `documents_folder_link` custom field

### 5. OCR extraction not persisted to PostgreSQL
- Extracted fields go to GHL custom fields only
- No Activity record for "document received at 10:15, extracted 6 fields"
- Audit trail broken if GHL purges data

### 6. `Case.assigned_rcic` is a string, not a FK
- `assigned_rcic: Mapped[str] = mapped_column(String(100))` in `db_models.py:100`
- No users table → no performance analytics, no access control, typo-fragile

### 7. Document checklist not dynamic
- Loaded at case initiation from `programs.yaml`
- If IRCC changes requirements mid-case, system doesn't know
- Compliance risk

## Medium gaps

### 8. No Google Drive backup for case documents
### 9. Document dedup is in-memory only (lost on restart)
### 10. No retention policy (GDPR/PIPEDA exposure)
### 11. Dependents table not populated with OCR data

## Recommended fixes (prioritized)

### Priority 1 — Unblock RCIC workflow (6-8 hrs)

**1A. Add `documents` table** (migration + model)
```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    case_id VARCHAR(50) NOT NULL REFERENCES cases(case_id),
    contact_id VARCHAR(50) NOT NULL REFERENCES contacts(id),
    document_type VARCHAR(100),
    filename VARCHAR(255),
    file_hash VARCHAR(64) UNIQUE,
    file_size_bytes INT,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    uploaded_by VARCHAR(100),
    extracted_fields JSONB,
    ocr_method VARCHAR(20),
    ocr_confidence VARCHAR(20),
    extracted_at TIMESTAMP WITH TIME ZONE,
    storage_url VARCHAR(1000),
    storage_backend VARCHAR(20),
    retention_deleted_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX ix_documents_case ON documents(case_id);
```

**1B. Add `case_required_documents` table** for per-case checklist tracking

**1C. Add `GET /cases/{case_id}/documents` endpoint**

**1D. Add SeaweedFS (S3-compatible) container on Railway** for raw file storage

**1E. Modify `/extract/upload` to:**
- Store file in SeaweedFS
- Insert row in `documents` table
- Link to case via FK

### Priority 2 — Staff performance unlock (3 hrs)

**2A. Add `users` table** (replaces string-based RCIC assignments)
**2B. Alembic migration** to convert existing string names to FKs
**2C. Add new Metabase views** for staff performance

### Priority 3 — Compliance (2 hrs)

**3A. Document retention cleanup task** (scheduled APScheduler job)
**3B. Submission validation** (block `stage = submitted` if required docs missing)

## Implementation order

```
Week 1: Priority 1 (docs unblock)
  Day 1: SeaweedFS container + bucket + CORS
  Day 2: documents + case_required_documents tables + migration
  Day 3: /extract/upload writes to SeaweedFS + documents row
  Day 4: /cases/{id}/documents API + Chrome extension "View Docs" button
  Day 5: Seed demo_premium_data updates + Metabase view for docs

Week 2: Priority 2 + 3
  Day 6: users table + migration from string names
  Day 7: Metabase staff performance views
  Day 8: Retention cleanup scheduled job
  Day 9: Paperless-ngx container + OCR archive integration
  Day 10: Docuseal container + retainer flow switch
```
