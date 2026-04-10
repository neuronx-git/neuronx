/**
 * NeuronX RCIC Assistant — Content Script
 * Runs on IRCC portal pages. Detects form fields and fills them with client data.
 *
 * Supported IRCC pages:
 * - PR Portal (prson-srpj.apps.cic.gc.ca)
 * - Express Entry profile
 * - Work/Study permit applications
 * - General IRCC forms
 */

// Field mappings: maps client data keys to IRCC page selectors
// These are discovered by inspecting IRCC portal DOM elements
const FIELD_MAPPINGS = {
  // Common fields across most IRCC pages
  common: {
    'full_name': ['#familyName', '#FamilyName', 'input[name="familyName"]', 'input[name*="family_name"]', 'input[name*="lastName"]'],
    'given_name': ['#givenName', '#GivenName', 'input[name="givenName"]', 'input[name*="given_name"]', 'input[name*="firstName"]'],
    'date_of_birth': ['#dob', '#DOB', 'input[name="dob"]', 'input[name*="dateOfBirth"]', 'input[name*="birthDate"]'],
    'country_of_citizenship': ['#countryOfCitizenship', 'select[name*="citizenship"]', 'select[name*="country"]', '#citizenship'],
    'passport_number': ['#passportNumber', 'input[name*="passport"]', 'input[name*="travelDoc"]'],
    'email': ['#email', 'input[name="email"]', 'input[type="email"]'],
    'phone': ['#phone', '#phoneNumber', 'input[name*="phone"]', 'input[type="tel"]'],
    'marital_status': ['#maritalStatus', 'select[name*="marital"]', 'select[name*="civilStatus"]'],
  },

  // Express Entry specific
  express_entry: {
    'education_level': ['select[name*="education"]', '#educationLevel', 'select[name*="levelOfStudy"]'],
    'work_experience': ['input[name*="workExperience"]', '#yearsOfExperience'],
    'language_test': ['select[name*="languageTest"]', '#languageExam'],
    'noc_code': ['input[name*="noc"]', '#nocCode', 'input[name*="occupation"]'],
    'settlement_funds': ['input[name*="funds"]', '#settlementFunds'],
  },

  // Spousal Sponsorship specific
  spousal: {
    'sponsor_name': ['#sponsorFamilyName', 'input[name*="sponsor"]'],
    'sponsor_status': ['select[name*="sponsorStatus"]', '#sponsorImmigrationStatus'],
    'relationship_type': ['select[name*="relationship"]', '#relationshipType'],
    'marriage_date': ['input[name*="marriageDate"]', '#dateOfMarriage'],
  },

  // Work Permit specific
  work_permit: {
    'employer_name': ['input[name*="employer"]', '#employerName'],
    'job_title': ['input[name*="jobTitle"]', '#positionTitle'],
    'lmia_status': ['input[name*="lmia"]', '#lmiaNumber'],
  },

  // Use of Representative (IMM 5476) specific
  representative: {
    'rep_family_name': ['input[name*="repFamily"]', '#representativeFamilyName'],
    'rep_given_name': ['input[name*="repGiven"]', '#representativeGivenName'],
    'rep_organization': ['input[name*="organization"]', '#firmName'],
    'rep_member_id': ['input[name*="memberID"]', '#membershipNumber', '#rcicNumber'],
    'rep_email': ['input[name*="repEmail"]', '#representativeEmail'],
    'rep_phone': ['input[name*="repPhone"]', '#representativePhone'],
  }
};

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'getFieldCount') {
    const count = countFillableFields();
    sendResponse({ count });
    return true;
  }

  if (message.action === 'autofill') {
    const result = fillFields(message.data);
    sendResponse(result);
    return true;
  }

  if (message.action === 'detectPageType') {
    const pageType = detectIRCCPageType();
    sendResponse({ pageType });
    return true;
  }
});

/**
 * Detect which type of IRCC page we're on
 */
function detectIRCCPageType() {
  const url = window.location.href.toLowerCase();
  const title = document.title.toLowerCase();
  const bodyText = document.body?.innerText?.toLowerCase() || '';

  if (url.includes('prson-srpj') || url.includes('pr-portal')) return 'pr_portal';
  if (url.includes('express-entry') || bodyText.includes('express entry')) return 'express_entry';
  if (url.includes('work-permit') || bodyText.includes('work permit')) return 'work_permit';
  if (url.includes('study-permit') || bodyText.includes('study permit')) return 'study_permit';
  if (url.includes('sponsor') || bodyText.includes('sponsorship')) return 'spousal';
  if (bodyText.includes('use of a representative') || bodyText.includes('imm 5476')) return 'representative';
  if (url.includes('cic.gc.ca') || url.includes('ircc') || url.includes('canada.ca')) return 'generic_ircc';

  return 'unknown';
}

/**
 * Count fillable fields on the current page
 */
function countFillableFields() {
  const inputs = document.querySelectorAll('input:not([type="hidden"]):not([type="submit"]):not([type="button"]):not([readonly])');
  const selects = document.querySelectorAll('select:not([readonly])');
  const textareas = document.querySelectorAll('textarea:not([readonly])');
  return inputs.length + selects.length + textareas.length;
}

/**
 * Fill form fields with client data
 */
