from ..core.agent_base import Agent
from typing import Any, Dict, Tuple
import n8n_automation.db as db
import re

class ComplianceAgent(Agent):
    """
    Checks tweets for banned words, hashtag count, links, and excessive mentions.
    """
    BANNED_WORDS = ["scam", "fake", "NSFW", "hate", "violence"]
    MAX_LENGTH = 250
    MAX_HASHTAGS = 2
    MAX_MENTIONS = 2

    def run(self, input_data: Any, context: Dict[str, Any]) -> Tuple[bool, str]:
        tweet = input_data[0] if isinstance(input_data, list) else input_data
        if any(word.lower() in tweet.lower() for word in self.BANNED_WORDS):
            db.log_agent_step('compliance', tweet, 'Banned word', 'local', status='REJECTED')
            return False, "Banned word"
        if len(tweet) > self.MAX_LENGTH:
            db.log_agent_step('compliance', tweet, 'Too long', 'local', status='REJECTED')
            return False, "Too long"
        if tweet.count('#') > self.MAX_HASHTAGS:
            db.log_agent_step('compliance', tweet, 'Too many hashtags', 'local', status='REJECTED')
            return False, "Too many hashtags"
        if len(re.findall(r'http[s]?://', tweet)) > 0:
            db.log_agent_step('compliance', tweet, 'Contains link', 'local', status='REJECTED')
            return False, "Contains link"
        if tweet.count('@') > self.MAX_MENTIONS:
            db.log_agent_step('compliance', tweet, 'Too many mentions', 'local', status='REJECTED')
            return False, "Too many mentions"
        db.log_agent_step('compliance', tweet, 'OK', 'local', status='OK')
        return True, "OK"
