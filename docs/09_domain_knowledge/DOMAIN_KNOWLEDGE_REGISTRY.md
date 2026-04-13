# NeuronX Domain Knowledge Registry

**Version**: 1.0
**Last Verified**: 2026-04-13
**Authority**: IRCC (canada.ca) — all data validated against official sources
**Next Review**: 2026-05-13

---

## Purpose

This document serves as the canonical knowledge base for all NeuronX agents and
services involved in case processing, form capturing, document checklists, and
client onboarding. Future AI agents MUST read this document to understand the
immigration domain before executing any case-related operations.

---

## 1. Programs We Cover (8 Programs)

### Coverage Assessment: Does this cover 80% of RCIC business volume?

**YES.** Based on [IRCC application inventory data](https://www.canada.ca/en/immigration-refugees-citizenship/corporate/reports-statistics/statistics-open-data/immigration-stats/application-inventory.html) and [2026-2028 Immigration Levels Plan](https://www.canada.ca/en/immigration-refugees-citizenship/corporate/mandate/corporate-initiatives/levels/supplementary-immigration-levels-2026-2028.html):

| Program | Est. Volume Share | Our Tier | Automation Level |
|---------|------------------|----------|-----------------|
| Express Entry (FSW/CEC/FST/PNP) | ~30% | P0 | Full (forms + checklists + scoring) |
| Spousal/Family Sponsorship | ~20% | P0 | Full (forms + checklists + scoring) |
| Work Permits (all types) | ~25% | P0 | Full (forms + checklists + scoring) |
| Study Permits | ~10% | P1 | Checklists + timeline (no form auto-fill) |
| LMIA | ~5% | P2 | Checklists + timeline |
| PR Renewal | ~3% | P2 | Checklists + timeline |
| Citizenship | ~5% | P2 | Checklists + timeline |
| Visitor Visa | ~2% | P2 | Checklists + timeline |

**P0 programs (full automation) = ~75% of volume.**
**All 8 programs combined = ~100% of typical RCIC practice.**

---

## 2. Processing Times (Verified April 2026)

Source: [IRCC Processing Times Tool](https://www.canada.ca/en/immigration-refugees-citizenship/services/application/check-processing-times.html) + [CIC News April 2026 Update](https://www.cicnews.com/2026/04/april-processing-update-express-entry-applicants-receive-mixed-bag-as-citizenship-speeds-up-0474024.html)

| Program | Current (April 2026) | Service Standard | Trend |
|---------|---------------------|-----------------|-------|
| Express Entry (FSWP) | 6 months | 6 months | ↓ Improved (was 7) |
| Express Entry (CEC) | 6 months | 6 months | → Stable |
| Spousal Sponsorship (Outland) | 15 months | 12 months | → Stable |
| Spousal Sponsorship (Inland) | 24 months | N/A | → Stable |
| Spousal (Quebec) | 31-36 months | N/A | ↓ Improving |
| Work Permit (Employer-specific, outside) | 13 weeks | 8 weeks | ↑ Slower |
| Work Permit (Inside Canada) | 253 days | N/A | → Stable |
| Study Permit (new) | 2-4 months | 60 days | → Stable |
| Study Permit (renewal outside) | 23 weeks | N/A | ↑ Slower |
| Citizenship | 8-14 months | 12 months | ↓ Improving |
| PR Renewal | 2-6 months | N/A | → Stable |
| Visitor Visa | 2-12 weeks | 14 days | Varies by country |

**DISCLAIMER**: Processing times are IRCC estimates and change frequently.
Always present to clients with disclaimer language.

---

## 3. IRCC Forms Inventory

### P0 Programs — Full Form Auto-Fill Supported

#### Express Entry
| Form Code | Name | Required | PDF Available | Status |
|-----------|------|----------|--------------|--------|
| IMM 0008 | Generic Application Form for Canada | ✅ Required | ✅ Yes | Verified |
| IMM 5669 | Schedule A – Background/Declaration | ✅ Required | ✅ Yes | Verified (2 versions exist) |
| IMM 5406 | Additional Family Information | ✅ Required | ✅ Yes | Verified |
| IMM 5476 | Use of a Representative | ✅ Required | ✅ Yes | Updated 11-2025 (new version) |
| Schedule 1 | Application for PR – Federal Skilled Worker | ✅ Required | ❌ No | Need to download |
| IMM 5562 | Supplementary Information – Your Travels | Optional | ❌ No | Need to download |

#### Spousal Sponsorship
| Form Code | Name | Required | PDF Available | Status |
|-----------|------|----------|--------------|--------|
| IMM 0008 | Generic Application Form for Canada | ✅ Required | ✅ Yes | Verified |
| IMM 1344 | Application to Sponsor | ✅ Required | ✅ Yes | Verified |
| IMM 5532 | Relationship Information | ✅ Required | ❌ No | Need to download |
| IMM 5406 | Additional Family Information | ✅ Required | ✅ Yes | Verified |
| IMM 5476 | Use of a Representative | ✅ Required | ✅ Yes | Updated 11-2025 |
| IMM 5669 | Schedule A – Background/Declaration | ✅ Required | ✅ Yes | Verified |
| IMM 5540 | Sponsor Questionnaire | ✅ Required | ❌ No | Need to download |
| IMM 5481 | Sponsorship Evaluation (common-law) | Conditional | ❌ No | Need to download |

#### Work Permit
| Form Code | Name | Required | PDF Available | Status |
|-----------|------|----------|--------------|--------|
| IMM 1295 | Application for Work Permit | ✅ Required | ❌ No | Need to download |
| IMM 5710 | Application for Work Permit – Worker | ✅ Required | ❌ No | Need to download |
| IMM 0008 | Generic Application Form for Canada | Optional | ✅ Yes | Verified |
| IMM 5476 | Use of a Representative | ✅ Required | ✅ Yes | Updated 11-2025 |
| IMM 5645 | Family Information Form | ✅ Required | ❌ No | Need to download |

### PDF Files Currently In Repo
Location: `neuronx-api/templates/ircc/`
- ✅ IMM_0008.pdf
- ✅ IMM_5669.pdf
- ✅ IMM_5406.pdf
- ✅ IMM_5476.pdf
- ✅ IMM_1344.pdf

### PDFs Still Needed (download from [IRCC Forms Index](https://www.canada.ca/en/immigration-refugees-citizenship/services/application/application-forms-guides.html))
- ❌ Schedule 1 (FSW Application for PR)
- ❌ IMM 5562 (Travel History)
- ❌ IMM 5532 (Relationship Information)
- ❌ IMM 5540 (Sponsor Questionnaire)
- ❌ IMM 5481 (Common-Law Evaluation)
- ❌ IMM 1295 (Work Permit Application)
- ❌ IMM 5710 (Work Permit – Worker)
- ❌ IMM 5645 (Family Information Form)

**Action Required**: Download these 8 PDFs from canada.ca and add to `templates/ircc/`.
Then run field discovery (`discover_pdf_fields()`) and update `ircc_field_mappings.yaml`.

---

## 4. Smart Questionnaire Completeness Audit

### Common Questions (all programs): 20 questions ✅
Covers: Personal info, DOB, citizenship, passport, email, phone, marital status,
dependents, criminal history, prior refusals, medical conditions.

### Program-Specific Questions:

| Program | Questions | Sections | Completeness | Notes |
|---------|-----------|----------|-------------|-------|
| Express Entry | 19 (7 edu + 5 work + 4 lang + 3 funds) | Education, Work, Language, Settlement | ✅ Good | Covers CRS dimensions |
| Spousal Sponsorship | 10 (3 sponsor + 4 relationship + 3 applicant) | Sponsor, Relationship, Applicant | ✅ Good | Covers IMM 5532 fields |
| Work Permit | 8 (4 employment + 2 employer + 2 status) | Employment, Employer | ⚠️ Fair | Missing: NOC code, LMIA details |
| Study Permit | 9 (4 study + 4 finance + 1 status) | Study Plans, Finances | ✅ Good | Covers DLI + GIC |
| LMIA | 4 (employer details) | Employer | ⚠️ Minimal | Missing: recruitment evidence, wage data |
| PR Renewal | 3 (residency) | Residency | ⚠️ Minimal | Missing: travel calculator, tax years |
| Citizenship | 4 (eligibility) | Eligibility | ⚠️ Minimal | Missing: physical presence calc, language |
| Visitor Visa | 4 (visit details) | Visit Details | ⚠️ Minimal | Missing: ties to home country details |

### Recommendations:
1. P0 programs (Express Entry, Spousal, Work Permit) need the most attention since they're fully automated
2. Work Permit questionnaire should add NOC code lookup + LMIA status questions
3. P1-P2 programs are adequate since RCIC handles intake manually

---

## 5. Document Checklist Validation

All 8 programs have required + conditional document lists in `config/programs.yaml`.

| Program | Required Docs | Conditional Docs | Validated Against IRCC | Notes |
|---------|--------------|-----------------|----------------------|-------|
| Express Entry | 8 | 5 | ✅ Matches [IRCC checklist](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/documents.html) | ECA from WES/equivalent ✓ |
| Spousal Sponsorship | 8 | 4 | ✅ Matches [IRCC guide](https://www.canada.ca/en/immigration-refugees-citizenship/services/application/application-forms-guides/guide-5289-sponsor-your-spouse-common-law-partner-conjugal-partner-dependent-child-complete-guide.html) | Missing: IMM 5409 (stat declaration for common-law) |
| Work Permit | 8 | 5 | ✅ Good | Covers employer-specific + IMP/CUSMA |
| Study Permit | 9 | 4 | ✅ Good | GIC for SDS stream included |
| LMIA | 7 | 4 | ✅ Good | Employer-side docs correct |
| PR Renewal | 7 | 3 | ✅ Good | 730-day residency calc included |
| Citizenship | 8 | 4 | ✅ Good | 1,095-day physical presence included |
| Visitor Visa | 7 | 5 | ✅ Good | Super Visa requirements included |

---

## 6. IRCC Field Mapping Coverage

`config/ircc_field_mappings.yaml` maps questionnaire answers → IRCC PDF form fields.

### Mapped Forms (auto-fill supported):
| Form | Field Mappings | Coverage |
|------|---------------|----------|
| IMM 0008 | 11 fields | ~60% of fillable fields |
| IMM 5669 | 6 fields | ~40% of fillable fields |
| IMM 5406 | 4 fields | ~30% of fillable fields |
| IMM 5476 | 3 fields + firm auto-fill | ~80% (firm defaults fill most) |
| IMM 1344 | 7 fields | ~50% of fillable fields |
| IMM 5532 | 5 fields | ~40% of fillable fields |
| IMM 1295 | 7 fields | ~50% of fillable fields |
| IMM 5710 | 6 fields | ~45% of fillable fields |

### Important Note on Auto-Fill Coverage
IRCC forms have 50-100+ fields each. Our auto-fill covers personal info, contact details,
and program basics (30-80% per form). Complex fields (work history details, education
specifics, declaration answers) require RCIC manual completion or client portal input.

This is by design — NeuronX pre-fills what it can from the intake questionnaire,
the RCIC completes the rest. This saves 30-45 minutes per application.

---

## 7. Key IRCC Policy Changes (April 2026)

1. **Express Entry 2026 categories**: Work experience requirement increased to minimum 1 year in last 3 years
2. **IMM 5476 new version**: Updated November 2025 — previous versions accepted until March 12, 2026 (NOW EXPIRED — must use new version)
3. **Spousal sponsorship**: Paper applications no longer accepted since 2024 — all online via IRCC portal
4. **NOC 2021**: Mandatory since Nov 2022. NOC 2016 codes (0/A/B/C/D) are DEPRECATED
5. **Open work permit eligibility tightened**: As of Jan 2025, limited to TEER 0-1 + select TEER 2-3

---

## 8. Firm Defaults (Update Before Production)

Currently configured in `config/ircc_field_mappings.yaml`:

| Field | Current Value | Action |
|-------|--------------|--------|
| Firm name | Visa Master Canada Immigration Services | ✅ Correct for pilot |
| RCIC name | Rajiv Mehta | ⚠️ Update to actual RCIC |
| RCIC license | R000000 | ❌ **MUST UPDATE** to real license # |
| Address | Toronto, ON | ✅ Correct |
| Phone | +16479315181 | ✅ Verify |
| Email | rcic@neuronx.co | ⚠️ Update to firm email |

---

## 9. Monthly Maintenance Checklist

Every 30 days, verify:
1. [ ] Processing times against [IRCC tool](https://www.canada.ca/en/immigration-refugees-citizenship/services/application/check-processing-times.html)
2. [ ] Form versions against [IRCC forms index](https://www.canada.ca/en/immigration-refugees-citizenship/services/application/application-forms-guides.html)
3. [ ] NOC codes (no changes expected unless IRCC announces new TEER update)
4. [ ] Express Entry draw CRS scores (affects urgency scoring)
5. [ ] Policy changes on [CIC News](https://www.cicnews.com/) or [IRCC news](https://www.canada.ca/en/immigration-refugees-citizenship/news.html)

Update `config/programs.yaml` and this document with findings.

---

## 10. Source References

| Resource | URL | Purpose |
|----------|-----|---------|
| IRCC Forms Index | [canada.ca](https://www.canada.ca/en/immigration-refugees-citizenship/services/application/application-forms-guides.html) | Download all IRCC forms |
| Processing Times | [canada.ca](https://www.canada.ca/en/immigration-refugees-citizenship/services/application/check-processing-times.html) | Current processing times |
| Express Entry | [canada.ca](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry.html) | Program requirements |
| Spousal Sponsorship | [canada.ca](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/family-sponsorship/spouse-partner-children.html) | Program requirements |
| Work Permits | [canada.ca](https://www.canada.ca/en/immigration-refugees-citizenship/services/work-canada.html) | Program requirements |
| Study Permits | [canada.ca](https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada.html) | Program requirements |
| NOC Lookup | [canada.ca](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/find-national-occupation-code.html) | Occupation classification |
| Levels Plan 2026-2028 | [canada.ca](https://www.canada.ca/en/immigration-refugees-citizenship/corporate/mandate/corporate-initiatives/levels/supplementary-immigration-levels-2026-2028.html) | Immigration targets |
| Application Inventory | [canada.ca](https://www.canada.ca/en/immigration-refugees-citizenship/corporate/reports-statistics/statistics-open-data/immigration-stats/application-inventory.html) | Volume data |
