#!/usr/bin/env python3
"""
Simple Flask 3-in-1 Platform Runner
Testing application structure without complex dependencies
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from app import create_app
    print("✅ Successfully imported app module")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Creating minimal Flask app instead...")
    
    class MockConfig:
        SECRET_KEY = 'dev-key'
        DEBUG = True
    
    class MockApp:
        def __init__(self):
            self.config = MockConfig()
            
        def run(self, debug=True, port=5000):
            print(f"🚀 Mock app would run on port {port}")
            print("📂 Project structure exists:")
            self.show_structure()
            
        def show_structure(self):
            """Show project structure"""
            key_paths = [
                'app/__init__.py',
                'app/routes/home.py',
                'app/routes/agents.py', 
                'app/routes/ai_services.py',
                'app/routes/portfolio.py',
                'app/routes/webdev.py',
                'app/templates/',
                'app/static/',
                'agents/',
                'models/',
                'README.md',
                'TODO.md'
            ]
            
            for path in key_paths:
                full_path = project_root / path
                if full_path.exists():
                    print(f"  ✅ {path}")
                else:
                    print(f"  ❌ {path} (missing)")

if __name__ == '__main__':
    try:
        app = create_app()
        print("✅ Flask app created successfully")
        print("🏗️ 3-in-1 Platform Ready:")
        print("   1. Portfolio Section")
        print("   2. Web Development Services")
        print("   3. AI Services Hub")
        app.run(debug=True)
    except:
        print("Using mock app for testing...")
        mock_app = MockApp()
        mock_app.run()