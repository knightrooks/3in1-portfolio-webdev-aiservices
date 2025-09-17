#!/usr/bin/env python3
"""
Agent Migration Script
Moves all agent content from app/ai/agents/<agent_name> to agents/<agent_name>
Merges content intelligently and removes duplicates
"""

import os
import shutil
import json
from pathlib import Path
from typing import List, Dict, Any

# Base directories
SOURCE_DIR = Path("/workspaces/3in1-portfolio-webdev-aiservices/app/ai/agents")
TARGET_DIR = Path("/workspaces/3in1-portfolio-webdev-aiservices/agents")

def get_agents_in_source() -> List[str]:
    """Get list of agents in source directory"""
    agents = []
    for item in SOURCE_DIR.iterdir():
        if item.is_dir() and item.name not in ['__pycache__', '.git']:
            agents.append(item.name)
    return sorted(agents)

def merge_yaml_files(source_file: Path, target_file: Path):
    """Merge YAML configuration files"""
    import yaml
    
    try:
        # Load source
        with open(source_file, 'r') as f:
            source_data = yaml.safe_load(f) or {}
            
        # Load target if exists
        target_data = {}
        if target_file.exists():
            with open(target_file, 'r') as f:
                target_data = yaml.safe_load(f) or {}
        
        # Merge (source takes precedence for conflicts)
        merged_data = {**target_data, **source_data}
        
        # Write merged data
        with open(target_file, 'w') as f:
            yaml.dump(merged_data, f, default_flow_style=False, indent=2)
            
        print(f"    ✅ Merged YAML: {source_file.name}")
        
    except Exception as e:
        print(f"    ⚠️ YAML merge failed for {source_file.name}: {e}")
        # Fallback to copy
        shutil.copy2(source_file, target_file)

def merge_json_files(source_file: Path, target_file: Path):
    """Merge JSON configuration files"""
    try:
        # Load source
        with open(source_file, 'r') as f:
            source_data = json.load(f)
            
        # Load target if exists
        target_data = {}
        if target_file.exists():
            with open(target_file, 'r') as f:
                target_data = json.load(f)
        
        # Merge (source takes precedence)
        merged_data = {**target_data, **source_data}
        
        # Write merged data
        with open(target_file, 'w') as f:
            json.dump(merged_data, f, indent=2)
            
        print(f"    ✅ Merged JSON: {source_file.name}")
        
    except Exception as e:
        print(f"    ⚠️ JSON merge failed for {source_file.name}: {e}")
        # Fallback to copy
        shutil.copy2(source_file, target_file)

def should_overwrite_file(source_file: Path, target_file: Path) -> bool:
    """Determine if source file should overwrite target"""
    
    # Always merge config files
    if source_file.suffix in ['.yaml', '.yml']:
        return False  # Will be handled by merge_yaml_files
    if source_file.suffix == '.json':
        return False  # Will be handled by merge_json_files
    
    # For Python files, check if target is just a stub
    if source_file.suffix == '.py' and target_file.exists():
        try:
            with open(target_file, 'r') as f:
                target_content = f.read().strip()
            
            # If target is just a TODO stub or very small, overwrite
            if (len(target_content) < 200 or 
                'TODO:' in target_content or 
                '# TODO' in target_content or
                target_content.count('\n') < 10):
                return True
            
            # Check source file size - if significantly larger, prefer source
            with open(source_file, 'r') as f:
                source_content = f.read().strip()
            
            if len(source_content) > len(target_content) * 2:
                return True
                
        except Exception:
            pass
    
    # Default: overwrite if target doesn't exist
    return not target_file.exists()

def copy_directory_contents(source_dir: Path, target_dir: Path, agent_name: str):
    """Recursively copy directory contents with intelligent merging"""
    
    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)
    
    for source_item in source_dir.iterdir():
        if source_item.name.startswith('.'):
            continue
            
        target_item = target_dir / source_item.name
        
        if source_item.is_dir():
            # Recursively copy directories
            copy_directory_contents(source_item, target_item, agent_name)
            
        elif source_item.is_file():
            # Handle file copying/merging
            if source_item.suffix in ['.yaml', '.yml']:
                target_item.parent.mkdir(parents=True, exist_ok=True)
                merge_yaml_files(source_item, target_item)
                
            elif source_item.suffix == '.json':
                target_item.parent.mkdir(parents=True, exist_ok=True)
                merge_json_files(source_item, target_item)
                
            elif should_overwrite_file(source_item, target_item):
                target_item.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_item, target_item)
                
                action = "Created" if not target_item.exists() else "Overwrote"
                print(f"    ✅ {action}: {source_item.relative_to(source_dir)}")
                
            else:
                print(f"    ⏭️ Skipped (exists): {source_item.relative_to(source_dir)}")

def migrate_agent(agent_name: str) -> bool:
    """Migrate a single agent from source to target"""
    source_agent_dir = SOURCE_DIR / agent_name
    target_agent_dir = TARGET_DIR / agent_name
    
    if not source_agent_dir.exists():
        print(f"  ❌ Source not found: {source_agent_dir}")
        return False
    
    print(f"  📁 Source: {source_agent_dir}")
    print(f"  📁 Target: {target_agent_dir}")
    
    try:
        # Copy all contents
        copy_directory_contents(source_agent_dir, target_agent_dir, agent_name)
        return True
        
    except Exception as e:
        print(f"  ❌ Migration failed: {e}")
        return False

def cleanup_source_directory():
    """Remove the source agents directory after successful migration"""
    try:
        print(f"\n🗑️ Cleaning up source directory: {SOURCE_DIR}")
        shutil.rmtree(SOURCE_DIR)
        print("✅ Source directory removed successfully")
    except Exception as e:
        print(f"❌ Failed to remove source directory: {e}")

def main():
    """Main migration function"""
    print("🚀 Starting agent migration from app/ai/agents to agents/")
    print("=" * 70)
    
    # Get list of agents to migrate
    agents = get_agents_in_source()
    print(f"Found {len(agents)} agents to migrate: {', '.join(agents)}")
    print()
    
    success_count = 0
    failed_count = 0
    
    # Migrate each agent
    for agent_name in agents:
        print(f"🔄 Migrating {agent_name}...")
        
        if migrate_agent(agent_name):
            success_count += 1
            print(f"  ✅ {agent_name} migrated successfully\n")
        else:
            failed_count += 1
            print(f"  ❌ {agent_name} migration failed\n")
    
    # Summary
    print("=" * 70)
    print("📊 MIGRATION SUMMARY")
    print("=" * 70)
    print(f"✅ Successfully migrated: {success_count} agents")
    print(f"❌ Failed migrations: {failed_count} agents")
    print(f"📁 Total agents: {len(agents)}")
    
    if failed_count == 0:
        print("\n🎉 All agents migrated successfully!")
        
        # Ask about cleanup
        response = input("\n🗑️ Remove source directory app/ai/agents? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            cleanup_source_directory()
        else:
            print("⏭️ Source directory preserved")
    else:
        print(f"\n⚠️ {failed_count} migrations failed. Please check and retry.")
    
    print("\n✨ Migration process completed!")

if __name__ == "__main__":
    main()