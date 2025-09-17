# Contributing to 3-in-1 Portfolio Platform

Thank you for your interest in contributing to the 3-in-1 Portfolio Platform! This guide will help you get started with contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [AI Agent Development](#ai-agent-development)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

### Our Pledge

- **Be Respectful**: Treat everyone with respect and kindness
- **Be Inclusive**: Welcome contributors from all backgrounds
- **Be Collaborative**: Work together towards common goals
- **Be Constructive**: Provide helpful feedback and suggestions

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Python 3.8+** installed
- **Node.js 14+** for frontend development
- **Git** for version control
- **Docker** (optional, for containerized development)
- Basic knowledge of **Flask**, **JavaScript**, and **AI/ML concepts**

### Development Setup

1. **Fork the Repository**
```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/your-username/3in1-portfolio-webdev-aiservices.git
cd 3in1-portfolio-webdev-aiservices
```

2. **Set Up Development Environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copy environment file
cp .env.example .env
# Edit .env with your local configuration
```

3. **Initialize Database**
```bash
python manage.py db init
python manage.py db migrate -m "Initial migration"
python manage.py db upgrade
```

4. **Run Tests**
```bash
python tests/run_tests.py all
```

5. **Start Development Server**
```bash
python manage.py run --debug
```

### Development with Docker

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Run tests in container
docker-compose exec app python tests/run_tests.py all

# View logs
docker-compose logs -f app
```

## Development Workflow

### Branch Strategy

We use **Git Flow** with the following branch structure:

- **`main`**: Production-ready code
- **`develop`**: Integration branch for features
- **`feature/*`**: New features and enhancements
- **`bugfix/*`**: Bug fixes
- **`hotfix/*`**: Emergency fixes for production
- **`agent/*`**: New AI agent development

### Workflow Steps

1. **Create Feature Branch**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

2. **Make Changes**
```bash
# Make your changes
git add .
git commit -m "feat: add new feature description"
```

3. **Keep Branch Updated**
```bash
git checkout develop
git pull origin develop
git checkout feature/your-feature-name
git rebase develop
```

4. **Push and Create PR**
```bash
git push origin feature/your-feature-name
# Create Pull Request on GitHub
```

### Commit Message Convention

We follow **Conventional Commits** specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Code formatting changes
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests
- `chore`: Changes to build process or auxiliary tools

**Examples:**
```bash
feat(ai): add new data scientist agent
fix(payments): resolve stripe webhook validation issue
docs(api): update authentication endpoint documentation
test(webdev): add unit tests for pricing calculator
```

## Coding Standards

### Python Code Style

Follow **PEP 8** guidelines with these specific requirements:

```python
# Use type hints
def calculate_price(service: str, features: List[str]) -> float:
    """Calculate service pricing based on features."""
    pass

# Use docstrings for all functions and classes
class PaymentProcessor:
    """Handles payment processing for various gateways."""
    
    def process_payment(self, amount: float, method: str) -> dict:
        """
        Process a payment transaction.
        
        Args:
            amount: Payment amount in USD
            method: Payment method ('stripe' or 'paypal')
            
        Returns:
            dict: Transaction result with status and details
        """
        pass

# Use descriptive variable names
user_subscription = get_user_subscription(user_id)
payment_result = process_stripe_payment(amount, payment_method)
```

### JavaScript Code Style

Use **ES6+** features and follow these conventions:

```javascript
// Use const/let instead of var
const apiEndpoint = '/api/ai/chat';
let sessionId = null;

// Use arrow functions for callbacks
const sendMessage = async (message, agent) => {
    try {
        const response = await fetch(apiEndpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, agent })
        });
        return await response.json();
    } catch (error) {
        console.error('Failed to send message:', error);
        throw error;
    }
};

// Use descriptive function names
const updateChatInterface = (message, isAgent = false) => {
    // Implementation
};
```

### Code Organization

```
app/
├── routes/           # URL route handlers
├── services/         # Business logic layer
├── models/           # Database models
├── templates/        # HTML templates
└── static/
    ├── css/          # Stylesheets
    ├── js/           # JavaScript modules
    └── img/          # Images

agents/
└── agent_name/
    ├── config.yaml   # Agent configuration
    ├── services/     # Agent logic
    ├── tests/        # Agent tests
    └── static/       # Agent assets
```

## Testing Guidelines

### Writing Tests

All new features must include comprehensive tests:

```python
# Unit test example
import pytest
from app.services.payments import PaymentProcessor

class TestPaymentProcessor:
    def setup_method(self):
        self.processor = PaymentProcessor()
    
    def test_calculate_price_basic_service(self):
        """Test basic service pricing calculation."""
        price = self.processor.calculate_price(
            service_type='website',
            pages=5,
            features=['seo', 'cms']
        )
        assert price == 2300.0
    
    def test_calculate_price_invalid_service(self):
        """Test error handling for invalid service type."""
        with pytest.raises(ValueError):
            self.processor.calculate_price('invalid_service')
```

### Test Categories

1. **Unit Tests** (`tests/test_*.py`)
   - Test individual functions and classes
   - Mock external dependencies
   - Fast execution (< 1 second per test)

2. **Integration Tests** (`tests/integration/`)
   - Test component interactions
   - Use test database
   - Test API endpoints

3. **AI Agent Tests** (`agents/*/tests/`)
   - Test agent responses
   - Test agent routing
   - Mock AI model calls

### Running Tests

```bash
# Run all tests
python tests/run_tests.py all

# Run specific test category
python tests/run_tests.py pattern=webdev

# Run tests with coverage
python tests/run_tests.py coverage

# Run tests for specific agent
python -m pytest agents/developer/tests/ -v
```

### Test Quality Standards

- **Coverage**: Maintain >90% code coverage
- **Assertions**: Use descriptive assertion messages
- **Mocking**: Mock external services and APIs
- **Data**: Use fixtures for test data
- **Performance**: Tests should run quickly

## AI Agent Development

### Creating a New Agent

1. **Generate Agent Structure**
```bash
python scripts/generate_agent.py --name "your_agent" --type "professional"
```

2. **Configure Agent**
```yaml
# agents/your_agent/config.yaml
name: "Your Agent"
description: "Agent description and purpose"
personality: "Professional, helpful, knowledgeable"
specialties:
  - "Domain expertise 1"
  - "Domain expertise 2"
pricing:
  basic: 0
  pro: 29.99
  enterprise: 99.99
```

3. **Implement Agent Logic**
```python
# agents/your_agent/services/agent.py
from agents.base_agent import BaseAgent

class YourAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="your_agent")
    
    async def process_query(self, query: str, context: dict = None) -> dict:
        """Process user query and return response."""
        # Implement agent logic
        response = await self.generate_response(query, context)
        
        return {
            'response': response,
            'agent': self.name,
            'confidence': self.calculate_confidence(query),
            'follow_up_questions': self.generate_follow_ups(query)
        }
```

4. **Create Agent Tests**
```python
# agents/your_agent/tests/test_agent.py
import pytest
from agents.your_agent.services.agent import YourAgent

class TestYourAgent:
    def setup_method(self):
        self.agent = YourAgent()
    
    @pytest.mark.asyncio
    async def test_process_query(self):
        """Test basic query processing."""
        response = await self.agent.process_query("test query")
        
        assert response['response'] is not None
        assert response['agent'] == 'your_agent'
        assert 0 <= response['confidence'] <= 1
```

### Agent Development Guidelines

**Agent Personality:**
- Consistent personality traits
- Appropriate response tone
- Unique characteristics that differentiate from other agents

**Response Quality:**
- Relevant and helpful responses
- Context-aware interactions
- Error handling for edge cases

**Performance:**
- Response time < 5 seconds
- Efficient memory usage
- Proper resource cleanup

### Agent Integration

```python
# app/ai/agent_registry.py
from agents.your_agent.services.agent import YourAgent

AVAILABLE_AGENTS = {
    'your_agent': {
        'class': YourAgent,
        'name': 'Your Agent',
        'description': 'Agent description',
        'status': 'active'
    }
}
```

## Documentation

### Documentation Standards

**Code Documentation:**
- Use docstrings for all public functions/classes
- Include parameter types and return types
- Provide usage examples

**API Documentation:**
- Update `docs/API.md` for new endpoints
- Include request/response examples
- Document error codes and responses

**User Documentation:**
- Update README.md for new features
- Create guides for complex features
- Include screenshots where helpful

### Documentation Tools

```bash
# Generate API documentation
python scripts/generate_api_docs.py

# Build documentation site
mkdocs build

# Serve documentation locally
mkdocs serve
```

## Submitting Changes

### Pull Request Process

1. **Pre-submission Checklist**
   - [ ] Code follows style guidelines
   - [ ] Tests pass (`python tests/run_tests.py all`)
   - [ ] Documentation is updated
   - [ ] Commit messages follow convention
   - [ ] No merge conflicts with develop branch

2. **Pull Request Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

3. **Review Process**
   - Automated CI/CD checks must pass
   - At least one maintainer review required
   - Address all review comments
   - Keep PR focused and atomic

### Code Review Guidelines

**For Reviewers:**
- Review code for logic, style, and performance
- Test the changes locally
- Provide constructive feedback
- Approve when standards are met

**For Contributors:**
- Respond to review comments promptly
- Make requested changes
- Ask questions if unclear
- Thank reviewers for their time

## Release Process

### Version Numbering

We use **Semantic Versioning** (SemVer):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Workflow

1. **Prepare Release**
```bash
# Update version
echo "1.2.0" > VERSION

# Update CHANGELOG.md
git add CHANGELOG.md VERSION
git commit -m "chore: prepare release v1.2.0"
```

2. **Create Release Branch**
```bash
git checkout -b release/v1.2.0
git push origin release/v1.2.0
```

3. **Testing and QA**
```bash
# Run full test suite
python tests/run_tests.py all

# Performance testing
python tests/run_tests.py performance

# Security testing
python tests/run_tests.py security
```

4. **Merge and Tag**
```bash
# Merge to main
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags

# Merge to develop
git checkout develop
git merge --no-ff release/v1.2.0
git push origin develop
```

### Deployment

Production deployments are handled through CI/CD pipelines triggered by tags on the main branch.

## Community Guidelines

### Getting Help

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and community support
- **Discord**: Real-time community chat
- **Email**: Direct contact for sensitive issues

### Recognition

Contributors are recognized in several ways:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Special recognition for significant contributions

### Issue Triage

**Bug Reports:**
1. Reproduce the issue
2. Label appropriately (bug, critical, etc.)
3. Assign to appropriate maintainer
4. Provide guidance to contributor if needed

**Feature Requests:**
1. Evaluate feasibility and scope
2. Discuss with maintainers
3. Label as enhancement
4. Provide implementation guidance

## Development Resources

### Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [AI/ML Integration Patterns](https://docs.python.org/3/library/asyncio.html)
- [Payment Gateway Integration](https://stripe.com/docs)
- [WebSocket Development](https://flask-socketio.readthedocs.io/)

### Tools and Utilities

```bash
# Code formatting
black app/ agents/ tests/

# Linting
flake8 app/ agents/ tests/

# Type checking
mypy app/

# Security scanning
bandit -r app/
```

### Debugging

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use Flask debug toolbar
from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)

# Profile performance
from flask_profiler import Profiler
Profiler(app)
```

Thank you for contributing to the 3-in-1 Portfolio Platform! Your contributions help make this project better for everyone.

## Questions?

If you have questions about contributing, please:
1. Check existing documentation
2. Search GitHub issues
3. Start a discussion
4. Contact maintainers

We're here to help and welcome all contributions! 🚀