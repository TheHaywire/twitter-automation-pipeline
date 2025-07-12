# Gemini + Twitter Automation: Free, Local Solution (Python)

## Overview
Automate content curation, AI tweet generation, and posting to Twitter using only free tools:
- **Python** (>=3.7)
- **Tweepy** (Twitter API)
- **Google Gemini API** (for AI text generation)
- **feedparser** (for news/RSS, optional)
- **dotenv** (for secrets)

---

## 1. Prerequisites & Setup

### A. Twitter Developer Account
- Sign up at [Twitter Developer Portal](https://developer.twitter.com/en/portal/projects-and-apps)
- Create an app, generate:
  - API Key & Secret
  - Access Token & Secret
- Set app permissions to **Read and Write**

### B. Google Gemini API
- Get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey)
- Review [Gemini API Python Quickstart](https://ai.google.dev/gemini-api/docs/quickstart?hl=en)

### C. Install Python Packages
```sh
pip install tweepy google-generativeai python-dotenv feedparser schedule
```

### D. Store Secrets in `.env`
```
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_TOKEN_SECRET=...
GEMINI_API_KEY=...
```

---

## 2. Workflow Design

### A. Fetch Trending Topics or News
- Use Tweepy to fetch Twitter trends:
  ```python
  import tweepy
  api = tweepy.API(auth)
  trends = api.trends_place(id=1)  # 1 = Worldwide
  topics = [t['name'] for t in trends[0]['trends']]
  ```
- Or use `feedparser` to get news headlines:
  ```python
  import feedparser
  feed = feedparser.parse('https://news.google.com/rss')
  headlines = [entry.title for entry in feed.entries]
  ```

### B. Generate Tweets with Gemini
- Use the Gemini API for text generation:
  ```python
  import google.generativeai as genai
  genai.configure(api_key=GEMINI_API_KEY)
  model = genai.GenerativeModel('gemini-2.5-flash')
  prompt = f"Write a concise, engaging tweet about: {topic}"
  response = model.generate_content(prompt)
  tweet = response.text
  ```

### C. Post Tweets with Tweepy
- Authenticate and post:
  ```python
  api.update_status(tweet)
  ```

### D. (Optional) Schedule Tweets
- Use the `schedule` library or cron to automate posting times.

### E. (Optional) Log Tweets
- Save posted tweets to a CSV or Google Sheet for memory/analytics.

---

## 3. Security & Best Practices
- **Never hardcode secrets**; always use `.env` and `python-dotenv`.
- **Rate limits:** Respect Twitter and Gemini API rate limits.
- **Error handling:** Add try/except blocks for API calls.
- **Content filtering:** Optionally filter AI output for compliance/brand safety.

---

## 4. Extensibility
- Add more sources (RSS, web scraping, etc.) for content ideas.
- Use Gemini for reply/engagement automation.
- Integrate with Google Sheets for persistent memory.
- Deploy as a background service (systemd, tmux, or cloud VM).

---

## 5. References & Further Reading
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Tweepy Docs](https://docs.tweepy.org/en/stable/)
- [Automate Social Media Posts with Python (FollowedApp)](https://followedapp.com/automate-social-media-posts/)
- [DigitalOcean: Scrape Web Pages and Post to Twitter](https://www.digitalocean.com/community/tutorials/how-to-scrape-web-pages-and-post-content-to-twitter-with-python-3)
- [Mastering Twitter Automation with Tweepy (Medium)](https://medium.com/@danielwume/mastering-twitter-automation-with-tweepy-a-comprehensive-guide-with-advanced-python-code-examples-defb6deae181)

---

## 6. Example Directory Structure
```
project-root/
  |-- .env
  |-- main.py
  |-- requirements.txt
  |-- README.md
  |-- logs/
  |-- data/
```

---

## 7. Next Steps
- Use this plan to scaffold your project.
- Start with authentication and a simple tweet post.
- Add Gemini integration for AI-generated content.
- Expand with scheduling, logging, and analytics as needed.

---

## 8. Optional Enhancements

### A. Scheduling
- Use the `schedule` Python package to run posting jobs at set intervals.
- Example:
  ```python
  import schedule, time
  schedule.every().day.at("09:00").do(post_tweet_function)
  while True:
      schedule.run_pending()
      time.sleep(1)
  ```

### B. Logging
- Use Python's built-in `logging` module for runtime logs.
- Log posted tweets to a CSV file or Google Sheet (with `gspread`).

### C. Analytics
- Track engagement by fetching tweet stats with Tweepy (`api.get_status`).
- Store analytics in CSV or Google Sheets for review.

### D. Engagement Automation
- Use Tweepy to monitor mentions, replies, or DMs.
- Use Gemini to generate automated replies based on incoming tweets.
- Example: Stream mentions and auto-reply with AI-generated content.

--- 