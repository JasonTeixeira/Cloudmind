import http from 'k6/http';
import { browser } from 'k6/experimental/browser';
import { check, sleep } from 'k6';
import { Rate, Counter, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('error_rate');
const pageLoadTime = new Trend('page_load_time');
const interactionTime = new Trend('interaction_time');
const apiCallsCounter = new Counter('api_calls');

// Test configuration
export const options = {
  scenarios: {
    // Browser-based load testing
    browser_load_test: {
      executor: 'constant-vus',
      exec: 'browserTest',
      vus: 5,
      duration: '2m',
      options: {
        browser: {
          type: 'chromium',
        },
      },
    },
    // API load testing
    api_load_test: {
      executor: 'ramping-vus',
      exec: 'apiTest',
      startVUs: 0,
      stages: [
        { duration: '30s', target: 10 },
        { duration: '1m', target: 20 },
        { duration: '30s', target: 0 },
      ],
    },
    // Stress testing
    stress_test: {
      executor: 'ramping-vus',
      exec: 'stressTest',
      startVUs: 0,
      stages: [
        { duration: '1m', target: 50 },
        { duration: '2m', target: 100 },
        { duration: '1m', target: 0 },
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% of requests must complete below 2s
    http_req_failed: ['rate<0.05'], // Error rate must be below 5%
    error_rate: ['rate<0.1'],
    page_load_time: ['p(95)<5000'], // 95% of page loads under 5s
    interaction_time: ['p(95)<1000'], // 95% of interactions under 1s
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';

// Browser-based testing
export async function browserTest() {
  const page = browser.newPage();
  
  try {
    // Test homepage load
    const startTime = Date.now();
    await page.goto(BASE_URL);
    await page.waitForSelector('[data-testid="app-container"]', { timeout: 10000 });
    const loadTime = Date.now() - startTime;
    pageLoadTime.add(loadTime);
    
    check(page, {
      'homepage loads successfully': () => page.locator('[data-testid="app-container"]').isVisible(),
    });

    // Test navigation to dashboard
    const navStart = Date.now();
    await page.click('[data-testid="dashboard-link"]');
    await page.waitForSelector('[data-testid="dashboard-content"]', { timeout: 10000 });
    const navTime = Date.now() - navStart;
    interactionTime.add(navTime);

    // Test pricing calculator
    await page.goto(`${BASE_URL}/pricing`);
    await page.waitForSelector('[data-testid="pricing-calculator"]', { timeout: 10000 });
    
    // Interact with pricing calculator
    const calcStart = Date.now();
    await page.fill('[data-testid="quantity-input-1"]', '10');
    await page.click('[data-testid="calculate-button"]');
    await page.waitForSelector('[data-testid="pricing-result"]', { timeout: 10000 });
    const calcTime = Date.now() - calcStart;
    interactionTime.add(calcTime);

    // Test command palette
    await page.keyboard.press('Meta+k');
    await page.waitForSelector('[placeholder="Search commands..."]', { timeout: 5000 });
    await page.type('[placeholder="Search commands..."]', 'dashboard');
    await page.keyboard.press('Enter');
    await page.waitForSelector('[data-testid="dashboard-content"]', { timeout: 10000 });

    check(page, {
      'command palette works': () => page.locator('[data-testid="dashboard-content"]').isVisible(),
    });

    sleep(1);

  } catch (error) {
    console.error('Browser test error:', error);
    errorRate.add(1);
  } finally {
    page.close();
  }
}

// API load testing
export function apiTest() {
  const endpoints = [
    '/api/v1/pricing/tokens',
    '/api/v1/dashboard/metrics',
    '/api/v1/cost/events',
    '/api/v1/projects',
  ];

  endpoints.forEach(endpoint => {
    const response = http.get(`${BASE_URL}${endpoint}`, {
      headers: {
        'Accept': 'application/json',
        'User-Agent': 'k6-load-test',
      },
    });

    apiCallsCounter.add(1);

    const success = check(response, {
      [`${endpoint} status is 200`]: (r) => r.status === 200,
      [`${endpoint} response time < 2s`]: (r) => r.timings.duration < 2000,
      [`${endpoint} has valid JSON`]: (r) => {
        try {
          JSON.parse(r.body);
          return true;
        } catch {
          return false;
        }
      },
    });

    if (!success) {
      errorRate.add(1);
    }
  });

  // Test POST requests
  const pricingCalculation = {
    items: [
      { service_token_id: '1', quantity: 10 }
    ]
  };

  const postResponse = http.post(`${BASE_URL}/api/v1/pricing/calculate`, 
    JSON.stringify(pricingCalculation), 
    {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    }
  );

  check(postResponse, {
    'pricing calculation succeeds': (r) => r.status === 200,
    'pricing calculation response time < 3s': (r) => r.timings.duration < 3000,
  });

  sleep(1);
}

// Stress testing
export function stressTest() {
  // Simulate heavy user interactions
  const pages = [
    '/',
    '/dashboard',
    '/pricing',
    '/cost-analysis',
    '/client-portal',
    '/infrastructure',
    '/security',
    '/reports',
  ];

  // Random page access
  const randomPage = pages[Math.floor(Math.random() * pages.length)];
  const response = http.get(`${BASE_URL}${randomPage}`, {
    headers: {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'User-Agent': 'k6-stress-test',
    },
  });

  const success = check(response, {
    [`${randomPage} loads under stress`]: (r) => r.status === 200,
    [`${randomPage} response time acceptable`]: (r) => r.timings.duration < 5000,
  });

  if (!success) {
    errorRate.add(1);
  }

  // Simulate concurrent API calls
  const apiRequests = [
    http.get(`${BASE_URL}/api/v1/pricing/tokens`),
    http.get(`${BASE_URL}/api/v1/dashboard/metrics`),
    http.get(`${BASE_URL}/api/v1/cost/events`),
  ];

  apiRequests.forEach((response, index) => {
    check(response, {
      [`concurrent API call ${index} succeeds`]: (r) => r.status === 200,
    });
  });

  sleep(0.5);
}

// Setup function
export function setup() {
  console.log('🚀 Starting frontend load testing...');
  console.log(`📍 Target URL: ${BASE_URL}`);
  
  // Verify the application is running
  const response = http.get(BASE_URL);
  if (response.status !== 200) {
    throw new Error(`Application not accessible at ${BASE_URL}. Status: ${response.status}`);
  }
  
  console.log('✅ Application is accessible, starting tests...');
  return { baseUrl: BASE_URL };
}

// Teardown function
export function teardown(data) {
  console.log('🏁 Load testing completed');
  console.log(`📊 Total API calls made: ${apiCallsCounter.value}`);
}

// Handle summary
export function handleSummary(data) {
  const summary = {
    timestamp: new Date().toISOString(),
    test_duration: data.state.testRunDurationMs,
    scenarios: Object.keys(data.metrics).filter(key => key.startsWith('scenario_')),
    metrics: {
      http_req_duration: data.metrics.http_req_duration,
      http_req_failed: data.metrics.http_req_failed,
      error_rate: data.metrics.error_rate?.values || {},
      page_load_time: data.metrics.page_load_time?.values || {},
      interaction_time: data.metrics.interaction_time?.values || {},
      api_calls: data.metrics.api_calls?.values || {},
    },
    thresholds: data.thresholds,
  };

  // Save detailed results
  return {
    'load-test-results.json': JSON.stringify(summary, null, 2),
    stdout: generateTextSummary(summary),
  };
}

function generateTextSummary(summary) {
  return `
🚀 Frontend Load Test Results
============================

📅 Test Duration: ${(summary.test_duration / 1000).toFixed(2)}s
📊 Scenarios: ${summary.scenarios.length}

📈 Key Metrics:
- HTTP Request Duration (p95): ${summary.metrics.http_req_duration?.values?.['p(95)']?.toFixed(2) || 'N/A'}ms
- HTTP Request Failure Rate: ${(summary.metrics.http_req_failed?.values?.rate * 100)?.toFixed(2) || 'N/A'}%
- Page Load Time (p95): ${summary.metrics.page_load_time?.['p(95)']?.toFixed(2) || 'N/A'}ms
- Interaction Time (p95): ${summary.metrics.interaction_time?.['p(95)']?.toFixed(2) || 'N/A'}ms
- Total API Calls: ${summary.metrics.api_calls?.count || 'N/A'}

🎯 Threshold Results:
${Object.entries(summary.thresholds || {})
  .map(([key, result]) => `- ${key}: ${result.ok ? '✅ PASS' : '❌ FAIL'}`)
  .join('\n')}

${Object.values(summary.thresholds || {}).every(t => t.ok) 
  ? '🎉 All thresholds passed!' 
  : '⚠️  Some thresholds failed. Check the detailed results.'}
`;
}
