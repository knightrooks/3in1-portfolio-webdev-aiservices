#!/usr/bin/env python3
"""
Comprehensive HTTP Endpoint Verification Script
Tests all pages, subpages, and API endpoints to verify 200 status codes or identify errors
"""

import requests
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:3000"
MAX_WORKERS = 5
REQUEST_TIMEOUT = 30
RESULTS_FILE = "endpoint_verification_results.json"

# Comprehensive list of endpoints to test
ENDPOINTS_TO_TEST = {
    # Core Application Routes
    "main": [
        "/",
        "/health",
        "/api/health", 
        "/status",
    ],
    
    # Portfolio Routes
    "portfolio": [
        "/portfolio",
        "/portfolio/",
        "/portfolio/about",
        "/portfolio/projects", 
        "/portfolio/skills",
        "/portfolio/contact",
        "/portfolio/testimonials",
    ],
    
    # WebDev Service Routes
    "webdev": [
        "/webdev",
        "/webdev/",
        "/webdev/services",
        "/webdev/pricing",
        "/webdev/quote",
        "/webdev/custom",
        "/webdev/ecommerce", 
        "/webdev/marketing",
        "/webdev/seo",
        "/webdev/maintenance",
        "/webdev/contact",
    ],
    
    # AI Agent Routes
    "agents": [
        "/agents",
        "/agents/",
        "/agents/emotionaljenny",
        "/agents/strictwife",
        "/agents/gossipqueen", 
        "/agents/lazyjohn",
        "/agents/girlfriend",
        "/agents/coderbot",
        "/agents/developer",
        "/agents/strategist",
        "/agents/security_expert",
        "/agents/data_scientist", 
        "/agents/marketing_specialist",
        "/agents/operations_manager",
        "/agents/content_creator",
        "/agents/product_manager", 
        "/agents/customer_success",
        "/agents/research_analyst",
    ],
    
    # Agent API Endpoints 
    "agent_apis": [
        "/agents/emotionaljenny/chat",
        "/agents/emotionaljenny/speak",
        "/agents/emotionaljenny/voice",
        "/agents/strictwife/chat",
        "/agents/strictwife/speak", 
        "/agents/gossipqueen/chat",
        "/agents/lazyjohn/chat",
        "/agents/girlfriend/chat",
        "/agents/coderbot/chat",
        "/agents/developer/chat",
        "/agents/strategist/chat",
        "/agents/security_expert/chat",
        "/agents/data_scientist/chat",
        "/agents/marketing_specialist/chat",
        "/agents/operations_manager/chat", 
        "/agents/content_creator/chat",
        "/agents/product_manager/chat",
        "/agents/customer_success/chat",
        "/agents/research_analyst/chat",
    ],
    
    # AI Services Routes
    "ai_services": [
        "/ai_services",
        "/ai_services/",
        "/ai_services/chat",
        "/ai_services/models",
        "/ai_services/analytics",
    ],
    
    # Models Management
    "models": [
        "/models",
        "/models/",
        "/models/dashboard",
        "/models/deepseek-coder",
        "/models/llama3.2",
        "/models/gemma2", 
        "/models/mistral",
        "/models/qwen2.5",
        "/models/phi3",
    ],
    
    # Authentication Routes  
    "auth": [
        "/auth/login",
        "/auth/register",
        "/auth/logout",
    ],
    
    # API Routes
    "api": [
        "/api/v1/status",
        "/api/v1/health",
        "/api/agents/list",
        "/api/models/list",
    ],
    
    # Static Assets (sample)
    "static": [
        "/static/css/style.css",
        "/static/js/main.js", 
        "/static/images/logo.png",
        "/favicon.ico",
    ]
}

