# 🏗️ Flask 3-in-1 Platform: Portfolio + Web Development + AI Services

## 📋 Project Overview

A comprehensive **Flask-based 3-in-1 platform** that combines:

1. **Portfolio Section** - Personal/professional showcase
2. **Web Development Services** - Commercial service offerings  
3. **AI Services** - Multi-agent AI hub with entertaining personas

---

## 🌟 Key Features

- **Multi-Agent AI System** with **10 unique personalities** (Lazy John, ChatterBox Chloe, Emo Jenny, etc.)
- **Professional Service Hub** for web development offerings
- **Personal Portfolio** showcase with projects and testimonials
- **Payment Integration** (Stripe/PayPal) for individual agent subscriptions
- **Authentication & Role Management** for user access control
- **Multiple AI Model Support** with advanced orchestration layer

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

## 🤖 AI Models Integration

### **Supported Models**
- `deepseek-coder` - Programming and code generation
- `gemma2` - General conversation and reasoning  
- `llama3.2` - Advanced natural language understanding
- `mathstral` - Mathematical computations and problem-solving
- `mistral` - Efficient conversational AI
- `nomic-embed-text` - Text embeddings for semantic search
- `phi3` - Compact reasoning model
- `qwen2.5` - Multilingual support
- `qwen2.5-coder` - Specialized coding assistant
- `snowflake-arctic-embed` - Advanced embedding capabilities
- `yi` - General-purpose language model

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