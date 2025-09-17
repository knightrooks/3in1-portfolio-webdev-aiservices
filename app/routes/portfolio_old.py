from flask import Blueprint, render_template, request

# Create Blueprint
portfolio_bp = Blueprint('portfolio', __name__)

# Portfolio data - Manual content (no external fetching)
PORTFOLIO_DATA = {
    'personal_info': {
        'name': 'Professor Johnny',
        'alias': '@onelastai',
        'tagline': 'AI Orchestrator & Security Architect',
        'bio': 'I orchestrate intelligence and architect security solutions. Specializing in AI systems and cybersecurity frameworks.',
        'location': 'Digital Realm',
        'email': 'contact@axeyaxe.com',
        'github': 'https://github.com/1-manarmy',
        'linkedin': 'https://linkedin.com/in/onelastai',
        'twitter': 'https://twitter.com/onelastai',
        'instagram': 'https://instagram.com/onelastai',
        'facebook': 'https://facebook.com/onelastai',
        'telegram': 'https://t.me/onelastai',
        'website': 'https://axeyaxe.com'
    },
    'specialties': [
        'AI & Machine Learning',
        'Cybersecurity & Ethical Hacking', 
        'Flask & Python Development',
        'Deep Learning & Neural Networks',
        'Automation & Digital Security',
        'Penetration Testing & Security Analysis',
        'Intelligent Systems Architecture',
        'Data Science & Analytics'
    ],
    'philosophy': [
        'Innovation through strategic thinking and technical excellence',
        'Building secure, intelligent systems that anticipate threats',
        'Combining AI capabilities with cybersecurity expertise',
        'Crafting solutions that are both powerful and elegant',
        'Leading through expertise and continuous learning',
        'Creating technology that enhances human potential'
    ],
    'current_focus': {
        'working_on': 'Advanced AI Security Integration',
        'exploring': 'Next-Generation Threat Detection',
        'collaborating': 'AI-Powered Security Solutions',
        'innovation': 'Intelligent Security Automation',
        'expertise': 'AI Systems, Cybersecurity, Full-Stack Development'
    }
}

@portfolio_bp.route('/')
def index():
    """Portfolio homepage."""
    return render_template('portfolio/index.html', data=PORTFOLIO_DATA)

@portfolio_bp.route('/about')
def about():
    """About me page."""
    print("DEBUG: About route called, tagline:", PORTFOLIO_DATA['personal_info']['tagline'])
    return render_template('portfolio/about.html', data=PORTFOLIO_DATA)

@portfolio_bp.route('/projects')
def projects():
    """Projects showcase."""
    # This will fetch from GitHub API later
    projects_data = {
        'featured': [
            {
                'name': 'AI Security Framework',
                'description': 'Advanced AI-powered cybersecurity analysis framework',
                'technologies': ['Python', 'TensorFlow', 'Flask', 'Redis'],
                'status': 'Active',
                'github': '#',
                'demo': '#'
            },
            {
                'name': 'Intelligent Automation Suite',
                'description': 'Machine learning automation for digital operations',
                'technologies': ['Python', 'Scikit-learn', 'Docker', 'API'],
                'status': 'In Development',
                'github': '#',
                'demo': '#'
            },
            {
                'name': 'Neural Network Orchestrator',
                'description': 'Multi-model AI orchestration platform',
                'technologies': ['Python', 'PyTorch', 'FastAPI', 'PostgreSQL'],
                'status': 'Research',
                'github': '#',
                'demo': '#'
            }
        ]
    }
    return render_template('portfolio/projects.html', data=PORTFOLIO_DATA, projects=projects_data)

@portfolio_bp.route('/skills')
def skills():
    """Skills & expertise page."""
    skills_data = {
        'technical': {
            'languages': ['Python', 'JavaScript', 'Go', 'Rust', 'C++'],
            'frameworks': ['Flask', 'Django', 'FastAPI', 'React', 'Vue.js'],
            'ai_ml': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'Keras', 'Transformers'],
            'security': ['Metasploit', 'Burp Suite', 'Nmap', 'Wireshark', 'OWASP'],
            'databases': ['MySQL', 'PostgreSQL', 'Redis', 'MongoDB', 'ChromaDB'],
            'devops': ['Docker', 'Kubernetes', 'AWS', 'NGINX', 'Git']
        },
        'certifications': [
            'Certified Ethical Hacker (CEH)',
            'AWS Solutions Architect',
            'Machine Learning Specialist',
            'Cybersecurity Framework Expert'
        ]
    }
    return render_template('portfolio/skills.html', data=PORTFOLIO_DATA, skills=skills_data)

@portfolio_bp.route('/contact')
def contact():
    """Contact page."""
    return render_template('portfolio/contact.html', data=PORTFOLIO_DATA)

@portfolio_bp.route('/testimonials')
def testimonials():
    """Client testimonials."""
    testimonials_data = [
        {
            'client': 'Tech Startup CEO',
            'company': 'AI Innovations Ltd',
            'feedback': 'Professor Johnny transformed our security posture completely. His AI-driven approach is revolutionary.',
            'rating': 5,
            'project': 'Security Audit & AI Implementation'
        },
        {
            'client': 'CTO',
            'company': 'CyberDefense Corp',
            'feedback': 'The most skilled penetration tester we\'ve worked with. Found vulnerabilities others missed.',
            'rating': 5,
            'project': 'Advanced Penetration Testing'
        },
        {
            'client': 'Data Science Lead',
            'company': 'ML Research Institute',
            'feedback': 'Incredible machine learning expertise. Built models that exceeded all our expectations.',
            'rating': 5,
            'project': 'Custom ML Pipeline Development'
        }
    ]
    return render_template('portfolio/testimonials.html', data=PORTFOLIO_DATA, testimonials=testimonials_data)