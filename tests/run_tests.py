"""
Test Runner Script
Comprehensive test execution and reporting
"""

import pytest
import sys
import os
import subprocess
from pathlib import Path


def run_tests():
    """Run comprehensive test suite"""
    
    # Add project root to Python path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    print("=" * 60)
    print("🧪 COMPREHENSIVE TEST SUITE EXECUTION")
    print("=" * 60)
    
    # Test categories
    test_categories = {
        "Unit Tests": [
            "tests/conftest.py",
            "tests/test_home.py", 
            "tests/test_portfolio.py",
            "tests/test_webdev.py",
            "tests/test_ai_services.py",
            "tests/test_agents.py",
            "tests/test_payments.py"
        ],
        "Integration Tests": [
            "tests/integration/test_integration.py",
            "tests/integration/test_workflows.py"
        ]
    }
    
    overall_results = {}
    
    # Run each test category
    for category, test_files in test_categories.items():
        print(f"\n📋 Running {category}")
        print("-" * 40)
        
        # Check which test files exist
        existing_files = []
        for test_file in test_files:
            if os.path.exists(test_file):
                existing_files.append(test_file)
            else:
                print(f"⚠️  Test file not found: {test_file}")
        
        if existing_files:
            # Run pytest for existing files
            cmd = [
                "python", "-m", "pytest",
                *existing_files,
                "-v",  # Verbose output
                "--tb=short",  # Short traceback format
                "--color=yes",  # Colored output
                "--durations=10",  # Show 10 slowest tests
                "--maxfail=5",  # Stop after 5 failures
            ]
            
            try:
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=300  # 5 minute timeout
                )
                
                overall_results[category] = {
                    'returncode': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'files_tested': len(existing_files)
                }
                
                print(f"✅ {category} completed (Exit code: {result.returncode})")
                if result.returncode != 0:
                    print(f"❌ Some tests failed in {category}")
                    
            except subprocess.TimeoutExpired:
                print(f"⏱️  {category} tests timed out")
                overall_results[category] = {'timeout': True}
            except Exception as e:
                print(f"💥 Error running {category}: {e}")
                overall_results[category] = {'error': str(e)}
        else:
            print(f"📂 No test files found for {category}")
            overall_results[category] = {'no_files': True}
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST EXECUTION SUMMARY")
    print("=" * 60)
    
    total_categories = len(test_categories)
    successful_categories = 0
    
    for category, result in overall_results.items():
        print(f"\n📋 {category}:")
        
        if 'returncode' in result:
            if result['returncode'] == 0:
                print(f"   ✅ PASSED ({result['files_tested']} files)")
                successful_categories += 1
            else:
                print(f"   ❌ FAILED ({result['files_tested']} files)")
        elif 'timeout' in result:
            print(f"   ⏱️  TIMEOUT")
        elif 'error' in result:
            print(f"   💥 ERROR: {result['error']}")
        elif 'no_files' in result:
            print(f"   📂 NO FILES FOUND")
    
    print(f"\n🏆 Overall Success Rate: {successful_categories}/{total_categories} categories")
    
    # Detailed output for failures
    print("\n" + "=" * 60)
    print("📝 DETAILED RESULTS")
    print("=" * 60)
    
    for category, result in overall_results.items():
        if 'returncode' in result and result['returncode'] != 0:
            print(f"\n❌ {category} Failures:")
            print("-" * 30)
            print(result['stdout'])
            if result['stderr']:
                print("STDERR:")
                print(result['stderr'])
    
    return overall_results


def run_specific_tests(test_pattern):
    """Run specific tests matching a pattern"""
    print(f"🎯 Running tests matching pattern: {test_pattern}")
    
    cmd = [
        "python", "-m", "pytest",
        "-k", test_pattern,
        "-v",
        "--tb=short",
        "--color=yes"
    ]
    
    result = subprocess.run(cmd)
    return result.returncode


def run_coverage_analysis():
    """Run test coverage analysis"""
    print("📊 Running test coverage analysis...")
    
    try:
        # Install coverage if not available
        subprocess.run([sys.executable, "-m", "pip", "install", "coverage"], 
                      capture_output=True)
        
        # Run tests with coverage
        cmd = [
            "python", "-m", "coverage", "run", 
            "-m", "pytest", "tests/",
            "--quiet"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Generate coverage report
            report_cmd = ["python", "-m", "coverage", "report", "-m"]
            report_result = subprocess.run(report_cmd, capture_output=True, text=True)
            
            print("📈 Coverage Report:")
            print(report_result.stdout)
        else:
            print("❌ Coverage analysis failed")
            print(result.stderr)
            
    except Exception as e:
        print(f"💥 Coverage analysis error: {e}")


def run_performance_tests():
    """Run performance-focused tests"""
    print("🚀 Running performance tests...")
    
    cmd = [
        "python", "-m", "pytest",
        "-k", "performance",
        "-v",
        "--tb=short"
    ]
    
    result = subprocess.run(cmd)
    return result.returncode


def run_security_tests():
    """Run security-focused tests"""
    print("🔒 Running security tests...")
    
    cmd = [
        "python", "-m", "pytest", 
        "-k", "security",
        "-v",
        "--tb=short"
    ]
    
    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "all":
            run_tests()
        elif command == "coverage":
            run_coverage_analysis()
        elif command == "performance":
            run_performance_tests()
        elif command == "security":
            run_security_tests()
        elif command.startswith("pattern="):
            pattern = command.split("=", 1)[1]
            run_specific_tests(pattern)
        else:
            print("Usage:")
            print("  python run_tests.py all          - Run all tests")
            print("  python run_tests.py coverage     - Run with coverage")
            print("  python run_tests.py performance  - Run performance tests")
            print("  python run_tests.py security     - Run security tests")
            print("  python run_tests.py pattern=NAME - Run tests matching pattern")
    else:
        # Default: run all tests
        run_tests()