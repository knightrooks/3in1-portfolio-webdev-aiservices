"""
Services Blueprint
Handles web development services functionality
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for

services_bp = Blueprint('services', __name__)

@services_bp.route('/')
def index():
    """Services overview page"""
    services_data = [
        {
            'name': 'Frontend Development',
            'description': 'Responsive, modern web interfaces using latest technologies',
            'technologies': ['React', 'Vue.js', 'Angular', 'HTML5/CSS3', 'JavaScript'],
            'price_range': '$500 - $3,000',
            'icon': 'frontend-icon'
        },
        {
            'name': 'Backend Development',
            'description': 'Robust server-side applications and APIs',
            'technologies': ['Python/Flask', 'Django', 'Node.js', 'PostgreSQL', 'MongoDB'],
            'price_range': '$800 - $5,000',
            'icon': 'backend-icon'
        },
        {
            'name': 'Full-Stack Development',
            'description': 'Complete web applications from frontend to backend',
            'technologies': ['MERN Stack', 'Django + React', 'Flask + Vue.js'],
            'price_range': '$1,500 - $8,000',
            'icon': 'fullstack-icon'
        },
        {
            'name': 'Database Design',
            'description': 'Efficient database architecture and optimization',
            'technologies': ['PostgreSQL', 'MongoDB', 'Redis', 'Database Migration'],
            'price_range': '$300 - $2,000',
            'icon': 'database-icon'
        }
    ]
    return render_template('services/index.html', services=services_data)

@services_bp.route('/packages')
def packages():
    """Service packages and pricing"""
    packages_data = [
        {
            'name': 'Starter Package',
            'price': '$999',
            'duration': '2-3 weeks',
            'features': [
                'Basic website (5 pages max)',
                'Responsive design',
                'Contact form',
                'SEO optimization',
                'Basic hosting setup'
            ],
            'ideal_for': 'Small businesses, personal websites'
        },
        {
            'name': 'Professional Package',
            'price': '$2,499',
            'duration': '4-6 weeks',
            'features': [
                'Custom web application',
                'Database integration',
                'User authentication',
                'API development',
                'Advanced features',
                'Testing & deployment'
            ],
            'ideal_for': 'Medium businesses, startups'
        },
        {
            'name': 'Enterprise Package',
            'price': '$5,999+',
            'duration': '8-12 weeks',
            'features': [
                'Complex web platform',
                'Multiple integrations',
                'Advanced security',
                'Scalable architecture',
                'Performance optimization',
                'Ongoing maintenance'
            ],
            'ideal_for': 'Large businesses, enterprises'
        }
    ]
    return render_template('services/packages.html', packages=packages_data)

@services_bp.route('/inquiry', methods=['GET', 'POST'])
def inquiry():
    """Service inquiry form"""
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get('name')
        email = request.form.get('email')
        service_type = request.form.get('service_type')
        budget = request.form.get('budget')
        description = request.form.get('description')
        
        # In a real application, you would save this to a database or send an email
        flash(f'Thank you {name}! Your inquiry has been received. We will contact you at {email} soon.', 'success')
        return redirect(url_for('services.inquiry'))
    
    return render_template('services/inquiry.html')

@services_bp.route('/testimonials')
def testimonials():
    """Client testimonials"""
    testimonials_data = [
        {
            'client': 'Sarah Johnson',
            'company': 'TechStart Inc.',
            'text': 'Excellent work on our e-commerce platform. Professional, timely, and exceeded expectations.',
            'rating': 5,
            'project': 'E-commerce Development'
        },
        {
            'client': 'Mike Chen',
            'company': 'DataFlow Solutions',
            'text': 'Great backend development skills. The API is robust and well-documented.',
            'rating': 5,
            'project': 'API Development'
        },
        {
            'client': 'Emily Rodriguez',
            'company': 'Creative Agency',
            'text': 'Beautiful frontend work. The website is exactly what we envisioned.',
            'rating': 4,
            'project': 'Frontend Development'
        }
    ]
    return render_template('services/testimonials.html', testimonials=testimonials_data)