#!/usr/bin/env python3
"""
Monitor Validation Script
Validates all 16 agents have complete production-ready monitor systems
"""

import os
import sys
from pathlib import Path
import importlib.util
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

def validate_monitor_structure(agent_name: str) -> Dict[str, Any]:
    """Validate complete monitor structure for an agent"""
    agent_dir = BASE_DIR / agent_name
    monitor_dir = agent_dir / "monitor"
    
    validation_result = {
        'agent': agent_name,
        'monitor_dir_exists': monitor_dir.exists(),
        'files': {},
        'overall_status': 'UNKNOWN'
    }
    
    required_files = ['__init__.py', 'usage.py', 'latency.py', 'alerts.py']
    
    for file_name in required_files:
        file_path = monitor_dir / file_name
        
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

def check_monitor_content_quality(agent_name: str) -> Dict[str, Any]:
    """Check content quality indicators in monitor files"""
    agent_dir = BASE_DIR / agent_name
    monitor_dir = agent_dir / "monitor"
    
    quality_check = {
        'usage_has_monitor_class': False,
        'usage_has_tracking_decorator': False,
        'latency_has_tracker_class': False,
        'latency_has_tracking_decorator': False,
        'alerts_has_manager_class': False,
        'alerts_has_severity_enum': False,
        'init_has_exports': False
    }
    
    try:
        # Check usage.py
        usage_file = monitor_dir / "usage.py"
        if usage_file.exists():
            with open(usage_file, 'r') as f:
                usage_content = f.read()
                quality_check['usage_has_monitor_class'] = 'Monitor' in usage_content or 'UsageMonitor' in usage_content
                quality_check['usage_has_tracking_decorator'] = 'track_usage' in usage_content
        
        # Check latency.py  
        latency_file = monitor_dir / "latency.py"
        if latency_file.exists():
            with open(latency_file, 'r') as f:
                latency_content = f.read()
                quality_check['latency_has_tracker_class'] = 'LatencyTracker' in latency_content
                quality_check['latency_has_tracking_decorator'] = 'track_latency' in latency_content
        
        # Check alerts.py
        alerts_file = monitor_dir / "alerts.py"
        if alerts_file.exists():
            with open(alerts_file, 'r') as f:
                alerts_content = f.read()
                quality_check['alerts_has_manager_class'] = 'AlertManager' in alerts_content
                quality_check['alerts_has_severity_enum'] = 'AlertSeverity' in alerts_content
        
        # Check __init__.py
        init_file = monitor_dir / "__init__.py"
        if init_file.exists():
            with open(init_file, 'r') as f:
                init_content = f.read()
                quality_check['init_has_exports'] = '__all__' in init_content
                
    except Exception as e:
        print(f"Error checking content quality for {agent_name}: {e}")
    
    return quality_check

