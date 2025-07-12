# Setup Guide

This guide will walk you through setting up the Twitter Automation Pipeline step by step.

## Prerequisites

- Python 3.8 or higher
- Twitter Developer Account
- Google Gemini API Key
- Basic command line knowledge

## Step 1: Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

## Step 2: Get API Keys

### Twitter API (X) Setup

1. **Create Twitter Developer Account**
   - Go to [Twitter Developer Portal](https://developer.twitter.com/)
   - Sign in with your Twitter account
   - Apply for a developer account (usually approved within 24 hours)

2. **Create a New App**
   - Click "Create App" or "Create Project"
   - Give your app a name (e.g., "Twitter Automation")
   - Select "Read and Write" permissions
   - Add your website URL (can be placeholder)

3. **Get OAuth2 Credentials**
   - Go to "Keys and Tokens" tab
   - Copy the "Client ID" and "Client Secret"
   - Set up OAuth2 redirect URI: `http://127.0.0.1:8080/callback`

### Google Gemini API Setup

1. **Get API Key**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the generated API key

## Step 3: Configure Environment

1. **Create .env file**
   ```bash
   # Copy the example (if available) or create manually
   cp .env.example .env
   ```

2. **Edit .env file**
   ```bash
   # Add your API keys
   X_CLIENT_ID=your_twitter_client_id_here
   X_CLIENT_SECRET=your_twitter_client_secret_here
   X_REDIRECT_URI=http://127.0.0.1:8080/callback
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   
   # System settings
   DRY_RUN=true                    # Start with true for testing
   SCHEDULE_TIMES=09:00,15:00,21:00
   LOG_DB_PATH=logs/agentic_research.db
   STRICTNESS=strict
   ```

## Step 4: Test Configuration

```bash
# Test that everything is set up correctly
python3 -c "from n8n_automation.app_config import Config; print('Config loaded successfully')"
```

## Step 5: Run in Test Mode

```bash
# Run the pipeline in DRY_RUN mode (no actual posting)
python3 -m n8n_automation.app --once
```

You should see output like:
```
===== TWEET/THREAD PREVIEW =====
Tweet 1: [Generated tweet content here]

DRY_RUN is enabled. This tweet/thread would NOT be posted.
```

## Step 6: Enable Real Posting

Once you're satisfied with the test results:

1. **Edit .env file**
   ```bash
   DRY_RUN=false
   ```

2. **Run for real posting**
   ```bash
   python3 -m n8n_automation.app --once
   ```

The system will now ask for your approval before posting each tweet.

## Troubleshooting

### Common Issues

#### "GEMINI_API_KEY not set"
- Make sure your `.env` file exists and contains the API key
- Check that the key is valid and not expired

#### "Twitter authentication failed"
- Verify your Twitter API credentials
- Ensure you have the correct permissions (Read and Write)
- Check that the redirect URI matches exactly

#### "Pipeline hangs on user input"
- Set `DRY_RUN=true` in your `.env` file
- This prevents the system from waiting for manual approval

#### "All LLM providers failed"
- Check your internet connection
- Verify your Gemini API key is valid
- Check the Google AI Studio for any service issues

### Getting Help

1. **Check the logs**
   ```bash
   tail -f logs/app.log
   ```

2. **Check the database**
   ```bash
   sqlite3 logs/agentic_research.db "SELECT * FROM research_log ORDER BY timestamp DESC LIMIT 10;"
   ```

3. **Verify configuration**
   ```bash
   python3 -c "from n8n_automation.app_config import Config; print(f'DRY_RUN: {Config.DRY_RUN}'); print(f'GEMINI_KEY: {Config.GEMINI_API_KEY[:10]}...' if Config.GEMINI_API_KEY else 'None')"
   ```

## Next Steps

Once setup is complete:

1. **Customize Content**: Edit agent prompts in the `agents/` directory
2. **Set Schedule**: Modify `SCHEDULE_TIMES` in `.env` for automated posting
3. **Monitor Performance**: Check the database for engagement metrics
4. **Scale Up**: Consider running multiple instances for different accounts

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and rotate them regularly
- Monitor your API usage to stay within limits
- Review generated content before posting in production

## Support

If you encounter issues:

1. Check this setup guide
2. Review the main README.md
3. Check the troubleshooting section
4. Verify all API credentials are correct
5. Ensure you have the latest version of the codebase 