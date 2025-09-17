# AI Agents Architecture Index

This directory contains the complete architecture for all 10 AI agents in the system.

## Agent Directory Structure

Each agent follows this comprehensive architecture:

```
agent_name/
├── __init__.py                    # Flask blueprint registration  
├── config.yaml                    # Agent configuration
├── registry.yaml                  # Multi-agent metadata
├── persona/                       # Persona definitions
│   └── agent_name.yaml
├── api/                           # REST + WebSocket endpoints
│   ├── routes.py                  # HTTP routes
│   ├── socket.py                  # WebSocket setup
│   └── events.py                  # WebSocket events
├── services/                      # Core business logic
│   ├── cortex/                    # Reasoning & orchestration
│   │   ├── controller.py          # Main controller
│   │   ├── planner.py             # Task planning
│   │   ├── executor.py            # Task execution
│   │   └── hooks.py               # Event hooks
│   ├── brain/                     # Memory & cognition
│   │   ├── chroma/                # Vector database
│   │   │   ├── embedder.py        # Text embeddings
│   │   │   ├── vector_store.py    # Vector storage
│   │   │   └── recall.py          # Memory recall
│   │   ├── episodic.py            # Episode memory
│   │   ├── feedback.py            # Learning feedback
│   │   └── memory_sync.py         # Memory synchronization
│   ├── engine/                    # AI model inference
│   │   ├── local_runner.py        # Local model execution
│   │   ├── api_runner.py          # API model execution  
│   │   └── dispatcher.py          # Model routing
│   ├── feed/                      # External data
│   │   ├── fetch.py               # Data fetching
│   │   └── preprocess.py          # Data preprocessing
│   └── auth/                      # Authentication
│       ├── token.py               # Token management
│       └── roles.py               # Role management
├── monitor/                       # Performance monitoring
│   ├── latency.py                 # Response time tracking
│   ├── usage.py                   # Usage analytics
│   └── alerts.py                  # Alert system
├── analytics/                     # User analytics
│   ├── logger.py                  # Interaction logging
│   └── metrics.py                 # Metrics collection
├── session/                       # Session management
│   ├── store.py                   # Session storage
│   └── cleanup.py                 # Session cleanup
├── templates/                     # Frontend templates
│   └── agent_name.html            # Chat interface
├── static/                        # Static assets
│   ├── style.css                  # Agent styling
│   ├── agent_name.js              # JavaScript logic
│   └── utils.js                   # Utility functions
└── tests/                         # Test suite
    ├── test_routes.py             # Route testing
    ├── test_controller.py         # Controller testing
    ├── test_memory.py             # Memory testing
    └── simulator.py               # Agent simulation
```

## Available Agents

### Business Strategist AI (`strategist`)
- **Description**: Expert in business strategy, market analysis, and strategic planning
- **Primary Model**: gemma2
- **Personality**: analytical_advisor
- **Color Theme**: #1f4e79
- **Endpoint**: `/ai/agents/strategist/`

### Senior Developer AI (`developer`)
- **Description**: Expert software developer and architect with advanced capabilities
- **Primary Model**: deepseek-coder
- **Personality**: technical_expert
- **Color Theme**: #2d5a27
- **Endpoint**: `/ai/agents/developer/`

### Cybersecurity Expert AI (`security_expert`)
- **Description**: Expert in cybersecurity with advanced threat analysis
- **Primary Model**: llama3_2
- **Personality**: security_specialist
- **Color Theme**: #8b0000
- **Endpoint**: `/ai/agents/security_expert/`

### Content Creator AI (`content_creator`)
- **Description**: Expert content strategist with advanced multilingual capabilities
- **Primary Model**: llama3_2
- **Personality**: creative_communicator
- **Color Theme**: #663399
- **Endpoint**: `/ai/agents/content_creator/`

### Research Analyst AI (`research_analyst`)
- **Description**: Advanced research specialist with long-context analysis
- **Primary Model**: yi
- **Personality**: analytical_researcher
- **Color Theme**: #006666
- **Endpoint**: `/ai/agents/research_analyst/`

### Data Scientist AI (`data_scientist`)
- **Description**: Advanced data science specialist with mathematical modeling
- **Primary Model**: mathstral
- **Personality**: quantitative_analyst
- **Color Theme**: #cc6600
- **Endpoint**: `/ai/agents/data_scientist/`

### Customer Success AI (`customer_success`)
- **Description**: Expert in customer experience with emotional intelligence
- **Primary Model**: yi
- **Personality**: empathetic_advisor
- **Color Theme**: #0066cc
- **Endpoint**: `/ai/agents/customer_success/`

### Product Manager AI (`product_manager`)
- **Description**: Strategic product management with user research expertise
- **Primary Model**: gemma2
- **Personality**: product_strategist
- **Color Theme**: #ff6600
- **Endpoint**: `/ai/agents/product_manager/`

### Marketing Specialist AI (`marketing_specialist`)
- **Description**: Digital marketing expert with creative content capabilities
- **Primary Model**: llama3_2
- **Personality**: creative_marketer
- **Color Theme**: #e91e63
- **Endpoint**: `/ai/agents/marketing_specialist/`

### Operations Manager AI (`operations_manager`)
- **Description**: Business operations specialist with process optimization
- **Primary Model**: phi3
- **Personality**: efficiency_optimizer
- **Color Theme**: #4a4a4a
- **Endpoint**: `/ai/agents/operations_manager/`


## Usage

Each agent can be accessed via:
- **REST API**: `/ai/agents/{agent_id}/chat`
- **WebSocket**: `/ai/agents/{agent_id}/ws`
- **Web Interface**: `/ai/agents/{agent_id}/`

## Development

To extend an agent:
1. Modify the `config.yaml` for configuration changes
2. Update `persona/{agent_id}.yaml` for personality changes
3. Extend `services/cortex/controller.py` for new capabilities
4. Add routes in `api/routes.py` for new endpoints
5. Update tests in `tests/` directory

## Architecture Benefits

- **Modular**: Each agent is completely self-contained
- **Scalable**: Individual agents can be scaled independently
- **Maintainable**: Clear separation of concerns
- **Testable**: Comprehensive test coverage for each component
- **Extensible**: Easy to add new capabilities or agents
