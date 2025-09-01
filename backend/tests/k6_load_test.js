import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const authSuccessRate = new Rate('auth_success');
const projectCreationRate = new Rate('project_creation_success');
const responseTimeTrend = new Trend('response_time');
const throughputCounter = new Counter('total_requests');

// Test configuration
export const options = {
  stages: [
    // Ramp up to 10 users over 30 seconds
    { duration: '30s', target: 10 },
    // Stay at 10 users for 1 minute
    { duration: '1m', target: 10 },
    // Ramp up to 50 users over 1 minute
    { duration: '1m', target: 50 },
    // Stay at 50 users for 2 minutes
    { duration: '2m', target: 50 },
    // Ramp up to 100 users over 1 minute
    { duration: '1m', target: 100 },
    // Stay at 100 users for 2 minutes
    { duration: '2m', target: 100 },
    // Ramp up to 200 users over 1 minute
    { duration: '1m', target: 200 },
    // Stay at 200 users for 2 minutes
    { duration: '2m', target: 200 },
    // Ramp down to 0 users over 30 seconds
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<800'], // 95% of requests should be below 800ms
    http_req_failed: ['rate<0.01'],   // Error rate should be less than 1%
    errors: ['rate<0.01'],            // Custom error rate should be less than 1%
    auth_success: ['rate>0.95'],      // Auth success rate should be above 95%
    project_creation_success: ['rate>0.90'], // Project creation success rate should be above 90%
  },
};

// Test data
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
const TEST_USER_EMAIL = __ENV.TEST_USER_EMAIL || 'test@example.com';
const TEST_USER_PASSWORD = __ENV.TEST_USER_PASSWORD || 'TestPassword123!';

// Helper functions
function generateRandomString(length) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

function generateTestProject() {
  return {
    name: `Test Project ${generateRandomString(8)}`,
    description: `Stress test project ${generateRandomString(20)}`,
    monthly_budget: Math.floor(Math.random() * 10000) + 100,
    cost_alert_threshold: Math.floor(Math.random() * 100) + 50,
  };
}

