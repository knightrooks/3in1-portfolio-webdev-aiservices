"""
Web Development Services Routing System
Comprehensive routing for all web development services, templates, and tools
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

# Create Blueprint
webdev_bp = Blueprint("webdev", __name__, template_folder="../../webdev")

# Web Development Services Configuration
WEBDEV_SERVICES = {
    "hero": {
        "title": "Professional Web Development Services",
        "tagline": "From concept to launch, we build web solutions that work.",
        "description": "Custom websites, web applications, and digital solutions designed to help your business grow online.",
        "technologies": [
            "React",
            "Vue.js",
            "Flask",
            "Django",
            "Node.js",
            "Python",
            "JavaScript",
            "TypeScript",
        ],
        "specialties": [
            "Frontend Development",
            "Backend Development",
            "Full-Stack Solutions",
            "API Development",
        ],
    },
    "services": [
        {
            "id": "websites",
            "name": "Custom Websites",
            "icon": "fas fa-globe",
            "short_desc": "Professional, responsive websites built with modern technologies.",
            "long_desc": "Custom websites tailored to your business needs, from simple landing pages to complex corporate sites.",
            "price_from": "$1,500",
            "price_to": "$10,000",
            "features": [
                "Responsive Design",
                "SEO Optimized",
                "Fast Loading",
                "Mobile-First",
                "CMS Integration",
            ],
            "technologies": ["HTML5", "CSS3", "JavaScript", "React", "Vue.js"],
            "category": "websites",
        },
        {
            "id": "web-apps",
            "name": "Web Applications",
            "icon": "fas fa-laptop-code",
            "short_desc": "Custom web applications with advanced functionality.",
            "long_desc": "Full-featured web applications with complex business logic, user authentication, and database integration.",
            "price_from": "$3,000",
            "price_to": "$25,000",
            "features": [
                "User Authentication",
                "Database Integration",
                "API Development",
                "Real-time Features",
                "Admin Panels",
            ],
            "technologies": ["Flask", "Django", "Node.js", "PostgreSQL", "MongoDB"],
            "category": "applications",
        },
        {
            "id": "ecommerce",
            "name": "E-commerce Solutions",
            "icon": "fas fa-shopping-cart",
            "short_desc": "Complete online stores with payment processing and inventory management.",
            "long_desc": "Full-featured e-commerce platforms with shopping carts, payment gateways, and order management.",
            "price_from": "$5,000",
            "price_to": "$20,000",
            "features": [
                "Payment Processing",
                "Inventory Management",
                "Order Tracking",
                "Customer Accounts",
                "Admin Dashboard",
            ],
            "technologies": ["Shopify", "WooCommerce", "Stripe", "PayPal"],
            "category": "ecommerce",
        },
        {
            "id": "apis",
            "name": "API Development",
            "icon": "fas fa-exchange-alt",
            "short_desc": "RESTful APIs and microservices for your applications.",
            "long_desc": "Scalable API solutions for connecting your applications and enabling third-party integrations.",
            "price_from": "$2,000",
            "price_to": "$15,000",
            "features": [
                "RESTful Architecture",
                "Authentication",
                "Rate Limiting",
                "Documentation",
                "Testing",
            ],
            "technologies": ["Flask", "FastAPI", "Django REST", "Node.js"],
            "category": "backend",
        },
        {
            "id": "seo",
            "name": "SEO Optimization",
            "icon": "fas fa-search",
            "short_desc": "Improve your website's search engine rankings and visibility.",
            "long_desc": "Comprehensive SEO services to increase your online visibility and drive organic traffic.",
            "price_from": "$800",
            "price_to": "$3,000",
            "features": [
                "Keyword Research",
                "On-page SEO",
                "Technical SEO",
                "Content Optimization",
                "Analytics",
            ],
            "technologies": ["Google Analytics", "Search Console", "SEMrush", "Ahrefs"],
            "category": "marketing",
        },
        {
            "id": "maintenance",
            "name": "Website Maintenance",
            "icon": "fas fa-tools",
            "short_desc": "Keep your website updated, secure, and running smoothly.",
            "long_desc": "Ongoing maintenance services to ensure your website remains secure, updated, and performing optimally.",
            "price_from": "$200",
            "price_to": "$1000",
            "features": [
                "Security Updates",
                "Content Updates",
                "Performance Monitoring",
                "Backup Services",
                "24/7 Support",
            ],
            "technologies": [
                "Monitoring Tools",
                "Security Scanners",
                "Backup Solutions",
            ],
            "category": "maintenance",
        },
    ],
    "technologies": [
        {"name": "Python/Flask", "icon": "fab fa-python", "category": "backend"},
        {"name": "JavaScript/React", "icon": "fab fa-js", "category": "frontend"},
        {"name": "HTML5/CSS3", "icon": "fab fa-html5", "category": "frontend"},
        {"name": "MySQL/PostgreSQL", "icon": "fas fa-database", "category": "database"},
        {"name": "AWS/Cloud", "icon": "fab fa-aws", "category": "infrastructure"},
        {"name": "Docker", "icon": "fab fa-docker", "category": "deployment"},
    ],
    "portfolio_projects": [
        {
            "name": "E-commerce Platform",
            "tech": ["React", "Node.js", "MongoDB"],
            "category": "ecommerce",
        },
        {
            "name": "Corporate Website",
            "tech": ["HTML5", "CSS3", "JavaScript"],
            "category": "websites",
        },
        {
            "name": "API Gateway",
            "tech": ["Python", "Flask", "PostgreSQL"],
            "category": "backend",
        },
    ],
}


# Routes
@webdev_bp.route("/")
def index():
    """Web Development Services homepage."""
    return render_template(
        "webdev/index.html",
        services=WEBDEV_SERVICES,
        page_title="Web Development Services",
    )


@webdev_bp.route("/api")
def api_overview():
    """API overview for webdev services"""
    service_apis = {}

    for service in WEBDEV_SERVICES["services"]:
        service_apis[service["id"]] = {
            "info": service,
            "endpoints": {
                "details": f'/webdev/{service["id"]}',
                "quote": f'/webdev/quote?service={service["id"]}',
                "portfolio": f'/webdev/portfolio?category={service["category"]}',
            },
        }

    return jsonify(
        {
            "success": True,
            "data": {
                "total_services": len(WEBDEV_SERVICES["services"]),
                "categories": list(
                    set(s["category"] for s in WEBDEV_SERVICES["services"])
                ),
                "technologies": WEBDEV_SERVICES["technologies"],
                "services": service_apis,
            },
        }
    )


@webdev_bp.route("/websites")
def websites():
    """Website Development Service."""
    service_data = next(
        (s for s in WEBDEV_SERVICES["services"] if s["id"] == "websites"), None
    )

    return render_template(
        "webdev/websites.html",
        service=service_data,
        page_title="Custom Website Development",
    )


@webdev_bp.route("/apps")
def apps():
    """Web Applications Service."""
    service_data = next(
        (s for s in WEBDEV_SERVICES["services"] if s["id"] == "web-apps"), None
    )

    return render_template(
        "webdev/apps.html",
        service=service_data,
        page_title="Web Application Development",
    )


@webdev_bp.route("/ecommerce")
def ecommerce():
    """E-commerce Solutions Service."""
    service_data = next(
        (s for s in WEBDEV_SERVICES["services"] if s["id"] == "ecommerce"), None
    )

    return render_template(
        "webdev/ecommerce.html", service=service_data, page_title="E-commerce Solutions"
    )


@webdev_bp.route("/seo")
def seo():
    """SEO Optimization Service."""
    service_data = next(
        (s for s in WEBDEV_SERVICES["services"] if s["id"] == "seo"), None
    )

    return render_template(
        "webdev/seo.html", service=service_data, page_title="SEO Optimization Services"
    )


@webdev_bp.route("/maintenance")
def maintenance():
    """Website Maintenance Service."""
    service_data = next(
        (s for s in WEBDEV_SERVICES["services"] if s["id"] == "maintenance"), None
    )

    return render_template(
        "webdev/maintenance.html",
        service=service_data,
        page_title="Website Maintenance Services",
    )


@webdev_bp.route("/marketing")
def marketing():
    """Digital Marketing Services."""
    marketing_services = [
        s for s in WEBDEV_SERVICES["services"] if s["category"] in ["marketing", "seo"]
    ]

    return render_template(
        "webdev/marketing.html",
        services=marketing_services,
        page_title="Digital Marketing Services",
    )


@webdev_bp.route("/pricing")
def pricing():
    """Pricing page for all services."""
    return render_template(
        "webdev/pricing.html",
        services=WEBDEV_SERVICES,
        page_title="Web Development Pricing",
    )


@webdev_bp.route("/quote")
def quote_form():
    """Quote request form."""
    service_id = request.args.get("service", "")
    selected_service = None

    if service_id:
        selected_service = next(
            (s for s in WEBDEV_SERVICES["services"] if s["id"] == service_id), None
        )

    return render_template(
        "webdev/quote.html",
        services=WEBDEV_SERVICES["services"],
        selected_service=selected_service,
        page_title="Request a Quote",
    )


@webdev_bp.route("/quote", methods=["POST"])
def submit_quote():
    """Handle quote form submission."""
    try:
        # Get form data
        quote_data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone", ""),
            "company": request.form.get("company", ""),
            "service": request.form.get("service"),
            "budget": request.form.get("budget"),
            "timeline": request.form.get("timeline"),
            "description": request.form.get("description"),
            "timestamp": datetime.now().isoformat(),
            "status": "new",
        }

        # Save to quotes file
        quotes_file = Path("data/quotes.json")
        quotes_file.parent.mkdir(exist_ok=True)

        quotes = []
        if quotes_file.exists():
            with open(quotes_file, "r") as f:
                quotes = json.load(f)

        quotes.append(quote_data)

        with open(quotes_file, "w") as f:
            json.dump(quotes, f, indent=2)

        flash(
            "Thank you! Your quote request has been submitted. We'll get back to you within 24 hours.",
            "success",
        )
        return redirect(url_for("webdev.quote_form"))

    except Exception as e:
        flash(
            "Sorry, there was an error submitting your request. Please try again.",
            "error",
        )
        return redirect(url_for("webdev.quote_form"))


@webdev_bp.route("/portfolio")
def portfolio():
    """Portfolio showcase for web development projects."""
    category = request.args.get("category", "all")

    projects = WEBDEV_SERVICES["portfolio_projects"]
    if category != "all":
        projects = [p for p in projects if p["category"] == category]

    categories = list(set(p["category"] for p in WEBDEV_SERVICES["portfolio_projects"]))

    return render_template(
        "webdev/portfolio.html",
        projects=projects,
        categories=categories,
        current_category=category,
        page_title="Web Development Portfolio",
    )


@webdev_bp.route("/technologies")
def technologies():
    """Technologies and tools showcase."""
    tech_by_category = {}

    for tech in WEBDEV_SERVICES["technologies"]:
        category = tech["category"]
        if category not in tech_by_category:
            tech_by_category[category] = []
        tech_by_category[category].append(tech)

    return render_template(
        "webdev/technologies.html",
        technologies=tech_by_category,
        page_title="Technologies & Tools",
    )


@webdev_bp.route("/process")
def process():
    """Development process overview."""
    process_steps = [
        {
            "step": 1,
            "title": "Discovery & Planning",
            "description": "Understanding your requirements and planning the project architecture.",
            "duration": "1-2 weeks",
            "deliverables": ["Project Scope", "Technical Specification", "Timeline"],
        },
        {
            "step": 2,
            "title": "Design & Prototyping",
            "description": "Creating wireframes, mockups, and interactive prototypes.",
            "duration": "1-3 weeks",
            "deliverables": ["UI/UX Design", "Prototype", "Style Guide"],
        },
        {
            "step": 3,
            "title": "Development",
            "description": "Building the application with regular progress updates.",
            "duration": "2-8 weeks",
            "deliverables": ["Working Application", "Code Documentation", "Testing"],
        },
        {
            "step": 4,
            "title": "Testing & Launch",
            "description": "Quality assurance testing and deployment to production.",
            "duration": "1-2 weeks",
            "deliverables": ["QA Testing", "Deployment", "Training"],
        },
        {
            "step": 5,
            "title": "Support & Maintenance",
            "description": "Ongoing support, updates, and maintenance services.",
            "duration": "Ongoing",
            "deliverables": ["24/7 Support", "Updates", "Monitoring"],
        },
    ]

    return render_template(
        "webdev/process.html", steps=process_steps, page_title="Development Process"
    )


@webdev_bp.route("/health")
def health():
    """Health check for webdev services"""
    health_data = {
        "status": "healthy",
        "services_count": len(WEBDEV_SERVICES["services"]),
        "technologies_count": len(WEBDEV_SERVICES["technologies"]),
        "categories": list(set(s["category"] for s in WEBDEV_SERVICES["services"])),
        "timestamp": time.time(),
    }

    return jsonify({"success": True, "data": health_data})


@webdev_bp.route("/analytics")
def analytics():
    """Analytics for webdev services"""
    analytics_data = {
        "total_services": len(WEBDEV_SERVICES["services"]),
        "service_categories": {},
        "technology_categories": {},
        "price_ranges": {},
        "portfolio_projects": len(WEBDEV_SERVICES["portfolio_projects"]),
    }

    # Service categories
    for service in WEBDEV_SERVICES["services"]:
        category = service["category"]
        analytics_data["service_categories"][category] = (
            analytics_data["service_categories"].get(category, 0) + 1
        )

    # Technology categories
    for tech in WEBDEV_SERVICES["technologies"]:
        category = tech["category"]
        analytics_data["technology_categories"][category] = (
            analytics_data["technology_categories"].get(category, 0) + 1
        )

    # Price ranges
    for service in WEBDEV_SERVICES["services"]:
        if "price_from" in service:
            price_from = (
                service["price_from"]
                .replace("$", "")
                .replace(",", "")
                .replace("/mo", "")
            )
            try:
                price_num = int(price_from)
                if price_num < 1000:
                    range_key = "under_1k"
                elif price_num < 5000:
                    range_key = "1k_to_5k"
                else:
                    range_key = "over_5k"
                analytics_data["price_ranges"][range_key] = (
                    analytics_data["price_ranges"].get(range_key, 0) + 1
                )
            except ValueError:
                pass

    return jsonify({"success": True, "data": analytics_data, "timestamp": time.time()})
