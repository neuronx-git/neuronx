/**
 * NeuronX RCIC Assistant — Background Service Worker
 * Handles API calls and manages state.
 */

// Default configuration
const DEFAULT_CONFIG = {
  apiUrl: 'https://neuronx-production-62f9.up.railway.app',
  locationId: 'FlRL82M0D6nclmKT7eXH',
};

// Listen for installation
chrome.runtime.onInstalled.addListener(() => {
  console.log('[NeuronX] Extension installed');
  chrome.storage.local.set(DEFAULT_CONFIG);
});

// Handle messages from popup or content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'fetchClientData') {
    fetchClientData(message.contactId)
      .then(data => sendResponse({ success: true, data }))
      .catch(err => sendResponse({ success: false, error: err.message }));
    return true; // async response
  }

  if (message.action === 'searchClients') {
    searchClients(message.query)
      .then(results => sendResponse({ success: true, results }))
      .catch(err => sendResponse({ success: false, error: err.message }));
    return true;
  }
});

async function fetchClientData(contactId) {
  const config = await chrome.storage.local.get(['apiUrl']);
  const apiUrl = config.apiUrl || DEFAULT_CONFIG.apiUrl;

  const resp = await fetch(`${apiUrl}/clients/${contactId}/form-data`);
  if (!resp.ok) throw new Error(`API error: ${resp.status}`);
  return resp.json();
}

async function searchClients(query) {
  const config = await chrome.storage.local.get(['apiUrl']);
  const apiUrl = config.apiUrl || DEFAULT_CONFIG.apiUrl;

  const resp = await fetch(`${apiUrl}/clients/search?q=${encodeURIComponent(query)}`);
  if (!resp.ok) throw new Error(`Search error: ${resp.status}`);
  return resp.json();
}
