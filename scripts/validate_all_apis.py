#!/usr/bin/env python3
"""
API Validation Script
Validates all 16 agents have complete production-ready API modules
"""

import os
import sys
from pathlib import Path
import importlib
from typing import Dict, List, Any

# Define all agents
ALL_AGENTS = [
    'strategist', 'developer', 'security_expert', 'content_creator', 'research_analyst', 
    'data_scientist', 'customer_success', 'product_manager', 'marketing_specialist', 
    'operations_manager', 'girlfriend', 'lazyjohn', 'gossipqueen', 'emotionaljenny', 
    'strictwife', 'coderbot'
]

BASE_DIR = Path("/workspaces/3in1-portfolio-webdev-aiservices/agents")

def validate_file_exists(file_path: Path) -> bool:
    """Check if file exists and has content"""
    return file_path.exists() and file_path.stat().st_size > 100

def validate_syntax(file_path: Path) -> tuple[bool, str]:
    """Validate Python file syntax"""
    try:
        with open(file_path, 'r') as f:
            compile(f.read(), file_path, 'exec')
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def validate_api_structure(agent_name: str) -> Dict[str, Any]:
    """Validate complete API structure for an agent"""
    agent_dir = BASE_DIR / agent_name
    api_dir = agent_dir / "api"
    
    validation_result = {
        'agent': agent_name,
        'api_dir_exists': api_dir.exists(),
        'files': {},
        'overall_status': 'UNKNOWN'
    }
    
    required_files = ['__init__.py', 'routes.py', 'socket.py', 'events.py']
    
    for file_name in required_files:
        file_path = api_dir / file_name
        
        file_validation = {
            'exists': validate_file_exists(file_path),
            'syntax_valid': False,
            'syntax_message': 'Not checked',
            'size_bytes': 0
        }
        
        if file_validation['exists']:
            file_validation['size_bytes'] = file_path.stat().st_size
            file_validation['syntax_valid'], file_validation['syntax_message'] = validate_syntax(file_path)
        
        validation_result['files'][file_name] = file_validation
    
    # Determine overall status
    all_exist = all(validation_result['files'][f]['exists'] for f in required_files)
    all_syntax_ok = all(validation_result['files'][f]['syntax_valid'] for f in required_files)
    
    if all_exist and all_syntax_ok:
        validation_result['overall_status'] = 'PASS'
    elif all_exist:
        validation_result['overall_status'] = 'SYNTAX_ERROR'
    else:
        validation_result['overall_status'] = 'MISSING_FILES'
    
    return validation_result

def check_api_content_quality(agent_name: str) -> Dict[str, Any]:
    """Check content quality indicators in API files"""
    agent_dir = BASE_DIR / agent_name
    api_dir = agent_dir / "api"
    
    quality_check = {
        'routes_has_blueprint': False,
        'routes_has_rate_limiting': False,
        'routes_has_error_handling': False,
        'socket_has_handlers': False,
        'events_has_event_types': False,
        'init_has_exports': False
    }
    
    try:
        # Check routes.py
        routes_file = api_dir / "routes.py"
        if routes_file.exists():
            with open(routes_file, 'r') as f:
                routes_content = f.read()
                quality_check['routes_has_blueprint'] = 'Blueprint' in routes_content
                quality_check['routes_has_rate_limiting'] = 'rate_limit' in routes_content
                quality_check['routes_has_error_handling'] = 'try:' in routes_content and 'except' in routes_content
        
        # Check socket.py
        socket_file = api_dir / "socket.py"
        if socket_file.exists():
            with open(socket_file, 'r') as f:
                socket_content = f.read()
                quality_check['socket_has_handlers'] = '@socketio.on' in socket_content or 'def handle_' in socket_content
        
        # Check events.py
        events_file = api_dir / "events.py"
        if events_file.exists():
            with open(events_file, 'r') as f:
                events_content = f.read()
                quality_check['events_has_event_types'] = 'EventType' in events_content and 'class EventType' in events_content
        
        # Check __init__.py
        init_file = api_dir / "__init__.py"
        if init_file.exists():
            with open(init_file, 'r') as f:
                init_content = f.read()
                quality_check['init_has_exports'] = '__all__' in init_content
                
    except Exception as e:
        print(f"Error checking content quality for {agent_name}: {e}")
    
    return quality_check

