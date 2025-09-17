"""
Task Executor - Executes AI tasks using appropriate models
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional


class TaskExecutor:
    """Executes tasks using AI models."""

    def __init__(self):
        """Initialize the task executor."""
        self.logger = logging.getLogger(__name__)
        self.execution_history = []
        self.active_executions = {}

    async def execute_plan(
        self, plan: Dict, models: Dict, session_context: Dict = None
    ) -> Dict:
        """Execute a complete task plan."""
        plan_id = plan["id"]
        tasks = plan["tasks"]

        self.logger.info(f"Executing plan {plan_id} with {len(tasks)} tasks")

        # Initialize execution tracking
        execution = {
            "plan_id": plan_id,
            "started_at": datetime.now().isoformat(),
            "status": "running",
            "completed_tasks": [],
            "failed_tasks": [],
            "results": {},
            "session_context": session_context or {},
        }

        self.active_executions[plan_id] = execution

        try:
            # Execute tasks based on dependencies
            results = await self._execute_tasks_with_dependencies(
                tasks, models, execution
            )

            # Compile final response
            response = await self._compile_response(results, plan, execution)

            execution["status"] = "completed"
            execution["completed_at"] = datetime.now().isoformat()
            execution["final_response"] = response

            # Archive execution
            self.execution_history.append(execution)
            del self.active_executions[plan_id]

            return response

        except Exception as e:
            execution["status"] = "failed"
            execution["error"] = str(e)
            execution["failed_at"] = datetime.now().isoformat()

            self.logger.error(f"Plan execution failed: {e}")

            # Return error response
            return {
                "content": f"I apologize, but I encountered an error while processing your request: {str(e)}",
                "metadata": {"status": "error", "plan_id": plan_id, "error": str(e)},
            }

    async def _execute_tasks_with_dependencies(
        self, tasks: List[Dict], models: Dict, execution: Dict
    ) -> Dict:
        """Execute tasks respecting their dependencies."""
        results = {}
        completed_tasks = set()

        # Create dependency graph
        dependency_graph = self._build_dependency_graph(tasks)

        # Execute tasks in dependency order
        while len(completed_tasks) < len(tasks):
            # Find tasks ready to execute (all dependencies completed)
            ready_tasks = [
                task
                for task in tasks
                if task["id"] not in completed_tasks
                and all(dep in completed_tasks for dep in task.get("dependencies", []))
            ]

            if not ready_tasks:
                # Check for circular dependencies
                remaining_tasks = [
                    task for task in tasks if task["id"] not in completed_tasks
                ]
                raise Exception(
                    f"Circular dependency detected in tasks: {[t['id'] for t in remaining_tasks]}"
                )

            # Execute ready tasks (can be done in parallel)
            batch_results = await self._execute_task_batch(
                ready_tasks, models, results, execution
            )
            results.update(batch_results)

            # Mark tasks as completed
            for task in ready_tasks:
                completed_tasks.add(task["id"])

        return results

    def _build_dependency_graph(self, tasks: List[Dict]) -> Dict:
        """Build a dependency graph from tasks."""
        graph = {}
        for task in tasks:
            task_id = task["id"]
            dependencies = task.get("dependencies", [])
            graph[task_id] = dependencies
        return graph

    async def _execute_task_batch(
        self, tasks: List[Dict], models: Dict, previous_results: Dict, execution: Dict
    ) -> Dict:
        """Execute a batch of tasks that can run in parallel."""
        batch_results = {}

        # Execute tasks concurrently
        task_coroutines = [
            self._execute_single_task(task, models, previous_results, execution)
            for task in tasks
        ]

        results = await asyncio.gather(*task_coroutines, return_exceptions=True)

        # Process results
        for task, result in zip(tasks, results):
            task_id = task["id"]

            if isinstance(result, Exception):
                self.logger.error(f"Task {task_id} failed: {result}")
                execution["failed_tasks"].append(
                    {
                        "task_id": task_id,
                        "error": str(result),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
                batch_results[task_id] = {"status": "failed", "error": str(result)}
            else:
                execution["completed_tasks"].append(
                    {
                        "task_id": task_id,
                        "timestamp": datetime.now().isoformat(),
                        "result": result,
                    }
                )
                batch_results[task_id] = result

        return batch_results

    async def _execute_single_task(
        self, task: Dict, models: Dict, previous_results: Dict, execution: Dict
    ) -> Dict:
        """Execute a single task."""
        task_id = task["id"]
        task_name = task["name"]

        self.logger.info(f"Executing task {task_id}: {task_name}")

        # Prepare task context
        task_context = {
            "task": task,
            "previous_results": previous_results,
            "session_context": execution["session_context"],
            "execution_id": execution["plan_id"],
        }

        # Determine which model to use
        model_name = self._select_model_for_task(task, models)
        model = models.get(model_name)

        if not model:
            raise Exception(f"Model {model_name} not available for task {task_id}")

        # Execute task based on type
        if task["type"] == "processing":
            result = await self._execute_processing_task(task, model, task_context)
        elif task["type"] == "verification":
            result = await self._execute_verification_task(task, model, task_context)
        else:
            result = await self._execute_generic_task(task, model, task_context)

        return {
            "task_id": task_id,
            "status": "completed",
            "result": result,
            "model_used": model_name,
            "timestamp": datetime.now().isoformat(),
        }

    def _select_model_for_task(self, task: Dict, models: Dict) -> str:
        """Select the best model for a specific task."""
        # Simple model selection logic (can be enhanced with ML)
        available_models = list(models.keys())

        if not available_models:
            raise Exception("No models available")

        # Task-specific model preferences
        task_name = task["name"].lower()
        task_desc = task.get("description", "").lower()

        # Code-related tasks
        if any(
            keyword in task_name + task_desc
            for keyword in ["code", "develop", "implement"]
        ):
            for model in ["deepseek-coder", "codellama"]:
                if model in available_models:
                    return model

        # Security tasks
        if any(
            keyword in task_name + task_desc
            for keyword in ["security", "vulnerability", "threat"]
        ):
            for model in ["llama3.2", "deepseek-coder"]:
                if model in available_models:
                    return model

        # Strategic/analytical tasks
        if any(
            keyword in task_name + task_desc
            for keyword in ["strategy", "analyze", "plan"]
        ):
            for model in ["gemma2", "llama3.2"]:
                if model in available_models:
                    return model

        # Default to first available model
        return available_models[0]

    async def _execute_processing_task(
        self, task: Dict, model: Any, context: Dict
    ) -> Dict:
        """Execute a processing task."""
        # Prepare prompt for the model
        prompt = self._build_task_prompt(task, context)

        # Execute using the model (mock implementation)
        try:
            # This would call the actual model
            result = await self._call_model(model, prompt, task)

            return {
                "type": "processing",
                "output": result,
                "prompt_used": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            }
        except Exception as e:
            raise Exception(f"Model execution failed: {e}")

    async def _execute_verification_task(
        self, task: Dict, model: Any, context: Dict
    ) -> Dict:
        """Execute a verification task."""
        # Get results from previous tasks to verify
        previous_results = context["previous_results"]

        # Build verification prompt
        verification_prompt = self._build_verification_prompt(task, previous_results)

        try:
            result = await self._call_model(model, verification_prompt, task)

            return {
                "type": "verification",
                "verification_result": result,
                "verified_tasks": list(previous_results.keys()),
            }
        except Exception as e:
            raise Exception(f"Verification failed: {e}")

    async def _execute_generic_task(
        self, task: Dict, model: Any, context: Dict
    ) -> Dict:
        """Execute a generic task."""
        prompt = self._build_task_prompt(task, context)

        try:
            result = await self._call_model(model, prompt, task)

            return {"type": "generic", "output": result}
        except Exception as e:
            raise Exception(f"Generic task execution failed: {e}")

    def _build_task_prompt(self, task: Dict, context: Dict) -> str:
        """Build a prompt for the task."""
        base_prompt = f"""