class EndpointVerifier:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.results = defaultdict(list)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EndpointVerifier/1.0 (Testing)'
        })
    
    def test_endpoint(self, endpoint_path, method="GET"):
        """Test a single endpoint"""
        url = f"{self.base_url}{endpoint_path}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            elif method.upper() == "POST":
                response = self.session.post(url, timeout=REQUEST_TIMEOUT, json={})
            else:
                response = self.session.request(method, url, timeout=REQUEST_TIMEOUT)
            
            result = {
                "endpoint": endpoint_path,
                "method": method,
                "status_code": response.status_code,
                "success": 200 <= response.status_code < 400,
                "response_time": response.elapsed.total_seconds(),
                "content_length": len(response.content),
                "content_type": response.headers.get('content-type', ''),
                "error": None,
                "redirect_url": response.url if response.url != url else None
            }
            
            # Additional checks
            if response.status_code == 404:
                result["error"] = "Page not found"
            elif response.status_code == 500:
                result["error"] = "Internal server error" 
            elif response.status_code == 403:
                result["error"] = "Access forbidden"
            elif response.status_code >= 400:
                result["error"] = f"HTTP {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            result = {
                "endpoint": endpoint_path,
                "method": method, 
                "status_code": None,
                "success": False,
                "response_time": None,
                "content_length": 0,
                "content_type": "",
                "error": "Connection refused - server not running",
                "redirect_url": None
            }
        except requests.exceptions.Timeout:
            result = {
                "endpoint": endpoint_path,
                "method": method,
                "status_code": None, 
                "success": False,
                "response_time": REQUEST_TIMEOUT,
                "content_length": 0,
                "content_type": "",
                "error": f"Timeout after {REQUEST_TIMEOUT}s",
                "redirect_url": None
            }
        except Exception as e:
            result = {
                "endpoint": endpoint_path,
                "method": method,
                "status_code": None,
                "success": False,
                "response_time": None,
                "content_length": 0, 
                "content_type": "",
                "error": str(e),
                "redirect_url": None
            }
        
        return result
    
    def verify_all_endpoints(self):
        """Verify all endpoints with concurrent requests"""
        print(f"🔍 Starting endpoint verification for {self.base_url}")
        print(f"📊 Testing {sum(len(endpoints) for endpoints in ENDPOINTS_TO_TEST.values())} endpoints...")
        print()
        
        all_endpoints = []
        for category, endpoints in ENDPOINTS_TO_TEST.items():
            for endpoint in endpoints:
                all_endpoints.append((category, endpoint))
        
        # Test server connectivity first
        print("🌐 Testing server connectivity...")
        connectivity_result = self.test_endpoint("/")
        if not connectivity_result["success"] and connectivity_result["error"] == "Connection refused - server not running":
            print("❌ Server is not running! Please start the Flask server first:")
            print(f"   python manage.py")
            return False
        
        successful_tests = 0
        failed_tests = 0
        
        # Use ThreadPoolExecutor for concurrent testing
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit all endpoint tests
            future_to_endpoint = {}
            for category, endpoint in all_endpoints:
                future = executor.submit(self.test_endpoint, endpoint)
                future_to_endpoint[future] = (category, endpoint)
            
            # Process completed tests
            for future in as_completed(future_to_endpoint):
                category, endpoint = future_to_endpoint[future]
                try:
                    result = future.result()
                    self.results[category].append(result)
                    
                    # Print result
                    if result["success"]:
                        print(f"✅ {endpoint:<40} → {result['status_code']} ({result['response_time']:.2f}s)")
                        successful_tests += 1
                    else:
                        print(f"❌ {endpoint:<40} → {result['error'] or result['status_code']}")
                        failed_tests += 1
                        
                except Exception as e:
                    print(f"💥 {endpoint:<40} → Exception: {str(e)}")
                    failed_tests += 1
        
        print()
        print(f"📈 Test Results Summary:")
        print(f"   ✅ Successful: {successful_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   📊 Total: {successful_tests + failed_tests}")
        print(f"   📈 Success Rate: {successful_tests/(successful_tests + failed_tests)*100:.1f}%")
        
        return True
    
    def generate_report(self):
        """Generate detailed report"""
        print("\n" + "="*80)
        print("📋 DETAILED ENDPOINT VERIFICATION REPORT")
        print("="*80)
        
        for category, results in self.results.items():
            print(f"\n🔧 {category.upper()} ENDPOINTS:")
            print("-" * 50)
            
            success_count = sum(1 for r in results if r["success"])
            total_count = len(results)
            
            print(f"Status: {success_count}/{total_count} successful ({success_count/total_count*100:.1f}%)")
            print()
            
            for result in results:
                status_icon = "✅" if result["success"] else "❌"
                status_code = result["status_code"] or "ERR"
                response_time = f"{result['response_time']:.2f}s" if result["response_time"] else "N/A"
                
                print(f"{status_icon} {result['endpoint']:<35} [{status_code}] {response_time}")
                
                if result["error"]:
                    print(f"   💬 Error: {result['error']}")
                if result["redirect_url"]:
                    print(f"   ↗️  Redirected to: {result['redirect_url']}")
                    
        print("\n" + "="*80)
    
    def save_results(self):
        """Save results to JSON file"""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "total_endpoints": sum(len(results) for results in self.results.values()),
            "successful_endpoints": sum(sum(1 for r in results if r["success"]) for results in self.results.values()),
            "results": dict(self.results)
        }
        
        try:
            with open(RESULTS_FILE, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            print(f"💾 Results saved to {RESULTS_FILE}")
        except Exception as e:
            print(f"❌ Failed to save results: {e}")


def main():
    print("🚀 HTTP Endpoint Verification Tool")
    print("=" * 50)
    
    # Check if server is specified
    base_url = sys.argv[1] if len(sys.argv) > 1 else BASE_URL
    
    print(f"🎯 Target: {base_url}")
    print(f"⚙️  Timeout: {REQUEST_TIMEOUT}s")
    print(f"🔄 Workers: {MAX_WORKERS}")
    print()
    
    verifier = EndpointVerifier(base_url)
    
    # Run verification
    if verifier.verify_all_endpoints():
        verifier.generate_report()
        verifier.save_results()
        
        # Calculate exit code
        total_tests = sum(len(results) for results in verifier.results.values())
        failed_tests = sum(sum(1 for r in results if not r["success"]) for results in verifier.results.values())
        
        if failed_tests > 0:
            print(f"\n⚠️  {failed_tests} endpoints failed - check server logs for details")
            sys.exit(1)
        else:
            print(f"\n🎉 All endpoints verified successfully!")
            sys.exit(0)
    else:
        print("❌ Verification failed - server not accessible")
        sys.exit(1)


if __name__ == "__main__":
    main()