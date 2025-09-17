"""
Portfolio Routing System
Comprehensive portfolio showcase and project management system
"""

from flask import Blueprint, render_template, request, jsonify, send_file, url_for
import json
import time
from pathlib import Path
from datetime import datetime

# Create Blueprint
portfolio_bp = Blueprint('portfolio', __name__, template_folder='../../portfolio')

# Portfolio Configuration
PORTFOLIO_DATA = {
    'personal_info': {
        'name': 'Professor Johnny',
        'alias': '@onelastai',
        'title': 'AI Orchestrator & Full-Stack Developer',
        'tagline': 'Building the future with AI, Web Development, and Innovation',
        'bio': 'Experienced full-stack developer and AI specialist with expertise in creating intelligent web solutions, secure applications, and cutting-edge AI services. Passionate about combining traditional web development with modern AI capabilities.',
        'location': 'Digital Realm',
        'email': 'contact@axeyaxe.com',
        'github': 'https://github.com/1-manarmy',
        'linkedin': 'https://linkedin.com/in/onelastai',
        'twitter': 'https://twitter.com/onelastai',
        'instagram': 'https://instagram.com/onelastai',
        'facebook': 'https://facebook.com/onelastai',
        'telegram': 'https://t.me/onelastai',
        'website': 'https://axeyaxe.com',
        'years_experience': 8,
        'projects_completed': 150,
        'clients_satisfied': 120,
        'ai_agents_created': 16
    },
    'specialties': [
        {
            'name': 'AI & Machine Learning',
            'icon': '🤖',
            'description': 'Custom AI agents, machine learning models, and intelligent automation',
            'technologies': ['Python', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'OpenAI API'],
            'experience_years': 5
        },
        {
            'name': 'Full-Stack Web Development',
            'icon': '🌐',
            'description': 'End-to-end web applications with modern frameworks and databases',
            'technologies': ['Flask', 'Django', 'React', 'Vue.js', 'Node.js', 'PostgreSQL'],
            'experience_years': 8
        },
        {
            'name': 'Cybersecurity & Ethical Hacking',
            'icon': '🔐',
            'description': 'Security audits, penetration testing, and secure application development',
            'technologies': ['Kali Linux', 'Metasploit', 'Burp Suite', 'OWASP', 'Security Frameworks'],
            'experience_years': 6
        },
        {
            'name': 'Cloud & DevOps',
            'icon': '☁️',
            'description': 'Cloud infrastructure, containerization, and deployment automation',
            'technologies': ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Terraform'],
            'experience_years': 4
        },
        {
            'name': 'API Development',
            'icon': '🔗',
            'description': 'RESTful APIs, microservices architecture, and system integrations',
            'technologies': ['Flask', 'FastAPI', 'GraphQL', 'REST', 'Microservices'],
            'experience_years': 7
        },
        {
            'name': 'Database Design',
            'icon': '🗄️',
            'description': 'Database architecture, optimization, and data modeling',
            'technologies': ['PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Data Modeling'],
            'experience_years': 6
        }
    ],
    'portfolio_categories': [
        {
            'id': 'ai-services',
            'name': 'AI Services & Agents',
            'icon': '🤖',
            'description': 'Intelligent AI agents and machine learning solutions',
            'color': '#2563eb'
        },
        {
            'id': 'web-applications',
            'name': 'Web Applications',
            'icon': '💻',
            'description': 'Full-stack web applications and platforms',
            'color': '#059669'
        },
        {
            'id': 'security-projects',
            'name': 'Security Projects',
            'icon': '🔒',
            'description': 'Cybersecurity tools and secure applications',
            'color': '#dc2626'
        },
        {
            'id': 'apis-integrations',
            'name': 'APIs & Integrations',
            'icon': '🔗',
            'description': 'API development and third-party integrations',
            'color': '#7c3aed'
        },
        {
            'id': 'automation-tools',
            'name': 'Automation Tools',
            'icon': '⚙️',
            'description': 'Workflow automation and productivity tools',
            'color': '#ea580c'
        }
    ],
    'featured_projects': [
        {
            'id': 'ai-agents-platform',
            'name': '16 AI Agents Platform',
            'category': 'ai-services',
            'description': 'Comprehensive AI services platform with 16 specialized agents for business and entertainment',
            'technologies': ['Python', 'Flask', 'AI/ML', 'WebSockets', 'REST API'],
            'features': ['Real-time Chat', 'Multi-Agent System', 'Analytics Dashboard', 'WebSocket Support'],
            'status': 'completed',
            'completion_date': '2025-09-17',
            'client': 'Internal Project',
            'image': '/static/images/portfolio/ai-agents-platform.jpg',
            'demo_url': '/agents',
            'github_url': 'https://github.com/knightrooks/ai-agents-platform'
        },
        {
            'id': 'webdev-services-platform',
            'name': 'Web Development Services Platform',
            'category': 'web-applications',
            'description': 'Complete web development services platform with portfolio, pricing, and client management',
            'technologies': ['Flask', 'HTML5', 'CSS3', 'JavaScript', 'Bootstrap'],
            'features': ['Service Showcase', 'Quote System', 'Portfolio Gallery', 'Contact Management'],
            'status': 'completed',
            'completion_date': '2025-09-17',
            'client': 'Business Platform',
            'image': '/static/images/portfolio/webdev-platform.jpg',
            'demo_url': '/webdev',
            'github_url': 'https://github.com/knightrooks/webdev-platform'
        },
        {
            'id': 'security-audit-tool',
            'name': 'Automated Security Audit Tool',
            'category': 'security-projects',
            'description': 'Comprehensive security auditing tool for web applications and infrastructure',
            'technologies': ['Python', 'Security Libraries', 'Web Scraping', 'Vulnerability Detection'],
            'features': ['Automated Scanning', 'Vulnerability Reports', 'Security Metrics', 'Compliance Checking'],
            'status': 'in-progress',
            'completion_date': '2025-10-15',
            'client': 'Security Consultancy',
            'image': '/static/images/portfolio/security-tool.jpg',
            'github_url': 'https://github.com/knightrooks/security-audit-tool'
        },
        {
            'id': 'api-gateway-service',
            'name': 'Multi-Service API Gateway',
            'category': 'apis-integrations',
            'description': 'Centralized API gateway for managing multiple microservices and third-party integrations',
            'technologies': ['Flask', 'Redis', 'JWT', 'Rate Limiting', 'Load Balancing'],
            'features': ['Request Routing', 'Authentication', 'Rate Limiting', 'Analytics', 'Health Monitoring'],
            'status': 'completed',
            'completion_date': '2025-08-30',
            'client': 'Enterprise Client',
            'image': '/static/images/portfolio/api-gateway.jpg',
            'github_url': 'https://github.com/knightrooks/api-gateway'
        },
        {
            'id': 'workflow-automation',
            'name': 'Business Workflow Automation',
            'category': 'automation-tools',
            'description': 'Automated workflow system for business process optimization and task management',
            'technologies': ['Python', 'Celery', 'RabbitMQ', 'Flask', 'Automation'],
            'features': ['Task Scheduling', 'Email Automation', 'Report Generation', 'Integration Hub'],
            'status': 'completed',
            'completion_date': '2025-07-20',
            'client': 'SME Business',
            'image': '/static/images/portfolio/workflow-automation.jpg',
            'github_url': 'https://github.com/knightrooks/workflow-automation'
        }
    ],
    'skills': [
        {'name': 'Python', 'level': 95, 'category': 'programming'},
        {'name': 'JavaScript', 'level': 88, 'category': 'programming'},
        {'name': 'Flask/Django', 'level': 92, 'category': 'frameworks'},
        {'name': 'React/Vue.js', 'level': 85, 'category': 'frameworks'},
        {'name': 'AI/Machine Learning', 'level': 90, 'category': 'ai'},
        {'name': 'Cybersecurity', 'level': 87, 'category': 'security'},
        {'name': 'Database Design', 'level': 89, 'category': 'database'},
        {'name': 'Cloud/DevOps', 'level': 82, 'category': 'infrastructure'},
        {'name': 'API Development', 'level': 93, 'category': 'backend'},
        {'name': 'UI/UX Design', 'level': 75, 'category': 'design'}
    ],
    'achievements': [
        {
            'title': '16 AI Agents Platform Launch',
            'date': '2025-09-17',
            'description': 'Successfully launched comprehensive AI services platform with 16 specialized agents',
            'icon': '🚀'
        },
        {
            'title': 'Cybersecurity Certification',
            'date': '2024-12-15',
            'description': 'Obtained advanced cybersecurity certification in ethical hacking and penetration testing',
            'icon': '🎓'
        },
        {
            'title': '150+ Projects Completed',
            'date': '2025-08-01',
            'description': 'Milestone achievement of completing over 150 successful projects across various domains',
            'icon': '🏆'
        },
        {
            'title': 'Full-Stack Excellence Award',
            'date': '2024-10-20',
            'description': 'Recognition for excellence in full-stack development and AI integration',
            'icon': '🥇'
        }
    ],
    'testimonials': [
        {
            'name': 'Sarah Johnson',
            'company': 'TechStart Inc.',
            'position': 'CEO',
            'content': 'Professor Johnny delivered an exceptional AI-powered web application that transformed our business processes. His expertise in both AI and web development is remarkable.',
            'rating': 5,
            'project': 'AI-Powered Business Platform',
            'image': '/static/images/testimonials/sarah-johnson.jpg'
        },
        {
            'name': 'Michael Chen',
            'company': 'SecureNet Solutions',
            'position': 'CTO',
            'content': 'The security audit tools and recommendations provided by Johnny significantly improved our infrastructure security. Highly professional and knowledgeable.',
            'rating': 5,
            'project': 'Security Infrastructure Audit',
            'image': '/static/images/testimonials/michael-chen.jpg'
        },
        {
            'name': 'Emily Rodriguez',
            'company': 'Digital Marketing Pro',
            'position': 'Marketing Director',
            'content': 'Our new website and AI-powered customer service system exceeded all expectations. Johnny is a true professional who delivers on promises.',
            'rating': 5,
            'project': 'E-commerce Platform with AI Chat',
            'image': '/static/images/testimonials/emily-rodriguez.jpg'
        }
    ]
}

