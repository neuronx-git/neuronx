import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.API_BASE_URL || 'http://localhost:8000';

export const options = {
  stages: [
    { duration: '10s', target: 5 },
    { duration: '30s', target: 5 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  // Health check
  const healthRes = http.get(`${BASE_URL}/health`);
  check(healthRes, {
    'health status 200': (r) => r.status === 200,
    'health has version': (r) => JSON.parse(r.body).version !== undefined,
  });

  // Root endpoint
  const rootRes = http.get(`${BASE_URL}/`);
  check(rootRes, {
    'root status 200': (r) => r.status === 200,
  });

  sleep(1);
}
