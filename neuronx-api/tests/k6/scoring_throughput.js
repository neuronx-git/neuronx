import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.API_BASE_URL || 'http://localhost:8000';

export const options = {
  stages: [
    { duration: '10s', target: 20 },
    { duration: '30s', target: 50 },
    { duration: '20s', target: 100 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<200', 'p(99)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

const programs = ['Express Entry', 'Spousal Sponsorship', 'Study Permit', 'Work Permit'];
const locations = ['In Canada', 'Outside Canada'];
const timelines = ['Urgent (30 days)', 'Near-term (1-3 months)', 'Medium (3-6 months)', 'Long-term (6+ months)'];

export default function () {
  const payload = JSON.stringify({
    contact_id: `load-test-${Date.now()}`,
    r1_program_interest: programs[Math.floor(Math.random() * programs.length)],
    r2_current_location: locations[Math.floor(Math.random() * locations.length)],
    r3_timeline_urgency: timelines[Math.floor(Math.random() * timelines.length)],
    r4_prior_applications: 'None',
    r5_budget_awareness: 'Aware',
  });

  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  const res = http.post(`${BASE_URL}/score/`, payload, params);
  check(res, {
    'score status 200': (r) => r.status === 200,
    'score has outcome': (r) => {
      try { return JSON.parse(r.body).outcome !== undefined; }
      catch(e) { return false; }
    },
  });

  sleep(0.5);
}