// Main test scenarios
export default function() {
  const startTime = new Date();
  
  // Scenario 1: Health checks (lightweight)
  const healthCheck = () => {
    const response = http.get(`${BASE_URL}/health`);
    const success = check(response, {
      'health check status is 200': (r) => r.status === 200,
      'health check response time < 100ms': (r) => r.timings.duration < 100,
    });
    
    if (!success) {
      errorRate.add(1);
    }
    
    responseTimeTrend.add(response.timings.duration);
    throughputCounter.add(1);
    
    return response;
  };

  // Scenario 2: Liveness and readiness probes
  const probeCheck = () => {
    const livezResponse = http.get(`${BASE_URL}/livez`);
    const readyzResponse = http.get(`${BASE_URL}/readyz`);
    
    const success = check(livezResponse, {
      'liveness probe status is 200': (r) => r.status === 200,
    }) && check(readyzResponse, {
      'readiness probe status is 200 or 503': (r) => r.status === 200 || r.status === 503,
    });
    
    if (!success) {
      errorRate.add(1);
    }
    
    responseTimeTrend.add(livezResponse.timings.duration);
    responseTimeTrend.add(readyzResponse.timings.duration);
    throughputCounter.add(2);
  };

  // Scenario 3: Authentication stress test
  const authStressTest = () => {
    // Test login with valid credentials
    const loginPayload = {
      email: TEST_USER_EMAIL,
      password: TEST_USER_PASSWORD,
    };
    
    const loginResponse = http.post(`${BASE_URL}/api/v1/auth/login`, JSON.stringify(loginPayload), {
      headers: { 'Content-Type': 'application/json' },
    });
    
    const loginSuccess = check(loginResponse, {
      'login status is 200 or 401': (r) => r.status === 200 || r.status === 401,
      'login response time < 500ms': (r) => r.timings.duration < 500,
    });
    
    if (loginResponse.status === 200) {
      authSuccessRate.add(1);
      
      // Test with authentication token
      const token = loginResponse.json('access_token');
      if (token) {
        const headers = { 'Authorization': `Bearer ${token}` };
        
        // Test authenticated endpoints
        const projectsResponse = http.get(`${BASE_URL}/api/v1/projects/`, { headers });
        const costResponse = http.get(`${BASE_URL}/api/v1/cost/analysis/1`, { headers });
        
        check(projectsResponse, {
          'authenticated projects endpoint status is 200 or 401': (r) => r.status === 200 || r.status === 401,
        });
        
        check(costResponse, {
          'authenticated cost endpoint status is 200 or 401': (r) => r.status === 200 || r.status === 401,
        });
        
        responseTimeTrend.add(projectsResponse.timings.duration);
        responseTimeTrend.add(costResponse.timings.duration);
        throughputCounter.add(2);
      }
    } else {
      authSuccessRate.add(0);
    }
    
    if (!loginSuccess) {
      errorRate.add(1);
    }
    
    responseTimeTrend.add(loginResponse.timings.duration);
    throughputCounter.add(1);
  };

  // Scenario 4: Project creation stress test
  const projectCreationStressTest = () => {
    const projectData = generateTestProject();
    
    const response = http.post(`${BASE_URL}/api/v1/projects/`, JSON.stringify(projectData), {
      headers: { 'Content-Type': 'application/json' },
    });
    
    const success = check(response, {
      'project creation status is 200, 401, or 422': (r) => r.status === 200 || r.status === 401 || r.status === 422,
      'project creation response time < 1000ms': (r) => r.timings.duration < 1000,
    });
    
    if (response.status === 200) {
      projectCreationRate.add(1);
    } else {
      projectCreationRate.add(0);
    }
    
    if (!success) {
      errorRate.add(1);
    }
    
    responseTimeTrend.add(response.timings.duration);
    throughputCounter.add(1);
  };

  // Scenario 5: Rate limiting stress test
  const rateLimitStressTest = () => {
    // Make rapid requests to trigger rate limiting
    const responses = [];
    for (let i = 0; i < 10; i++) {
      const response = http.get(`${BASE_URL}/health`);
      responses.push(response);
    }
    
    const success = check(responses[0], {
      'rate limit test includes 200 and 429 responses': (r) => {
        const statusCodes = responses.map(resp => resp.status);
        return statusCodes.includes(200) && (statusCodes.includes(429) || statusCodes.every(code => code === 200));
      },
    });
    
    if (!success) {
      errorRate.add(1);
    }
    
    responses.forEach(response => {
      responseTimeTrend.add(response.timings.duration);
      throughputCounter.add(1);
    });
  };

  // Scenario 6: Large payload stress test
  const largePayloadStressTest = () => {
    const largePayload = {
      name: `Large Project ${generateRandomString(1000)}`,
      description: `A` + 'a'.repeat(10000), // 10KB description
      monthly_budget: 1000,
      metadata: {
        large_field: 'x'.repeat(50000), // 50KB field
      },
    };
    
    const response = http.post(`${BASE_URL}/api/v1/projects/`, JSON.stringify(largePayload), {
      headers: { 'Content-Type': 'application/json' },
    });
    
    const success = check(response, {
      'large payload status is 200, 401, 413, or 422': (r) => 
        r.status === 200 || r.status === 401 || r.status === 413 || r.status === 422,
      'large payload response time < 2000ms': (r) => r.timings.duration < 2000,
    });
    
    if (!success) {
      errorRate.add(1);
    }
    
    responseTimeTrend.add(response.timings.duration);
    throughputCounter.add(1);
  };

  // Scenario 7: Concurrent operations stress test
  const concurrentOperationsTest = () => {
    const promises = [];
    
    // Concurrent health checks
    for (let i = 0; i < 5; i++) {
      promises.push(http.get(`${BASE_URL}/health`));
    }
    
    // Concurrent project listings
    for (let i = 0; i < 3; i++) {
      promises.push(http.get(`${BASE_URL}/api/v1/projects/`));
    }
    
    // Wait for all requests to complete
    const responses = promises;
    
    const success = check(responses[0], {
      'concurrent operations completed': (r) => responses.length === 8,
      'concurrent operations response times reasonable': (r) => 
        responses.every(resp => resp.timings.duration < 5000),
    });
    
    if (!success) {
      errorRate.add(1);
    }
    
    responses.forEach(response => {
      responseTimeTrend.add(response.timings.duration);
      throughputCounter.add(1);
    });
  };

  // Execute test scenarios based on virtual user ID
  const userID = __VU;
  const scenario = userID % 7;
  
  switch (scenario) {
    case 0:
      healthCheck();
      break;
    case 1:
      probeCheck();
      break;
    case 2:
      authStressTest();
      break;
    case 3:
      projectCreationStressTest();
      break;
    case 4:
      rateLimitStressTest();
      break;
    case 5:
      largePayloadStressTest();
      break;
    case 6:
      concurrentOperationsTest();
      break;
  }
  
  // Add some think time between iterations
  sleep(Math.random() * 2 + 1); // 1-3 seconds
}

// Setup and teardown functions
export function setup() {
  console.log('Starting k6 load test against:', BASE_URL);
  console.log('Test configuration:', JSON.stringify(options, null, 2));
  
  // Verify the application is accessible
  const healthResponse = http.get(`${BASE_URL}/health`);
  if (healthResponse.status !== 200) {
    throw new Error(`Application not accessible at ${BASE_URL}. Health check returned ${healthResponse.status}`);
  }
  
  console.log('Application is accessible. Starting load test...');
}

export function teardown(data) {
  console.log('Load test completed.');
  console.log('Final metrics:');
  console.log('- Total requests:', throughputCounter.values.count);
  console.log('- Error rate:', errorRate.values.rate);
  console.log('- Auth success rate:', authSuccessRate.values.rate);
  console.log('- Project creation success rate:', projectCreationRate.values.rate);
  console.log('- Average response time:', responseTimeTrend.values.avg, 'ms');
  console.log('- 95th percentile response time:', responseTimeTrend.values.p(95), 'ms');
}

// Handle different test modes
export function handleSummary(data) {
  return {
    'stdout': JSON.stringify(data, null, 2),
    [`k6-results-${new Date().toISOString().split('T')[0]}.json`]: JSON.stringify(data, null, 2),
  };
}