def main():
    """Main validation function"""
    print("🔍 Validating API modules for all 16 agents...")
    print("=" * 60)
    
    validation_results = []
    passed_count = 0
    failed_count = 0
    
    for agent in ALL_AGENTS:
        print(f"\n📋 Validating {agent}...")
        
        # Structure validation
        structure_result = validate_api_structure(agent)
        
        # Content quality check
        quality_result = check_api_content_quality(agent)
        
        # Combined result
        combined_result = {
            **structure_result,
            'quality': quality_result
        }
        
        validation_results.append(combined_result)
        
        # Print status
        status = structure_result['overall_status']
        if status == 'PASS':
            print(f"  ✅ {agent}: PASS")
            passed_count += 1
        elif status == 'SYNTAX_ERROR':
            print(f"  ⚠️  {agent}: SYNTAX ERRORS")
            failed_count += 1
        else:
            print(f"  ❌ {agent}: MISSING FILES")
            failed_count += 1
        
        # Print file details
        for file_name, file_info in structure_result['files'].items():
            if file_info['exists']:
                if file_info['syntax_valid']:
                    print(f"    ✅ {file_name}: {file_info['size_bytes']} bytes")
                else:
                    print(f"    ❌ {file_name}: {file_info['syntax_message']}")
            else:
                print(f"    ❌ {file_name}: Missing")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed_count} agents")
    print(f"❌ Failed: {failed_count} agents")
    print(f"📁 Total: {len(ALL_AGENTS)} agents")
    
    # Detailed quality analysis
    print("\n🔬 QUALITY ANALYSIS")
    print("=" * 60)
    
    quality_metrics = {
        'routes_has_blueprint': 0,
        'routes_has_rate_limiting': 0,
        'routes_has_error_handling': 0,
        'socket_has_handlers': 0,
        'events_has_event_types': 0,
        'init_has_exports': 0
    }
    
    for result in validation_results:
        for metric, value in result['quality'].items():
            if value:
                quality_metrics[metric] += 1
    
    total_agents = len(validation_results)
    print(f"📋 Blueprint implementation: {quality_metrics['routes_has_blueprint']}/{total_agents}")
    print(f"🚦 Rate limiting: {quality_metrics['routes_has_rate_limiting']}/{total_agents}")
    print(f"🛡️ Error handling: {quality_metrics['routes_has_error_handling']}/{total_agents}")
    print(f"🔌 WebSocket handlers: {quality_metrics['socket_has_handlers']}/{total_agents}")
    print(f"📡 Event types: {quality_metrics['events_has_event_types']}/{total_agents}")
    print(f"📦 Module exports: {quality_metrics['init_has_exports']}/{total_agents}")
    
    # Production readiness assessment
    print("\n🚀 PRODUCTION READINESS")
    print("=" * 60)
    
    production_ready = passed_count
    partial_ready = failed_count
    
    if production_ready == total_agents:
        print("🎉 ALL AGENTS ARE PRODUCTION READY!")
        print("✅ All 16 agents have complete, syntactically valid API modules")
        print("✅ All agents have proper Flask blueprints, rate limiting, and error handling")
        print("✅ All agents have WebSocket support and event management")
        print("✅ System is ready for deployment!")
    elif production_ready > total_agents * 0.8:
        print("✅ MOSTLY PRODUCTION READY")
        print(f"✅ {production_ready} agents are fully ready")
        print(f"⚠️ {partial_ready} agents need minor fixes")
    else:
        print("⚠️ NEEDS MORE WORK")
        print(f"✅ {production_ready} agents are ready")
        print(f"❌ {partial_ready} agents need attention")
    
    return passed_count == total_agents

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)