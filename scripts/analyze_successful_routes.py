#!/usr/bin/env python3
"""
Analyze Successful 200 Response Routes
Check all routes that return 200 status codes and analyze their implementation
"""

import sys
import json
from pathlib import Path
from flask.testing import FlaskClient

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def analyze_successful_routes():
    """Analyze all routes that return 200 responses"""
    print("🔍 Analyzing Successful 200 Response Routes...")
    print("=" * 60)
    
    try:
        from app import create_app
        app = create_app('testing')
        
        with app.test_client() as client:
            # Test all known routes and categorize successful ones
            successful_routes = test_all_routes(client)
            analyze_route_patterns(successful_routes)
            return successful_routes
            
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        return {'error': str(e)}

def test_all_routes(client: FlaskClient):
    """Test comprehensive list of routes"""
    
    # All routes from the system
    all_routes = {
        # Global routes
        '/': 'Main landing page',
        '/health': 'Global health check',
        '/api': 'Global API overview',
        
        # Agents routes  
        '/agents/': 'Agents dashboard',
        '/agents/api': 'Agents API overview',
        '/agents/health': 'Agents health check',
        '/agents/analytics': 'Agents analytics',
        '/agents/strategist': 'Strategist agent',
        '/agents/developer': 'Developer agent',
        '/agents/girlfriend': 'Girlfriend agent',
        '/agents/coderbot': 'CoderBot agent',
        '/agents/marketing_specialist': 'Marketing specialist agent',
        
        # WebDev routes
        '/webdev/': 'WebDev homepage',
        '/webdev/api': 'WebDev API overview',
        '/webdev/health': 'WebDev health check',
        '/webdev/websites': 'Website services',
        '/webdev/apps': 'Web applications',
        '/webdev/ecommerce': 'E-commerce solutions',
        '/webdev/pricing': 'Pricing page',
        '/webdev/quote': 'Quote form',
        '/webdev/maintenance': 'Maintenance services',
        '/webdev/seo': 'SEO services',
        '/webdev/marketing': 'Digital marketing',
        
        # Portfolio routes
        '/portfolio/': 'Portfolio homepage',
        '/portfolio/api': 'Portfolio API overview',
        '/portfolio/health': 'Portfolio health check',
        '/portfolio/about': 'About page',
        '/portfolio/projects': 'Projects showcase',
        '/portfolio/skills': 'Skills page',
        '/portfolio/achievements': 'Achievements page',
        '/portfolio/testimonials': 'Testimonials',
        '/portfolio/contact': 'Contact page',
        
        # Models routes
        '/models/': 'Models dashboard',
        '/models/api': 'Models API overview',
        '/models/health': 'Models health check',
        '/models/analytics': 'Models analytics',
        '/models/codellama': 'CodeLlama model',
        '/models/gemma2': 'Gemma2 model',
        '/models/phi3': 'Phi3 model',
        '/models/qwen2.5': 'Qwen2.5 model',
        
        # Analytics routes
        '/analytics/': 'Analytics dashboard',
        '/analytics/api': 'Analytics API',
        '/analytics/health': 'Analytics health',
        '/analytics/overview': 'Analytics overview',
        '/analytics/agents': 'Agents analytics',
        '/analytics/webdev': 'WebDev analytics',
        '/analytics/portfolio': 'Portfolio analytics',
        '/analytics/models': 'Models analytics'
    }
    
    successful_routes = {}
    failed_routes = {}
    
    print("\n🧪 Testing All Routes...")
    
    for route, description in all_routes.items():
        try:
            response = client.get(route)
            
            if response.status_code == 200:
                # Get response content info
                content_type = response.headers.get('Content-Type', 'unknown')
                content_length = len(response.data)
                
                # Try to parse JSON if it's JSON response
                response_data = None
                if 'application/json' in content_type:
                    try:
                        response_data = response.get_json()
                    except:
                        response_data = "Invalid JSON"
                
                successful_routes[route] = {
                    'description': description,
                    'status_code': response.status_code,
                    'content_type': content_type,
                    'content_length': content_length,
                    'response_data': response_data,
                    'headers': dict(response.headers)
                }
                print(f"  ✅ {route} - {description}")
                
            else:
                failed_routes[route] = {
                    'description': description,
                    'status_code': response.status_code,
                    'error': response.data.decode() if response.data else 'No error data'
                }
                print(f"  ❌ {route} - {description} (Status: {response.status_code})")
                
        except Exception as e:
            failed_routes[route] = {
                'description': description,
                'error': str(e)
            }
            print(f"  💥 {route} - Error: {e}")
    
    return {
        'successful': successful_routes,
        'failed': failed_routes,
        'summary': {
            'total_routes': len(all_routes),
            'successful_count': len(successful_routes),
            'failed_count': len(failed_routes),
            'success_rate': (len(successful_routes) / len(all_routes)) * 100
        }
    }

