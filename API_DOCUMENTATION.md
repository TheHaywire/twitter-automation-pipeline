# API Documentation

This document provides detailed technical documentation for the Twitter Automation Pipeline API, intended for developers who want to extend, modify, or integrate with the system.

## Table of Contents

- [Core Classes](#core-classes)
- [Agent System](#agent-system)
- [LLM Integration](#llm-integration)
- [Twitter Integration](#twitter-integration)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Extending the System](#extending-the-system)

## Core Classes

### Agent Base Class

```python
from n8n_automation.core.agent_base import Agent

class Agent(ABC):
    """Base class for all pipeline agents."""
    
    def __init__(self, name: str = None, description: str = None):
        """Initialize agent with name and description."""
        
    @abstractmethod
    def run(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """Execute agent logic and return output."""
```

**Key Methods:**
- `run(input_data, context)`: Main execution method (abstract)
- `__str__()`: String representation
- `__repr__()`: Detailed representation

### Pipeline Class

```python
from n8n_automation.core.pipeline import Pipeline

class Pipeline:
    """Orchestrates the execution of multiple agents."""
    
    def __init__(self, agents: List[Agent]):
        """Initialize with list of agents."""
        
    def run(self, initial_input: Any, context: Dict[str, Any]) -> Any:
        """Execute all agents in sequence."""
```

## Agent System

### 1. TrendAgent

**Purpose**: Identifies trending topics for content generation

```python
from n8n_automation.agents.trend import TrendAgent

agent = TrendAgent()
topic, topics_list = agent.run(None, {})
```

**Input**: `None`
**Output**: `Tuple[str, List[str]]` - (selected_topic, all_topics)
**Fallback**: Pre-defined topic library

### 2. IdeaAgent

**Purpose**: Generates content ideas based on trending topics

```python
from n8n_automation.agents.idea import IdeaAgent

agent = IdeaAgent(llm_router)
ideas = agent.run(topic, {'trend_topic': topic})
```

**Input**: `str` - Trending topic
**Output**: `List[str]` - Content ideas
**Styles**: question, hot_take, tip, thread, story, poll, quote, news, meme, cta, visual, event

### 3. HookAgent

**Purpose**: Creates compelling hooks for content

```python
from n8n_automation.agents.hook import HookAgent

agent = HookAgent(llm_router)
hook = agent.run(idea, context)
```

**Input**: `str` - Content idea
**Output**: `str` - Engaging hook
**Validation**: Ensures hook is compelling and relevant

### 4. DraftingAgent

**Purpose**: Writes complete tweet content

```python
from n8n_automation.agents.drafting import DraftingAgent

agent = DraftingAgent(llm_router)
tweets = agent.run(idea, context)
```

**Input**: `str` - Content idea
**Output**: `List[str]` - Complete tweets/thread
**Features**: Thread creation, hashtag optimization

### 5. ComplianceAgent

**Purpose**: Ensures brand safety and compliance

```python
from n8n_automation.agents.compliance import ComplianceAgent

agent = ComplianceAgent()
passed, reason = agent.run(tweet, context)
```

**Input**: `str` - Tweet content
**Output**: `Tuple[bool, str]` - (approved, reason)
**Checks**: Brand safety, content guidelines, legal compliance

### 6. PersonaAgent

**Purpose**: Applies brand voice and personality

```python
from n8n_automation.agents.persona import PersonaAgent

agent = PersonaAgent(llm_router)
styled_tweets = agent.run(tweets, context)
```

**Input**: `List[str]` - Raw tweets
**Output**: `List[str]` - Styled tweets
**Features**: Emoji optimization, tone adjustment, brand voice

### 7. PeerReviewAgent

**Purpose**: Final quality assurance

```python
from n8n_automation.agents.peer_review import PeerReviewAgent

agent = PeerReviewAgent(llm_router)
approved = agent.run(tweet, context)
```

**Input**: `str` - Styled tweet
**Output**: `bool` - Approval status
**Criteria**: Engagement potential, brand alignment, quality

### 8. EngagementAgent

**Purpose**: Monitors tweet performance

```python
from n8n_automation.agents.engagement import EngagementAgent

agent = EngagementAgent()
metrics = agent.run(tweet_id, context)
```

**Input**: `str` - Tweet ID
**Output**: `Dict` - Engagement metrics
**Metrics**: Likes, retweets, replies, impressions

## LLM Integration

### LLMRouter

```python
from n8n_automation.llm.router import LLMRouter
from n8n_automation.llm.gemini import GeminiLLM

# Initialize with multiple providers
providers = [GeminiLLM(api_key, model)]
router = LLMRouter(providers)

# Generate text
response = router.generate(prompt, **kwargs)
```

**Features:**
- Multiple LLM provider support
- Automatic fallback on failure
- Consistent interface across providers

### GeminiLLM

```python
from n8n_automation.llm.gemini import GeminiLLM

llm = GeminiLLM(api_key="your_key", model="gemini-2.5-flash")
response = llm.generate("Your prompt here")
```

**Configuration:**
- `api_key`: Google Gemini API key
- `model`: Model name (default: gemini-2.5-flash)
- `temperature`: Generation randomness (0.0-1.0)
- `max_tokens`: Maximum response length

## Twitter Integration

### TwitterAPI

```python
from n8n_automation.integrations.twitter_api import TwitterAPI

api = TwitterAPI()

# Post single tweet
tweet_id = api.post_tweet("Your tweet content")

# Post thread
tweet_ids = api.post_thread(["Tweet 1", "Tweet 2", "Tweet 3"])

# Get engagement metrics
metrics = api.get_engagement(tweet_id)
```

**Methods:**
- `post_tweet(text)`: Post single tweet
- `post_thread(tweets)`: Post thread of tweets
- `get_engagement(tweet_id)`: Get engagement metrics
- `authenticate()`: OAuth2 authentication

### TwitterAuth

```python
from n8n_automation.integrations.twitter_auth import TwitterAuth

auth = TwitterAuth(client_id, client_secret, redirect_uri)
tokens = auth.authenticate()
```

**OAuth2 Flow:**
1. Initialize with client credentials
2. Generate authorization URL
3. Handle callback with authorization code
4. Exchange code for access tokens

## Database Schema

### research_log Table

```sql
CREATE TABLE research_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent TEXT NOT NULL,
    input TEXT,
    output TEXT,
    source TEXT DEFAULT 'local',
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'OK'
);
```

**Columns:**
- `id`: Unique identifier
- `agent`: Agent name (e.g., 'trend_fetcher', 'idea_generator')
- `input`: Input data (JSON or text)
- `output`: Output data (JSON or text)
- `source`: Data source ('local', 'llm', 'api')
- `timestamp`: ISO timestamp
- `status`: Status ('OK', 'ERROR', 'REJECTED', 'FALLBACK')

### tweets Table

```sql
CREATE TABLE tweets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    posted_at TEXT DEFAULT CURRENT_TIMESTAMP,
    engagement_stats TEXT,
    status TEXT DEFAULT 'DRAFT'
);
```

**Columns:**
- `id`: Unique identifier
- `text`: Tweet content
- `posted_at`: ISO timestamp when posted
- `engagement_stats`: JSON engagement metrics
- `status`: Status ('DRAFT', 'POSTED', 'FAILED')

## Configuration

### Environment Variables

```python
from n8n_automation.app_config import Config

# Access configuration
api_key = Config.GEMINI_API_KEY
dry_run = Config.DRY_RUN
schedule_times = Config.SCHEDULE_TIMES
```

**Required Variables:**
- `X_CLIENT_ID`: Twitter OAuth2 client ID
- `X_CLIENT_SECRET`: Twitter OAuth2 client secret
- `X_REDIRECT_URI`: OAuth2 redirect URI
- `GEMINI_API_KEY`: Google Gemini API key

**Optional Variables:**
- `GEMINI_MODEL`: LLM model name (default: gemini-2.5-flash)
- `DRY_RUN`: Test mode (default: true)
- `SCHEDULE_TIMES`: Posting schedule (default: 09:00,15:00,21:00)
- `LOG_DB_PATH`: Database path (default: logs/agentic_research.db)
- `STRICTNESS`: Content strictness (default: strict)

## Error Handling

### Exception Types

```python
# LLM Errors
class LLMError(Exception):
    """Raised when LLM generation fails."""
    pass

# Twitter API Errors
class TwitterAPIError(Exception):
    """Raised when Twitter API calls fail."""
    pass

# Agent Errors
class AgentError(Exception):
    """Raised when agent processing fails."""
    pass
```

### Error Recovery

```python
# Automatic retry with exponential backoff
def retry_with_backoff(func, max_retries=3, base_delay=1):
    """Retry function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
```

## Extending the System

### Adding New Agents

```python
from n8n_automation.core.agent_base import Agent

class CustomAgent(Agent):
    """Custom agent for specific functionality."""
    
    def __init__(self, llm_router=None):
        super().__init__(
            name="custom_agent",
            description="Custom agent for specific tasks"
        )
        self.llm_router = llm_router
    
    def run(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """Implement custom agent logic."""
        # Your custom logic here
        return processed_output
```

### Adding New LLM Providers

```python
class CustomLLM:
    """Custom LLM provider implementation."""
    
    def __init__(self, api_key: str, **kwargs):
        self.api_key = api_key
        # Initialize your LLM client
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using custom LLM."""
        # Your LLM integration here
        return generated_text
```

### Custom Database Operations

```python
import n8n_automation.db as db

# Log custom operation
db.log_agent_step(
    agent="custom_agent",
    input_data="input",
    output_data="output",
    source="custom",
    status="OK"
)

# Query custom data
results = db.query("SELECT * FROM research_log WHERE agent = ?", ["custom_agent"])
```

### Configuration Extensions

```python
# Add custom configuration
class ExtendedConfig(Config):
    CUSTOM_SETTING = os.getenv('CUSTOM_SETTING', 'default_value')
    CUSTOM_API_KEY = os.getenv('CUSTOM_API_KEY')
```

## Best Practices

### Agent Development

1. **Inherit from Agent base class**
2. **Implement proper error handling**
3. **Log all operations to database**
4. **Use type hints for clarity**
5. **Add comprehensive docstrings**

### LLM Integration

1. **Use consistent prompt templates**
2. **Implement retry logic**
3. **Handle rate limits gracefully**
4. **Validate LLM outputs**
5. **Cache responses when appropriate**

### Twitter Integration

1. **Respect rate limits**
2. **Handle authentication errors**
3. **Validate tweet content before posting**
4. **Monitor engagement metrics**
5. **Implement proper error recovery**

### Testing

```python
# Unit test example
def test_custom_agent():
    agent = CustomAgent()
    result = agent.run("test_input", {})
    assert result is not None
    assert isinstance(result, str)

# Integration test example
def test_pipeline_integration():
    pipeline = build_pipeline(llm_router)
    result = pipeline.run("test_input", {})
    assert result is not None
```

## Performance Considerations

### Optimization Tips

1. **Cache LLM responses** for repeated prompts
2. **Batch database operations** when possible
3. **Use async operations** for I/O-bound tasks
4. **Implement connection pooling** for database
5. **Monitor memory usage** with large datasets

### Scalability

1. **Horizontal scaling** with multiple instances
2. **Load balancing** across LLM providers
3. **Database optimization** with proper indexing
4. **Rate limiting** to respect API limits
5. **Queue management** for high-volume operations

---

This documentation provides a comprehensive guide for developers working with the Twitter Automation Pipeline. For additional support, refer to the main README.md and SETUP.md files. 