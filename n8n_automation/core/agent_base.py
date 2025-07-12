"""
Agent Base Class

This module defines the base Agent class that all pipeline agents inherit from.
It provides a common interface and structure for the multi-agent AI system.

Key Features:
- Abstract base class for all agents
- Standardized run() method interface
- Type hints for input/output data
- Context passing between agents

Author: AI Assistant
Version: 1.0.0
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

class Agent(ABC):
    """
    Base class for all agents in the Twitter automation pipeline.
    
    All agents in the system inherit from this class and must implement
    the run() method. This ensures consistent interface and behavior
    across the entire pipeline.
    
    Attributes:
        name (str): Agent name for logging and identification
        description (str): Brief description of agent's purpose
        
    Methods:
        run(): Abstract method that must be implemented by subclasses
    """
    
    def __init__(self, name: str = None, description: str = None):
        """
        Initialize the agent with optional name and description.
        
        Args:
            name (str, optional): Agent name for logging
            description (str, optional): Agent description
        """
        self.name = name or self.__class__.__name__
        self.description = description or "AI Agent for Twitter automation"
    
    @abstractmethod
    def run(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """
        Run the agent with the given input and context.
        
        This is the main method that all agents must implement. It processes
        the input data using the provided context and returns the output
        that will be passed to the next agent in the pipeline.
        
        Args:
            input_data: The input data for this agent (can be any type)
            context: Dictionary containing information from previous agents
                     and global pipeline state
                     
        Returns:
            The output data from this agent (can be any type)
            
        Raises:
            Exception: If the agent fails to process the input
        """
        pass
    
    def __str__(self) -> str:
        """String representation of the agent."""
        return f"{self.name}: {self.description}"
    
    def __repr__(self) -> str:
        """Detailed string representation of the agent."""
        return f"{self.__class__.__name__}(name='{self.name}', description='{self.description}')"
