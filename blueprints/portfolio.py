"""
Portfolio Blueprint
Handles personal portfolio functionality
"""

from flask import Blueprint, render_template

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/')
def index():
    """Portfolio home page"""
    return render_template('portfolio/index.html')

@portfolio_bp.route('/about')
def about():
    """About me page"""
    return render_template('portfolio/about.html')

@portfolio_bp.route('/projects')
def projects():
    """Projects showcase"""
    projects_data = [
        {
            'title': 'E-Commerce Platform',
            'description': 'Full-stack e-commerce solution with payment integration',
            'technologies': ['Python', 'Flask', 'PostgreSQL', 'JavaScript'],
            'image': '/static/images/project1.jpg',
            'github': 'https://github.com/example/project1',
            'demo': 'https://demo1.example.com'
        },
        {
            'title': 'Data Analytics Dashboard',
            'description': 'Interactive dashboard for business intelligence and reporting',
            'technologies': ['React', 'D3.js', 'Node.js', 'MongoDB'],
            'image': '/static/images/project2.jpg',
            'github': 'https://github.com/example/project2',
            'demo': 'https://demo2.example.com'
        },
        {
            'title': 'Mobile App Backend',
            'description': 'RESTful API backend for iOS and Android mobile applications',
            'technologies': ['Django', 'REST Framework', 'PostgreSQL', 'Docker'],
            'image': '/static/images/project3.jpg',
            'github': 'https://github.com/example/project3',
            'demo': None
        }
    ]
    return render_template('portfolio/projects.html', projects=projects_data)

@portfolio_bp.route('/skills')
def skills():
    """Skills and expertise"""
    skills_data = {
        'frontend': ['HTML5', 'CSS3', 'JavaScript', 'React', 'Vue.js', 'Bootstrap', 'Tailwind CSS'],
        'backend': ['Python', 'Flask', 'Django', 'Node.js', 'PostgreSQL', 'MongoDB', 'Redis'],
        'tools': ['Git', 'Docker', 'AWS', 'Jenkins', 'Nginx', 'Linux', 'Postman'],
        'soft_skills': ['Problem Solving', 'Team Collaboration', 'Project Management', 'Communication']
    }
    return render_template('portfolio/skills.html', skills=skills_data)

@portfolio_bp.route('/contact')
def contact():
    """Contact information"""
    contact_info = {
        'email': 'contact@example.com',
        'linkedin': 'https://linkedin.com/in/example',
        'github': 'https://github.com/example',
        'twitter': 'https://twitter.com/example'
    }
    return render_template('portfolio/contact.html', contact=contact_info)