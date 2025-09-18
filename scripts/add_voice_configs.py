#!/usr/bin/env python3
"""
Script to add voice configurations to all AI agents
"""

import os
import yaml

# Voice configurations for each agent type
AGENT_VOICE_CONFIGS = {
    'strategist': {
        'enabled': True,
        'provider': 'gTTS',
        'properties': {
            'gender': 'neutral',
            'rate': 160,
            'volume': 0.85,
            'tone': 'analytical',
            'emotion': 'confident',
            'language': 'en',
            'accent': 'us'
        },
        'personality_modifiers': {
            'strategic_emphasis': True,
            'clear_articulation': True,
            'authoritative_tone': True
        },
        'azure_voice': 'en-US-RogerNeural',
        'fallback_voice': 'en-US-BrianNeural'
    },
    'security_expert': {
        'enabled': True,
        'provider': 'gTTS',
        'properties': {
            'gender': 'male',
            'rate': 150,
            'volume': 0.9,
            'tone': 'serious',
            'emotion': 'vigilant',
            'language': 'en',
            'accent': 'us'
        },
        'personality_modifiers': {
            'security_emphasis': True,
            'cautious_tone': True,
            'professional_delivery': True
        },
        'azure_voice': 'en-US-DavisNeural',
        'fallback_voice': 'en-US-GuyNeural'
    },
    'content_creator': {
        'enabled': True,
        'provider': 'gTTS',
        'properties': {
            'gender': 'female',
            'rate': 200,
            'volume': 0.85,
            'tone': 'creative',
            'emotion': 'inspiring',
            'language': 'en',
            'accent': 'us'
        },
        'personality_modifiers': {
            'creative_inflection': True,
            'engaging_tone': True,
            'dynamic_delivery': True
        },
        'azure_voice': 'en-US-JennyNeural',
        'fallback_voice': 'en-US-SaraNeural'
    },
    'developer': {
        'enabled': True,
        'provider': 'gTTS',
        'properties': {
            'gender': 'male',
            'rate': 165,
            'volume': 0.8,
            'tone': 'technical',
            'emotion': 'focused',
            'language': 'en',
            'accent': 'us'
        },
        'personality_modifiers': {
            'technical_precision': True,
            'logical_flow': True,
            'clear_explanations': True
        },
        'azure_voice': 'en-US-BrianNeural',
        'fallback_voice': 'en-US-DavisNeural'
    },
    'data_scientist': {
        'enabled': True,
        'provider': 'gTTS',
        'properties': {
            'gender': 'female',
            'rate': 170,
            'volume': 0.85,
            'tone': 'analytical',
            'emotion': 'curious',
            'language': 'en',
            'accent': 'us'
        },
        'personality_modifiers': {
            'data_emphasis': True,
            'methodical_delivery': True,
            'insightful_tone': True
        },
        'azure_voice': 'en-US-SaraNeural',
        'fallback_voice': 'en-US-AriaNeural'
    },
    'marketing_specialist': {
        'enabled': True,
        'provider': 'gTTS',
        'properties': {
            'gender': 'female',
            'rate': 190,
            'volume': 0.9,
            'tone': 'persuasive',
            'emotion': 'enthusiastic',
            'language': 'en',
            'accent': 'us'
        },
        'personality_modifiers': {
            'persuasive_tone': True,
            'energetic_delivery': True,
            'engaging_inflection': True
        },
        'azure_voice': 'en-US-JennyNeural',
        'fallback_voice': 'en-US-MichelleNeural'
    },
    'operations_manager': {
        'enabled': True,
        'provider': 'gTTS',
        'properties': {
            'gender': 'male',
            'rate': 155,
            'volume': 0.85,
            'tone': 'professional',
            'emotion': 'efficient',
            'language': 'en',
            'accent': 'us'
        },
        'personality_modifiers': {
            'process_oriented': True,
            'clear_directives': True,
            'organized_delivery': True
        },
        'azure_voice': 'en-US-GuyNeural',
        'fallback_voice': 'en-US-DavisNeural'
    },
    'product_manager': {
        'enabled': True,
        'provider': 'gTTS',
        'properties': {
            'gender': 'female',
            'rate': 175,
            'volume': 0.85,
            'tone': 'strategic',
            'emotion': 'visionary',
            'language': 'en',
            'accent': 'us'
        },
        'personality_modifiers': {
            'product_focus': True,
            'strategic_thinking': True,
            'user_centric_tone': True
        },
        'azure_voice': 'en-US-SaraNeural',
        'fallback_voice': 'en-US-AriaNeural'
    },
    'research_analyst': {
        'enabled': True,
        'provider': 'gTTS',
        'properties': {
            'gender': 'neutral',
            'rate': 160,
            'volume': 0.8,
            'tone': 'scholarly',
            'emotion': 'inquisitive',
            'language': 'en',
            'accent': 'us'
        },
        'personality_modifiers': {
            'research_emphasis': True,
            'thorough_delivery': True,
            'evidence_based_tone': True
        },
        'azure_voice': 'en-US-BrianNeural',
        'fallback_voice': 'en-US-RogerNeural'
    },
    'customer_success': {
        'enabled': True,
        'provider': 'gTTS',
        'properties': {
            'gender': 'female',
            'rate': 180,
            'volume': 0.85,
            'tone': 'helpful',
            'emotion': 'supportive',
            'language': 'en',
            'accent': 'us'
        },
        'personality_modifiers': {
            'customer_centric': True,
            'empathetic_delivery': True,
            'solution_oriented': True
        },
        'azure_voice': 'en-US-AriaNeural',
        'fallback_voice': 'en-US-MichelleNeural'
    }
}

def add_voice_config_to_agent(agent_name, agent_path):
    """Add voice configuration to an agent's config file"""
    config_file = os.path.join(agent_path, 'config.yaml')
    
    try:
        # Load existing config
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                content = f.read().strip()
                if content and content != '{}':
                    config = yaml.safe_load(content)
                else:
                    config = {}
        else:
            config = {}
        
        # Add voice configuration if it doesn't exist
        if 'voice_config' not in config and agent_name in AGENT_VOICE_CONFIGS:
            config['voice_config'] = AGENT_VOICE_CONFIGS[agent_name]
            
            # Write updated config back
            with open(config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
            print(f"✅ Added voice config to {agent_name}")
            return True
        else:
            print(f"⚠️  Voice config already exists or agent not in mapping: {agent_name}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {agent_name}: {e}")
        return False

def main():
    agents_dir = '/workspaces/3in1-portfolio-webdev-aiservices/agents'
    updated_count = 0
    
    # Process each agent directory
    for item in os.listdir(agents_dir):
        agent_path = os.path.join(agents_dir, item)
        
        if os.path.isdir(agent_path) and item in AGENT_VOICE_CONFIGS:
            if add_voice_config_to_agent(item, agent_path):
                updated_count += 1
    
    print(f"\n🎉 Updated {updated_count} agent voice configurations!")

if __name__ == '__main__':
    main()