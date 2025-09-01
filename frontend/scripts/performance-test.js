#!/usr/bin/env node

const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');
const fs = require('fs');
const path = require('path');

const PERFORMANCE_BUDGET = {
  'first-contentful-paint': 2000,
  'largest-contentful-paint': 4000,
  'cumulative-layout-shift': 0.1,
  'total-blocking-time': 300,
  'speed-index': 4000
};

const PAGES_TO_TEST = [
  { url: 'http://localhost:3000', name: 'homepage' },
  { url: 'http://localhost:3000/dashboard', name: 'dashboard' },
  { url: 'http://localhost:3000/pricing', name: 'pricing' },
  { url: 'http://localhost:3000/cost-analysis', name: 'cost-analysis' },
  { url: 'http://localhost:3000/client-portal', name: 'client-portal' }
];

async function runLighthouse(url, options) {
  const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });
  const runnerResult = await lighthouse(url, {
    ...options,
    port: chrome.port,
  });

  await chrome.kill();
  return runnerResult;
}

async function testPerformance() {
  console.log('🚀 Starting performance testing...\n');
  
  const results = [];
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const reportDir = path.join(__dirname, '..', 'performance-reports', timestamp);
  
  // Create reports directory
  if (!fs.existsSync(reportDir)) {
    fs.mkdirSync(reportDir, { recursive: true });
  }

  for (const page of PAGES_TO_TEST) {
    console.log(`📊 Testing ${page.name} (${page.url})...`);
    
    try {
      const runnerResult = await runLighthouse(page.url, {
        onlyCategories: ['performance'],
        output: ['json', 'html'],
        outputPath: path.join(reportDir, `${page.name}-lighthouse`),
      });

      const { lhr } = runnerResult;
      const performanceScore = lhr.categories.performance.score * 100;
      
      // Extract key metrics
      const metrics = {
        performanceScore,
        firstContentfulPaint: lhr.audits['first-contentful-paint'].numericValue,
        largestContentfulPaint: lhr.audits['largest-contentful-paint'].numericValue,
        cumulativeLayoutShift: lhr.audits['cumulative-layout-shift'].numericValue,
        totalBlockingTime: lhr.audits['total-blocking-time'].numericValue,
        speedIndex: lhr.audits['speed-index'].numericValue,
      };

      results.push({
        page: page.name,
        url: page.url,
        ...metrics,
        budgetViolations: checkBudgetViolations(metrics)
      });

      console.log(`  ✅ Performance Score: ${performanceScore.toFixed(1)}/100`);
      console.log(`  📈 FCP: ${metrics.firstContentfulPaint.toFixed(0)}ms`);
      console.log(`  📈 LCP: ${metrics.largestContentfulPaint.toFixed(0)}ms`);
      console.log(`  📈 CLS: ${metrics.cumulativeLayoutShift.toFixed(3)}`);
      console.log(`  📈 TBT: ${metrics.totalBlockingTime.toFixed(0)}ms`);
      console.log(`  📈 SI: ${metrics.speedIndex.toFixed(0)}ms\n`);

    } catch (error) {
      console.error(`❌ Error testing ${page.name}:`, error.message);
      results.push({
        page: page.name,
        url: page.url,
        error: error.message
      });
    }
  }

  // Generate summary report
  const summaryReport = generateSummaryReport(results);
  const summaryPath = path.join(reportDir, 'performance-summary.json');
  fs.writeFileSync(summaryPath, JSON.stringify(summaryReport, null, 2));

  console.log('📋 Performance Test Summary:');
  console.log('================================');
  
  let allPassed = true;
  results.forEach(result => {
    if (result.error) {
      console.log(`❌ ${result.page}: ERROR - ${result.error}`);
      allPassed = false;
    } else {
      const status = result.budgetViolations.length === 0 ? '✅' : '⚠️';
      console.log(`${status} ${result.page}: ${result.performanceScore.toFixed(1)}/100`);
      
      if (result.budgetViolations.length > 0) {
        result.budgetViolations.forEach(violation => {
          console.log(`   🚨 ${violation}`);
        });
        allPassed = false;
      }
    }
  });

  console.log(`\n📊 Reports saved to: ${reportDir}`);
  
  if (allPassed) {
    console.log('\n🎉 All performance tests passed!');
    process.exit(0);
  } else {
    console.log('\n⚠️  Some performance tests failed or have budget violations.');
    process.exit(1);
  }
}

function checkBudgetViolations(metrics) {
  const violations = [];
  
  Object.entries(PERFORMANCE_BUDGET).forEach(([metric, budget]) => {
    const actualValue = metrics[toCamelCase(metric)];
    if (actualValue > budget) {
      violations.push(`${metric}: ${actualValue.toFixed(0)} > ${budget} (budget)`);
    }
  });
  
  return violations;
}

function toCamelCase(str) {
  return str.replace(/-([a-z])/g, (g) => g[1].toUpperCase());
}

function generateSummaryReport(results) {
  const validResults = results.filter(r => !r.error);
  
  if (validResults.length === 0) {
    return { error: 'No valid results to summarize' };
  }

  const averageScore = validResults.reduce((sum, r) => sum + r.performanceScore, 0) / validResults.length;
  const totalViolations = validResults.reduce((sum, r) => sum + r.budgetViolations.length, 0);
  
  return {
    timestamp: new Date().toISOString(),
    totalPages: results.length,
    successfulTests: validResults.length,
    failedTests: results.length - validResults.length,
    averagePerformanceScore: averageScore,
    totalBudgetViolations: totalViolations,
    results: results,
    recommendations: generateRecommendations(validResults)
  };
}

function generateRecommendations(results) {
  const recommendations = [];
  
  // Check for common performance issues
  const avgFCP = results.reduce((sum, r) => sum + r.firstContentfulPaint, 0) / results.length;
  const avgLCP = results.reduce((sum, r) => sum + r.largestContentfulPaint, 0) / results.length;
  const avgCLS = results.reduce((sum, r) => sum + r.cumulativeLayoutShift, 0) / results.length;
  const avgTBT = results.reduce((sum, r) => sum + r.totalBlockingTime, 0) / results.length;
  
  if (avgFCP > PERFORMANCE_BUDGET['first-contentful-paint']) {
    recommendations.push('Optimize First Contentful Paint: Consider reducing server response times, optimizing CSS delivery, and removing render-blocking resources.');
  }
  
  if (avgLCP > PERFORMANCE_BUDGET['largest-contentful-paint']) {
    recommendations.push('Optimize Largest Contentful Paint: Optimize images, preload key resources, and improve server response times.');
  }
  
  if (avgCLS > PERFORMANCE_BUDGET['cumulative-layout-shift']) {
    recommendations.push('Reduce Cumulative Layout Shift: Set explicit dimensions for images and videos, avoid inserting content above existing content.');
  }
  
  if (avgTBT > PERFORMANCE_BUDGET['total-blocking-time']) {
    recommendations.push('Reduce Total Blocking Time: Break up long tasks, optimize third-party code, and use web workers for heavy computations.');
  }
  
  return recommendations;
}

// Run the performance test
if (require.main === module) {
  testPerformance().catch(console.error);
}

module.exports = { testPerformance, runLighthouse };
