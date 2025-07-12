from .agent_manager import AgentManager
from typing import Any, List

class Pipeline:
    """
    Defines and runs the agent workflow pipeline.
    """
    def __init__(self, agents: List[Any]):
        self.manager = AgentManager(agents)

    def run(self, initial_input: Any) -> Any:
        return self.manager.run_pipeline(initial_input)
