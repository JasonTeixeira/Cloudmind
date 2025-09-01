#!/usr/bin/env node

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

class FrontendTestRunner {
  constructor() {
    this.results = {
      timestamp: new Date().toISOString(),
      tests: {},
      summary: {
        total: 0,
        passed: 0,
        failed: 0,
        skipped: 0
      }
    };
    
    this.testSuites = [
      {
        name: 'Unit Tests',
        command: 'npm',
        args: ['run', 'test:unit', '--', '--coverage', '--watchAll=false'],
        timeout: 120000,
        required: true
      },
      {
        name: 'Integration Tests',
        command: 'npm',
        args: ['run', 'test:integration', '--', '--watchAll=false'],
        timeout: 180000,
        required: true
      },
      {
        name: 'Accessibility Tests',
        command: 'npm',
        args: ['run', 'test:accessibility', '--', '--watchAll=false'],
        timeout: 120000,
        required: true
      },
      {
        name: 'Type Checking',
        command: 'npm',
        args: ['run', 'type-check'],
        timeout: 60000,
        required: true
      },
      {
        name: 'Linting',
        command: 'npm',
        args: ['run', 'lint'],
        timeout: 60000,
        required: true
      },
      {
        name: 'E2E Tests',
        command: 'npm',
        args: ['run', 'test:e2e'],
        timeout: 600000,
        required: false,
        setup: this.setupE2E.bind(this)
      },
      {
        name: 'Visual Regression Tests',
        command: 'npm',
        args: ['run', 'test:visual'],
        timeout: 300000,
        required: false,
        setup: this.setupVisual.bind(this)
      },
      {
        name: 'Performance Tests',
        command: 'node',
        args: ['scripts/performance-test.js'],
        timeout: 300000,
        required: false,
        setup: this.setupPerformance.bind(this)
      },
      {
        name: 'Load Tests',
        command: 'k6',
        args: ['run', 'tests/load/frontend-load-test.js'],
        timeout: 300000,
        required: false,
        setup: this.setupLoadTests.bind(this)
      }
    ];
  }

  async run() {
    console.log('🚀 Starting comprehensive frontend testing suite...\n');
    console.log(`📅 Started at: ${this.results.timestamp}\n`);

    // Create results directory
    const resultsDir = path.join(__dirname, '..', 'test-results');
    if (!fs.existsSync(resultsDir)) {
      fs.mkdirSync(resultsDir, { recursive: true });
    }

    let allPassed = true;

    for (const suite of this.testSuites) {
      console.log(`🧪 Running ${suite.name}...`);
      
      try {
        // Run setup if provided
        if (suite.setup) {
          console.log(`⚙️  Setting up ${suite.name}...`);
          await suite.setup();
        }

        const result = await this.runTestSuite(suite);
        this.results.tests[suite.name] = result;
        
        if (result.success) {
          console.log(`✅ ${suite.name}: PASSED`);
          this.results.summary.passed++;
        } else {
          console.log(`❌ ${suite.name}: FAILED`);
          console.log(`   Error: ${result.error}`);
          this.results.summary.failed++;
          
          if (suite.required) {
            allPassed = false;
          }
        }
        
        this.results.summary.total++;
        
      } catch (error) {
        console.log(`💥 ${suite.name}: ERROR`);
        console.log(`   ${error.message}`);
        
        this.results.tests[suite.name] = {
          success: false,
          error: error.message,
          duration: 0
        };
        
        this.results.summary.failed++;
        this.results.summary.total++;
        
        if (suite.required) {
          allPassed = false;
        }
      }
      
      console.log(''); // Empty line for readability
    }

    // Generate final report
    await this.generateReport(resultsDir);
    
    // Print summary
    this.printSummary();
    
    // Exit with appropriate code
    process.exit(allPassed ? 0 : 1);
  }

  async runTestSuite(suite) {
    return new Promise((resolve) => {
      const startTime = Date.now();
      let output = '';
      let errorOutput = '';

      const child = spawn(suite.command, suite.args, {
        stdio: ['pipe', 'pipe', 'pipe'],
        shell: true
      });

      child.stdout.on('data', (data) => {
        output += data.toString();
      });

      child.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      child.on('close', (code) => {
        const duration = Date.now() - startTime;
        
        resolve({
          success: code === 0,
          exitCode: code,
          duration,
          output,
          error: code !== 0 ? errorOutput || `Process exited with code ${code}` : null
        });
      });

      child.on('error', (error) => {
        const duration = Date.now() - startTime;
        
        resolve({
          success: false,
          duration,
          error: error.message,
          output,
          errorOutput
        });
      });

      // Set timeout
      setTimeout(() => {
        child.kill('SIGTERM');
        resolve({
          success: false,
          duration: suite.timeout,
          error: `Test suite timed out after ${suite.timeout}ms`,
          output,
          errorOutput
        });
      }, suite.timeout);
    });
  }

  async setupE2E() {
    // Check if Cypress is installed
    try {
      await this.runCommand('npx', ['cypress', 'verify']);
    } catch (error) {
      throw new Error('Cypress not properly installed. Run: npm run cypress:install');
    }
  }

