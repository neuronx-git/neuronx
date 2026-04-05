# Make.com Orchestration Blueprint

## Objective
This blueprint defines the Make.com scenario required to catch the Vapi webhook, parse the data, and update GoHighLevel.

## Scenario Components

### 1. Trigger: Custom Webhook
- **Method**: POST
- **Data Structure**: JSON (Vapi `end-of-call-report`)

### 2. Module: JSON Parser (Iterator)
- **Input**: `message.toolCalls` array.
- **Action**: Iterate through each tool call to extract arguments.

### 3. Module: Tools / Text Aggregator
- **Action**: Aggregate the dispersed JSON strings from `capture_lead_data`, `score_lead`, and `end_call_summary` into a single variable block.

### 4. Module: OpenAI (GPT-4o) - *Optional but Recommended*
- **Prompt**: 
  "You are a data cleaner. Take this messy JSON aggregation and return a clean, flat JSON object with these exact keys: program_interest, country, urgency, complexity_flag, budget_awareness, estimated_score, summary. If a value is missing, use 'Unknown'."
- **Input**: The aggregated text from Step 3.

### 5. Module: HTTP Request (GHL API v2)
- **Method**: PUT
- **URL**: `https://services.leadconnectorhq.com/contacts/{{message.assistantOverrides.variableValues.contact_id}}`
- **Headers**: 
  - `Authorization`: `Bearer {{GHL_OAUTH_TOKEN}}`
  - `Version`: `2021-07-28`
- **Body**:
```json
{
  "customFields": [
    { "id": "ai_program_interest_id", "value": "{{program_interest}}" },
    { "id": "ai_country_id", "value": "{{country}}" },
    { "id": "ai_urgency_id", "value": "{{urgency}}" },
    { "id": "ai_summary_id", "value": "{{summary}}" }
  ],
  "tags": ["nx:call_completed"]
}
```

## Implementation Note
Since we are in the "No Code Phase 1", we are documenting this blueprint for the founder to import into their Make.com account. We are NOT writing a script to create this scenario programmatically yet, as Make's API for scenario creation is complex and requires a paid plan.

**Action Required**: The founder must import the attached `blueprint.json` (mock representation) into Make.com.