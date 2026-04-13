# Vapi <-> GHL Wiring Report

## Objective
Connect the GoHighLevel `WF-01A` workflow to the newly provisioned Vapi Assistant.

## Current State
- **GHL Tenant**: Ready (`FlRL82M0D6nclmKT7eXH`)
- **Vapi Assistant**: Created and configured (`289a9701-9199-4d03-9416-49d18bec2f69`)
- **Vapi Phone Number**: ✅ Provisioned (`43e01c63-f342-4a5c-84e8-5cd54810dd68`)

## The Webhook Architecture
The phone number has been successfully acquired via Authenticated UI Automation. The following JSON payload must now be injected into the GHL `WF-01A` Webhook action to trigger the AI call:

```json
{
  "phoneNumberId": "43e01c63-f342-4a5c-84e8-5cd54810dd68",
  "customer": {
    "number": "{{contact.phone}}",
    "name": "{{contact.first_name}}"
  },
  "assistantId": "289a9701-9199-4d03-9416-49d18bec2f69",
  "assistantOverrides": {
    "variableValues": {
      "first_name": "{{contact.first_name}}",
      "contact_id": "{{contact.id}}" 
    }
  }
}
```

## Verdict
✅ **READY FOR WIRING**
The `phoneNumberId` is now available. This JSON payload can be pasted directly into the GHL Workflow Webhook action to activate the AI.