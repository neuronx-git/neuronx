import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.API_BASE_URL || 'http://localhost:8000';

export const options = {
  scenarios: {
    webhook_burst: {
      executor: 'ramping-arrival-rate',
      startRate: 5,
      timeUnit: '1s',
      preAllocatedVUs: 50,
      maxVUs: 100,
      stages: [
        { duration: '10s', target: 20 },
        { duration: '30s', target: 50 },
        { duration: '10s', target: 0 },
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    http_req_failed: ['rate<0.05'],
  },
};

const ghlPayload = JSON.stringify({
  type: 'ContactCreate',
  locationId: 'test-location',
  id: 'contact-load-test',
  firstName: 'Load',
  lastName: 'Test',
  email: 'loadtest@example.com',
  phone: '+14165550000',
  tags: [],
  customFields: [],
});

export default function () {
  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  const res = http.post(`${BASE_URL}/webhooks/ghl`, ghlPayload, params);
  check(res, {
    'webhook accepted': (r) => r.status < 500,
  });

  sleep(0.1);
}
