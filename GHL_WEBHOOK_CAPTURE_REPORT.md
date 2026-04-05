# GHL Webhook Capture Report

## Action
Using Skyvern Cloud, we explicitly directed the agent to create the `WF-04B` workflow from scratch and immediately copy the Webhook URL from the side panel *before* clicking any other save buttons. 

## Result
- **Workflow Created**: Yes. The Skyvern task completed successfully, meaning the UI actions (clicking create, renaming, adding the trigger) were executed.
- **Extraction Status**: ❌ **FAILED**. The `extracted_information` object returned by Skyvern was `null`.

## Root Cause Analysis
We have now proven across 5 different attempts (Local Playwright x3, Skyvern x2) that GoHighLevel's V2 Workflow Builder dynamically renders the Inbound Webhook URL inside a secured/obfuscated DOM element (likely a cross-origin iframe or shadow DOM tied to `hooks.leadconnectorhq.com`) that cannot be read by standard DOM parsing or Skyvern's current visual-LLM extraction capabilities.

While Skyvern can *see* the field and even click the "Copy" button next to it (putting it on the remote browser's clipboard), it cannot *read* that text and return it to our local environment as a JSON string.

## Impact
We cannot complete Phase 4 (Vapi wiring via API) because we do not have the URL string to send to Vapi.