function fillFields(clientData) {
  const pageType = detectIRCCPageType();
  let filledCount = 0;
  let totalFields = 0;
  const errors = [];

  // Get relevant field mappings for this page type
  const mappings = { ...FIELD_MAPPINGS.common };
  if (pageType === 'express_entry') Object.assign(mappings, FIELD_MAPPINGS.express_entry);
  if (pageType === 'spousal') Object.assign(mappings, FIELD_MAPPINGS.spousal);
  if (pageType === 'work_permit') Object.assign(mappings, FIELD_MAPPINGS.work_permit);
  if (pageType === 'representative') Object.assign(mappings, FIELD_MAPPINGS.representative);

  // Also add firm defaults for representative form
  if (pageType === 'representative' && clientData.firm_defaults) {
    Object.assign(clientData, clientData.firm_defaults);
  }

  // Try to fill each mapped field
  for (const [dataKey, selectors] of Object.entries(mappings)) {
    const value = clientData[dataKey] || clientData[dataKey.replace(/_/g, '')] || '';
    if (!value) continue;

    totalFields++;
    let filled = false;

    for (const selector of selectors) {
      try {
        const element = document.querySelector(selector);
        if (element) {
          if (element.tagName === 'SELECT') {
            // For select elements, find matching option
            const options = Array.from(element.options);
            const match = options.find(o =>
              o.text.toLowerCase().includes(value.toLowerCase()) ||
              o.value.toLowerCase().includes(value.toLowerCase())
            );
            if (match) {
              element.value = match.value;
              element.dispatchEvent(new Event('change', { bubbles: true }));
              filled = true;
            }
          } else if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            element.value = value;
            element.dispatchEvent(new Event('input', { bubbles: true }));
            element.dispatchEvent(new Event('change', { bubbles: true }));
            filled = true;
          }

          if (filled) {
            // Highlight filled field
            element.style.backgroundColor = '#ECFDF5';
            element.style.borderColor = '#10B981';
            element.style.transition = 'all 0.3s';
            filledCount++;
            break;
          }
        }
      } catch (err) {
        errors.push(`${dataKey}: ${err.message}`);
      }
    }

    // If no selector matched, try fuzzy matching by field name/label
    if (!filled) {
      const fuzzyFilled = fuzzyFillField(dataKey, value);
      if (fuzzyFilled) {
        filledCount++;
        filled = true;
      }
    }
  }

  // Show notification banner
  showFillNotification(filledCount, totalFields, pageType);

  return {
    success: filledCount > 0,
    filledCount,
    totalFields,
    pageType,
    errors,
  };
}

/**
 * Fuzzy match: find fields by label text or name attribute
 */
function fuzzyFillField(dataKey, value) {
  const searchTerms = dataKey.replace(/_/g, ' ').toLowerCase().split(' ');

  // Search all labels
  const labels = document.querySelectorAll('label');
  for (const label of labels) {
    const labelText = label.textContent.toLowerCase();
    if (searchTerms.every(term => labelText.includes(term))) {
      const forId = label.getAttribute('for');
      if (forId) {
        const input = document.getElementById(forId);
        if (input) {
          input.value = value;
          input.dispatchEvent(new Event('input', { bubbles: true }));
          input.style.backgroundColor = '#FEF3C7'; // Yellow for fuzzy match
          input.style.borderColor = '#F59E0B';
          return true;
        }
      }
    }
  }

  // Search by name attribute containing the data key
  const cleanKey = dataKey.replace(/_/g, '');
  const inputs = document.querySelectorAll(`input[name*="${cleanKey}" i], select[name*="${cleanKey}" i]`);
  if (inputs.length === 1) {
    const input = inputs[0];
    input.value = value;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.style.backgroundColor = '#FEF3C7';
    input.style.borderColor = '#F59E0B';
    return true;
  }

  return false;
}

/**
 * Show a notification banner at the top of the page
 */
function showFillNotification(filled, total, pageType) {
  // Remove existing notification
  const existing = document.getElementById('neuronx-notification');
  if (existing) existing.remove();

  const banner = document.createElement('div');
  banner.id = 'neuronx-notification';
  banner.style.cssText = `
    position: fixed; top: 0; left: 0; right: 0; z-index: 999999;
    padding: 12px 20px; font-family: Inter, -apple-system, sans-serif;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    ${filled > 0
      ? 'background: #0F172A; color: white;'
      : 'background: #FEF2F2; color: #991B1B;'}
  `;

  const icon = filled > 0 ? '✅' : '⚠️';
  const message = filled > 0
    ? `${icon} NeuronX: Filled ${filled} of ${total} fields on this ${pageType.replace(/_/g, ' ')} page. Green = exact match, Yellow = fuzzy match. Please review before submitting.`
    : `${icon} NeuronX: No matching fields found on this page. Try a different IRCC page.`;

  banner.innerHTML = `
    <span style="font-size:13px;">${message}</span>
    <button onclick="this.parentElement.remove()" style="background:none; border:none; color:inherit; cursor:pointer; font-size:18px; margin-left:12px;">×</button>
  `;

  document.body.prepend(banner);

  // Auto-hide after 15 seconds
  setTimeout(() => {
    if (banner.parentElement) {
      banner.style.transition = 'opacity 0.5s';
      banner.style.opacity = '0';
      setTimeout(() => banner.remove(), 500);
    }
  }, 15000);
}

// Log that content script loaded
console.log('[NeuronX RCIC Assistant] Content script loaded on:', window.location.href);