@portfolio_bp.route('/')
def index():
    """Main portfolio homepage"""
    return render_template('portfolio/index.html', 
                         portfolio=PORTFOLIO_DATA,
                         page_title='Portfolio - Professor Johnny')

@portfolio_bp.route('/api')
def api_overview():
    """API overview for portfolio data"""
    return jsonify({
        'success': True,
        'data': {
            'personal_info': PORTFOLIO_DATA['personal_info'],
            'specialties_count': len(PORTFOLIO_DATA['specialties']),
            'projects_count': len(PORTFOLIO_DATA['featured_projects']),
            'skills_count': len(PORTFOLIO_DATA['skills']),
            'achievements_count': len(PORTFOLIO_DATA['achievements']),
            'testimonials_count': len(PORTFOLIO_DATA['testimonials']),
            'categories': PORTFOLIO_DATA['portfolio_categories']
        }
    })

@portfolio_bp.route('/about')
def about():
    """About page with detailed information"""
    return render_template('portfolio/about.html', 
                         portfolio=PORTFOLIO_DATA,
                         page_title='About - Professor Johnny')

@portfolio_bp.route('/projects')
def projects():
    """Projects showcase page"""
    category = request.args.get('category', 'all')
    
    if category == 'all':
        projects = PORTFOLIO_DATA['featured_projects']
    else:
        projects = [p for p in PORTFOLIO_DATA['featured_projects'] if p['category'] == category]
    
    return render_template('portfolio/projects.html', 
                         projects=projects,
                         categories=PORTFOLIO_DATA['portfolio_categories'],
                         current_category=category,
                         page_title='Projects Portfolio')

