from ..core.agent_base import Agent
from typing import Any, Dict, List
from ..llm.router import LLMRouter
import n8n_automation.db as db
import random

class DraftingAgent(Agent):
    """
    Generates a Twitter thread using the LLM, with thread template, hashtag handling, and uniqueness enforcement.
    """
    def __init__(self, llm_router: LLMRouter):
        self.llm = llm_router
        self.max_tweets = 5

    def extract_hashtags(self, idea: str, context: Dict[str, Any]) -> List[str]:
        # Extract hashtags from idea/context or fallback
        hashtags = []
        if 'hashtags' in context and context['hashtags']:
            hashtags = context['hashtags']
        else:
            hashtags = [w for w in idea.split() if w.startswith('#')]
        # Limit to 2
        return hashtags[:2]

    def run(self, input_data: Any, context: Dict[str, Any]) -> List[str]:
        hook = context.get('hook')
        idea = context.get('idea') or (input_data if isinstance(input_data, str) else input_data[0])
        hashtags = self.extract_hashtags(idea, context)
        # Thread template
        thread_template = [
            f"[HOOK]",  # Tweet 1: Hook/intro
            "Share a surprising insight, fact, or example about the topic.",  # Tweet 2
            "Offer an actionable tip, lesson, or perspective.",  # Tweet 3
            "Ask a thought-provoking question or spark a debate.",  # Tweet 4
            "End with a strong, topic-specific call to action (CTA)."  # Tweet 5
        ]
        tweets = []
        for idx, template in enumerate(thread_template):
            if idx == 0:
                prompt = f"Write a strong Twitter hook for this topic: '{hook}'. Make it concise, punchy, and engaging. Include 1 relevant hashtag: {' '.join(hashtags)}."
            elif idx == 4:
                prompt = f"Write a strong, topic-specific call to action for a Twitter thread about: '{idea}'. Encourage replies, shares, or opinions. Include 1 relevant hashtag: {' '.join(hashtags)}."
            else:
                prompt = f"Write a unique, engaging tweet for a thread about: '{idea}'. This tweet should: {template} Include 1 relevant hashtag: {' '.join(hashtags)}."
            output = self.llm.generate(prompt)
            # Uniqueness enforcement
            if output in tweets or any(output.strip() in t for t in tweets):
                continue
            if len(output) > 250 or len(output) < 20:
                continue
            tweets.append(output.strip())
            if len(tweets) >= self.max_tweets:
                break
        db.log_agent_step('drafting', {'hook': hook, 'idea': idea, 'hashtags': hashtags}, tweets, 'llm', status='OK' if tweets else 'REJECTED')
        context['tweets'] = tweets
        return tweets
