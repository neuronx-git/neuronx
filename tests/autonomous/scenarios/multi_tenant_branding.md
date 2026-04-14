# Autonomous Test: Multi-Tenant Branding Verification

## Objective
Verify that each configured tenant gets correct branding when their form is loaded.
Compare colors, logos, bot names, and form titles against tenants.yaml config.

## Test Steps

### For each tenant in config/tenants.yaml:

1. Read the tenant config from config/tenants.yaml
2. Navigate to https://neuronx-production-62f9.up.railway.app/form/{tenant_slug}/onboarding
3. Wait for page to load
4. Take a full-page screenshot
5. Verify:
   - Page title or header contains tenant name
   - Primary brand color is applied (check CSS)
   - Bot name matches config
   - Avatar image loads (no broken image)
   - Form is interactive (Typebot embed loads)

### Cross-Tenant Verification
6. Compare screenshots across tenants — they should NOT be identical
7. Verify each tenant has unique branding (different colors, names, logos)

## Expected Tenants (from tenants.yaml)
- vmc (Visa Master Canada) — primary tenant
- (additional tenants if configured)

## Output
JSON report with per-tenant pass/fail and screenshot paths.
