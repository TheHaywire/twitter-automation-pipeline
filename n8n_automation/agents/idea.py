from ..core.agent_base import Agent
from typing import Any, Dict, List
from ..llm.router import LLMRouter
import n8n_automation.db as db
import random

TWEET_STYLES = [
    {
        'name': 'question',
        'prompt': "Write a tweet about {topic} that asks a thought-provoking question to spark replies. Use an emoji and a relevant hashtag.",
        'example': "What’s the one productivity hack you swear by? 👇 #Productivity"
    },
    {
        'name': 'hot_take',
        'prompt': "Write a bold or contrarian opinion tweet about {topic} to spark debate. Use an emoji and a hashtag.",
        'example': "Hot take: Most 'AI-powered' apps are just fancy wrappers around APIs. Prove me wrong. 🤔 #AI"
    },
    {
        'name': 'tip',
        'prompt': "Write a concise, actionable tip about {topic} for Twitter. Use an emoji and a relevant hashtag.",
        'example': "Pro tip: When debugging, explain your code to a rubber duck. It works! 🦆 #DevTips"
    },
    {
        'name': 'thread',
        'prompt': "Write a Twitter thread starter (hook) about {topic}. Make it irresistible to read the rest of the thread. Use an emoji and a hashtag.",
        'example': "10 lessons I learned building my first SaaS business (a thread) 🧵👇 #SaaS"
    },
    {
        'name': 'story',
        'prompt': "Write a tweet that tells a personal story or journey about {topic}. Use a conversational tone, an emoji, and a hashtag.",
        'example': "3 years ago, I knew nothing about coding. Today, I’m a full-time developer. Here’s how I did it… #100DaysOfCode"
    },
    {
        'name': 'poll',
        'prompt': "Write a tweet that runs a poll about {topic}. Include 2-4 options, an emoji, and a hashtag.",
        'example': "Which do you prefer for note-taking? 🅰️ Notion 🅱️ Evernote 🅾️ Google Keep Vote below! 👇 #ProductivityPoll"
    },
    {
        'name': 'quote',
        'prompt': "Write an inspirational quote tweet about {topic}. Use an emoji and a hashtag.",
        'example': '“The best way to get started is to quit talking and begin doing.” – Walt Disney ✨ #Motivation'
    },
    {
        'name': 'news',
        'prompt': "Write a tweet announcing news or an update about {topic}. Use an emoji and a hashtag.",
        'example': "Excited to announce our new AI-powered analytics dashboard is live! 🚀 #AI"
    },
    {
        'name': 'meme',
        'prompt': "Write a funny meme-style tweet about {topic}. Reference a popular meme or GIF, use an emoji and a hashtag.",
        'example': "Me: I’ll just check Twitter for 5 minutes. Also me, 2 hours later: [insert meme GIF] 😂 #Relatable"
    },
    {
        'name': 'cta',
        'prompt': "Write a tweet about {topic} with a direct call to action (retweet, like, follow, reply). Use an emoji and a hashtag.",
        'example': "If you found this thread helpful, retweet to help others! 🔁 #Learning"
    },
    {
        'name': 'visual',
        'prompt': "Write a tweet about {topic} that references an image, GIF, or video. Use an emoji and a hashtag.",
        'example': "Just finished my latest digital painting! What do you think? 🎨👇 #Art [image attached]"
    },
    {
        'name': 'event',
        'prompt': "Write a tweet live-tweeting or sharing an update from an event about {topic}. Use an emoji and a hashtag.",
        'example': "Live from #CES2025: The new foldable phone is wild! Here’s a first look… 📱 #TechNews"
    }
]

class IdeaAgent(Agent):
    """
    Generates tweet ideas for a given topic using the LLM, supporting multiple tweet styles.
    """
    def __init__(self, llm_router: LLMRouter):
        self.llm = llm_router

    def select_style(self) -> dict:
        # Randomly select a tweet style for diversity
        return random.choice(TWEET_STYLES)

    def run(self, input_data: Any, context: Dict[str, Any]) -> List[str]:
        topic = input_data if isinstance(input_data, str) else input_data[0]
        style = self.select_style()
        prompt = style['prompt'].format(topic=topic)
        output = self.llm.generate(prompt)
        # Split ideas if LLM returns a list
        ideas = [line.strip('- ').strip() for line in output.split('\n') if line.strip() and not line.lower().startswith('idea')]
        # Quality checks
        filtered_ideas = []
        for idea in ideas:
            if len(idea) > 280:
                continue
            if style['name'] == 'poll' and not any(opt in idea for opt in ['🅰️', '🅱️', 'option', 'vote']):
                continue
            filtered_ideas.append(idea)
        db.log_agent_step('idea_generator', {'topic': topic, 'style': style['name']}, filtered_ideas, 'llm', status='OK' if filtered_ideas else 'REJECTED')
        context['tweet_style'] = style['name']
        context['tweet_style_prompt'] = style['prompt']
        return filtered_ideas[:5]