  async setupVisual() {
    // Check if Playwright is installed
    try {
      await this.runCommand('npx', ['playwright', 'install', '--with-deps']);
    } catch (error) {
      console.log('Installing Playwright browsers...');
      // Continue anyway, as this might be the first run
    }
  }

  async setupPerformance() {
    // Check if Lighthouse is available
    try {
      await this.runCommand('npx', ['lighthouse', '--version']);
    } catch (error) {
      throw new Error('Lighthouse not available. Install with: npm install -g lighthouse');
    }
  }

  async setupLoadTests() {
    // Check if k6 is available
    try {
      await this.runCommand('k6', ['version']);
    } catch (error) {
      throw new Error('k6 not available. Install from: https://k6.io/docs/getting-started/installation/');
    }
  }

  async runCommand(command, args) {
    return new Promise((resolve, reject) => {
      const child = spawn(command, args, { stdio: 'pipe' });
      
      child.on('close', (code) => {
        if (code === 0) {
          resolve();
        } else {
          reject(new Error(`Command failed with exit code ${code}`));
        }
      });

      child.on('error', reject);
    });
  }

  async generateReport(resultsDir) {
    const reportPath = path.join(resultsDir, 'comprehensive-test-report.json');
    fs.writeFileSync(reportPath, JSON.stringify(this.results, null, 2));

    // Generate HTML report
    const htmlReport = this.generateHTMLReport();
    const htmlPath = path.join(resultsDir, 'comprehensive-test-report.html');
    fs.writeFileSync(htmlPath, htmlReport);

    console.log(`📊 Test reports saved to:`);
    console.log(`   JSON: ${reportPath}`);
    console.log(`   HTML: ${htmlPath}\n`);
  }

  generateHTMLReport() {
    const { summary, tests } = this.results;
    const passRate = ((summary.passed / summary.total) * 100).toFixed(1);
    
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudMind Frontend Test Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #0a0a0f; color: #00f5ff; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 40px; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px; }
        .summary-card { background: #1a1a2e; border: 1px solid #00f5ff; border-radius: 8px; padding: 20px; text-align: center; }
        .summary-number { font-size: 2em; font-weight: bold; margin-bottom: 10px; }
        .test-results { display: grid; gap: 20px; }
        .test-result { background: #1a1a2e; border: 1px solid #333; border-radius: 8px; padding: 20px; }
        .test-result.passed { border-color: #00ff88; }
        .test-result.failed { border-color: #ff0080; }
        .test-name { font-size: 1.2em; font-weight: bold; margin-bottom: 10px; }
        .test-details { font-family: monospace; font-size: 0.9em; }
        .status { padding: 4px 8px; border-radius: 4px; font-weight: bold; }
        .status.passed { background: #00ff88; color: #000; }
        .status.failed { background: #ff0080; color: #fff; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 CloudMind Frontend Test Report</h1>
            <p>Generated: ${this.results.timestamp}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <div class="summary-number">${summary.total}</div>
                <div>Total Tests</div>
            </div>
            <div class="summary-card">
                <div class="summary-number" style="color: #00ff88">${summary.passed}</div>
                <div>Passed</div>
            </div>
            <div class="summary-card">
                <div class="summary-number" style="color: #ff0080">${summary.failed}</div>
                <div>Failed</div>
            </div>
            <div class="summary-card">
                <div class="summary-number">${passRate}%</div>
                <div>Pass Rate</div>
            </div>
        </div>
        
        <div class="test-results">
            ${Object.entries(tests).map(([name, result]) => `
                <div class="test-result ${result.success ? 'passed' : 'failed'}">
                    <div class="test-name">
                        ${name}
                        <span class="status ${result.success ? 'passed' : 'failed'}">
                            ${result.success ? 'PASSED' : 'FAILED'}
                        </span>
                    </div>
                    <div class="test-details">
                        Duration: ${(result.duration / 1000).toFixed(2)}s<br>
                        Exit Code: ${result.exitCode || 'N/A'}<br>
                        ${result.error ? `Error: ${result.error}` : ''}
                    </div>
                </div>
            `).join('')}
        </div>
    </div>
</body>
</html>`;
  }

  printSummary() {
    const { summary } = this.results;
    const passRate = ((summary.passed / summary.total) * 100).toFixed(1);
    
    console.log('📋 Test Summary:');
    console.log('================');
    console.log(`📊 Total Tests: ${summary.total}`);
    console.log(`✅ Passed: ${summary.passed}`);
    console.log(`❌ Failed: ${summary.failed}`);
    console.log(`📈 Pass Rate: ${passRate}%`);
    console.log('');
    
    if (summary.failed === 0) {
      console.log('🎉 All tests passed! Your frontend is ready for production.');
    } else {
      console.log('⚠️  Some tests failed. Please review the results above.');
    }
  }
}

// Run the test suite
if (require.main === module) {
  const runner = new FrontendTestRunner();
  runner.run().catch(console.error);
}

module.exports = FrontendTestRunner;
