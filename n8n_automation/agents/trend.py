from ..core.agent_base import Agent
from typing import Any, Dict, Tuple, List
import random
import n8n_automation.db as db

class TrendAgent(Agent):
    """
    Fetches or selects trending topics for tweet generation.
    """
    FALLBACK_TOPICS = [
        'AI', 'Artificial Intelligence', 'Machine Learning', 'Deep Learning', 'Generative AI',
        'LLM', 'ChatGPT', 'Gemini', 'OpenAI', 'Anthropic', 'Prompt Engineering', 'Agentic AI',
        'AI Security', 'AI Red Teaming', 'AI Regulation', 'AI Ethics', 'AI Safety', 'AI Compliance',
        'AI Risk', 'AI Governance', 'AI Policy', 'AI in Healthcare', 'AI in Finance', 'AI in Cybersecurity',
        'Cybersecurity', 'Zero Trust', 'Ransomware', 'Phishing', 'Data Breach', 'Zero-Day',
        'Threat Intelligence', 'Red Team', 'Blue Team', 'SOC', 'SIEM', 'Incident Response',
        'Supply Chain Security', 'Cloud Security', 'OT Security', 'IoT Security', 'Identity Theft',
        'Password Hygiene', 'MFA', 'DDoS', 'APT', 'Vulnerability', 'Patch Management',
        'Social Engineering', 'Insider Threat', 'Quantum Security', 'Privacy', 'Compliance',
        'CISA', 'NIST', 'ISO 42005', 'Tech', 'Innovation', 'Future', 'Automation', 'Data Science',
        'Big Data', 'Edge Computing', 'Quantum Computing', 'Blockchain', 'Web3', 'Metaverse',
        'Digital Transformation', 'Smart Home', 'Smart Cities', 'Cloud', 'DevOps', 'SRE',
        'API Security', 'Open Source', 'Digital Identity', 'Biometrics', 'Privacy by Design',
        'Digital Twins', '5G', '6G', 'IoT', 'Wearables', 'AR', 'VR', 'XR',
        'AI National Security', 'AI Policy', 'AI Summit', 'AI Safety Commitments', 'AI in Government',
        'AI in Education', 'AI in Law', 'AI in Art', 'AI in Music', 'AI in Gaming', 'AI in Social Media',
        'AI in Marketing', 'AI in Retail', 'AI in Manufacturing', 'AI in Energy', 'AI in Transportation', 'AI in Space',
    ]

    def run(self, input_data: Any, context: Dict[str, Any]) -> Tuple[str, List[str]]:
        # In the future, fetch from RSS/news APIs here
        topic = random.choice(self.FALLBACK_TOPICS)
        topics = self.FALLBACK_TOPICS
        db.log_agent_step('trend_fetcher', '', topic, 'local', status='FALLBACK')
        context['trend_topic'] = topic
        context['trend_topics'] = topics
        return topic, topics