Task: {task['name']}
Description: {task.get('description', 'No description provided')}

Session Context: {json.dumps(context['session_context'], indent=2)}

Previous Results:
{json.dumps(context['previous_results'], indent=2)}

Please execute this task and provide a comprehensive response.
"""

        return base_prompt.strip()

    def _build_verification_prompt(self, task: Dict, previous_results: Dict) -> str:
        """Build a verification prompt."""
        return f"""
Verification Task: {task['name']}

Please verify the following results and provide feedback:

{json.dumps(previous_results, indent=2)}

Check for:
1. Completeness
2. Accuracy
3. Consistency
4. Quality

Provide a verification report with any issues found and recommendations for improvement.
"""

    async def _call_model(self, model: Any, prompt: str, task: Dict) -> str:
        """Call the AI model with the prompt."""
        # Mock implementation - in reality, this would call the actual model
        # For now, return a simulated response based on task type

        task_name = task["name"].lower()

        if "analyze" in task_name:
            return f"Analysis completed for task '{task['name']}'. Key insights: [Mock analysis results based on the provided context and requirements.]"
        elif "develop" in task_name or "implement" in task_name:
            return f"Development task '{task['name']}' completed. [Mock code implementation or development output.]"
        elif "strategy" in task_name:
            return f"Strategic recommendations for '{task['name']}': [Mock strategic analysis and recommendations.]"
        elif "verify" in task_name:
            return f"Verification complete for '{task['name']}'. All previous results appear valid and consistent."
        else:
            return f"Task '{task['name']}' completed successfully. [Mock response based on task requirements.]"

    async def _compile_response(
        self, results: Dict, plan: Dict, execution: Dict
    ) -> Dict:
        """Compile final response from task results."""
        # Aggregate all task results
        successful_tasks = [
            task_result
            for task_result in results.values()
            if task_result.get("status") == "completed"
        ]

        failed_tasks = [
            task_result
            for task_result in results.values()
            if task_result.get("status") == "failed"
        ]

        # Create comprehensive response
        if failed_tasks:
            # Partial completion
            response_content = self._create_partial_response(
                successful_tasks, failed_tasks, plan
            )
            status = "partial"
        else:
            # Full completion
            response_content = self._create_complete_response(successful_tasks, plan)
            status = "completed"

        return {
            "content": response_content,
            "metadata": {
                "plan_id": plan["id"],
                "status": status,
                "completed_tasks": len(successful_tasks),
                "failed_tasks": len(failed_tasks),
                "total_tasks": len(plan["tasks"]),
                "execution_time": self._calculate_execution_time(execution),
                "models_used": list(
                    set(
                        [task.get("model_used", "unknown") for task in successful_tasks]
                    )
                ),
            },
        }

    def _create_complete_response(
        self, successful_tasks: List[Dict], plan: Dict
    ) -> str:
        """Create response for successfully completed plan."""
        # Extract key results from tasks
        key_outputs = []
        for task in successful_tasks:
            result = task.get("result", {})
            output = (
                result.get("output")
                or result.get("verification_result")
                or "Task completed"
            )
            key_outputs.append(output)

        # Compile into coherent response
        response = f"I've successfully completed your request. Here's what I've accomplished:\n\n"

        for i, output in enumerate(key_outputs, 1):
            response += f"{i}. {output}\n\n"

        response += "Is there anything specific you'd like me to elaborate on or any follow-up questions you have?"

        return response

    def _create_partial_response(
        self, successful_tasks: List[Dict], failed_tasks: List[Dict], plan: Dict
    ) -> str:
        """Create response for partially completed plan."""
        response = (
            "I've completed most of your request, though I encountered some issues:\n\n"
        )

        # Add successful results
        if successful_tasks:
            response += "✅ **Completed Successfully:**\n"
            for task in successful_tasks:
                result = task.get("result", {})
                output = (
                    result.get("output")
                    or result.get("verification_result")
                    or "Task completed"
                )
                response += f"- {output}\n"
            response += "\n"

        # Add failed tasks
        if failed_tasks:
            response += "❌ **Issues Encountered:**\n"
            for task in failed_tasks:
                error = task.get("error", "Unknown error")
                response += f"- {error}\n"
            response += "\n"

        response += "Would you like me to retry the failed tasks or proceed with a different approach?"

        return response

    def _calculate_execution_time(self, execution: Dict) -> float:
        """Calculate total execution time in seconds."""
        start_time = datetime.fromisoformat(execution["started_at"])
        end_time = datetime.now()
        return (end_time - start_time).total_seconds()

    def get_execution_status(self, plan_id: str) -> Dict:
        """Get current status of a plan execution."""
        if plan_id in self.active_executions:
            return self.active_executions[plan_id]

        # Check execution history
        for execution in self.execution_history:
            if execution["plan_id"] == plan_id:
                return execution

        return None
