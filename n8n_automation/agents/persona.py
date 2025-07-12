from ..core.agent_base import Agent
from typing import Any, Dict, List
from ..llm.router import LLMRouter
import n8n_automation.db as db
import re

class PersonaAgent(Agent):
    """
    Rewrites tweets in a confident, modern, and friendly voice using the LLM, with strict quality checks and retry logic.
    """
    def __init__(self, llm_router: LLMRouter):
        self.llm = llm_router
        self.max_retries = 3
        self.meta_patterns = re.compile(r"(original tweet|rewrite|help you|paste|share|transform|let me|I can|send me|give me|please|content|instruction|how to|ready to|I'll need|I'm ready|Let's do this|just|output|improve|improved|tweet itself|message for you|what would you like|would you like me|your tweet here|I'll transform|I'll rewrite|I'll help|I'll make|I'll turn|I'll convert|I'll change|I'll edit|I'll fix|I'll update|I'll enhance|I'll modify|I'll adjust|I'll reword|I'll paraphrase|I'll restyle|I'll rephrase|I'll polish|I'll clean up|I'll tidy up|I'll jazz up|I'll spice up|I'll liven up|I'll brighten up|I'll freshen up|I'll pep up|I'll perk up|I'll jazz|I'll spice|I'll liven|I'll brighten|I'll freshen|I'll pep|I'll perk)", re.IGNORECASE)

    def is_meta_output(self, text: str) -> bool:
        return bool(self.meta_patterns.search(text))

    def run(self, input_data: Any, context: Dict[str, Any]) -> List[str]:
        tweets = input_data if isinstance(input_data, list) else [input_data]
        styled = []
        for tweet in tweets:
            for attempt in range(self.max_retries):
                prompt = (
                    "Rewrite the following tweet in a confident, modern, and friendly voice. Use emojis and line breaks. "
                    "Do NOT ask for the original tweet, do NOT give instructions, do NOT mention rewriting—just output the improved tweet itself.\n"
                    "Example: 'AI is changing the world 🌍 faster than ever! Are you ready to adapt? #AI #Future'\n"
                    f"Tweet: {tweet}"
                )
                output = self.llm.generate(prompt)
                if len(output) > 250 or len(output) < 20:
                    continue
                if self.is_meta_output(output):
                    continue
                styled.append(output.replace('\n', '\n'))
                break
        db.log_agent_step('persona_stylist', tweets, styled, 'llm', status='OK' if styled else 'REJECTED')
        context['styled_tweets'] = styled
        return styled