@portfolio_bp.route('/projects/<project_id>')
def project_detail(project_id):
    """Individual project detail page"""
    project = next((p for p in PORTFOLIO_DATA['featured_projects'] if p['id'] == project_id), None)
    
    if not project:
        return render_template('errors/404.html'), 404
    
    # Get related projects from same category
    related_projects = [p for p in PORTFOLIO_DATA['featured_projects'] 
                       if p['category'] == project['category'] and p['id'] != project_id][:3]
    
    return render_template('portfolio/project_detail.html', 
                         project=project,
                         related_projects=related_projects,
                         page_title=f'{project["name"]} - Project Details')

@portfolio_bp.route('/skills')
def skills():
    """Skills and expertise page"""
    skills_by_category = {}
    
    for skill in PORTFOLIO_DATA['skills']:
        category = skill['category']
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)
    
    return render_template('portfolio/skills.html', 
                         skills=skills_by_category,
                         specialties=PORTFOLIO_DATA['specialties'],
                         page_title='Skills & Expertise')

@portfolio_bp.route('/achievements')
def achievements():
    """Achievements and milestones page"""
    return render_template('portfolio/achievements.html', 
                         achievements=PORTFOLIO_DATA['achievements'],
                         personal_info=PORTFOLIO_DATA['personal_info'],
                         page_title='Achievements & Milestones')

@portfolio_bp.route('/testimonials')
def testimonials():
    """Client testimonials page"""
    return render_template('portfolio/testimonials.html', 
                         testimonials=PORTFOLIO_DATA['testimonials'],
                         page_title='Client Testimonials')

@portfolio_bp.route('/contact')
def contact():
    """Contact information page"""
    return render_template('portfolio/contact.html', 
                         personal_info=PORTFOLIO_DATA['personal_info'],
                         page_title='Contact Information')

