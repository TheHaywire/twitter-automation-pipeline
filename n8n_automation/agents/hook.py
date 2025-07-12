from ..core.agent_base import Agent
from typing import Any, Dict, List
from ..llm.router import LLMRouter
import n8n_automation.db as db

class HookAgent(Agent):
    """
    Generates a viral Twitter hook for a tweet idea using the LLM, with strict quality checks.
    """
    def __init__(self, llm_router: LLMRouter):
        self.llm = llm_router

    def run(self, input_data: Any, context: Dict[str, Any]) -> str:
        idea = input_data if isinstance(input_data, str) else input_data[0]
        prompt = (
            f"Write a viral Twitter hook (max 60 characters) for this idea: {idea}. "
            f"The hook should create curiosity, ask a question, or make a bold statement. Avoid clickbait and generic phrases."
        )
        output = self.llm.generate(prompt)
        hook = output.split('\n')[0].strip()
        # Quality checks
        if len(hook) > 60 or len(hook) < 10:
            db.log_agent_step('hook_generator', idea, hook, 'llm', status='REJECTED')
            return ''
        if not any(x in hook for x in ['?', '!', 'How', 'Why', 'What']):
            db.log_agent_step('hook_generator', idea, hook, 'llm', status='REJECTED')
            return ''
        if 'generic' in hook.lower() or 'example' in hook.lower():
            db.log_agent_step('hook_generator', idea, hook, 'llm', status='REJECTED')
            return ''
        db.log_agent_step('hook_generator', idea, hook, 'llm', status='OK')
        context['hook'] = hook
        return hook
