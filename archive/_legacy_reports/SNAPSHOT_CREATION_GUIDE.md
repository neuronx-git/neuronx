# NeuronX Gold Snapshot Creation & Installation Guide

## Part 1: Create the Gold Snapshot
**Goal**: Package the "NeuronX Test Lab" configuration into a reusable template.

1.  **Switch to Agency View**:
    - Click "Switch to Agency View" at the top left of your GHL dashboard.
2.  **Navigate to Snapshots**:
    - Go to **Settings > Snapshots**.
3.  **Create New Snapshot**:
    - Click the green **+ Create New Snapshot** button.
    - **Name**: `NeuronX Gold v1.0 — 2026-03-17`.
    - **Select Account**: Choose `NeuronX Test Lab` from the dropdown.
    - Click **Save**.
4.  **Verify Creation**:
    - Ensure the new snapshot appears in the list.
    - Note the **Snapshot ID** (optional but useful).

## Part 2: Create a Clean Lab Tenant
**Goal**: Provision a fresh sub-account to test the installation.

1.  **Navigate to Sub-Accounts**:
    - Still in Agency View, go to **Sub-Accounts**.
2.  **Create Sub-Account**:
    - Click **+ Create Sub-Account**.
    - Choose **Regular Account** (or "Blank Snapshot" if prompted, do NOT select a pre-made template yet).
    - Select manually or use Google Maps to find a dummy business (e.g., "NeuronX Clean Lab").
    - **Account Name**: `NeuronX Clean Lab`.
    - **Address/Phone**: Use dummy data if allowed, or your own.
    - **Timezone**: Eastern Time (US & Canada).
3.  **Finish Setup**:
    - Click **Save**.
    - **Important**: Copy the **Location ID** from the URL or settings immediately after creation.
      - Example: `https://app.gohighlevel.com/v2/location/XXXXXXXXXXXXXXXXXXXX/dashboard`
      - The ID is the `XXXXXXXXXXXXXXXXXXXX` part.

## Part 3: Install the Gold Snapshot
**Goal**: Push the configuration into the clean tenant.

1.  **Go to Snapshots**:
    - Agency View > Settings > Snapshots.
2.  **Load Snapshot**:
    - Find `NeuronX Gold v1.0 — 2026-03-17`.
    - Click the **Refresh** icon (optional, to ensure latest data).
    - Click the **Push to Linked Accounts** icon (arrow pointing up/right) OR **Load Snapshot** on the sub-account directly.
    - *Better Method*: Go to **Sub-Accounts**, find `NeuronX Clean Lab`, click **Manage Client**, then **Actions > Load Snapshot**.
3.  **Select Elements**:
    - Choose `NeuronX Gold v1.0 — 2026-03-17`.
    - Click **Proceed**.
    - **Select All**: Ensure Pipelines, Workflows, Campaigns, Triggers, Forms, Funnels, Calendars, Custom Fields, Tags are ALL selected.
    - **Conflict Resolution**: "Overwrite" (since it's a blank account).
    - Click **Proceed/Copy**.
4.  **Confirm**:
    - Wait for the success notification.

## Part 4: Post-Install Configuration (Manual)
**Goal**: Basic setup to allow UAT.

1.  **Switch to Sub-Account**:
    - Click "Switch to Sub-Account" and select `NeuronX Clean Lab`.
2.  **Phone Number**:
    - Go to **Settings > Phone Numbers**.
    - Buy a temporary number ($1.15) or use a trial number if available. *Required for SMS testing.*
3.  **Email Domain**:
    - Go to **Settings > Email Services**.
    - Use the default LeadConnector domain (sufficient for internal UAT, no need to set up dedicated domain for this throwaway test).

## Part 5: Provide Location ID for UAT
**Goal**: Allow Trae to run the verification suite.

1.  Copy the **Location ID** of the `NeuronX Clean Lab`.
2.  Paste it into the chat with Trae.
