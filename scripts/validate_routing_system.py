#!/usr/bin/env python3
"""
Comprehensive Routing System Validation
Tests all routing systems across the 4 core service areas and global endpoints
"""

import sys
import time
import requests
import json
from pathlib import Path
from flask import Flask
from flask.testing import FlaskClient

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def validate_routing_system():
    """Validate all routing systems"""
    print("🔍 Validating 3-in-1 Platform Routing System...")
    print("=" * 60)
    
    try:
        # Import and create app
        from app import create_app
        app = create_app('testing')
        
        with app.test_client() as client:
            validation_results = {
                'global_routes': validate_global_routes(client),
                'agents_routes': validate_agents_routes(client),
                'webdev_routes': validate_webdev_routes(client),
                'portfolio_routes': validate_portfolio_routes(client),
                'models_routes': validate_models_routes(client)
            }
            
            # Summary
            print_validation_summary(validation_results)
            return validation_results
            
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        return {'error': str(e)}

def validate_global_routes(client: FlaskClient):
    """Validate global platform routes"""
    print("\n🌐 Testing Global Routes...")
    
    routes = {
        '/': 'Main landing page',
        '/health': 'Global health check',
        '/api': 'Global API overview'
    }
    
    results = {}
    
    for route, description in routes.items():
        try:
            response = client.get(route)
            status = 'PASS' if response.status_code == 200 else f'FAIL ({response.status_code})'
            results[route] = {
                'status': status,
                'description': description,
                'response_code': response.status_code
            }
            
            if response.status_code == 200:
                print(f"  ✅ {route} - {description}")
            else:
                print(f"  ❌ {route} - {description} (Status: {response.status_code})")
                
        except Exception as e:
            results[route] = {
                'status': f'ERROR: {str(e)}',
                'description': description
            }
            print(f"  ❌ {route} - Error: {e}")
    
    return results

def validate_agents_routes(client: FlaskClient):
    """Validate AI Agents routing system"""
    print("\n🤖 Testing AI Agents Routes...")
    
    routes = {
        '/agents/': 'Agents dashboard',
        '/agents/api': 'Agents API overview',
        '/agents/health': 'Agents health check',
        '/agents/analytics': 'Agents analytics',
        '/agents/strategist': 'Strategist agent detail',
        '/agents/developer': 'Developer agent detail',
        '/agents/girlfriend': 'Girlfriend agent detail'
    }
    
    return test_route_group(client, routes, "Agents")

def validate_webdev_routes(client: FlaskClient):
    """Validate Web Development routing system"""
    print("\n🌐 Testing WebDev Routes...")
    
    routes = {
        '/webdev/': 'WebDev homepage',
        '/webdev/api': 'WebDev API overview',
        '/webdev/websites': 'Website services',
        '/webdev/apps': 'Web applications',
        '/webdev/ecommerce': 'E-commerce solutions',
        '/webdev/pricing': 'Pricing page',
        '/webdev/quote': 'Quote form',
        '/webdev/health': 'WebDev health check'
    }
    
    return test_route_group(client, routes, "WebDev")

def validate_portfolio_routes(client: FlaskClient):
    """Validate Portfolio routing system"""
    print("\n💼 Testing Portfolio Routes...")
    
    routes = {
        '/portfolio/': 'Portfolio homepage',
        '/portfolio/api': 'Portfolio API overview',
        '/portfolio/about': 'About page',
        '/portfolio/projects': 'Projects showcase',
        '/portfolio/skills': 'Skills page',
        '/portfolio/achievements': 'Achievements page',
        '/portfolio/testimonials': 'Testimonials',
        '/portfolio/contact': 'Contact page',
        '/portfolio/health': 'Portfolio health check'
    }
    
    return test_route_group(client, routes, "Portfolio")

def validate_models_routes(client: FlaskClient):
    """Validate AI Models routing system"""
    print("\n🧠 Testing Models Routes...")
    
    routes = {
        '/models/': 'Models dashboard',
        '/models/api': 'Models API overview',
        '/models/health': 'Models health check',
        '/models/analytics': 'Models analytics',
        '/models/codellama': 'Code Llama model detail',
        '/models/gemma2': 'Gemma2 model detail'
    }
    
    return test_route_group(client, routes, "Models")