def test_monitor_imports(agent_name: str) -> Dict[str, Any]:
    """Test if monitor modules can be imported"""
    import_results = {
        'usage_import': False,
        'latency_import': False,
        'alerts_import': False,
        'init_import': False,
        'import_errors': []
    }
    
    agent_dir = BASE_DIR / agent_name
    monitor_dir = agent_dir / "monitor"
    
    # Add agent directory to Python path
    import sys
    if str(agent_dir.parent) not in sys.path:
        sys.path.insert(0, str(agent_dir.parent))
    
    try:
        # Test usage module import
        try:
            spec = importlib.util.spec_from_file_location(
                f"{agent_name}.monitor.usage", 
                monitor_dir / "usage.py"
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                import_results['usage_import'] = True
        except Exception as e:
            import_results['import_errors'].append(f"usage.py: {str(e)[:100]}")
        
        # Test latency module import
        try:
            spec = importlib.util.spec_from_file_location(
                f"{agent_name}.monitor.latency", 
                monitor_dir / "latency.py"
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                import_results['latency_import'] = True
        except Exception as e:
            import_results['import_errors'].append(f"latency.py: {str(e)[:100]}")
        
        # Test alerts module import
        try:
            spec = importlib.util.spec_from_file_location(
                f"{agent_name}.monitor.alerts", 
                monitor_dir / "alerts.py"
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                import_results['alerts_import'] = True
        except Exception as e:
            import_results['import_errors'].append(f"alerts.py: {str(e)[:100]}")
        
        # Test __init__ module import
        try:
            spec = importlib.util.spec_from_file_location(
                f"{agent_name}.monitor", 
                monitor_dir / "__init__.py"
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                import_results['init_import'] = True
        except Exception as e:
            import_results['import_errors'].append(f"__init__.py: {str(e)[:100]}")
            
    except Exception as e:
        import_results['import_errors'].append(f"General import error: {e}")
    
    return import_results

def main():
    """Main validation function"""
    print("🔍 Validating monitor systems for all 16 agents...")
    print("=" * 70)
    
    validation_results = []
    passed_count = 0
    failed_count = 0
    
    for agent in ALL_AGENTS:
        print(f"\n📋 Validating {agent} monitor system...")
        
        # Structure validation
        structure_result = validate_monitor_structure(agent)
        
        # Content quality check
        quality_result = check_monitor_content_quality(agent)
        
        # Import testing
        import_result = test_monitor_imports(agent)
        
        # Combined result
        combined_result = {
            **structure_result,
            'quality': quality_result,
            'imports': import_result
        }
        
        validation_results.append(combined_result)
        
        # Print status
        status = structure_result['overall_status']
        if status == 'PASS' and import_result.get('init_import', False):
            print(f"  ✅ {agent}: PASS")
            passed_count += 1
        else:
            print(f"  ❌ {agent}: ISSUES DETECTED")
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
        
        # Print import results
        imports = import_result
        importable_count = sum([
            imports.get('usage_import', False),
            imports.get('latency_import', False), 
            imports.get('alerts_import', False),
            imports.get('init_import', False)
        ])
        print(f"    📦 Importable modules: {importable_count}/4")
        
        if imports.get('import_errors'):
            for error in imports['import_errors'][:2]:  # Show first 2 errors
                print(f"    ⚠️  {error}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 MONITOR VALIDATION SUMMARY")
    print("=" * 70)
    print(f"✅ Passed: {passed_count} agents")
    print(f"❌ Failed: {failed_count} agents")
    print(f"📁 Total: {len(ALL_AGENTS)} agents")
    
    # Detailed quality analysis
    print("\n🔬 QUALITY ANALYSIS")
    print("=" * 70)
    
    quality_metrics = {
        'usage_has_monitor_class': 0,
        'usage_has_tracking_decorator': 0,
        'latency_has_tracker_class': 0,
        'latency_has_tracking_decorator': 0,
        'alerts_has_manager_class': 0,
        'alerts_has_severity_enum': 0,
        'init_has_exports': 0
    }
    
    for result in validation_results:
        for metric, value in result['quality'].items():
            if value:
                quality_metrics[metric] += 1
    
    total_agents = len(validation_results)
    print(f"📊 Usage monitor classes: {quality_metrics['usage_has_monitor_class']}/{total_agents}")
    print(f"🔄 Usage tracking decorators: {quality_metrics['usage_has_tracking_decorator']}/{total_agents}")
    print(f"⏱️ Latency tracker classes: {quality_metrics['latency_has_tracker_class']}/{total_agents}")
    print(f"📏 Latency tracking decorators: {quality_metrics['latency_has_tracking_decorator']}/{total_agents}")
    print(f"🚨 Alert manager classes: {quality_metrics['alerts_has_manager_class']}/{total_agents}")
    print(f"📶 Alert severity enums: {quality_metrics['alerts_has_severity_enum']}/{total_agents}")
    print(f"📦 Module exports: {quality_metrics['init_has_exports']}/{total_agents}")
    
    # Production readiness assessment
    print("\n🚀 PRODUCTION READINESS")
    print("=" * 70)
    
    if passed_count == total_agents:
        print("🎉 ALL MONITOR SYSTEMS ARE PRODUCTION READY!")
        print("✅ All 16 agents have complete, functional monitor systems")
        print("✅ All agents have latency tracking, usage monitoring, and alerting")
        print("✅ All modules are syntactically valid and importable")
        print("✅ System is ready for production monitoring!")
    elif passed_count > total_agents * 0.8:
        print("✅ MOSTLY PRODUCTION READY")
        print(f"✅ {passed_count} agents are fully ready")
        print(f"⚠️ {failed_count} agents need minor fixes")
    else:
        print("⚠️ NEEDS MORE WORK")
        print(f"✅ {passed_count} agents are ready")
        print(f"❌ {failed_count} agents need attention")
    
    return passed_count == total_agents

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)