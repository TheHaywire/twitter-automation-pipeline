from typing import List, Any, Dict
from .agent_base import Agent

class AgentManager:
    """
    Orchestrates the agent pipeline, manages context, and handles errors.
    """
    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def run_pipeline(self, initial_input: Any) -> Any:
        context: Dict[str, Any] = {}
        data = initial_input
        for agent in self.agents:
            try:
                data = agent.run(data, context)
            except Exception as e:
                context['error'] = str(e)
                break
        return data
