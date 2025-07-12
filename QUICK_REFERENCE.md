# Quick Reference Guide

## 🚀 Essential Commands

### Setup
```bash
pip install -r requirements.txt
python3 -m n8n_automation.app --once  # Test run
```

### Configuration
```bash
# Enable real posting
sed -i '' 's/DRY_RUN=true/DRY_RUN=false/' .env

# Enable test mode  
sed -i '' 's/DRY_RUN=false/DRY_RUN=true/' .env
```

### Monitoring
```bash
# View logs
tail -f logs/app.log

# Check recent operations
sqlite3 logs/agentic_research.db "SELECT agent, status FROM research_log ORDER BY timestamp DESC LIMIT 10;"

# Check posted tweets
sqlite3 logs/agentic_research.db "SELECT text, posted_at FROM tweets ORDER BY id DESC LIMIT 5;"
```

## 🔧 Troubleshooting

### Common Issues
- **"GEMINI_API_KEY not set"**: Add API key to `.env`
- **"All LLM providers failed"**: Check internet and API key
- **Pipeline hangs**: Set `DRY_RUN=true` in `.env`
- **Twitter auth fails**: Verify OAuth2 credentials

### Debug Commands
```bash
# Test configuration
python3 -c "from n8n_automation.app_config import Config; print('Config OK')"

# Test LLM
python3 -c "from n8n_automation.llm.gemini import GeminiLLM; llm = GeminiLLM(); print('LLM OK')"

# Check errors
sqlite3 logs/agentic_research.db "SELECT * FROM research_log WHERE status LIKE '%ERROR%';"
```

## 📊 Database Queries

### Performance Check
```sql
SELECT agent, COUNT(*) as runs, 
       SUM(CASE WHEN status = 'OK' THEN 1 ELSE 0 END) as success
FROM research_log 
GROUP BY agent;
```

### Recent Activity
```sql
SELECT agent, input, status, timestamp 
FROM research_log 
ORDER BY timestamp DESC LIMIT 10;
```

## ⚙️ Configuration

### Required Environment Variables
- `X_CLIENT_ID` - Twitter OAuth2 client ID
- `X_CLIENT_SECRET` - Twitter OAuth2 client secret  
- `X_REDIRECT_URI` - OAuth2 redirect URI
- `GEMINI_API_KEY` - Google Gemini API key

### Optional Settings
- `DRY_RUN=true/false` - Test mode
- `SCHEDULE_TIMES=09:00,15:00,21:00` - Posting schedule
- `STRICTNESS=strict/medium/lenient` - Content filtering

## 📈 Content Styles

The system supports these tweet styles:
- question, hot_take, tip, thread, story
- poll, quote, news, meme, cta, visual, event

## 🆘 Emergency

### Stop Operations
```bash
pkill -f "n8n_automation"
echo "DRY_RUN=true" > .env
```

### Reset System
```bash
cp logs/agentic_research.db logs/backup_$(date +%Y%m%d).db
rm logs/agentic_research.db
python3 -c "import n8n_automation.db as db; db.init_db()"
```

---

For detailed documentation, see README.md and API_DOCUMENTATION.md 