def test_route_group(client: FlaskClient, routes: dict, group_name: str):
    """Test a group of routes"""
    results = {}
    
    for route, description in routes.items():
        try:
            response = client.get(route)
            
            # Check for template errors or missing templates
            if response.status_code == 500:
                status = 'TEMPLATE_ERROR'
            elif response.status_code == 404:
                status = 'NOT_FOUND'
            elif response.status_code == 200:
                status = 'PASS'
            else:
                status = f'FAIL ({response.status_code})'
            
            results[route] = {
                'status': status,
                'description': description,
                'response_code': response.status_code
            }
            
            if response.status_code == 200:
                print(f"  ✅ {route} - {description}")
            elif response.status_code == 500:
                print(f"  ⚠️  {route} - {description} (Template/Server Error)")
            elif response.status_code == 404:
                print(f"  🔍 {route} - {description} (Route Not Found)")
            else:
                print(f"  ❌ {route} - {description} (Status: {response.status_code})")
                
        except Exception as e:
            results[route] = {
                'status': f'ERROR: {str(e)}',
                'description': description
            }
            print(f"  ❌ {route} - Error: {e}")
    
    return results

def print_validation_summary(results: dict):
    """Print comprehensive validation summary"""
    print("\n" + "=" * 60)
    print("📊 ROUTING VALIDATION SUMMARY")
    print("=" * 60)
    
    total_routes = 0
    passed_routes = 0
    failed_routes = 0
    template_errors = 0
    
    for service_name, service_results in results.items():
        if service_name == 'error':
            continue
            
        print(f"\n🔍 {service_name.upper().replace('_', ' ')}")
        service_passed = 0
        service_total = 0
        
        for route, route_data in service_results.items():
            status = route_data['status']
            service_total += 1
            total_routes += 1
            
            if status == 'PASS':
                service_passed += 1
                passed_routes += 1
                print(f"  ✅ {route}")
            elif status == 'TEMPLATE_ERROR':
                template_errors += 1
                print(f"  ⚠️  {route} (Template Missing)")
            else:
                failed_routes += 1
                print(f"  ❌ {route} ({status})")
        
        print(f"  📈 Service Score: {service_passed}/{service_total}")
    
    # Overall statistics
    print(f"\n📊 OVERALL STATISTICS")
    print(f"✅ Passed: {passed_routes}")
    print(f"❌ Failed: {failed_routes}")
    print(f"⚠️  Template Errors: {template_errors}")
    print(f"📁 Total Routes: {total_routes}")
    
    success_rate = (passed_routes / total_routes) * 100 if total_routes > 0 else 0
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    # Status determination
    if success_rate >= 90:
        print(f"\n🎉 EXCELLENT! Routing system is production-ready!")
    elif success_rate >= 75:
        print(f"\n✅ GOOD! Most routes working, minor issues to fix")
    elif success_rate >= 50:
        print(f"\n⚠️  PARTIAL! Significant issues need attention")
    else:
        print(f"\n❌ CRITICAL! Major routing problems detected")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if template_errors > 0:
        print(f"  📄 Create missing templates for {template_errors} routes")
    if failed_routes > 0:
        print(f"  🔧 Fix {failed_routes} broken routes")
    print(f"  📈 Continue monitoring route performance")

def validate_blueprint_imports():
    """Validate that all blueprints can be imported"""
    print("\n🔧 Testing Blueprint Imports...")
    
    blueprints = {
        'agents': 'app.routes.agents',
        'webdev': 'app.routes.webdev', 
        'portfolio': 'app.routes.portfolio',
        'models': 'app.routes.models'
    }
    
    import_results = {}
    
    for bp_name, module_path in blueprints.items():
        try:
            module = __import__(module_path, fromlist=[f'{bp_name}_bp'])
            blueprint = getattr(module, f'{bp_name}_bp')
            import_results[bp_name] = {
                'status': 'SUCCESS',
                'blueprint_name': blueprint.name,
                'url_prefix': blueprint.url_prefix
            }
            print(f"  ✅ {bp_name} blueprint imported successfully")
        except Exception as e:
            import_results[bp_name] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"  ❌ {bp_name} blueprint failed: {e}")
    
    return import_results

def main():
    """Main validation function"""
    print("🚀 Starting Comprehensive Routing System Validation")
    start_time = time.time()
    
    # Test blueprint imports first
    import_results = validate_blueprint_imports()
    
    # Test routing system
    routing_results = validate_routing_system()
    
    # Final summary
    end_time = time.time()
    print(f"\n⏱️  Validation completed in {end_time - start_time:.2f} seconds")
    
    # Save results to file
    results = {
        'timestamp': time.time(),
        'duration': end_time - start_time,
        'blueprint_imports': import_results,
        'routing_validation': routing_results
    }
    
    results_file = project_root / 'data' / 'routing_validation_results.json'
    results_file.parent.mkdir(exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"📄 Results saved to: {results_file}")

if __name__ == '__main__':
    main()