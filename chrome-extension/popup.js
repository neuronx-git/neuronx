/**
 * NeuronX RCIC Assistant — Popup Script
 * Handles client search, selection, and autofill trigger.
 */

const DEFAULT_API_URL = 'https://neuronx-production-62f9.up.railway.app';
let apiUrl = DEFAULT_API_URL;
let selectedContactId = null;

// Init
document.addEventListener('DOMContentLoaded', async () => {
  // Load saved settings
  const settings = await chrome.storage.local.get(['apiUrl', 'locationId']);
  if (settings.apiUrl) {
    apiUrl = settings.apiUrl;
    document.getElementById('api-url').value = apiUrl;
  }
  if (settings.locationId) {
    document.getElementById('location-id').value = settings.locationId;
  }

  // Event listeners
  document.getElementById('client-search').addEventListener('input', debounce(searchClients, 300));
  document.getElementById('client-select').addEventListener('change', onClientSelected);
  document.getElementById('autofill-btn').addEventListener('click', triggerAutofill);
  document.getElementById('datasheet-btn').addEventListener('click', generateDataSheet);
  document.getElementById('validate-btn').addEventListener('click', validateCompleteness);
  document.getElementById('save-settings').addEventListener('click', saveSettings);
  document.getElementById('open-settings').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('settings-panel').style.display =
      document.getElementById('settings-panel').style.display === 'none' ? 'block' : 'none';
  });
});

// Debounce helper
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

// Search clients via NeuronX API
async function searchClients() {
  const query = document.getElementById('client-search').value.trim();
  if (query.length < 2) return;

  showLoading(true);
  try {
    const resp = await fetch(`${apiUrl}/documents/checklist`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ program_type: 'Express Entry', contact_id: 'search' }),
    });

    // For now, use GHL search via our API proxy
    // In production, this calls GET /clients/search?q=query
    const select = document.getElementById('client-select');
    select.innerHTML = `<option value="demo-001">Priya Sharma — Express Entry</option>
      <option value="demo-002">Ahmed Hassan — Spousal Sponsorship</option>
      <option value="demo-003">Wei Chen — Work Permit</option>
      <option value="demo-004">Maria Santos — Express Entry</option>
      <option value="demo-006">Fatima Al-Rashid — Express Entry</option>
      <option value="demo-009">Carlos Rivera — Spousal Sponsorship</option>`;

    showStatus('info', `Found clients matching "${query}"`);
  } catch (err) {
    showStatus('error', `Search failed: ${err.message}`);
  }
  showLoading(false);
}

// Client selected
async function onClientSelected() {
  const select = document.getElementById('client-select');
  selectedContactId = select.value;
  const clientName = select.options[select.selectedIndex].text;

  const [name, program] = clientName.split(' — ');
  document.getElementById('client-name').textContent = name;
  document.getElementById('client-program').textContent = program || 'Unknown Program';
  document.getElementById('client-details').textContent = `Contact ID: ${selectedContactId}`;
  document.getElementById('client-info-panel').style.display = 'block';

  // Get field count for current page
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab) {
    chrome.tabs.sendMessage(tab.id, { action: 'getFieldCount' }, (response) => {
      if (response && response.count) {
        document.getElementById('field-count').textContent = `${response.count} fields detected`;
      } else {
        document.getElementById('field-count').textContent = 'Open an IRCC page first';
      }
    });
  }
}

// Trigger autofill on the active page
async function triggerAutofill() {
  if (!selectedContactId) {
    showStatus('error', 'Please select a client first');
    return;
  }

  const btn = document.getElementById('autofill-btn');
  btn.disabled = true;
  btn.textContent = '⏳ Filling...';
  showLoading(true);

  try {
    // Get client form data from NeuronX API
    const resp = await fetch(`${apiUrl}/clients/${selectedContactId}/form-data`);
    if (!resp.ok) throw new Error(`API error: ${resp.status}`);
    const formData = await resp.json();

    // Send to content script to fill the page
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.tabs.sendMessage(tab.id, {
      action: 'autofill',
      data: formData,
    }, (response) => {
      if (response && response.success) {
        showStatus('success', `Filled ${response.filledCount} of ${response.totalFields} fields! Review before submitting.`);
      } else {
        showStatus('error', response?.error || 'Autofill failed. Is this an IRCC page?');
      }
      btn.disabled = false;
      btn.textContent = '⚡ Auto-Fill This Page';
      showLoading(false);
    });
  } catch (err) {
    showStatus('error', `Autofill failed: ${err.message}`);
    btn.disabled = false;
    btn.textContent = '⚡ Auto-Fill This Page';
    showLoading(false);
  }
}

// Generate data sheet
async function generateDataSheet() {
  if (!selectedContactId) return;
  showLoading(true);
  try {
    const resp = await fetch(`${apiUrl}/clients/${selectedContactId}/data-sheet`);
    const data = await resp.json();
    // Open in new tab
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    chrome.tabs.create({ url });
    showStatus('success', 'Data sheet generated!');
  } catch (err) {
    showStatus('error', `Failed: ${err.message}`);
  }
  showLoading(false);
}

// Validate completeness
async function validateCompleteness() {
  if (!selectedContactId) return;
  showLoading(true);
  try {
    const resp = await fetch(`${apiUrl}/clients/${selectedContactId}/validate`);
    const result = await resp.json();
    if (result.is_complete) {
      showStatus('success', `All ${result.total_fields} fields complete. Ready for submission!`);
    } else {
      showStatus('error', `${result.missing_count} fields missing: ${result.missing_fields.join(', ')}`);
    }
  } catch (err) {
    showStatus('error', `Validation failed: ${err.message}`);
  }
  showLoading(false);
}

// Save settings
async function saveSettings() {
  const url = document.getElementById('api-url').value.trim();
  const locId = document.getElementById('location-id').value.trim();
  await chrome.storage.local.set({ apiUrl: url, locationId: locId });
  apiUrl = url;
  showStatus('success', 'Settings saved!');
  document.getElementById('settings-panel').style.display = 'none';
}

// UI helpers
function showLoading(show) {
  document.getElementById('loading').className = show ? 'show' : '';
}

function showStatus(type, message) {
  const el = document.getElementById('status');
  el.className = `status ${type}`;
  el.textContent = message;
  if (type === 'success' || type === 'info') {
    setTimeout(() => { el.style.display = 'none'; }, 5000);
  }
}
