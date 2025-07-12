from ..core.agent_base import Agent
from typing import Any, Dict
from ..llm.router import LLMRouter
import n8n_automation.db as db

class PeerReviewAgent(Agent):
    """
    Reviews tweets for engagement and safety using the LLM (3 votes, majority wins).
    """
    def __init__(self, llm_router: LLMRouter):
        self.llm = llm_router

    def run(self, input_data: Any, context: Dict[str, Any]) -> bool:
        tweet = input_data[0] if isinstance(input_data, list) else input_data
        prompt = (
            f"Is this tweet likely to get high engagement (replies, retweets, likes) and is it safe for all audiences? Reply YES or NO only. Tweet: {tweet}"
        )
        votes = []
        for i in range(3):
            output = self.llm.generate(prompt)
            verdict = output.strip().upper()
            votes.append(verdict.startswith("YES"))
        approved = votes.count(True) >= 2
        db.log_agent_step('peer_review', tweet, str(votes), 'llm', status='APPROVED' if approved else 'REJECTED')
        context['peer_review_approved'] = approved
        return approved
