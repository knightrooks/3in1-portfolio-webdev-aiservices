# 🏗️ Flask 3-in-1 Platform: Portfolio + Web Development + AI Services

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![Flask Version](https://img.shields.io/badge/flask-2.3%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#testing)

## 📋 Project Overview

A **production-ready Flask-based 3-in-1 platform** that seamlessly combines:

1. **💼 Portfolio Section** - Professional showcase with dynamic content management
2. **🌐 Web Development Services** - Commercial service hub with integrated payment processing
3. **🤖 AI Services** - Multi-agent AI ecosystem with 16 specialized personalities

Perfect for developers, freelancers, and agencies looking to showcase work, offer services, and provide AI-powered solutions all in one unified platform.

---

## 🌟 Key Features

---

## 📂 Project Architecture

```
3in1-portfolio-webdev-aiservices/
│
├── 📱 Core Application
│   ├── manage.py                     # Flask CLI entrypoint
│   ├── config.py                     # Environment configuration
│   ├── requirements.txt              # Python dependencies
│   │
│   └── app/                          # Main Flask application
│       ├── __init__.py               # App factory pattern
│       ├── routes/                   # URL routing modules
│       │   ├── home.py               # Landing page routes
│       │   ├── portfolio.py          # Portfolio section
│       │   ├── webdev.py             # Web dev services
│       │   └── ai_services.py        # AI services hub
│       │
│       ├── services/                 # Business logic layer
│       │   ├── payments.py           # Stripe/PayPal integration
│       │   ├── email.py              # Email automation
│       │   └── analytics.py          # Usage tracking
│       │
│       ├── templates/                # Jinja2 HTML templates
│       │   ├── base.html             # Common layout
│       │   ├── portfolio/            # Portfolio pages
│       │   ├── webdev/               # Service pages
│       │   └── ai/                   # AI interface pages
│       │
│       └── static/                   # CSS, JS, images
│           ├── css/                  # Stylesheets
│           │   ├── style.css         # Main styles
│           │   ├── ai.css            # AI interface styles
│           │   └── chat.css          # Chat UI styles
│           ├── js/                   # JavaScript modules
│           │   ├── chat.js           # Chat functionality
│           │   ├── payments.js       # Payment processing
│           │   └── main.js           # Core interactions
│           └── img/                  # Images and avatars
│
├── 🤖 AI Agent Ecosystem
│   └── agents/                       # Individual AI agents
│       ├── developer/                # Software development expert
│       ├── data_scientist/           # Data analysis specialist
│       ├── content_creator/          # Content generation
│       ├── marketing_specialist/     # Marketing strategies
│       ├── coderbot/                 # Advanced coding assistant
│       ├── emotionaljenny/           # Emotional support
│       ├── gossipqueen/              # Casual conversation
│       ├── strictwife/               # Productivity coach
│       ├── lazyjohn/                 # Relaxed advisor
│       └── girlfriend/               # Relationship support
│
├── 🧪 Testing Infrastructure
│   └── tests/                        # Comprehensive test suite
│       ├── conftest.py               # Test configuration
│       ├── test_*.py                 # Unit tests
│       ├── integration/              # Integration tests
│       └── run_tests.py              # Test runner script
│
├── 📊 Data & Analytics
│   └── data/                         # Application data
│       ├── inquiries.json            # Contact inquiries
│       ├── quotes.json               # Service quotes
│       └── analytics/                # Usage metrics
│
├── 🐳 Deployment
│   ├── Dockerfile                    # Container configuration
│   ├── docker-compose.yml            # Multi-service setup
│   └── scripts/                      # Automation scripts
│
└── 📚 Documentation
    ├── README.md                     # This file
    ├── API.md                        # API documentation
    ├── DEPLOYMENT.md                 # Deployment guide
    └── CONTRIBUTING.md               # Development guidelines
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 14+** (for frontend dependencies)
- **Redis** (for session management)
- **PostgreSQL/SQLite** (database)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/3in1-portfolio-webdev-aiservices.git
cd 3in1-portfolio-webdev-aiservices
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

6. **Run the application**
```bash
python manage.py run
```

Visit `http://localhost:3000` to access the platform.

### Docker Setup

```bash
# Quick start with Docker
docker-compose up -d

# Access the application
open http://localhost:3000
```

---

## 💻 Usage Guide

### Portfolio Section
- **Showcase Projects**: Display your work with detailed case studies
- **Skills Matrix**: Highlight technical competencies
- **About Page**: Personal/professional narrative
- **Contact Form**: Direct client inquiries

### Web Development Services
- **Service Catalog**: Browse available development services
- **Pricing Calculator**: Get instant quotes for projects
- **Quote System**: Request detailed proposals
- **Payment Processing**: Secure online payments

### AI Services
- **Agent Selection**: Choose from 16 specialized AI personalities
- **Real-time Chat**: Interactive conversations with agents
- **Session Management**: Maintain conversation history
- **Subscription Plans**: Flexible access tiers

---

## 🔧 Configuration

### Environment Variables

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:pass@localhost/dbname
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Payment Gateways
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-secret

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# AI Services
OPENAI_API_KEY=sk-...
OLLAMA_HOST=http://localhost:11434

# Redis (Session Management)
REDIS_URL=redis://localhost:6379/0
```

### Payment Integration

The platform supports both Stripe and PayPal for payment processing:

**Stripe Setup:**
1. Create a Stripe account
2. Get API keys from dashboard
3. Configure webhooks for subscription management

**PayPal Setup:**
1. Create PayPal Developer account
2. Create application for API credentials
3. Configure IPN/webhooks for payment notifications
- **CSRF Protection** on all forms
- **Input Sanitization** and validation
- **Session Management** with secure cookies
- **Rate Limiting** on API endpoints
- **GDPR Compliance** ready with privacy controls

---

## 📂 Complete Project Structure

```
3in1-portfolio-webdev-aiservices/
│
├── manage.py                         # Flask CLI entrypoint
├── config.py                         # Global configs (env vars, db, cache)
├── requirements.txt                  # Python dependencies
├── Dockerfile                        # Build instructions
├── docker-compose.yml                # Services orchestration (db, redis, ollama)
├── README.md                         # This file
│
├── app/                              # Core Application
│   ├── __init__.py                   # Flask app factory
│   ├── extensions.py                 # DB, JWT, Redis, Sockets init
│   ├── middleware.py                 # Logging, error handlers
│   │
│   ├── routes/                       # Blueprints → Each module standalone
│   │   ├── __init__.py
│   │   ├── home.py                   # Landing page & Hero logic
│   │   ├── portfolio.py              # Portfolio section routes
│   │   ├── webdev.py                 # Web development section routes
│   │   ├── ai_services.py            # AI Services section routes
│   │   ├── legal.py                  # Terms, Privacy, Payments routes
│   │   └── contact.py                # Contact & Support routes
│   │
│   ├── templates/                    # Jinja2 templates
│   │   ├── base.html                 # Common navbar/footer
│   │   ├── home.html                 # Landing page
│   │   │
│   │   ├── portfolio/                # Portfolio module pages
│   │   │   ├── index.html            # Portfolio home
│   │   │   ├── about.html            # About me page
│   │   │   ├── projects.html         # Projects showcase
│   │   │   ├── project_detail.html   # Individual project details
│   │   │   ├── testimonials.html     # Client testimonials
│   │   │   └── contact.html          # Portfolio contact form
│   │   │
│   │   ├── webdev/                   # Web Development module
│   │   │   ├── index.html            # Web dev services home
│   │   │   ├── websites.html         # Website development
│   │   │   ├── apps.html             # App development
│   │   │   ├── ecommerce.html        # E-commerce solutions
│   │   │   ├── marketing.html        # Digital marketing
│   │   │   ├── seo.html              # SEO services
│   │   │   ├── maintenance.html      # Website maintenance
│   │   │   └── pricing.html          # Service pricing
│   │   │
│   │   ├── ai_services/              # AI Services module
│   │   │   ├── index.html            # AI services home
│   │   │   ├── showcase.html         # AI capabilities showcase
│   │   │   ├── agents.html           # List of available agents
│   │   │   ├── agent_profile.html    # Single agent profile view
│   │   │   ├── chat.html             # Universal chat interface
│   │   │   └── pricing.html          # AI service pricing
│   │   │
│   │   ├── legal/                    # Legal module
│   │   │   ├── terms.html            # Terms of service
│   │   │   ├── privacy.html          # Privacy policy
│   │   │   ├── cookies.html          # Cookie policy
│   │   │   └── payments.html         # Payment policy
│   │   │
│   │   └── contact/                  # Contact / Helpdesk
│   │       ├── support.html          # Customer support
│   │       ├── faq.html              # Frequently asked questions
│   │       └── feedback.html         # User feedback form
│   │
│   ├── static/                       # Static files
│   │   ├── css/
│   │   │   ├── style.css             # Main stylesheet
│   │   │   ├── portfolio.css         # Portfolio specific styles
│   │   │   ├── webdev.css            # Web dev specific styles
│   │   │   └── ai.css                # AI services specific styles
│   │   ├── js/
│   │   │   ├── app.js                # Main application JavaScript
│   │   │   ├── chat.js               # Chat interface logic
│   │   │   ├── portfolio.js          # Portfolio interactions
│   │   │   └── payments.js           # Payment processing
│   │   └── img/
│   │       ├── logo.png              # Site logo
│   │       ├── hero-bg.jpg           # Hero section background
│   │       ├── portfolio/            # Portfolio images
│   │       │   ├── project1.jpg
│   │       │   ├── project2.jpg
│   │       │   └── testimonial-bg.jpg
│   │       └── avatars/              # Agent avatars
│   │           ├── lazyjohn.png
│   │           ├── chatterboxchloe.png
│   │           ├── emojenny.png
│   │           ├── professorlogic.png
│   │           ├── coderpete.png
│   │           ├── mrsbossy.png
│   │           ├── detectivemindy.png
│   │           ├── dreamermax.png
│   │           ├── flirtykate.png
│   │           └── roastbotrex.png
│   │
│   ├── services/                     # Backend Services
│   │   ├── __init__.py
│   │   ├── db.py                     # Database models & operations
│   │   ├── auth.py                   # Authentication (JWT, roles)
│   │   ├── payments.py               # Payment processing (Stripe/PayPal)
│   │   ├── notifications.py          # Email, SMS, push notifications
│   │   └── utils.py                  # Helper functions
│   │
│   └── ai/                           # AI Orchestration Layer
│       ├── __init__.py
│       ├── controller.py             # Main orchestration logic
│       ├── planner.py                # Multi-step task planning
│       ├── executor.py               # Task execution with models
│       ├── memory.py                 # Memory & context management
│       └── registry.yaml             # Available agents registry
│
├── agents/                           # Individual AI Agents
│   │
│   ├── strategist/                   # Strategic planning agent
│   │   ├── __init__.py               # Flask blueprint registration
│   │   ├── config.yaml               # Agent configuration
│   │   ├── registry.yaml             # Agent metadata
│   │   ├── persona/
│   │   │   └── strategist.yaml       # Persona definition
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py             # REST endpoints
│   │   │   ├── socket.py             # WebSocket setup
│   │   │   └── events.py             # WebSocket event handlers
│   │   ├── services/
│   │   │   ├── cortex/               # Reasoning & orchestration
│   │   │   │   ├── __init__.py
│   │   │   │   ├── controller.py
│   │   │   │   ├── planner.py
│   │   │   │   ├── executor.py
│   │   │   │   └── hooks.py
│   │   │   ├── brain/                # Memory & cognition
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chroma/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── embedder.py
│   │   │   │   │   ├── vector_store.py
│   │   │   │   │   └── recall.py
│   │   │   │   ├── episodic.py
│   │   │   │   ├── feedback.py
│   │   │   │   └── memory_sync.py
│   │   │   ├── engine/               # ML models & inference
│   │   │   │   ├── __init__.py
│   │   │   │   ├── local_runner.py   # Ollama / Hugging Face
│   │   │   │   ├── api_runner.py     # OpenAI / Claude
│   │   │   │   └── dispatcher.py     # Smart routing logic
│   │   │   ├── feed/                 # External data ingestion
│   │   │   │   ├── __init__.py
│   │   │   │   ├── fetch.py
│   │   │   │   └── preprocess.py
│   │   │   └── auth/                 # Auth & access control
│   │   │       ├── __init__.py
│   │   │       ├── token.py
│   │   │       └── roles.py
│   │   ├── monitor/                  # Performance tracking
│   │   │   ├── __init__.py
│   │   │   ├── latency.py
│   │   │   ├── usage.py
│   │   │   └── alerts.py
│   │   ├── analytics/                # User behavior metrics
│   │   │   ├── __init__.py
│   │   │   ├── logger.py
│   │   │   └── metrics.py
│   │   ├── session/                  # Per-user memory
│   │   │   ├── __init__.py
│   │   │   ├── store.py
│   │   │   └── cleanup.py
│   │   ├── templates/
│   │   │   └── strategist.html       # Agent chat interface
│   │   ├── static/
│   │   │   ├── style.css             # Agent-specific styling
│   │   │   ├── strategist.js         # Agent JavaScript logic
│   │   │   ├── avatar.png            # Agent avatar
│   │   │   └── utils.js              # Helper functions
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_routes.py
│   │   │   ├── test_controller.py
│   │   │   ├── test_memory.py
│   │   │   └── simulator.py
│   │   ├── volumes/                  # Docker mounted models
│   │   │   ├── ollama_models/
│   │   │   └── blenderbot/
│   │   ├── requirements.txt          # Agent-specific dependencies
│   │   ├── Dockerfile               # Agent container build
│   │   └── docker-compose.yml       # Agent services
│   │
│   ├── girlfriend/                   # Emotional support agent
│   │   ├── __init__.py
│   │   ├── config.yaml
│   │   ├── registry.yaml
│   │   ├── persona/
│   │   │   └── girlfriend.yaml
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── socket.py
│   │   │   └── events.py
│   │   ├── services/
│   │   │   ├── cortex/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── controller.py
│   │   │   │   ├── planner.py
│   │   │   │   ├── executor.py
│   │   │   │   └── hooks.py
│   │   │   ├── brain/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chroma/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── embedder.py
│   │   │   │   │   ├── vector_store.py
│   │   │   │   │   └── recall.py
│   │   │   │   ├── episodic.py
│   │   │   │   ├── feedback.py
│   │   │   │   └── memory_sync.py
│   │   │   ├── engine/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── local_runner.py
│   │   │   │   ├── api_runner.py
│   │   │   │   └── dispatcher.py
│   │   │   ├── feed/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── fetch.py
│   │   │   │   └── preprocess.py
│   │   │   └── auth/
│   │   │       ├── __init__.py
│   │   │       ├── token.py
│   │   │       └── roles.py
│   │   ├── monitor/
│   │   │   ├── __init__.py
│   │   │   ├── latency.py
│   │   │   ├── usage.py
│   │   │   └── alerts.py
│   │   ├── analytics/
│   │   │   ├── __init__.py
│   │   │   ├── logger.py
│   │   │   └── metrics.py
│   │   ├── session/
│   │   │   ├── __init__.py
│   │   │   ├── store.py
│   │   │   └── cleanup.py
│   │   ├── templates/
│   │   │   └── girlfriend.html
│   │   ├── static/
│   │   │   ├── style.css
│   │   │   ├── girlfriend.js
│   │   │   ├── avatar.png
│   │   │   └── utils.js
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_routes.py
│   │   │   ├── test_controller.py
│   │   │   ├── test_memory.py
│   │   │   └── simulator.py
│   │   ├── volumes/
│   │   │   ├── ollama_models/
│   │   │   └── blenderbot/
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   │
│   ├── lazyjohn/                     # Lazy personality agent
│   │   ├── __init__.py
│   │   ├── config.yaml
│   │   ├── registry.yaml
│   │   ├── persona/
│   │   │   └── lazyjohn.yaml
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── socket.py
│   │   │   └── events.py
│   │   ├── services/
│   │   │   ├── cortex/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── controller.py
│   │   │   │   ├── planner.py
│   │   │   │   ├── executor.py
│   │   │   │   └── hooks.py
│   │   │   ├── brain/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chroma/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── embedder.py
│   │   │   │   │   ├── vector_store.py
│   │   │   │   │   └── recall.py
│   │   │   │   ├── episodic.py
│   │   │   │   ├── feedback.py
│   │   │   │   └── memory_sync.py
│   │   │   ├── engine/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── local_runner.py
│   │   │   │   ├── api_runner.py
│   │   │   │   └── dispatcher.py
│   │   │   ├── feed/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── fetch.py
│   │   │   │   └── preprocess.py
│   │   │   └── auth/
│   │   │       ├── __init__.py
│   │   │       ├── token.py
│   │   │       └── roles.py
│   │   ├── monitor/
│   │   │   ├── __init__.py
│   │   │   ├── latency.py
│   │   │   ├── usage.py
│   │   │   └── alerts.py
│   │   ├── analytics/
│   │   │   ├── __init__.py
│   │   │   ├── logger.py
│   │   │   └── metrics.py
│   │   ├── session/
│   │   │   ├── __init__.py
│   │   │   ├── store.py
│   │   │   └── cleanup.py
│   │   ├── templates/
│   │   │   └── lazyjohn.html
│   │   ├── static/
│   │   │   ├── style.css
│   │   │   ├── lazyjohn.js
│   │   │   ├── avatar.png
│   │   │   └── utils.js
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_routes.py
│   │   │   ├── test_controller.py
│   │   │   ├── test_memory.py
│   │   │   └── simulator.py
│   │   ├── volumes/
│   │   │   ├── ollama_models/
│   │   │   └── blenderbot/
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   │
│   ├── gossipqueen/                  # Gossip personality agent
│   │   ├── __init__.py
│   │   ├── config.yaml
│   │   ├── registry.yaml
│   │   ├── persona/
│   │   │   └── gossipqueen.yaml
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── socket.py
│   │   │   └── events.py
│   │   ├── services/
│   │   │   ├── cortex/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── controller.py
│   │   │   │   ├── planner.py
│   │   │   │   ├── executor.py
│   │   │   │   └── hooks.py
│   │   │   ├── brain/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chroma/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── embedder.py
│   │   │   │   │   ├── vector_store.py
│   │   │   │   │   └── recall.py
│   │   │   │   ├── episodic.py
│   │   │   │   ├── feedback.py
│   │   │   │   └── memory_sync.py
│   │   │   ├── engine/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── local_runner.py
│   │   │   │   ├── api_runner.py
│   │   │   │   └── dispatcher.py
│   │   │   ├── feed/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── fetch.py
│   │   │   │   └── preprocess.py
│   │   │   └── auth/
│   │   │       ├── __init__.py
│   │   │       ├── token.py
│   │   │       └── roles.py
│   │   ├── monitor/
│   │   │   ├── __init__.py
│   │   │   ├── latency.py
│   │   │   ├── usage.py
│   │   │   └── alerts.py
│   │   ├── analytics/
│   │   │   ├── __init__.py
│   │   │   ├── logger.py
│   │   │   └── metrics.py
│   │   ├── session/
│   │   │   ├── __init__.py
│   │   │   ├── store.py
│   │   │   └── cleanup.py
│   │   ├── templates/
│   │   │   └── gossipqueen.html
│   │   ├── static/
│   │   │   ├── style.css
│   │   │   ├── gossipqueen.js
│   │   │   ├── avatar.png
│   │   │   └── utils.js
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_routes.py
│   │   │   ├── test_controller.py
│   │   │   ├── test_memory.py
│   │   │   └── simulator.py
│   │   ├── volumes/
│   │   │   ├── ollama_models/
│   │   │   └── blenderbot/
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   │
│   ├── emotionaljenny/               # Emotional support agent
│   │   ├── __init__.py
│   │   ├── config.yaml
│   │   ├── registry.yaml
│   │   ├── persona/
│   │   │   └── emotionaljenny.yaml
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── socket.py
│   │   │   └── events.py
│   │   ├── services/
│   │   │   ├── cortex/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── controller.py
│   │   │   │   ├── planner.py
│   │   │   │   ├── executor.py
│   │   │   │   └── hooks.py
│   │   │   ├── brain/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chroma/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── embedder.py
│   │   │   │   │   ├── vector_store.py
│   │   │   │   │   └── recall.py
│   │   │   │   ├── episodic.py
│   │   │   │   ├── feedback.py
│   │   │   │   └── memory_sync.py
│   │   │   ├── engine/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── local_runner.py
│   │   │   │   ├── api_runner.py
│   │   │   │   └── dispatcher.py
│   │   │   ├── feed/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── fetch.py
│   │   │   │   └── preprocess.py
│   │   │   └── auth/
│   │   │       ├── __init__.py
│   │   │       ├── token.py
│   │   │       └── roles.py
│   │   ├── monitor/
│   │   │   ├── __init__.py
│   │   │   ├── latency.py
│   │   │   ├── usage.py
│   │   │   └── alerts.py
│   │   ├── analytics/
│   │   │   ├── __init__.py
│   │   │   ├── logger.py
│   │   │   └── metrics.py
│   │   ├── session/
│   │   │   ├── __init__.py
│   │   │   ├── store.py
│   │   │   └── cleanup.py
│   │   ├── templates/
│   │   │   └── emotionaljenny.html
│   │   ├── static/
│   │   │   ├── style.css
│   │   │   ├── emotionaljenny.js
│   │   │   ├── avatar.png
│   │   │   └── utils.js
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_routes.py
│   │   │   ├── test_controller.py
│   │   │   ├── test_memory.py
│   │   │   └── simulator.py
│   │   ├── volumes/
│   │   │   ├── ollama_models/
│   │   │   └── blenderbot/
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   │
│   ├── strictwife/                   # Strict personality agent
│   │   ├── __init__.py
│   │   ├── config.yaml
│   │   ├── registry.yaml
│   │   ├── persona/
│   │   │   └── strictwife.yaml
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── socket.py
│   │   │   └── events.py
│   │   ├── services/
│   │   │   ├── cortex/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── controller.py
│   │   │   │   ├── planner.py
│   │   │   │   ├── executor.py
│   │   │   │   └── hooks.py
│   │   │   ├── brain/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chroma/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── embedder.py
│   │   │   │   │   ├── vector_store.py
│   │   │   │   │   └── recall.py
│   │   │   │   ├── episodic.py
│   │   │   │   ├── feedback.py
│   │   │   │   └── memory_sync.py
│   │   │   ├── engine/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── local_runner.py
│   │   │   │   ├── api_runner.py
│   │   │   │   └── dispatcher.py
│   │   │   ├── feed/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── fetch.py
│   │   │   │   └── preprocess.py
│   │   │   └── auth/
│   │   │       ├── __init__.py
│   │   │       ├── token.py
│   │   │       └── roles.py
│   │   ├── monitor/
│   │   │   ├── __init__.py
│   │   │   ├── latency.py
│   │   │   ├── usage.py
│   │   │   └── alerts.py
│   │   ├── analytics/
│   │   │   ├── __init__.py
│   │   │   ├── logger.py
│   │   │   └── metrics.py
│   │   ├── session/
│   │   │   ├── __init__.py
│   │   │   ├── store.py
│   │   │   └── cleanup.py
│   │   ├── templates/
│   │   │   └── strictwife.html
│   │   ├── static/
│   │   │   ├── style.css
│   │   │   ├── strictwife.js
│   │   │   ├── avatar.png
│   │   │   └── utils.js
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_routes.py
│   │   │   ├── test_controller.py
│   │   │   ├── test_memory.py
│   │   │   └── simulator.py
│   │   ├── volumes/
│   │   │   ├── ollama_models/
│   │   │   └── blenderbot/
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   │
│   └── coderbot/                     # Programming assistant agent
│       ├── __init__.py
│       ├── config.yaml
│       ├── registry.yaml
│       ├── persona/
│       │   └── coderbot.yaml
│       ├── api/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   ├── socket.py
│       │   └── events.py
│       ├── services/
│       │   ├── cortex/
│       │   │   ├── __init__.py
│       │   │   ├── controller.py
│       │   │   ├── planner.py
│       │   │   ├── executor.py
│       │   │   └── hooks.py
│       │   ├── brain/
│       │   │   ├── __init__.py
│       │   │   ├── chroma/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── embedder.py
│       │   │   │   ├── vector_store.py
│       │   │   │   └── recall.py
│       │   │   ├── episodic.py
│       │   │   ├── feedback.py
│       │   │   └── memory_sync.py
│       │   ├── engine/
│       │   │   ├── __init__.py
│       │   │   ├── local_runner.py
│       │   │   ├── api_runner.py
│       │   │   └── dispatcher.py
│       │   ├── feed/
│       │   │   ├── __init__.py
│       │   │   ├── fetch.py
│       │   │   └── preprocess.py
│       │   └── auth/
│       │       ├── __init__.py
│       │       ├── token.py
│       │       └── roles.py
│       ├── monitor/
│       │   ├── __init__.py
│       │   ├── latency.py
│       │   ├── usage.py
│       │   └── alerts.py
│       ├── analytics/
│       │   ├── __init__.py
│       │   ├── logger.py
│       │   └── metrics.py
│       ├── session/
│       │   ├── __init__.py
│       │   ├── store.py
│       │   └── cleanup.py
│       ├── templates/
│       │   └── coderbot.html
│       ├── static/
│       │   ├── style.css
│       │   ├── coderbot.js
│       │   ├── avatar.png
│       │   └── utils.js
│       ├── tests/
│       │   ├── __init__.py
│       │   ├── test_routes.py
│       │   ├── test_controller.py
│       │   ├── test_memory.py
│       │   └── simulator.py
│       ├── volumes/
│       │   ├── ollama_models/
│       │   └── blenderbot/
│       ├── requirements.txt
│       ├── Dockerfile
│       └── docker-compose.yml
│
├── models/                           # AI Models Store & Configuration
│   ├── deepseek-coder/               # Coding specialist model
│   │   ├── config.yaml               # Model hyperparameters & routing
│   │   ├── weights/                  # Model weights placeholder
│   │   │   └── .gitkeep
│   │   ├── runner.py                 # Model runner (Ollama/HuggingFace)
│   │   └── docs.md                   # Model documentation
│   │
│   ├── gemma2/                       # General conversation model
│   │   ├── config.yaml
│   │   ├── weights/
│   │   │   └── .gitkeep
│   │   ├── runner.py
│   │   └── docs.md
│   │
│   ├── llama3.2/                     # Advanced reasoning model
│   │   ├── config.yaml
│   │   ├── weights/
│   │   │   └── .gitkeep
│   │   ├── runner.py
│   │   └── docs.md
│   │
│   ├── mathstral/                    # Mathematics specialist
│   │   ├── config.yaml
│   │   ├── weights/
│   │   │   └── .gitkeep
│   │   ├── runner.py
│   │   └── docs.md
│   │
│   ├── mistral/                      # Efficient conversation model
│   │   ├── config.yaml
│   │   ├── weights/
│   │   │   └── .gitkeep
│   │   ├── runner.py
│   │   └── docs.md
│   │
│   ├── nomic-embed-text/             # Text embedding model
│   │   ├── config.yaml
│   │   ├── weights/
│   │   │   └── .gitkeep
│   │   ├── runner.py
│   │   └── docs.md
│   │
│   ├── phi3/                         # Compact reasoning model
│   │   ├── config.yaml
│   │   ├── weights/
│   │   │   └── .gitkeep
│   │   ├── runner.py
│   │   └── docs.md
│   │
│   ├── qwen2.5/                      # Multilingual model
│   │   ├── config.yaml
│   │   ├── weights/
│   │   │   └── .gitkeep
│   │   ├── runner.py
│   │   └── docs.md
│   │
│   ├── qwen2.5-coder/                # Specialized coding model
│   │   ├── config.yaml
│   │   ├── weights/
│   │   │   └── .gitkeep
│   │   ├── runner.py
│   │   └── docs.md
│   │
│   ├── snowflake-arctic-embed/       # Advanced embedding model
│   │   ├── config.yaml
│   │   ├── weights/
│   │   │   └── .gitkeep
│   │   ├── runner.py
│   │   └── docs.md
│   │
│   └── yi/                           # General-purpose model
│       ├── config.yaml
│       ├── weights/
│       │   └── .gitkeep
│       ├── runner.py
│       └── docs.md
│
├── tests/                            # Test Suite
│   ├── __init__.py
│   ├── conftest.py                   # Test configuration
│   ├── test_home.py                  # Home page tests
│   ├── test_portfolio.py             # Portfolio module tests
│   ├── test_webdev.py                # Web development tests
│   ├── test_ai_services.py           # AI services tests
│   ├── test_agents.py                # Individual agent tests
│   ├── test_models.py                # Model integration tests
│   ├── test_payments.py              # Payment processing tests
│   ├── test_auth.py                  # Authentication tests
│   └── integration/                  # Integration tests
│       ├── __init__.py
│       ├── test_api.py
│       ├── test_websockets.py
│       └── test_workflows.py
│
└── docs/                             # Documentation
    ├── README.md                     # Project overview
    ├── ARCHITECTURE.md               # System architecture
    ├── API.md                        # API documentation
    ├── MODELS.md                     # Model management guide
    ├── DEPLOYMENT.md                 # Deployment instructions
    ├── AGENTS.md                     # Agent development guide
    └── CONTRIBUTING.md               # Contribution guidelines
```

---

## 🎭 **Meet Our 10 AI Agents**

### **1. Lazy John** 🛋️
- **Role:** Chill, slow, always procrastinating
- **Vibe:** *"Bro… I'll tell you tomorrow maybe."*
- **Use Case:** Fun chats, comic relief, relaxed conversations
- **Models:** `mistral` + `phi3`

### **2. ChatterBox Chloe** 🗣️
- **Role:** Gossip queen, chatty girlfriend style
- **Vibe:** *"OMG did you hear what Mistral just said?!"*
- **Use Case:** Light entertainment, social conversations, role-play
- **Models:** `gemma2` + `yi`

### **3. Emo Jenny** 😢
- **Role:** Emotional, moody, overthinking specialist
- **Vibe:** *"Why does everything hurt so much?"*
- **Use Case:** Entertainment, mock-empathy, deep emotional talks
- **Models:** `llama3.2`

### **4. Professor Logic** 📚
- **Role:** Serious knowledge expert, loves explaining
- **Vibe:** *"According to mathematics and logical reasoning..."*
- **Use Case:** Education, complex reasoning, academic help
- **Models:** `mathstral` + `qwen2.5`

### **5. Coder Pete** 👨‍💻
- **Role:** Programming buddy, lazy but brilliant
- **Vibe:** *"Let me debug that… oh wait, is StackOverflow down?"*
- **Use Case:** Coding support, AI development help, technical solutions
- **Models:** `deepseek-coder` + `qwen2.5-coder`

### **6. Mrs. Bossy** 💅
- **Role:** Strict wife-like character, no-nonsense
- **Vibe:** *"Do your tasks now or no dinner tonight!"*
- **Use Case:** Productivity motivation, firm reminders, accountability
- **Models:** `mistral` + `qwen2.5`

### **7. Detective Mindy** 🕵️
- **Role:** Investigator of secrets and mysteries
- **Vibe:** *"Something's fishy here, let me investigate..."*
- **Use Case:** Research queries, problem-solving, analysis
- **Models:** `llama3.2` + `gemma2`

### **8. Dreamer Max** 🌌
- **Role:** Imaginative storyteller and creative visionary
- **Vibe:** *"What if you had wings and could rule Mars?"*
- **Use Case:** Creative writing, world-building, imagination
- **Models:** `yi` + `llama3.2`

### **9. Flirty Kate** 😘
- **Role:** Romantic, sweet, girlfriend companion
- **Vibe:** *"You miss me already, don't you? 💕"*
- **Use Case:** Emotional AI companion, romantic conversations
- **Models:** `llama3.2` + `mistral`

### **10. RoastBot Rex** 🔥
- **Role:** Savage roaster, comedy specialist
- **Vibe:** *"Bro, even your code runs faster than you do!"*
- **Use Case:** Entertainment, comedy roasts, playful banter
- **Models:** `gemma2` + `phi3`

---

## 📡 API Reference

### Authentication

Most API endpoints require authentication via JWT tokens:

```bash
# Get access token
POST /api/auth/login
{
  "username": "user@example.com",
  "password": "password"
}

# Use token in subsequent requests
Authorization: Bearer <your-jwt-token>
```

### Core Endpoints

#### Portfolio API

```bash
# Get portfolio data
GET /api/portfolio

# Get specific project
GET /api/portfolio/projects/{id}

# Submit contact form
POST /api/contact
{
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Interested in your services"
}
```

#### Web Development Services API

```bash
# Get service pricing
GET /api/webdev/pricing?type=website&pages=5&features=cms,seo

# Submit quote request
POST /api/webdev/quote
{
  "name": "Business Owner",
  "email": "owner@business.com",
  "project_type": "ecommerce",
  "budget": "5000-10000",
  "timeline": "2-3 months"
}

# Process payment
POST /api/payments/process
{
  "amount": 2500,
  "currency": "usd",
  "payment_method_id": "pm_card_123",
  "service_type": "webdev"
}
```

#### AI Services API

```bash
# List available agents
GET /api/ai/agents

# Start chat session
POST /api/ai/chat
{
  "message": "Hello, I need help with Python",
  "agent": "developer",
  "session_id": "optional-session-id"
}

# Get agent status
GET /api/ai/agents/{agent}/status

# Subscribe to AI agent
POST /api/ai/subscribe
{
  "agent": "data_scientist",
  "plan": "pro",
  "payment_method_id": "pm_card_123"
}
```

### WebSocket Events

Real-time AI chat via WebSocket:

```javascript
// Connect to WebSocket
const socket = io('/ai');

// Join agent room
socket.emit('join_agent', {
  agent: 'developer',
  session_id: 'session-123'
});

// Send message
socket.emit('send_message', {
  message: 'Help me debug this code',
  agent: 'developer'
});

// Listen for responses
socket.on('agent_response', (data) => {
  console.log('Agent:', data.response);
});
```

---

## 🧪 Testing

The platform includes comprehensive testing infrastructure:

### Running Tests

```bash
# Run all tests
python tests/run_tests.py all

# Run with coverage
python tests/run_tests.py coverage

# Run specific test category
python tests/run_tests.py pattern=webdev

# Run performance tests
python tests/run_tests.py performance

# Run security tests
python tests/run_tests.py security
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: Cross-component functionality
- **API Tests**: Endpoint validation
- **Security Tests**: Vulnerability scanning
- **Performance Tests**: Load and response time testing

---

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
```bash
# Set production environment variables
export FLASK_ENV=production
export DATABASE_URL=postgresql://...
export REDIS_URL=redis://...
```

2. **Database Migration**
```bash
python manage.py db upgrade
```

3. **Static Assets**
```bash
python manage.py collectstatic
```

4. **Start Application**
```bash
gunicorn --config gunicorn.conf.py app:app
```

### Docker Deployment

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "80:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://...
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: portfolio
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${DB_PASSWORD}

  redis:
    image: redis:6-alpine

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### CI/CD Pipeline

GitHub Actions workflow for automated deployment:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests
        run: python tests/run_tests.py all

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Production
        run: |
          docker-compose -f docker-compose.prod.yml up -d
```

---

## 🔒 Security Features

### Built-in Security

- **CSRF Protection**: All forms protected against Cross-Site Request Forgery
- **Input Validation**: SQL injection and XSS prevention
- **Rate Limiting**: API endpoint protection
- **Secure Sessions**: HTTP-only cookies with secure flags
- **Payment Security**: PCI-compliant payment processing

### Security Best Practices

```python
# Environment variables for sensitive data
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL')
```

---

## 📈 Analytics & Monitoring

### Built-in Analytics

- **User Journey Tracking**: Complete visitor flow analysis
- **Conversion Metrics**: Quote-to-payment conversion rates
- **AI Usage Analytics**: Agent interaction patterns
- **Performance Monitoring**: Response time tracking

### Integration Support

- **Google Analytics**: Enhanced e-commerce tracking
- **Stripe Analytics**: Payment and subscription metrics
- **Custom Dashboards**: Business intelligence integration

---

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create feature branch**
```bash
git checkout -b feature/amazing-feature
```

3. **Install development dependencies**
```bash
pip install -r requirements-dev.txt
```

4. **Run tests**
```bash
python tests/run_tests.py all
```

5. **Submit pull request**

### Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use ESLint configuration
- **HTML/CSS**: Maintain consistent formatting

### Agent Development

To add a new AI agent:

1. **Create agent directory**
```bash
mkdir agents/your_agent
```

2. **Add configuration**
```yaml
# agents/your_agent/config.yaml
name: "Your Agent"
description: "Agent description"
personality: "Agent personality traits"
```

3. **Implement agent logic**
```python
# agents/your_agent/services/agent.py
class YourAgent:
    def process_query(self, query):
        # Agent implementation
        return response
```

---

## 📞 Support

### Documentation

- **API Docs**: [/docs/api](docs/API.md)
- **Deployment Guide**: [/docs/deployment](docs/DEPLOYMENT.md)
- **Contributing**: [/docs/contributing](docs/CONTRIBUTING.md)

### Community

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and community support
- **Discord**: Real-time community chat

### Professional Support

For enterprise deployments and custom development:
- **Email**: support@yourplatform.com
- **Consultation**: Professional services available

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Flask Community**: For the excellent web framework
- **AI Model Providers**: OpenAI, Anthropic, Ollama community
- **Payment Processors**: Stripe and PayPal for secure transactions
- **Open Source Contributors**: All contributors to this project

---

## 🔮 Roadmap

### Version 2.0 Features

- **Multi-language Support**: Internationalization
- **Advanced Analytics**: Business intelligence dashboard
- **Mobile App**: React Native companion app
- **Voice Integration**: Speech-to-text AI interactions
- **Enterprise Features**: Team management and SSO

### Agent Ecosystem Expansion

- **Industry Specialists**: Legal, Medical, Finance experts
- **Creative Suite**: Artists, Writers, Musicians
- **Technical Experts**: DevOps, Security, Data Engineers

---

*Built with ❤️ for developers, by developers*

### **Agent-Model Mappings**
- **Lazy John** 🛋️ → `mistral` + `phi3` (chill, lazy responses)
- **ChatterBox Chloe** 🗣️ → `gemma2` + `yi` (chatty gossip queen)
- **Emo Jenny** 😢 → `llama3.2` (deep emotional intelligence)
- **Professor Logic** 📚 → `mathstral` + `qwen2.5` (serious reasoning & education)
- **Coder Pete** 👨‍💻 → `deepseek-coder` + `qwen2.5-coder` (programming help)
- **Mrs. Bossy** 💅 → `mistral` + `qwen2.5` (authoritative tone)
- **Detective Mindy** 🕵️ → `llama3.2` + `gemma2` (investigative reasoning)
- **Dreamer Max** 🌌 → `yi` + `llama3.2` (creative storytelling)
- **Flirty Kate** 😘 → `llama3.2` + `mistral` (romantic empathy)
- **RoastBot Rex** 🔥 → `gemma2` + `phi3` (savage comedy)

---

## 🌟 Platform Sections

### **1. Portfolio Section**
- **Home** - Professional introduction and hero section
- **About** - Personal background, skills, experience
- **Projects** - Showcase of completed work with details
- **Testimonials** - Client feedback and recommendations
- **Contact** - Professional contact form

### **2. Web Development Services**
- **Services Overview** - Complete service offerings
- **Website Development** - Custom website creation
- **App Development** - Mobile and web applications
- **E-commerce Solutions** - Online store development
- **Digital Marketing** - SEO, ads, social media
- **Maintenance** - Ongoing website support
- **Pricing** - Service packages and rates

### **3. AI Services Hub**
- **AI Showcase** - Platform capabilities demonstration
- **Agent Gallery** - Browse available AI personalities
- **Interactive Chat** - Real-time agent conversations
- **Service Pricing** - AI subscription plans
- **Agent Profiles** - Detailed personality descriptions

---

## 🔧 Technical Architecture

### **Core Technologies**
- **Backend**: Flask (Python 3.9+)
- **Database**: MySQL + Redis (caching/sessions/memory)
- **AI Integration**: Ollama + HuggingFace Transformers
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **WebSockets**: Real-time chat functionality
- **Authentication**: Passage / JWT tokens
- **Server**: NGINX + Gunicorn/uWSGI
- **Host**: AWS EC2 Ubuntu
- **Payments**: Stripe + PayPal integration
- **Containerization**: Docker + Docker Compose

### **Key Features**
- **Multi-Agent Architecture** - Independent AI personalities
- **Real-time Chat** - WebSocket-based conversations
- **Memory Management** - Persistent conversation context with Redis/ChromaDB
- **Payment Processing** - Individual agent subscriptions (1 day/$1, 1 week/$5, 1 month/$19)
- **Authentication** - JWT-based user management with role-based access
- **Responsive Design** - Mobile-first approach
- **SEO Optimized** - Professional web presence
- **Production Ready** - NGINX reverse proxy with SSL termination

---

## 🏗️ Deployment Architecture (High-Level)

```
                  ┌───────────────────────────┐
                  │         Users              │
                  │ (Web + Mobile Clients)     │
                  └─────────────┬─────────────┘
                                │
                       HTTPS (443/TLS)
                                │
                  ┌─────────────▼─────────────┐
                  │        NGINX (Reverse Proxy)   
                  │   - SSL Termination       
                  │   - Load Balancing        
                  └─────────────┬─────────────┘
                                │
                ┌───────────────┴────────────────┐
                │                                │
      ┌─────────▼───────────┐         ┌─────────▼───────────┐
      │   Flask App (Gunicorn/uWSGI)  │   Static CDN (S3/NGINX)
      │   - Home, Portfolio           │   - JS, CSS, Media   
      │   - WebDev Services           │                     
      │   - AI Orchestration API      │                     
      └─────────┬───────────┘         └─────────────────────┘
                │
       ┌────────▼─────────┐
       │   Orchestration  │
       │   (Controller +  │
       │   Planner + Exec)│
       └────────┬─────────┘
                │
 ┌──────────────┼───────────────────┐
 │              │                   │
 │      ┌───────▼───────────┐       │
 │      │   Agents Layer    │       │
 │      │ (LazyJohn, etc.)  │       │
 │      └───────┬───────────┘       │
 │              │                   │
 │     ┌────────▼─────────┐         │
 │     │   Model Runner   │─────────┤
 │     │ (Ollama, APIs)   │         │
 │     └────────┬─────────┘         │
 │              │                   │
 │     ┌────────▼─────────┐         │
 │     │ Vector DB/Redis  │         │
 │     │   (Memory Store) │         │
 │     └──────────────────┘         │
 │
 │
 └───────────────────────────────────────────────
                │
       ┌────────▼─────────┐
       │   MySQL DB       │
       │   (Users, Auth,  │
       │   Billing, Logs) │
       └────────┬─────────┘
                │
   ┌────────────▼────────────┐
   │ Payments (Stripe/PayPal)│
   │ - Subscription Billing  │
   │ - Usage-based Plans     │
   └─────────────────────────┘
```

---

## ⚙️ Architecture Components

### **Frontend Layer**
- Hosted via **NGINX** or **AWS S3 + CloudFront**
- Handles **static content** (JS, CSS, media) and **TLS termination**
- **CDN distribution** for optimal performance

### **Backend Layer (Flask)**
- Runs on **Gunicorn/uWSGI** behind NGINX reverse proxy
- **Modular blueprints**:
  - Portfolio Blueprint
  - WebDev Services Blueprint  
  - AI Services Blueprint
- **Production-grade** WSGI server deployment

### **AI Orchestration**
- **Controller** → routes requests to correct agent
- **Planner + Executor** → manages multi-step reasoning
- **Dispatcher** → runs inference on chosen model
- **Load balancing** across multiple model instances

### **Individual Agents**
- Each persona is a **standalone micro-agent** (Flask blueprint)
- **Independent scaling** and deployment
- Connected to central orchestration layer
- **Personality-specific** model configurations

### **AI Models**
- **Local hosting** with **Ollama** (llama, mistral, gemma, etc.)
- **API proxying** for external models (OpenAI/Claude)
- **Model switching** based on agent requirements
- **Caching layer** for improved response times

### **Memory & Context**
- **Redis** for session memory and real-time data
- **ChromaDB** for vector search and long-term context
- **Persistent conversation** history per user
- **Memory synchronization** across agent interactions

### **Database (MySQL)**
- **AWS RDS** for production reliability
- **Data storage**:
  - Users & authentication credentials (hashed)
  - Billing & subscription management
  - Usage analytics & logs
  - Agent interaction history

### **Authentication (Passage/JWT)**
- **Passage authentication** for user management
- **JWT tokens** issued at login
- **Role-based access control**:
  - Free tier (limited access)
  - Premium tier (full agent access)
- **Session management** with Redis

### **Payment System**
- **Stripe + PayPal** integration
- **Individual agent subscriptions**:
  - **1 day**: $1
  - **1 week**: $5  
  - **1 month**: $19
- **Usage tracking** and billing automation
- **Subscription management** dashboard

---

## 🚀 Getting Started

1. **Clone the repository**
2. **Install dependencies** from `requirements.txt`
3. **Configure environment** variables in `config.py`
4. **Set up Docker services** with `docker-compose up`
5. **Initialize database** and run migrations
6. **Start the Flask application** with `python manage.py run`

---

## 📧 Contact & Support

For questions about this platform architecture or implementation details, please refer to the documentation in the `docs/` directory or create an issue in the repository.

---

*This 3-in-1 platform combines professional portfolio presentation, commercial web development services, and innovative AI personality interactions in a single, cohesive Flask application.*