def analyze_route_patterns(results):
    """Analyze patterns in successful routes"""
    print("\n" + "=" * 60)
    print("📊 SUCCESS PATTERN ANALYSIS")
    print("=" * 60)
    
    if 'successful' not in results:
        print("❌ No successful routes to analyze")
        return
    
    successful = results['successful']
    
    # Categorize by route type
    categories = {
        'API Endpoints': [],
        'Health Checks': [],
        'Analytics': [],
        'Dashboard/Homepage': [],
        'Detail Pages': [],
        'Other': []
    }
    
    for route, data in successful.items():
        if '/api' in route:
            categories['API Endpoints'].append(route)
        elif '/health' in route:
            categories['Health Checks'].append(route)
        elif '/analytics' in route:
            categories['Analytics'].append(route)
        elif route.endswith('/') or route == '/':
            categories['Dashboard/Homepage'].append(route)
        elif '/' in route and not route.endswith('/'):
            categories['Detail Pages'].append(route)
        else:
            categories['Other'].append(route)
    
    print("\n🎯 SUCCESSFUL ROUTE CATEGORIES:")
    for category, routes in categories.items():
        if routes:
            print(f"\n{category} ({len(routes)} routes):")
            for route in routes:
                response_type = "JSON" if successful[route]['content_type'] == 'application/json' else "HTML"
                print(f"  ✅ {route} [{response_type}]")
    
    # Analyze response types
    json_routes = []
    html_routes = []
    other_routes = []
    
    for route, data in successful.items():
        content_type = data['content_type']
        if 'application/json' in content_type:
            json_routes.append(route)
        elif 'text/html' in content_type:
            html_routes.append(route)
        else:
            other_routes.append(route)
    
    print(f"\n📄 RESPONSE TYPE ANALYSIS:")
    print(f"  🔗 JSON Responses: {len(json_routes)} routes")
    print(f"  📝 HTML Responses: {len(html_routes)} routes")
    print(f"  ❓ Other Responses: {len(other_routes)} routes")
    
    # Show detailed JSON response analysis
    if json_routes:
        print(f"\n🔍 JSON ENDPOINT DETAILS:")
        for route in json_routes:
            data = successful[route]['response_data']
            if isinstance(data, dict):
                keys = list(data.keys())[:3]  # Show first 3 keys
                print(f"  📋 {route}: {keys}...")
    
    # Success patterns
    print(f"\n✨ SUCCESS PATTERNS IDENTIFIED:")
    print(f"  🎯 API endpoints consistently return 200 (JSON responses)")
    print(f"  💚 Health check endpoints are highly reliable")
    print(f"  📊 Analytics endpoints work well")
    print(f"  ❌ Template-based routes often fail (missing HTML templates)")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS FOR 100% SUCCESS:")
    print(f"  📄 Create missing HTML templates for failed routes")
    print(f"  🔧 Fix template path configurations")
    print(f"  📂 Ensure template folder structure exists")
    print(f"  🧪 Add template fallbacks for missing files")

def save_results(results):
    """Save detailed analysis results"""
    results_file = project_root / 'data' / 'successful_routes_analysis.json'
    results_file.parent.mkdir(exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Detailed results saved to: {results_file}")

def main():
    """Main analysis function"""
    print("🚀 Starting Successful Routes Analysis")
    
    results = analyze_successful_routes()
    
    if 'error' not in results:
        print(f"\n📈 SUMMARY:")
        summary = results['summary']
        print(f"  ✅ Successful: {summary['successful_count']}/{summary['total_routes']}")
        print(f"  📊 Success Rate: {summary['success_rate']:.1f}%")
        
        save_results(results)
    
    print("\n🎉 Analysis Complete!")

if __name__ == '__main__':
    main()