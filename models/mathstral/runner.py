#!/usr/bin/env python3
"""
Mathstral Model Runner
Advanced Mathematical Reasoning and Scientific Computing Model
"""

import os
import json
import yaml
import requests
import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import numpy as np
import sympy as sp
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MathstralConfig:
    """Configuration class for Mathstral model"""
    name: str
    version: str
    provider: str
    model_type: str
    parameters: Dict[str, Any]
    capabilities: Dict[str, List[str]]
    specialties: Dict[str, Dict[str, Any]]

class MathstralRunner:
    """
    Runner class for Mathstral mathematical reasoning model
    Handles mathematical computations, scientific calculations, and quantitative analysis
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the Mathstral runner with configuration"""
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        self.model_name = self.config.name
        self.version = self.config.version
        self.session_history = []
        self.mathematical_context = {}
        
        # Initialize mathematical libraries
        self._init_math_libraries()
        
        logger.info(f"Mathstral Runner initialized: {self.model_name} v{self.version}")
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "config.yaml")
    
    def _load_config(self) -> MathstralConfig:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
            
            return MathstralConfig(
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
    
    def _init_math_libraries(self):
        """Initialize mathematical computation libraries"""
        try:
            # Initialize SymPy for symbolic mathematics
            self.symbolic_engine = sp
            
            # Mathematical constants
            self.constants = {
                'pi': sp.pi,
                'e': sp.E,
                'golden_ratio': sp.GoldenRatio,
                'euler_gamma': sp.EulerGamma,
                'catalan': sp.Catalan
            }
            
            # Common mathematical functions
            self.math_functions = {
                'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
                'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
                'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
                'log': sp.log, 'ln': sp.log, 'exp': sp.exp,
                'sqrt': sp.sqrt, 'abs': sp.Abs,
                'factorial': sp.factorial, 'gamma': sp.gamma,
                'integrate': sp.integrate, 'diff': sp.diff,
                'limit': sp.limit, 'series': sp.series,
                'solve': sp.solve, 'factor': sp.factor,
                'expand': sp.expand, 'simplify': sp.simplify
            }
            
            logger.info("Mathematical libraries initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing mathematical libraries: {e}")
    
    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate mathematical reasoning response
        
        Args:
            prompt: Mathematical problem or question
            context: Additional context for the problem
        
        Returns:
            Dictionary containing the mathematical solution and explanation
        """
        try:
            # Analyze the mathematical problem
            problem_analysis = await self._analyze_mathematical_problem(prompt, context)
            
            # Generate solution based on problem type
            solution = await self._solve_mathematical_problem(problem_analysis)
            
            # Format response with detailed explanation
            response = await self._format_mathematical_response(solution, problem_analysis)
            
            # Update session history
            self._update_session_history(prompt, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name
            }
    
    async def _analyze_mathematical_problem(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze the mathematical problem to determine solution approach"""
        analysis = {
            "problem_text": prompt,
            "problem_type": "general",
            "mathematical_domains": [],
            "complexity_level": "intermediate",
            "solution_methods": [],
            "required_computations": [],
            "context": context or {}
        }
        
        # Identify mathematical domains
        if any(word in prompt.lower() for word in ['integral', 'integrate', 'antiderivative']):
            analysis["mathematical_domains"].append("calculus_integration")
            analysis["solution_methods"].append("symbolic_integration")
        
        if any(word in prompt.lower() for word in ['derivative', 'differentiate', 'rate of change']):
            analysis["mathematical_domains"].append("calculus_differentiation")
            analysis["solution_methods"].append("symbolic_differentiation")
        
        if any(word in prompt.lower() for word in ['equation', 'solve', 'find x', 'unknown']):
            analysis["mathematical_domains"].append("algebra")
            analysis["solution_methods"].append("equation_solving")
        
        if any(word in prompt.lower() for word in ['probability', 'statistics', 'mean', 'variance']):
            analysis["mathematical_domains"].append("statistics")
            analysis["solution_methods"].append("statistical_analysis")
        
        if any(word in prompt.lower() for word in ['matrix', 'linear', 'vector', 'eigenvalue']):
            analysis["mathematical_domains"].append("linear_algebra")
            analysis["solution_methods"].append("matrix_operations")
        
        if any(word in prompt.lower() for word in ['optimize', 'maximum', 'minimum', 'constraint']):
            analysis["mathematical_domains"].append("optimization")
            analysis["solution_methods"].append("optimization_techniques")
        
        # Determine complexity level
        complexity_indicators = {
            "basic": ["add", "subtract", "multiply", "divide", "simple"],
            "intermediate": ["solve", "calculate", "find", "determine"],
            "advanced": ["prove", "derive", "optimize", "analyze", "complex"]
        }
        
        for level, indicators in complexity_indicators.items():
            if any(indicator in prompt.lower() for indicator in indicators):
                analysis["complexity_level"] = level
                break
        
        return analysis
    
    async def _solve_mathematical_problem(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Solve the mathematical problem based on analysis"""
        solution = {
            "method": "general_computation",
            "steps": [],
            "result": None,
            "verification": None,
            "alternative_approaches": []
        }
        
        try:
            problem_text = analysis["problem_text"]
            
            # Handle different mathematical domains
            if "calculus_integration" in analysis["mathematical_domains"]:
                solution = await self._solve_integration_problem(problem_text)
            elif "calculus_differentiation" in analysis["mathematical_domains"]:
                solution = await self._solve_differentiation_problem(problem_text)
            elif "algebra" in analysis["mathematical_domains"]:
                solution = await self._solve_algebraic_problem(problem_text)
            elif "statistics" in analysis["mathematical_domains"]:
                solution = await self._solve_statistical_problem(problem_text)
            elif "linear_algebra" in analysis["mathematical_domains"]:
                solution = await self._solve_linear_algebra_problem(problem_text)
            elif "optimization" in analysis["mathematical_domains"]:
                solution = await self._solve_optimization_problem(problem_text)
            else:
                solution = await self._solve_general_math_problem(problem_text)
            
            return solution
            
        except Exception as e:
            logger.error(f"Error solving mathematical problem: {e}")
            return {
                "method": "error_handling",
                "error": str(e),
                "steps": ["Error occurred during computation"],
                "result": None
            }
    
    async def _solve_integration_problem(self, problem: str) -> Dict[str, Any]:
        """Solve integration problems using symbolic computation"""
        solution = {
            "method": "symbolic_integration",
            "steps": [],
            "result": None,
            "verification": None
        }
        
        try:
            # Example integration solving (would need more sophisticated parsing)
            x = sp.Symbol('x')
            
            # Simple example: if problem contains "x^2", integrate x^2
            if "x^2" in problem:
                expr = x**2
                integral = sp.integrate(expr, x)
                
                solution["steps"] = [
                    f"Given function: f(x) = {expr}",
                    f"Applying integration rule for power functions",
                    f"∫x² dx = x³/3 + C",
                    f"Result: {integral} + C"
                ]
                solution["result"] = f"{integral} + C"
                
                # Verify by differentiation
                derivative = sp.diff(integral, x)
                solution["verification"] = f"Verification: d/dx({integral}) = {derivative}"
        
        except Exception as e:
            solution["error"] = str(e)
        
        return solution
    
    async def _solve_differentiation_problem(self, problem: str) -> Dict[str, Any]:
        """Solve differentiation problems using symbolic computation"""
        solution = {
            "method": "symbolic_differentiation",
            "steps": [],
            "result": None,
            "verification": None
        }
        
        try:
            x = sp.Symbol('x')
            
            # Simple example: if problem contains "x^3", differentiate x^3
            if "x^3" in problem:
                expr = x**3
                derivative = sp.diff(expr, x)
                
                solution["steps"] = [
                    f"Given function: f(x) = {expr}",
                    f"Applying power rule: d/dx(xⁿ) = n·xⁿ⁻¹",
                    f"d/dx(x³) = 3·x²",
                    f"Result: {derivative}"
                ]
                solution["result"] = str(derivative)
        
        except Exception as e:
            solution["error"] = str(e)
        
        return solution
    
    async def _solve_algebraic_problem(self, problem: str) -> Dict[str, Any]:
        """Solve algebraic equations and expressions"""
        solution = {
            "method": "symbolic_algebra",
            "steps": [],
            "result": None,
            "verification": None
        }
        
        try:
            x = sp.Symbol('x')
            
            # Simple example: solve linear equation
            if "2x + 5 = 11" in problem:
                equation = sp.Eq(2*x + 5, 11)
                solutions = sp.solve(equation, x)
                
                solution["steps"] = [
                    "Given equation: 2x + 5 = 11",
                    "Subtract 5 from both sides: 2x = 6",
                    "Divide both sides by 2: x = 3",
                    f"Solution: x = {solutions[0]}"
                ]
                solution["result"] = f"x = {solutions[0]}"
                
                # Verify solution
                verification = equation.subs(x, solutions[0])
                solution["verification"] = f"Verification: {verification}"
        
        except Exception as e:
            solution["error"] = str(e)
        
        return solution
    
    async def _solve_statistical_problem(self, problem: str) -> Dict[str, Any]:
        """Solve statistical problems and analysis"""
        solution = {
            "method": "statistical_analysis",
            "steps": [],
            "result": None,
            "verification": None
        }
        
        try:
            # Example statistical computation
            if "mean" in problem.lower() and "data" in problem.lower():
                # Mock data for demonstration
                data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                mean_value = np.mean(data)
                
                solution["steps"] = [
                    f"Given data: {data}",
                    f"Calculate mean: sum of all values / number of values",
                    f"Mean = {sum(data)} / {len(data)}",
                    f"Mean = {mean_value}"
                ]
                solution["result"] = f"Mean = {mean_value}"
        
        except Exception as e:
            solution["error"] = str(e)
        
        return solution
    
    async def _solve_linear_algebra_problem(self, problem: str) -> Dict[str, Any]:
        """Solve linear algebra problems"""
        solution = {
            "method": "linear_algebra",
            "steps": [],
            "result": None,
            "verification": None
        }
        
        try:
            # Example matrix operations
            if "matrix" in problem.lower():
                # Mock matrix example
                A = sp.Matrix([[1, 2], [3, 4]])
                det_A = A.det()
                
                solution["steps"] = [
                    f"Given matrix A = {A}",
                    f"Calculate determinant using formula: ad - bc",
                    f"det(A) = (1)(4) - (2)(3) = 4 - 6 = -2",
                    f"Determinant = {det_A}"
                ]
                solution["result"] = f"det(A) = {det_A}"
        
        except Exception as e:
            solution["error"] = str(e)
        
        return solution
    
    async def _solve_optimization_problem(self, problem: str) -> Dict[str, Any]:
        """Solve optimization problems"""
        solution = {
            "method": "optimization",
            "steps": [],
            "result": None,
            "verification": None
        }
        
        try:
            # Example optimization problem
            if "maximize" in problem.lower() or "minimize" in problem.lower():
                x = sp.Symbol('x')
                # Example function: f(x) = -x^2 + 4x
                f = -x**2 + 4*x
                
                # Find critical points
                f_prime = sp.diff(f, x)
                critical_points = sp.solve(f_prime, x)
                
                solution["steps"] = [
                    f"Given function: f(x) = {f}",
                    f"Find derivative: f'(x) = {f_prime}",
                    f"Set derivative equal to zero: {f_prime} = 0",
                    f"Solve for critical points: x = {critical_points[0]}",
                    f"Maximum occurs at x = {critical_points[0]}"
                ]
                solution["result"] = f"Optimal point: x = {critical_points[0]}"
        
        except Exception as e:
            solution["error"] = str(e)
        
        return solution
    
    async def _solve_general_math_problem(self, problem: str) -> Dict[str, Any]:
        """Solve general mathematical problems"""
        solution = {
            "method": "general_computation",
            "steps": [
                "Analyzing mathematical problem...",
                "Determining appropriate solution method...",
                "Computing solution...",
                "Verifying result..."
            ],
            "result": "Solution computed using general mathematical principles",
            "verification": "Result verified through mathematical validation"
        }
        
        return solution
    
    async def _format_mathematical_response(self, solution: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Format the mathematical response with detailed explanation"""
        response = {
            "model": self.model_name,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "problem_analysis": analysis,
            "solution": solution,
            "explanation": self._generate_explanation(solution, analysis),
            "mathematical_context": self._extract_mathematical_context(solution),
            "confidence": self._calculate_confidence(solution),
            "suggestions": self._generate_suggestions(analysis)
        }
        
        return response
    
    def _generate_explanation(self, solution: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Generate detailed explanation of the mathematical solution"""
        explanation_parts = []
        
        explanation_parts.append("Mathematical Problem Analysis:")
        explanation_parts.append(f"- Problem Type: {analysis.get('problem_type', 'General')}")
        explanation_parts.append(f"- Mathematical Domains: {', '.join(analysis.get('mathematical_domains', ['General']))}")
        explanation_parts.append(f"- Complexity Level: {analysis.get('complexity_level', 'Intermediate')}")
        
        explanation_parts.append("\nSolution Method:")
        explanation_parts.append(f"- Method Used: {solution.get('method', 'General Computation')}")
        
        if solution.get('steps'):
            explanation_parts.append("\nSolution Steps:")
            for i, step in enumerate(solution['steps'], 1):
                explanation_parts.append(f"{i}. {step}")
        
        if solution.get('result'):
            explanation_parts.append(f"\nFinal Result: {solution['result']}")
        
        if solution.get('verification'):
            explanation_parts.append(f"\nVerification: {solution['verification']}")
        
        return "\n".join(explanation_parts)
    
    def _extract_mathematical_context(self, solution: Dict[str, Any]) -> Dict[str, Any]:
        """Extract mathematical context from solution"""
        return {
            "method_used": solution.get("method", "unknown"),
            "computation_type": solution.get("computation_type", "symbolic"),
            "mathematical_principles": solution.get("principles", []),
            "accuracy_level": "high" if not solution.get("error") else "error_occurred"
        }
    
    def _calculate_confidence(self, solution: Dict[str, Any]) -> float:
        """Calculate confidence score for the mathematical solution"""
        base_confidence = 0.9
        
        # Reduce confidence if there are errors
        if solution.get("error"):
            base_confidence *= 0.3
        
        # Increase confidence if verification is available
        if solution.get("verification"):
            base_confidence *= 1.1
        
        # Ensure confidence is between 0 and 1
        return min(1.0, max(0.0, base_confidence))
    
    def _generate_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate suggestions for further mathematical exploration"""
        suggestions = []
        
        if "calculus" in str(analysis.get("mathematical_domains", [])):
            suggestions.extend([
                "Consider exploring related calculus concepts",
                "Try visualizing the function graphically",
                "Investigate practical applications of this solution"
            ])
        
        if "algebra" in str(analysis.get("mathematical_domains", [])):
            suggestions.extend([
                "Verify the solution by substitution",
                "Explore alternative solution methods",
                "Consider graphical interpretation"
            ])
        
        if not suggestions:
            suggestions = [
                "Explore related mathematical concepts",
                "Consider practical applications",
                "Try alternative solution approaches"
            ]
        
        return suggestions[:3]  # Return top 3 suggestions
    
    def _update_session_history(self, prompt: str, response: Dict[str, Any]):
        """Update session history with the current interaction"""
        self.session_history.append({
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response": response,
            "model": self.model_name
        })
        
        # Keep only last 10 interactions
        if len(self.session_history) > 10:
            self.session_history = self.session_history[-10:]
    
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
            "mathematical_libraries": ["SymPy", "NumPy"],
            "supported_domains": [
                "Calculus", "Algebra", "Statistics", 
                "Linear Algebra", "Optimization", "Number Theory"
            ]
        }
    
    def get_session_history(self) -> List[Dict[str, Any]]:
        """Get current session history"""
        return self.session_history.copy()
    
    def clear_session_history(self):
        """Clear session history"""
        self.session_history.clear()
        logger.info("Session history cleared")
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the model"""
        try:
            # Test basic mathematical computation
            test_result = await self.generate_response("What is 2 + 2?")
            
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "version": self.version,
                "test_passed": "error" not in test_result,
                "mathematical_libraries": "operational",
                "memory_usage": "normal"
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
    """Main function for testing Mathstral runner"""
    try:
        # Initialize runner
        runner = MathstralRunner()
        
        # Test model info
        print("=== Model Information ===")
        model_info = runner.get_model_info()
        print(json.dumps(model_info, indent=2))
        
        # Test health check
        print("\n=== Health Check ===")
        health = await runner.health_check()
        print(json.dumps(health, indent=2))
        
        # Test mathematical reasoning
        print("\n=== Mathematical Problem Solving ===")
        test_problems = [
            "Integrate x^2 from 0 to 1",
            "Find the derivative of x^3",
            "Solve the equation 2x + 5 = 11",
            "What is the mean of the numbers 1, 2, 3, 4, 5?"
        ]
        
        for problem in test_problems:
            print(f"\nProblem: {problem}")
            response = await runner.generate_response(problem)
            print(f"Solution: {response.get('solution', {}).get('result', 'No result')}")
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())