@portfolio_bp.route('/resume')
def resume():
    """Resume/CV page"""
    resume_data = {
        'personal_info': PORTFOLIO_DATA['personal_info'],
        'specialties': PORTFOLIO_DATA['specialties'],
        'skills': PORTFOLIO_DATA['skills'],
        'featured_projects': PORTFOLIO_DATA['featured_projects'][:5],  # Top 5 projects
        'achievements': PORTFOLIO_DATA['achievements'],
        'education': [
            {
                'degree': 'Master of Computer Science',
                'institution': 'Tech University',
                'year': '2018',
                'specialization': 'Artificial Intelligence & Cybersecurity'
            },
            {
                'degree': 'Bachelor of Computer Engineering',
                'institution': 'Engineering College',
                'year': '2016',
                'specialization': 'Software Development'
            }
        ],
        'experience': [
            {
                'position': 'Senior Full-Stack Developer & AI Specialist',
                'company': 'Freelance/Consulting',
                'period': '2020 - Present',
                'responsibilities': [
                    'Develop custom AI agents and intelligent web applications',
                    'Provide cybersecurity consulting and penetration testing',
                    'Build full-stack web applications with modern frameworks',
                    'Design and implement scalable API architectures'
                ]
            },
            {
                'position': 'Lead Developer',
                'company': 'TechSolutions Corp',
                'period': '2018 - 2020',
                'responsibilities': [
                    'Led development team of 5 engineers',
                    'Architected enterprise-level web applications',
                    'Implemented security best practices and protocols',
                    'Mentored junior developers and conducted code reviews'
                ]
            }
        ]
    }
    
    return render_template('portfolio/resume.html', 
                         resume=resume_data,
                         page_title='Resume - Professor Johnny')

@portfolio_bp.route('/analytics')
def analytics():
    """Portfolio analytics and statistics"""
    analytics_data = {
        'project_stats': {
            'total_projects': len(PORTFOLIO_DATA['featured_projects']),
            'completed_projects': len([p for p in PORTFOLIO_DATA['featured_projects'] if p['status'] == 'completed']),
            'in_progress_projects': len([p for p in PORTFOLIO_DATA['featured_projects'] if p['status'] == 'in-progress']),
            'categories': {}
        },
        'skill_stats': {
            'total_skills': len(PORTFOLIO_DATA['skills']),
            'average_skill_level': sum(s['level'] for s in PORTFOLIO_DATA['skills']) / len(PORTFOLIO_DATA['skills']),
            'skill_categories': {}
        },
        'specialty_stats': {
            'total_specialties': len(PORTFOLIO_DATA['specialties']),
            'total_experience_years': sum(s['experience_years'] for s in PORTFOLIO_DATA['specialties']),
            'average_experience': sum(s['experience_years'] for s in PORTFOLIO_DATA['specialties']) / len(PORTFOLIO_DATA['specialties'])
        },
        'achievement_stats': {
            'total_achievements': len(PORTFOLIO_DATA['achievements']),
            'recent_achievements': len([a for a in PORTFOLIO_DATA['achievements'] if '2025' in a['date']])
        }
    }
    
    # Project categories
    for project in PORTFOLIO_DATA['featured_projects']:
        category = project['category']
        analytics_data['project_stats']['categories'][category] = analytics_data['project_stats']['categories'].get(category, 0) + 1
    
    # Skill categories
    for skill in PORTFOLIO_DATA['skills']:
        category = skill['category']
        analytics_data['skill_stats']['skill_categories'][category] = analytics_data['skill_stats']['skill_categories'].get(category, 0) + 1
    
    return jsonify({
        'success': True,
        'data': analytics_data,
        'timestamp': time.time()
    })

@portfolio_bp.route('/health')
def health():
    """Health check for portfolio system"""
    health_data = {
        'status': 'healthy',
        'data_integrity': {
            'personal_info': bool(PORTFOLIO_DATA['personal_info']),
            'projects': len(PORTFOLIO_DATA['featured_projects']) > 0,
            'skills': len(PORTFOLIO_DATA['skills']) > 0,
            'specialties': len(PORTFOLIO_DATA['specialties']) > 0,
            'achievements': len(PORTFOLIO_DATA['achievements']) > 0,
            'testimonials': len(PORTFOLIO_DATA['testimonials']) > 0
        },
        'content_stats': {
            'projects_count': len(PORTFOLIO_DATA['featured_projects']),
            'skills_count': len(PORTFOLIO_DATA['skills']),
            'specialties_count': len(PORTFOLIO_DATA['specialties'])
        },
        'timestamp': time.time()
    }
    
    # Check data integrity
    all_checks_passed = all(health_data['data_integrity'].values())
    health_data['overall_status'] = 'healthy' if all_checks_passed else 'degraded'
    
    return jsonify({
        'success': True,
        'data': health_data
    })

@portfolio_bp.route('/download/resume')
def download_resume():
    """Download resume as PDF (placeholder - would need PDF generation)"""
    # This would typically generate a PDF resume
    # For now, return a JSON response indicating the feature
    return jsonify({
        'success': False,
        'message': 'PDF resume generation coming soon',
        'alternatives': {
            'web_resume': url_for('portfolio.resume'),
            'contact_for_resume': PORTFOLIO_DATA['personal_info']['email']
        }
    })