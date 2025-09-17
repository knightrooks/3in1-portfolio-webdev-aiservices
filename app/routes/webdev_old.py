"""
Web Development Services Routing System
Comprehensive routing for all web development services, templates, and tools
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import json
from datetime import datetime
import os
import time
from pathlib import Path

# Create Blueprint
webdev_bp = Blueprint('webdev', __name__, template_folder='../templates/webdev')

# Web Development Services Configuration
WEBDEV_SERVICES = {
    'hero': {
        'title': 'Professional Web Development Services',
        'tagline': 'From concept to launch, we build web solutions that work.',
        'description': 'Custom websites, web applications, and digital solutions designed to help your business grow online.',
        'technologies': ['React', 'Vue.js', 'Flask', 'Django', 'Node.js', 'Python', 'JavaScript', 'TypeScript'],
        'specialties': ['Frontend Development', 'Backend Development', 'Full-Stack Solutions', 'API Development']
    },
    'services': [
        {
            'id': 'websites',
            'name': 'Custom Websites',
            'icon': 'fas fa-globe',
            'short_desc': 'Professional, responsive websites built with modern technologies.',
            'long_desc': 'Custom websites tailored to your business needs, from simple landing pages to complex corporate sites.',
            'price_from': '$1,500',
            'price_to': '$10,000',
            'features': ['Responsive Design', 'SEO Optimized', 'Fast Loading', 'Mobile-First', 'CMS Integration'],
            'technologies': ['HTML5', 'CSS3', 'JavaScript', 'React', 'Vue.js'],
            'category': 'websites'
        },
        {
            'id': 'web-apps',
            'name': 'Web Applications',
            'icon': 'fas fa-laptop-code',
            'short_desc': 'Custom web applications with advanced functionality.',
            'long_desc': 'Full-featured web applications with complex business logic, user authentication, and database integration.',
            'price_from': '$3,000',
            'price_to': '$25,000',
            'features': ['User Authentication', 'Database Integration', 'API Development', 'Real-time Features', 'Admin Panels'],
            'technologies': ['Flask', 'Django', 'Node.js', 'PostgreSQL', 'MongoDB'],
            'category': 'applications'
        },
            'features': ['Custom Development', 'Database Integration', 'User Authentication', 'API Integration']
        },
        {
            'id': 'ecommerce',
            'name': 'E-commerce Solutions',
            'icon': 'fas fa-shopping-cart',
            'short_desc': 'Complete online stores with payment processing.',
            'price_from': '$2,500',
            'features': ['Payment Gateway', 'Inventory Management', 'Order Processing', 'Admin Dashboard']
        },
        {
            'id': 'maintenance',
            'name': 'Website Maintenance',
            'icon': 'fas fa-tools',
            'short_desc': 'Keep your website updated, secure, and running smoothly.',
            'price_from': '$200/mo',
            'features': ['Security Updates', 'Content Updates', 'Performance Monitoring', 'Backup Services']
        }
    ],
    'technologies': [
        {'name': 'Python/Flask', 'icon': 'fab fa-python'},
        {'name': 'JavaScript/React', 'icon': 'fab fa-js'},
        {'name': 'HTML5/CSS3', 'icon': 'fab fa-html5'},
        {'name': 'MySQL/PostgreSQL', 'icon': 'fas fa-database'},
        {'name': 'AWS/Cloud', 'icon': 'fab fa-aws'},
        {'name': 'Docker', 'icon': 'fab fa-docker'}
    ]
}

@webdev_bp.route('/')
def index():
    """Web Development Services homepage."""
    return render_template('webdev/index.html', services=WEBDEV_SERVICES)

@webdev_bp.route('/websites')
def websites():
    """Website Development Service."""
    service_data = {
        'title': 'Custom Website Development',
        'description': 'Professional, responsive websites built with modern technologies and best practices.',
        'features': [
            'Responsive Design for all devices',
            'SEO Optimized structure',
            'Fast loading times (< 3 seconds)',
            'Mobile-first approach',
            'Cross-browser compatibility',
            'Contact forms and integrations',
            'Content Management System',
            'Google Analytics integration'
        ],
        'packages': [
            {
                'name': 'Starter Website',
                'price': '$1,500',
                'features': ['Up to 5 pages', 'Responsive design', 'Contact form', 'SEO basics', '3 months support']
            },
            {
                'name': 'Business Website',
                'price': '$2,500',
                'features': ['Up to 10 pages', 'CMS integration', 'Advanced SEO', 'Analytics setup', '6 months support']
            },
            {
                'name': 'Premium Website',
                'price': '$4,000',
                'features': ['Unlimited pages', 'Custom functionality', 'E-commerce ready', 'Performance optimization', '1 year support']
            }
        ]
    }
    return render_template('webdev/websites.html', data=service_data)

@webdev_bp.route('/apps')
def apps():
    """Web Application Development."""
    return render_template('webdev/apps.html')

@webdev_bp.route('/ecommerce')
def ecommerce():
    """E-commerce Development."""
    return render_template('webdev/ecommerce.html')

@webdev_bp.route('/maintenance')
def maintenance():
    """Website Maintenance Services."""
    return render_template('webdev/maintenance.html')

@webdev_bp.route('/seo')
def seo():
    """SEO Services."""
    return render_template('webdev/seo.html')

@webdev_bp.route('/marketing')
def marketing():
    """Digital Marketing Services."""
    return render_template('webdev/marketing.html')

@webdev_bp.route('/quote')
def quote():
    """Get a Quote."""
    package = request.args.get('package', '')
    service = request.args.get('service', '')
    return render_template('webdev/quote.html', package=package, service=service)

@webdev_bp.route('/quote', methods=['POST'])
def quote_submit():
    """Handle quote form submission."""
    try:
        # Extract form data
        form_data = {
            'name': request.form.get('name', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'company': request.form.get('company', ''),
            'service': request.form.get('service', ''),
            'package': request.form.get('package', ''),
            'budget': request.form.get('budget', ''),
            'timeline': request.form.get('timeline', ''),
            'description': request.form.get('description', ''),
            'website': request.form.get('website', ''),
            'goals': request.form.getlist('goals'),
            'submitted_at': datetime.now().isoformat()
        }
        
        # Save to JSON file (in production, would use database)
        quotes_file = 'data/quotes.json'
        os.makedirs('data', exist_ok=True)
        
        quotes = []
        if os.path.exists(quotes_file):
            try:
                with open(quotes_file, 'r') as f:
                    quotes = json.load(f)
            except:
                quotes = []
        
        quotes.append(form_data)
        
        with open(quotes_file, 'w') as f:
            json.dump(quotes, f, indent=2)
        
        flash('Thank you! Your quote request has been submitted successfully. We\'ll get back to you within 24 hours.', 'success')
        return redirect(url_for('webdev.quote'))
        
    except Exception as e:
        flash('Sorry, there was an error submitting your request. Please try again or contact us directly.', 'error')
        return redirect(url_for('webdev.quote'))

@webdev_bp.route('/service-inquiry', methods=['POST'])
def service_inquiry():
    """Handle service inquiry form submission."""
    try:
        # Extract form data
        form_data = {
            'name': request.form.get('name', ''),
            'email': request.form.get('email', ''),
            'service': request.form.get('service', ''),
            'message': request.form.get('message', ''),
            'phone': request.form.get('phone', ''),
            'company': request.form.get('company', ''),
            'submitted_at': datetime.now().isoformat()
        }
        
        # Save to JSON file
        inquiries_file = 'data/inquiries.json'
        os.makedirs('data', exist_ok=True)
        
        inquiries = []
        if os.path.exists(inquiries_file):
            try:
                with open(inquiries_file, 'r') as f:
                    inquiries = json.load(f)
            except:
                inquiries = []
        
        inquiries.append(form_data)
        
        with open(inquiries_file, 'w') as f:
            json.dump(inquiries, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your inquiry! We\'ll get back to you soon.'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Sorry, there was an error. Please try again.'
        }), 500

# Service packages configuration
SERVICE_PACKAGES = {
    'websites': {
        'starter': {
            'name': 'Starter Website',
            'price': 1500,
            'features': ['Up to 5 pages', 'Responsive design', 'Contact form', 'SEO basics', '3 months support'],
            'timeline': '2-3 weeks'
        },
        'business': {
            'name': 'Business Website',
            'price': 2500,
            'features': ['Up to 10 pages', 'CMS integration', 'Advanced SEO', 'Analytics setup', '6 months support'],
            'timeline': '3-4 weeks'
        },
        'premium': {
            'name': 'Premium Website',
            'price': 4000,
            'features': ['Unlimited pages', 'Custom functionality', 'E-commerce ready', 'Performance optimization', '1 year support'],
            'timeline': '4-6 weeks'
        }
    },
    'apps': {
        'basic': {
            'name': 'Basic Web App',
            'price': 3000,
            'features': ['User authentication', 'Basic CRUD', 'Responsive design', 'Database integration', '3 months support'],
            'timeline': '4-5 weeks'
        },
        'professional': {
            'name': 'Professional Web App',
            'price': 5000,
            'features': ['Advanced features', 'API integration', 'Admin panel', 'User management', '6 months support'],
            'timeline': '6-8 weeks'
        },
        'enterprise': {
            'name': 'Enterprise Web App',
            'price': 8000,
            'features': ['Custom architecture', 'Scalable infrastructure', 'Advanced security', 'Full documentation', '1 year support'],
            'timeline': '8-12 weeks'
        }
    },
    'ecommerce': {
        'starter': {
            'name': 'E-commerce Starter',
            'price': 2500,
            'features': ['Up to 50 products', 'Payment gateway', 'Order management', 'Basic analytics', '3 months support'],
            'timeline': '3-4 weeks'
        },
        'professional': {
            'name': 'E-commerce Professional',
            'price': 4500,
            'features': ['Unlimited products', 'Multi-payment options', 'Inventory management', 'Customer accounts', '6 months support'],
            'timeline': '5-6 weeks'
        },
        'enterprise': {
            'name': 'E-commerce Enterprise',
            'price': 8000,
            'features': ['Custom features', 'Multi-vendor support', 'Advanced analytics', 'Mobile app', '1 year support'],
            'timeline': '8-10 weeks'
        }
    },
    'maintenance': {
        'basic': {
            'name': 'Basic Maintenance',
            'price': 200,
            'billing': 'monthly',
            'features': ['Security updates', 'Content updates (2/month)', 'Basic monitoring', 'Email support'],
            'timeline': 'Ongoing'
        },
        'professional': {
            'name': 'Professional Maintenance',
            'price': 400,
            'billing': 'monthly',
            'features': ['Priority updates', 'Content updates (8/month)', 'Performance monitoring', 'Phone support'],
            'timeline': 'Ongoing'
        },
        'enterprise': {
            'name': 'Enterprise Maintenance',
            'price': 800,
            'billing': 'monthly',
            'features': ['24/7 monitoring', 'Unlimited updates', 'Performance optimization', 'Dedicated support'],
            'timeline': 'Ongoing'
        }
    },
    'seo': {
        'starter': {
            'name': 'SEO Starter',
            'price': 800,
            'billing': 'monthly',
            'features': ['Keyword research', 'On-page optimization', 'Basic reporting', 'Google Analytics setup'],
            'timeline': '3-6 months'
        },
        'professional': {
            'name': 'SEO Professional',
            'price': 1500,
            'billing': 'monthly',
            'features': ['Advanced SEO strategy', 'Content optimization', 'Link building', 'Detailed reporting'],
            'timeline': '6-12 months'
        },
        'enterprise': {
            'name': 'SEO Enterprise',
            'price': 2500,
            'billing': 'monthly',
            'features': ['Full SEO management', 'Technical SEO', 'Competitor analysis', 'Dedicated SEO manager'],
            'timeline': '12+ months'
        }
    },
    'marketing': {
        'starter': {
            'name': 'Marketing Starter',
            'price': 1200,
            'billing': 'monthly',
            'features': ['Google Ads management', 'Social media (2 platforms)', 'Basic email marketing', 'Monthly reporting'],
            'timeline': 'Ongoing'
        },
        'professional': {
            'name': 'Marketing Professional',
            'price': 2500,
            'billing': 'monthly',
            'features': ['Multi-platform ads', 'Social media (4 platforms)', 'Advanced email marketing', 'Content creation'],
            'timeline': 'Ongoing'
        },
        'enterprise': {
            'name': 'Marketing Enterprise',
            'price': 5000,
            'billing': 'monthly',
            'features': ['Full-funnel marketing', 'Omnichannel campaigns', 'Custom analytics', 'Dedicated manager'],
            'timeline': 'Ongoing'
        }
    }
}

@webdev_bp.route('/api/packages/<service>')
def get_service_packages(service):
    """API endpoint to get service packages."""
    if service in SERVICE_PACKAGES:
        return jsonify(SERVICE_PACKAGES[service])
    return jsonify({'error': 'Service not found'}), 404

@webdev_bp.route('/pricing')
def pricing():
    """Pricing Information."""
    return render_template('webdev/pricing.html')