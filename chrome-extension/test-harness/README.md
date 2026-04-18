# Chrome Extension Test Harness

Self-contained environment to test the NeuronX RCIC Assistant extension without needing:
- Live NeuronX API / Railway
- Real GHL credentials
- Access to actual IRCC portal

## Contents

| File | Purpose |
|---|---|
| `mock_server.py` | FastAPI server — returns mock clients + form data (port 8000) |
| `demo-ircc-form.html` | Static HTML replicating IRCC Express Entry form field IDs |
| `playwright_test.spec.js` | Automated E2E test (optional) |

## 5-minute setup

### 1. Start the mock API
```bash
cd chrome-extension/test-harness
pip install fastapi uvicorn
python mock_server.py
```
Server runs on `http://127.0.0.1:8000` — leave it running.

### 2. Open the demo form in Chrome
```bash
open demo-ircc-form.html  # macOS
# or drag file into Chrome
```
You'll see a replica IRCC form with a test panel in the top-right.

### 3. Load the extension in Chrome (dev mode)
1. `chrome://extensions/` → enable **Developer mode** (top-right)
2. Click **Load unpacked** → select `chrome-extension/` (parent dir)
3. Extension appears in toolbar (pin it)

### 4. Point extension at mock API
1. Click extension icon → **Settings** (top-right gear/link)
2. API URL: `http://127.0.0.1:8000`
3. Location ID: `test-location` (mock ignores it)
4. **Save Settings**

### 5. Run the test
1. On the demo form page, click extension icon again
2. Type `john` in search → select **John Smith**
3. Click **⚡ Auto-Fill This Page**
4. Watch form fields populate + test-panel log on the right

### Expected result

| Field | Filled with |
|---|---|
| `givenName` | John |
| `familyName` | Smith |
| `dob` | 1990-05-15 |
| `email` | john.smith@demo.neuronx.co |
| `phone` | +14165550100 |
| `maritalStatus` | married |
| `countryOfCitizenship` | India |
| `passportNumber` | K1234567 |
| `educationLevel` | Bachelor's Degree |
| `yearsOfExperience` | 5 |
| `nocCode` | 2173 |
| `settlementFunds` | 25000 |
| `representativeGivenName` | Rajiv |
| `representativeFamilyName` | Mehta |
| `firmName` | Visa Master Canada |
| `membershipNumber` | R123456 |

Extension notification banner should show: "Filled 15 of ~16 fields"

## Troubleshooting

### "Failed to fetch" or CORS errors
Mock server allows `*` origins. If you see CORS errors, check:
- Mock server is running (`curl http://127.0.0.1:8000/health`)
- Extension settings point to `http://127.0.0.1:8000` (not https)

### Fields not filling
- Check Chrome DevTools console on the demo form page
- Check extension popup console (right-click popup → Inspect)
- Verify content script injected: look for `[NeuronX]` log lines

### Testing other clients
Mock server has 3 clients:
- `John Smith` (Express Entry, India)
- `Maria Garcia` (Spousal, Mexico)
- `Raj Patel` (Work Permit, India)

## Test other IRCC forms

The demo form mimics the **Express Entry profile**. To test other form variants:
1. Copy `demo-ircc-form.html` → `demo-spousal-form.html` or `demo-work-permit.html`
2. Modify field IDs to match the real IRCC form
3. Repeat the test

Field IDs the extension targets (from `content.js`):
- Common: `givenName`, `familyName`, `dob`, `email`, `phone`, `maritalStatus`, `countryOfCitizenship`, `passportNumber`
- Express Entry: `educationLevel`, `yearsOfExperience`, `nocCode`, `settlementFunds`, `languageExam`
- Spousal: `sponsor_name`, `marriage_date`, `relationship_type`, `sponsor_status`
- Work Permit: `employer_name`, `job_title`, `lmia_status`
- Representative: `representativeGivenName`, `representativeFamilyName`, `firmName`, `membershipNumber`, `representativeEmail`, `representativePhone`

## Production readiness checklist

Before shipping extension to real RCICs:
- [ ] Add Bearer-token auth to extension → API calls
- [ ] Enforce HTTPS only in production manifest
- [ ] Add CSP header to manifest
- [ ] Test against 5+ real IRCC form pages — document selector coverage
- [ ] Add retry logic for API failures (3 attempts, 2s backoff)
- [ ] Field format validation (date YYYY-MM-DD, phone regex, NOC 4 digits)
- [ ] Audit log: POST to backend every fill event
- [ ] Rotate stored API tokens every 30 days
