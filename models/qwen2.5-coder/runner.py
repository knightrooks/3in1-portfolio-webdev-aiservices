#!/usr/bin/env python3
"""
Qwen 2.5 Coder Model Runner
Specialized Programming Model with Multi-Language Support
"""

import os
import json
import yaml
import asyncio
import logging
import ast
import re
import subprocess
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from dataclasses import dataclass
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Qwen25CoderConfig:
    """Configuration class for Qwen 2.5 Coder model"""
    name: str
    version: str
    provider: str
    model_type: str
    parameters: Dict[str, Any]
    capabilities: Dict[str, List[str]]
    specialties: Dict[str, Dict[str, Any]]

class CodeAnalyzer:
    """Analyzes code for quality, security, and performance"""
    
    def __init__(self):
        self.language_patterns = {
            'python': [r'def\s+\w+', r'import\s+\w+', r'from\s+\w+\s+import', r'class\s+\w+'],
            'javascript': [r'function\s+\w+', r'const\s+\w+\s*=', r'let\s+\w+\s*=', r'var\s+\w+\s*='],
            'java': [r'public\s+class', r'private\s+\w+', r'public\s+static\s+void\s+main'],
            'cpp': [r'#include\s*<', r'int\s+main\s*\(', r'class\s+\w+', r'namespace\s+\w+'],
            'go': [r'func\s+\w+', r'package\s+\w+', r'import\s+\(', r'type\s+\w+\s+struct'],
            'rust': [r'fn\s+\w+', r'use\s+\w+', r'struct\s+\w+', r'impl\s+\w+'],
            'typescript': [r'interface\s+\w+', r'type\s+\w+\s*=', r'function\s+\w+', r'const\s+\w+:\s*\w+'],
            'sql': [r'SELECT\s+', r'FROM\s+', r'WHERE\s+', r'CREATE\s+TABLE'],
        }
        
        self.security_patterns = {
            'sql_injection': [r'sql.*\+.*input', r'query.*\+.*user'],
            'xss': [r'innerHTML\s*=', r'document\.write\('],
            'hardcoded_secrets': [r'password\s*=\s*[\'"]', r'api_key\s*=\s*[\'"]'],
            'unsafe_functions': [r'eval\(', r'exec\(', r'subprocess\.call\(']
        }
        
        self.best_practices = {
            'python': ['Use type hints', 'Follow PEP 8', 'Use docstrings', 'Handle exceptions properly'],
            'javascript': ['Use const/let instead of var', 'Use strict mode', 'Handle async properly', 'Validate inputs'],
            'java': ['Use proper naming conventions', 'Handle exceptions', 'Use generics', 'Follow SOLID principles'],
            'go': ['Handle errors properly', 'Use proper package structure', 'Follow Go conventions', 'Use interfaces effectively']
        }
    
    def detect_language(self, code: str) -> str:
        """Detect programming language from code"""
        scores = {}
        
        for language, patterns in self.language_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, code, re.IGNORECASE | re.MULTILINE))
                score += matches
            if score > 0:
                scores[language] = score
        
        if scores:
            return max(scores, key=scores.get)
        return 'unknown'
    
    def analyze_code_quality(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code quality and provide suggestions"""
        analysis = {
            'language': language,
            'quality_score': 0.7,  # Base score
            'issues': [],
            'suggestions': [],
            'security_concerns': [],
            'best_practices': []
        }
        
        try:
            # Check for security issues
            for issue_type, patterns in self.security_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, code, re.IGNORECASE):
                        analysis['security_concerns'].append(f"Potential {issue_type} vulnerability detected")
                        analysis['quality_score'] -= 0.1
            
            # Add language-specific best practices
            if language in self.best_practices:
                analysis['best_practices'] = self.best_practices[language]
            
            # Basic code quality checks
            lines = code.split('\n')
            if any(len(line) > 120 for line in lines):
                analysis['issues'].append("Some lines exceed 120 characters")
                analysis['quality_score'] -= 0.05
            
            # Check for comments
            comment_ratio = sum(1 for line in lines if line.strip().startswith('#') or line.strip().startswith('//')) / max(len(lines), 1)
            if comment_ratio < 0.1:
                analysis['suggestions'].append("Consider adding more comments for better readability")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing code quality: {e}")
            analysis['error'] = str(e)
            return analysis

class CodeGenerator:
    """Generates code snippets and templates"""
    
    def __init__(self):
        self.templates = {
            'python': {
                'class': '''class {class_name}:
    def __init__(self):
        pass
    
    def method_name(self):
        pass''',
                'function': '''def {function_name}({parameters}):
    """
    {description}
    """
    pass''',
                'api_endpoint': '''@app.route('/{endpoint}', methods=['GET', 'POST'])
def {function_name}():
    try:
        # Implementation here
        return jsonify({{"status": "success"}})
    except Exception as e:
        return jsonify({{"error": str(e)}}), 500'''
            },
            'javascript': {
                'function': '''function {function_name}({parameters}) {{
    // {description}
}}''',
                'async_function': '''async function {function_name}({parameters}) {{
    try {{
        // {description}
    }} catch (error) {{
        console.error('Error:', error);
    }}
}}''',
                'react_component': '''import React from 'react';

const {component_name} = () => {{
    return (
        <div>
            {/* Component content */}
        </div>
    );
}};

export default {component_name};'''
            },
            'go': {
                'function': '''func {function_name}({parameters}) {return_type} {{
    // {description}
}}''',
                'struct': '''type {struct_name} struct {{
    // Add fields here
}}''',
                'http_handler': '''func {handler_name}(w http.ResponseWriter, r *http.Request) {{
    // Handle request
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{{"status": "success"}})
}}'''
            }
        }
        
        self.common_algorithms = {
            'sorting': {
                'quicksort': 'Efficient divide-and-conquer sorting algorithm',
                'mergesort': 'Stable divide-and-conquer sorting algorithm',
                'bubblesort': 'Simple but inefficient sorting algorithm'
            },
            'searching': {
                'binary_search': 'Efficient search in sorted arrays',
                'linear_search': 'Simple sequential search'
            },
            'data_structures': {
                'linked_list': 'Dynamic data structure with nodes',
                'binary_tree': 'Hierarchical tree data structure',
                'hash_table': 'Key-value storage with fast access'
            }
        }
    
    def generate_code_template(self, template_type: str, language: str, parameters: Dict[str, str]) -> str:
        """Generate code template based on type and parameters"""
        try:
            if language in self.templates and template_type in self.templates[language]:
                template = self.templates[language][template_type]
                return template.format(**parameters)
            else:
                return f"# Template for {template_type} in {language} not available"
                
        except Exception as e:
            logger.error(f"Error generating code template: {e}")
            return f"# Error generating template: {str(e)}"
    
    def suggest_improvements(self, code: str, language: str) -> List[str]:
        """Suggest code improvements"""
        suggestions = []
        
        try:
            if language == 'python':
                if 'print(' in code:
                    suggestions.append("Consider using logging instead of print statements")
                if 'except:' in code:
                    suggestions.append("Specify exception types instead of bare except clauses")
                if not re.search(r'def\s+\w+\([^)]*\):\s*"""', code):
                    suggestions.append("Add docstrings to functions for better documentation")
            
            elif language == 'javascript':
                if 'var ' in code:
                    suggestions.append("Use 'const' or 'let' instead of 'var'")
                if 'console.log' in code:
                    suggestions.append("Remove console.log statements in production code")
                if '== ' in code or '!= ' in code:
                    suggestions.append("Use strict equality operators (=== and !==)")
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error suggesting improvements: {e}")
            return ["Error analyzing code for improvements"]

class Qwen25CoderRunner:
    """
    Runner class for Qwen 2.5 Coder model
    Specialized in programming assistance and code generation
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the Qwen 2.5 Coder runner with configuration"""
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        self.model_name = self.config.name
        self.version = self.config.version
        self.session_history = []
        
        # Initialize coding components
        self.code_analyzer = CodeAnalyzer()
        self.code_generator = CodeGenerator()
        
        # Programming context
        self.programming_context = {
            'current_language': 'python',
            'project_type': 'general',
            'frameworks': [],
            'coding_style': 'clean_code'
        }
        
        logger.info(f"Qwen 2.5 Coder Runner initialized: {self.model_name} v{self.version}")
        logger.info("Advanced programming assistance enabled")
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "config.yaml")
    
    def _load_config(self) -> Qwen25CoderConfig:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
            
            return Qwen25CoderConfig(
                name=config_data['name'],
                version=config_data['version'],
                provider=config_data['provider'],
                model_type=config_data['model_type'],
                parameters=config_data['parameters'],
                capabilities=config_data['capabilities'],
                specialties=config_data['specialties']
            )
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
    
    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate programming-focused response
        
        Args:
            prompt: Programming question or code request
            context: Additional context including language preferences and project details
        
        Returns:
            Dictionary containing programming assistance response
        """
        try:
            # Analyze programming context
            programming_analysis = await self._analyze_programming_context(prompt, context)
            
            # Determine response type
            response_type = await self._determine_response_type(prompt, programming_analysis)
            
            # Generate appropriate programming response
            response = await self._generate_programming_response(prompt, programming_analysis, response_type, context)
            
            # Format comprehensive programming response
            formatted_response = await self._format_programming_response(response, programming_analysis)
            
            # Update session history
            self._update_session_history(prompt, formatted_response)
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name
            }
    
    async def _analyze_programming_context(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze programming context from prompt and additional context"""
        analysis = {
            "contains_code": False,
            "detected_language": "unknown",
            "programming_task": "general_question",
            "complexity_level": "intermediate",
            "frameworks_mentioned": [],
            "code_quality_request": False,
            "debug_request": False,
            "optimization_request": False
        }
        
        try:
            # Check if prompt contains code
            code_indicators = ['```', 'def ', 'function', 'class ', 'import ', '#include', 'SELECT', 'FROM']
            analysis["contains_code"] = any(indicator in prompt for indicator in code_indicators)
            
            if analysis["contains_code"]:
                # Extract code blocks
                code_blocks = re.findall(r'```[\w]*\n?(.*?)```', prompt, re.DOTALL)
                if code_blocks:
                    # Analyze the first code block
                    code = code_blocks[0]
                    analysis["detected_language"] = self.code_analyzer.detect_language(code)
            
            # Determine programming task type
            task_keywords = {
                'code_review': ['review', 'check', 'improve', 'quality'],
                'debugging': ['debug', 'error', 'bug', 'fix', 'problem'],
                'optimization': ['optimize', 'performance', 'faster', 'efficient'],
                'code_generation': ['create', 'generate', 'write', 'implement'],
                'explanation': ['explain', 'how does', 'what is', 'understand']
            }
            
            prompt_lower = prompt.lower()
            for task_type, keywords in task_keywords.items():
                if any(keyword in prompt_lower for keyword in keywords):
                    analysis["programming_task"] = task_type
                    break
            
            # Detect specific requests
            analysis["code_quality_request"] = any(word in prompt_lower for word in ['quality', 'review', 'improve'])
            analysis["debug_request"] = any(word in prompt_lower for word in ['debug', 'error', 'bug'])
            analysis["optimization_request"] = any(word in prompt_lower for word in ['optimize', 'performance'])
            
            # Detect frameworks
            frameworks = {
                'react': ['react', 'jsx', 'component'],
                'django': ['django', 'models.py', 'views.py'],
                'flask': ['flask', '@app.route'],
                'express': ['express', 'app.get', 'app.post'],
                'spring': ['spring', '@controller', '@service'],
                'tensorflow': ['tensorflow', 'tf.', 'keras'],
                'pytorch': ['pytorch', 'torch', 'nn.Module']
            }
            
            for framework, indicators in frameworks.items():
                if any(indicator in prompt_lower for indicator in indicators):
                    analysis["frameworks_mentioned"].append(framework)
            
            # Extract additional context
            if context:
                analysis["target_language"] = context.get("language", analysis["detected_language"])
                analysis["project_type"] = context.get("project_type", "general")
                analysis["experience_level"] = context.get("experience_level", "intermediate")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing programming context: {e}")
            return analysis
    
    async def _determine_response_type(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Determine the type of response needed"""
        try:
            if analysis["contains_code"] and analysis["code_quality_request"]:
                return "code_review"
            elif analysis["contains_code"] and analysis["debug_request"]:
                return "debugging_assistance"
            elif analysis["contains_code"] and analysis["optimization_request"]:
                return "performance_optimization"
            elif analysis["programming_task"] == "code_generation":
                return "code_generation"
            elif analysis["programming_task"] == "explanation":
                return "concept_explanation"
            else:
                return "general_programming_assistance"
                
        except Exception as e:
            logger.error(f"Error determining response type: {e}")
            return "general_programming_assistance"
    
    async def _generate_programming_response(self, prompt: str, analysis: Dict[str, Any], response_type: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate programming-specific response based on type"""
        response = {
            "content": "",
            "code_examples": [],
            "analysis": {},
            "suggestions": [],
            "resources": [],
            "confidence": 0.8
        }
        
        try:
            if response_type == "code_review":
                response = await self._provide_code_review(prompt, analysis)
            elif response_type == "debugging_assistance":
                response = await self._provide_debugging_help(prompt, analysis)
            elif response_type == "performance_optimization":
                response = await self._provide_optimization_suggestions(prompt, analysis)
            elif response_type == "code_generation":
                response = await self._generate_code_solution(prompt, analysis, context)
            elif response_type == "concept_explanation":
                response = await self._explain_programming_concept(prompt, analysis)
            else:
                response = await self._provide_general_programming_help(prompt, analysis)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating programming response: {e}")
            response["error"] = str(e)
            return response
    
    async def _provide_code_review(self, prompt: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Provide code review and quality analysis"""
        try:
            # Extract code from prompt
            code_blocks = re.findall(r'```[\w]*\n?(.*?)```', prompt, re.DOTALL)
            
            response = {
                "content": "I'll review your code and provide suggestions for improvement.",
                "code_examples": [],
                "analysis": {},
                "suggestions": [],
                "resources": []
            }
            
            if code_blocks:
                code = code_blocks[0]
                language = analysis["detected_language"]
                
                # Analyze code quality
                quality_analysis = self.code_analyzer.analyze_code_quality(code, language)
                response["analysis"] = quality_analysis
                
                # Generate improvement suggestions
                improvements = self.code_generator.suggest_improvements(code, language)
                response["suggestions"] = improvements
                
                # Create improved code example
                response["content"] += f"\n\n**Code Quality Analysis:**\n"
                response["content"] += f"- Language: {quality_analysis['language']}\n"
                response["content"] += f"- Quality Score: {quality_analysis['quality_score']:.2f}/1.0\n"
                
                if quality_analysis['issues']:
                    response["content"] += f"- Issues Found: {', '.join(quality_analysis['issues'])}\n"
                
                if quality_analysis['security_concerns']:
                    response["content"] += f"- Security Concerns: {', '.join(quality_analysis['security_concerns'])}\n"
                
                response["content"] += "\n**Suggestions for Improvement:**\n"
                for suggestion in improvements:
                    response["content"] += f"- {suggestion}\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Error providing code review: {e}")
            return {"error": str(e), "content": "Unable to review code at this time."}
    
    async def _provide_debugging_help(self, prompt: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Provide debugging assistance"""
        response = {
            "content": "I'll help you debug your code. Let me analyze the issue.",
            "code_examples": [],
            "analysis": {"debugging_approach": "systematic"},
            "suggestions": [
                "Check for syntax errors first",
                "Verify variable names and scope",
                "Add print statements or use debugger",
                "Test with simple inputs first"
            ],
            "resources": [
                "Use IDE debugger features",
                "Check language documentation",
                "Add logging for better visibility"
            ]
        }
        
        try:
            # Extract error information if present
            if "error" in prompt.lower() or "exception" in prompt.lower():
                response["content"] += "\n\n**Common Debugging Steps:**\n"
                response["content"] += "1. Read the error message carefully\n"
                response["content"] += "2. Check the line number mentioned in the error\n"
                response["content"] += "3. Verify all variables are properly defined\n"
                response["content"] += "4. Check for typos in function/variable names\n"
                response["content"] += "5. Ensure proper indentation (especially in Python)\n"
            
            # Language-specific debugging tips
            language = analysis.get("detected_language", "unknown")
            if language == "python":
                response["suggestions"].extend([
                    "Check indentation levels",
                    "Verify all imports are correct",
                    "Use try-except blocks for error handling"
                ])
            elif language == "javascript":
                response["suggestions"].extend([
                    "Check browser console for errors",
                    "Verify all parentheses and brackets are closed",
                    "Use console.log for debugging"
                ])
            
            return response
            
        except Exception as e:
            logger.error(f"Error providing debugging help: {e}")
            return {"error": str(e), "content": "Unable to provide debugging assistance."}
    
    async def _provide_optimization_suggestions(self, prompt: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Provide performance optimization suggestions"""
        response = {
            "content": "Here are optimization suggestions for your code:",
            "code_examples": [],
            "analysis": {"optimization_focus": "performance"},
            "suggestions": [
                "Profile your code to identify bottlenecks",
                "Use appropriate data structures",
                "Minimize I/O operations",
                "Consider caching frequently used data"
            ],
            "resources": [
                "Use profiling tools",
                "Study algorithm complexity",
                "Learn about memory management"
            ]
        }
        
        try:
            language = analysis.get("detected_language", "unknown")
            
            # Language-specific optimization tips
            if language == "python":
                response["suggestions"].extend([
                    "Use list comprehensions instead of loops where appropriate",
                    "Consider using NumPy for numerical computations",
                    "Use built-in functions which are implemented in C"
                ])
                response["code_examples"].append({
                    "title": "List Comprehension Example",
                    "code": "# Instead of:\nresult = []\nfor i in range(10):\n    result.append(i**2)\n\n# Use:\nresult = [i**2 for i in range(10)]"
                })
            
            elif language == "javascript":
                response["suggestions"].extend([
                    "Use async/await for better asynchronous code",
                    "Minimize DOM manipulations",
                    "Use event delegation for better performance"
                ])
            
            return response
            
        except Exception as e:
            logger.error(f"Error providing optimization suggestions: {e}")
            return {"error": str(e), "content": "Unable to provide optimization suggestions."}
    
    async def _generate_code_solution(self, prompt: str, analysis: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate code solution based on request"""
        response = {
            "content": "I'll generate a code solution for your request.",
            "code_examples": [],
            "analysis": {"generation_approach": "template_based"},
            "suggestions": [],
            "resources": []
        }
        
        try:
            language = analysis.get("target_language", "python")
            
            # Determine what to generate
            if "function" in prompt.lower():
                template_params = {
                    "function_name": "example_function",
                    "parameters": "param1, param2",
                    "description": "Function description here"
                }
                
                if language in self.code_generator.templates:
                    code = self.code_generator.generate_code_template("function", language, template_params)
                    response["code_examples"].append({
                        "title": f"Function Template ({language})",
                        "code": code
                    })
            
            elif "class" in prompt.lower():
                template_params = {
                    "class_name": "ExampleClass"
                }
                
                if language in self.code_generator.templates and "class" in self.code_generator.templates[language]:
                    code = self.code_generator.generate_code_template("class", language, template_params)
                    response["code_examples"].append({
                        "title": f"Class Template ({language})",
                        "code": code
                    })
            
            elif "api" in prompt.lower():
                if language == "python":
                    template_params = {
                        "endpoint": "example",
                        "function_name": "handle_example"
                    }
                    code = self.code_generator.generate_code_template("api_endpoint", language, template_params)
                    response["code_examples"].append({
                        "title": "API Endpoint (Flask)",
                        "code": code
                    })
            
            # Add general suggestions
            response["suggestions"] = [
                f"Customize the generated {language} code for your specific use case",
                "Add proper error handling",
                "Include appropriate documentation",
                "Test the code thoroughly"
            ]
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating code solution: {e}")
            return {"error": str(e), "content": "Unable to generate code solution."}
    
    async def _explain_programming_concept(self, prompt: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Explain programming concepts"""
        response = {
            "content": "Let me explain this programming concept for you.",
            "code_examples": [],
            "analysis": {"explanation_type": "conceptual"},
            "suggestions": [],
            "resources": []
        }
        
        try:
            # Detect specific concepts
            concepts = {
                'recursion': 'A programming technique where a function calls itself',
                'algorithm': 'A step-by-step procedure for solving a problem',
                'data structure': 'A way of organizing and storing data in a computer',
                'oop': 'Object-Oriented Programming - organizing code using objects and classes',
                'function': 'A reusable block of code that performs a specific task'
            }
            
            prompt_lower = prompt.lower()
            for concept, definition in concepts.items():
                if concept in prompt_lower:
                    response["content"] += f"\n\n**{concept.title()}:**\n{definition}\n"
                    
                    # Add code example for the concept
                    if concept == 'function' and analysis.get("detected_language") == "python":
                        response["code_examples"].append({
                            "title": "Function Example",
                            "code": "def greet(name):\n    \"\"\"Greets a person with their name\"\"\"\n    return f\"Hello, {name}!\"\n\n# Usage\nmessage = greet(\"Alice\")\nprint(message)  # Output: Hello, Alice!"
                        })
                    break
            
            return response
            
        except Exception as e:
            logger.error(f"Error explaining programming concept: {e}")
            return {"error": str(e), "content": "Unable to explain concept."}
    
    async def _provide_general_programming_help(self, prompt: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Provide general programming assistance"""
        response = {
            "content": "I'm Qwen 2.5 Coder, specialized in programming assistance. I can help you with:",
            "code_examples": [],
            "analysis": {"assistance_type": "general"},
            "suggestions": [
                "Code review and quality improvement",
                "Debugging and error resolution", 
                "Performance optimization",
                "Code generation and templates",
                "Programming concept explanations"
            ],
            "resources": [
                "Multi-language programming support",
                "Framework-specific guidance",
                "Best practices recommendations",
                "Algorithm and data structure help"
            ]
        }
        
        try:
            # Add language-specific capabilities
            detected_lang = analysis.get("detected_language", "unknown")
            if detected_lang != "unknown":
                response["content"] += f"\n\nI detected {detected_lang} in your request. I have expert-level knowledge in:"
                
                if detected_lang == "python":
                    response["content"] += "\n- Web frameworks (Django, Flask, FastAPI)\n- Data science (NumPy, Pandas, Scikit-learn)\n- Machine learning (TensorFlow, PyTorch)"
                elif detected_lang == "javascript":
                    response["content"] += "\n- Frontend frameworks (React, Vue, Angular)\n- Backend development (Node.js, Express)\n- Modern JavaScript (ES6+, TypeScript)"
                elif detected_lang == "java":
                    response["content"] += "\n- Spring Framework\n- Enterprise applications\n- Android development"
            
            response["content"] += "\n\nHow can I assist you with your programming needs today?"
            
            return response
            
        except Exception as e:
            logger.error(f"Error providing general programming help: {e}")
            return {"error": str(e), "content": "I'm here to help with programming questions."}
    
    async def _format_programming_response(self, response: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Format comprehensive programming response"""
        formatted_response = {
            "model": self.model_name,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "programming_analysis": analysis,
            "response": response,
            "coding_capabilities": {
                "multi_language_support": True,
                "code_quality_analysis": True,
                "debugging_assistance": True,
                "performance_optimization": True,
                "code_generation": True
            },
            "technical_expertise": {
                "detected_language": analysis.get("detected_language", "unknown"),
                "frameworks_recognized": analysis.get("frameworks_mentioned", []),
                "task_complexity": analysis.get("complexity_level", "intermediate")
            },
            "recommendations": self._generate_coding_recommendations(analysis, response)
        }
        
        return formatted_response
    
    def _generate_coding_recommendations(self, analysis: Dict[str, Any], response: Dict[str, Any]) -> List[str]:
        """Generate coding recommendations"""
        recommendations = []
        
        try:
            detected_lang = analysis.get("detected_language", "unknown")
            
            if detected_lang != "unknown":
                recommendations.append(f"Continue developing in {detected_lang} for consistency")
            
            if analysis.get("code_quality_request"):
                recommendations.append("Regular code reviews improve overall code quality")
            
            if analysis.get("frameworks_mentioned"):
                recommendations.append("Follow framework-specific best practices and conventions")
            
            if not recommendations:
                recommendations = [
                    "Use version control (Git) for code management",
                    "Write tests for your code to ensure reliability",
                    "Follow language-specific style guides and conventions"
                ]
            
            return recommendations[:3]
            
        except Exception as e:
            logger.error(f"Error generating coding recommendations: {e}")
            return ["Continue practicing and learning programming concepts"]
    
    def _update_session_history(self, prompt: str, response: Dict[str, Any]):
        """Update session history with programming context"""
        self.session_history.append({
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response": response,
            "model": self.model_name,
            "programming_context": response.get("programming_analysis", {}),
            "technical_expertise": response.get("technical_expertise", {})
        })
        
        # Keep last 15 interactions for programming context
        if len(self.session_history) > 15:
            self.session_history = self.session_history[-15:]
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information"""
        return {
            "name": self.model_name,
            "version": self.version,
            "provider": self.config.provider,
            "model_type": self.config.model_type,
            "capabilities": self.config.capabilities,
            "specialties": list(self.config.specialties.keys()),
            "parameters": self.config.parameters,
            "status": "operational",
            "programming_expertise": {
                "supported_languages": list(self.code_analyzer.language_patterns.keys()),
                "code_analysis": True,
                "code_generation": True,
                "debugging_assistance": True,
                "performance_optimization": True,
                "security_analysis": True
            },
            "framework_support": {
                "web_frameworks": ["Django", "Flask", "React", "Vue", "Express", "Spring"],
                "ml_frameworks": ["TensorFlow", "PyTorch", "Scikit-learn"],
                "mobile_frameworks": ["React Native", "Flutter"],
                "cloud_platforms": ["AWS", "Google Cloud", "Azure"]
            }
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on coding capabilities"""
        try:
            # Test code analysis
            test_code = "def hello_world():\n    print('Hello, World!')\n    return True"
            analysis_test = self.code_analyzer.analyze_code_quality(test_code, "python")
            
            # Test code generation
            template_test = self.code_generator.generate_code_template(
                "function", 
                "python", 
                {"function_name": "test_function", "parameters": "", "description": "Test function"}
            )
            
            # Test full pipeline
            response_test = await self.generate_response("Write a simple Python function")
            
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "version": self.version,
                "component_tests": {
                    "code_analysis": "error" not in analysis_test,
                    "code_generation": len(template_test) > 0,
                    "response_generation": "error" not in response_test
                },
                "programming_features": {
                    "multi_language_support": True,
                    "code_quality_analysis": True,
                    "template_generation": True,
                    "debugging_assistance": True
                },
                "all_tests_passed": (
                    "error" not in analysis_test and
                    len(template_test) > 0 and
                    "error" not in response_test
                )
            }
        except Exception as e:
            return {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "error": str(e)
            }

# Example usage and testing
async def main():
    """Main function for testing Qwen 2.5 Coder runner"""
    try:
        # Initialize runner
        runner = Qwen25CoderRunner()
        
        # Test model info
        print("=== Model Information ===")
        model_info = runner.get_model_info()
        print(json.dumps(model_info, indent=2))
        
        # Test health check
        print("\n=== Health Check ===")
        health = await runner.health_check()
        print(json.dumps(health, indent=2))
        
        # Test programming assistance
        print("\n=== Programming Assistance Tests ===")
        test_prompts = [
            "Write a Python function to calculate factorial",
            "Review this code: ```python\ndef bad_function(x):\n  if x>0:\n      return x*bad_function(x-1)\n```",
            "Explain what recursion is in programming",
            "How can I optimize this JavaScript loop for better performance?"
        ]
        
        for prompt in test_prompts:
            print(f"\nPrompt: {prompt}")
            response = await runner.generate_response(prompt)
            
            programming_analysis = response.get('programming_analysis', {})
            print(f"Detected Language: {programming_analysis.get('detected_language', 'unknown')}")
            print(f"Task Type: {programming_analysis.get('programming_task', 'general')}")
            
            response_content = response.get('response', {}).get('content', 'No response')
            print(f"Response: {response_content[:200]}...")
            
            if response.get('response', {}).get('code_examples'):
                print(f"Code examples provided: {len(response['response']['code_examples'])}")
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())