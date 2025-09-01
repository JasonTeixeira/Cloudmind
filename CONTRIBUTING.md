# Contributing to CloudMind

Thank you for your interest in contributing to CloudMind! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/cloudmind.git`
3. Install dependencies: `./tools/scripts/setup-dev.sh`
4. Create a feature branch: `git checkout -b feature/amazing-feature`
5. Make your changes
6. Test your changes: `./tools/scripts/test-setup.sh`
7. Commit and push
8. Create a Pull Request

## 🏗️ Development Environment

### Prerequisites

- **Python 3.11+** with pip and venv
- **Node.js 18+** with npm
- **PostgreSQL 16+**
- **Redis 7+**
- **Git**

### Setup

```bash
# Clone the repository
git clone https://github.com/cloudmind/cloudmind.git
cd cloudmind

# Run automated setup
./tools/scripts/setup-dev.sh

# Test the setup
./tools/scripts/test-setup.sh

# Start development servers
./tools/scripts/start-dev.sh
```

## 📝 Code Standards

### Python Backend

- **Code Style**: Black with 100-character line limit
- **Linting**: Ruff with comprehensive rules
- **Type Checking**: MyPy with strict settings
- **Security**: Bandit security scanner
- **Testing**: pytest with coverage reporting

```bash
# Run all checks
cd backend
ruff check app/ tests/
black --check app/ tests/
mypy app/
bandit -r app/
pytest --cov=app
```

### TypeScript Frontend

- **Code Style**: Prettier with ESLint
- **Type Checking**: TypeScript strict mode
- **Testing**: Jest and React Testing Library
- **E2E Testing**: Playwright

```bash
# Run all checks
cd frontend
npm run lint
npm run type-check
npm test
npm run test:e2e
```

## 🧪 Testing

### Backend Testing

```bash
cd backend
source venv/bin/activate

# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# All tests with coverage
pytest --cov=app --cov-report=html
```

### Frontend Testing

```bash
cd frontend

# Unit tests
npm test

# E2E tests
npm run test:e2e

# Visual regression tests
npm run test:visual
```

## 📋 Pull Request Process

### Before Submitting

1. **Run all tests**: Ensure all tests pass locally
2. **Code quality**: Run linters and formatters
3. **Documentation**: Update relevant documentation
4. **Changelog**: Add entry to CHANGELOG.md if applicable

### PR Requirements

- **Descriptive title**: Clearly describe what the PR does
- **Detailed description**: Explain the changes and motivation
- **Issue linking**: Reference related issues using keywords
- **Screenshots**: Include for UI changes
- **Breaking changes**: Clearly mark and explain any breaking changes

### Review Process

1. **Automated checks**: All CI/CD checks must pass
2. **Code review**: At least one maintainer approval required
3. **Testing**: Changes are tested in staging environment
4. **Documentation**: Ensure documentation is updated

## 🎯 Contribution Areas

### High Priority

- **Performance optimizations**
- **Security improvements**
- **Bug fixes**
- **Documentation improvements**
- **Test coverage expansion**

### Feature Development

- **AI/ML enhancements**
- **New cloud provider integrations**
- **Visualization improvements**
- **API endpoints**
- **Dashboard features**

### Infrastructure

- **Docker optimizations**
- **Kubernetes manifests**
- **CI/CD improvements**
- **Monitoring and logging**
- **Security hardening**

## 🔧 Development Workflows

### Backend Development

```bash
# Start backend only
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Database migrations
alembic revision --autogenerate -m "Description"
alembic upgrade head

# Add new dependencies
echo "new-package==1.0.0" >> requirements/base.txt
pip install -r requirements/dev.txt
```

### Frontend Development

```bash
# Start frontend only
cd frontend
npm run dev

# Add new dependencies
npm install package-name
npm install -D dev-package-name

# Generate components
npx create-component ComponentName
```

### Full Stack Development

```bash
# Start all services
./tools/scripts/start-dev.sh

# View logs
tail -f logs/backend.log
tail -f logs/frontend.log

# Stop all services
Ctrl+C (in start-dev.sh terminal)
```

## 🐛 Bug Reports

### Before Reporting

1. **Search existing issues**: Check if the bug is already reported
2. **Reproduce consistently**: Ensure the bug is reproducible
3. **Test latest version**: Verify the bug exists in the latest code

### Bug Report Template

```markdown
**Bug Description**
A clear description of what the bug is.

**Steps to Reproduce**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g., macOS 14.0]
- Browser: [e.g., Chrome 91]
- CloudMind Version: [e.g., 1.0.0]

**Additional Context**
Any other context about the problem.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
A clear description of the proposed feature.

**Problem Statement**
What problem does this feature solve?

**Proposed Solution**
Describe your preferred solution.

**Alternatives Considered**
Other solutions you've considered.

**Additional Context**
Screenshots, mockups, or examples.
```

## 📚 Documentation

### Types of Documentation

- **API Documentation**: OpenAPI/Swagger specs
- **User Guides**: How-to guides for end users
- **Developer Docs**: Technical documentation for contributors
- **Architecture Docs**: System design and architecture

### Documentation Standards

- **Clear and concise**: Write for your audience
- **Up-to-date**: Keep documentation current with code changes
- **Examples**: Include practical examples
- **Searchable**: Use clear headings and structure

## 🏆 Recognition

Contributors will be recognized in:

- **CONTRIBUTORS.md**: List of all contributors
- **Release notes**: Major contributors mentioned in releases
- **Hall of Fame**: Outstanding contributors featured prominently

## 📞 Getting Help

- **Discord**: Join our [Discord server](https://discord.gg/cloudmind)
- **GitHub Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers at dev@cloudmind.local

## 📄 License

By contributing to CloudMind, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to CloudMind! 🚀