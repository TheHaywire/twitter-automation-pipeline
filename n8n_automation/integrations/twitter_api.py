import requests
from typing import List, Optional
from .twitter_auth import get_valid_access_token, refresh_access_token
import n8n_automation.db as db
from datetime import datetime
import time

class TwitterAPI:
    """
    Handles posting tweets and threads using Twitter API v2.
    """
    def __init__(self):
        self.access_token, self.refresh_token = get_valid_access_token()

    def post_tweet(self, text: str, in_reply_to: Optional[str] = None) -> Optional[str]:
        post_url = 'https://api.twitter.com/2/tweets'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }
        data = {'text': text}
        if in_reply_to:
            data['reply'] = {'in_reply_to_tweet_id': in_reply_to}
        resp = requests.post(post_url, headers=headers, json=data)
        if resp.status_code == 201:
            tweet_id = resp.json()['data']['id']
            db.log_tweet(text, datetime.utcnow().isoformat(), engagement_stats=None, status='POSTED')
            return tweet_id
        elif resp.status_code == 401 and self.refresh_token:
            # Try to refresh token and retry
            tokens = refresh_access_token(self.refresh_token)
            if tokens and 'access_token' in tokens:
                self.access_token = tokens['access_token']
                self.refresh_token = tokens.get('refresh_token', self.refresh_token)
                headers['Authorization'] = f'Bearer {self.access_token}'
                resp = requests.post(post_url, headers=headers, json=data)
                if resp.status_code == 201:
                    tweet_id = resp.json()['data']['id']
                    db.log_tweet(text, datetime.utcnow().isoformat(), engagement_stats=None, status='POSTED')
                    return tweet_id
            db.log_tweet(text, datetime.utcnow().isoformat(), engagement_stats=None, status='FAILED')
            return None
        else:
            db.log_tweet(text, datetime.utcnow().isoformat(), engagement_stats=None, status='FAILED')
            return None

    def post_thread(self, tweets: List[str]) -> List[str]:
        tweet_ids = []
        in_reply_to = None
        for idx, tweet in enumerate(tweets):
            tweet_id = self.post_tweet(tweet, in_reply_to=in_reply_to)
            if tweet_id:
                tweet_ids.append(tweet_id)
                in_reply_to = tweet_id
                time.sleep(2)  # Avoid rate limits
            else:
                break
        return tweet_ids
