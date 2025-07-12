"""
Twitter Automation Pipeline - Main Application

This module orchestrates the complete Twitter automation workflow using a multi-agent AI system.
The pipeline generates, validates, and posts high-quality Twitter content automatically.

Key Components:
- Multi-agent AI pipeline (8 specialized agents)
- LLM integration (Google Gemini)
- Twitter API integration
- Comprehensive logging and monitoring
- DRY_RUN mode for safe testing

Usage:
    python3 -m n8n_automation.app --once    # Single run
    python3 -m n8n_automation.app           # Scheduled runs

Author: AI Assistant
Version: 1.0.0
"""

import logging
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables before importing config
from .app_config import Config
from .logging_config import setup_logging
from .llm.router import LLMRouter
from .llm.gemini import GeminiLLM
from .agents.trend import TrendAgent
from .agents.idea import IdeaAgent
from .agents.hook import HookAgent
from .agents.drafting import DraftingAgent
from .agents.compliance import ComplianceAgent
from .agents.persona import PersonaAgent
from .agents.peer_review import PeerReviewAgent
from .agents.engagement import EngagementAgent
from .core.pipeline import Pipeline
from .integrations.twitter_api import TwitterAPI
import n8n_automation.db as db
from .scheduler import schedule_jobs, run_scheduler
import sys
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

def build_pipeline(llm_router):
    """
    Builds the complete AI agent pipeline for Twitter content generation.
    
    The pipeline consists of 8 specialized agents that work sequentially:
    1. TrendAgent: Identifies trending topics
    2. IdeaAgent: Generates content ideas
    3. HookAgent: Creates compelling hooks
    4. DraftingAgent: Writes full tweets/threads
    5. ComplianceAgent: Ensures brand safety
    6. PersonaAgent: Applies brand voice
    7. PeerReviewAgent: Quality assurance
    8. EngagementAgent: Performance monitoring
    
    Args:
        llm_router: LLMRouter instance for AI text generation
        
    Returns:
        List[Agent]: Ordered list of agents in the pipeline
    """
    return [
        TrendAgent(),
        IdeaAgent(llm_router),
        HookAgent(llm_router),
        DraftingAgent(llm_router),
        ComplianceAgent(),
        PersonaAgent(llm_router),
        PeerReviewAgent(llm_router),
        EngagementAgent(),
    ]

def main(run_once: bool = False):
    """
    Main entry point for the Twitter automation pipeline.
    
    Initializes all components and runs the workflow either once or on a schedule.
    
    Args:
        run_once (bool): If True, run once and exit. If False, run on schedule.
        
    Workflow:
        1. Setup logging and database
        2. Initialize LLM router with Gemini
        3. Build agent pipeline
        4. Initialize Twitter API
        5. Run workflow (once or scheduled)
    """
    setup_logging()
    logging.info("Starting Twitter automation pipeline...")
    db.init_db()
    llm_router = LLMRouter([GeminiLLM(Config.GEMINI_API_KEY, Config.GEMINI_MODEL)])
    agents = build_pipeline(llm_router)
    pipeline = Pipeline(agents)
    twitter_api = TwitterAPI()

    def run_workflow():
        logging.info("Running agentic workflow...")
        summary_table = Table(title="Pipeline Run Summary", box=box.SIMPLE_HEAVY)
        summary_table.add_column("Step", style="bold cyan")
        summary_table.add_column("Input", style="white")
        summary_table.add_column("Output", style="yellow")
        summary_table.add_column("Status", style="bold")
        attempts = []
        # Try up to 5 topics (fallbacks)
        topics_tried = 0
        max_topics = 5
        topic, topics = agents[0].run(None, {})
        topics_list = [topic] + [t for t in topics if t != topic]
        for topic in topics_list[:max_topics]:
            topics_tried += 1
            summary_table.add_row("TrendAgent", "None", topic, "OK" if topic else "REJECTED")
            ideas = agents[1].run(topic, {})
            summary_table.add_row("IdeaAgent", topic, str(ideas), "OK" if ideas else "REJECTED")
            if not ideas:
                attempts.append((topic, "No ideas generated"))
                continue
            for idea in ideas:
                context = {'idea': idea, 'trend_topic': topic, 'trend_topics': topics}
                hook = agents[2].run(idea, context)
                summary_table.add_row("HookAgent", idea, hook, "OK" if hook else "REJECTED")
                if not hook:
                    attempts.append((idea, "No valid hook generated"))
                    continue
                tweets = agents[3].run(idea, context)
                summary_table.add_row("DraftingAgent", idea, str(tweets), "OK" if tweets else "REJECTED")
                if not tweets:
                    attempts.append((idea, "No valid tweets generated"))
                    continue
                passed, reason = agents[4].run(tweets[0], context)
                summary_table.add_row("ComplianceAgent", tweets[0], reason, "OK" if passed else "REJECTED")
                if not passed:
                    attempts.append((tweets[0], f"Compliance failed: {reason}"))
                    continue
                styled_tweets = agents[5].run(tweets, context)
                summary_table.add_row("PersonaAgent", str(tweets), str(styled_tweets), "OK" if styled_tweets else "REJECTED")
                if not styled_tweets:
                    attempts.append((tweets, "No styled tweets generated"))
                    continue
                approved = agents[6].run(styled_tweets[0], context)
                summary_table.add_row("PeerReviewAgent", styled_tweets[0], str(approved), "OK" if approved else "REJECTED")
                if not approved:
                    attempts.append((styled_tweets[0], "Peer review rejected"))
                    continue
                # DRY_RUN and human review logic
                console.print("[magenta bold]\n===== TWEET/THREAD PREVIEW =====[/magenta bold]")
                for idx, tweet in enumerate(styled_tweets):
                    console.print(f"[white]Tweet {idx+1}:[/white] {tweet}")
                console.print("[magenta bold]===============================\n[/magenta bold]")
                if Config.DRY_RUN:
                    console.print("[yellow]DRY_RUN is enabled. This tweet/thread would NOT be posted.[/yellow]")
                else:
                    approve = input("Approve this tweet/thread for posting? (y/n): ").strip().lower()
                    if approve != 'y':
                        console.print("[yellow]Tweet not posted.[/yellow]")
                        continue
                    tweet_ids = twitter_api.post_thread(styled_tweets)
                    if tweet_ids:
                        agents[7].run(tweet_ids[0], context)
                    else:
                        logging.warning("No tweet IDs returned; skipping engagement monitoring.")
                # Print summary
                console.print("[cyan bold]\n===== SUMMARY =====[/cyan bold]")
                console.print(f"[green]Topic:[/green] {topic}")
                console.print(f"[green]Idea:[/green] {idea}")
                console.print(f"[green]Hook:[/green] {hook}")
                console.print(f"[green]Tweets:[/green]")
                for idx, tweet in enumerate(styled_tweets):
                    console.print(f"  {idx+1}. {tweet}")
                console.print("[cyan bold]===================\n[/cyan bold]")
                console.print(summary_table)
                return
        # If we get here, all attempts failed
        console.print("[red bold]No valid tweet could be generated today after trying all topics and ideas.[/red bold]")
        if attempts:
            fail_table = Table(title="Failed Attempts", box=box.SIMPLE_HEAVY)
            fail_table.add_column("Input", style="white")
            fail_table.add_column("Reason", style="red")
            for input_val, reason in attempts:
                fail_table.add_row(str(input_val), reason)
            console.print(fail_table)
        console.print(summary_table)
        logging.info("Pipeline run complete.")

    if run_once:
        run_workflow()
    else:
        schedule_jobs(run_workflow, Config.SCHEDULE_TIMES)
        run_scheduler()

if __name__ == "__main__":
    run_once = '--once' in sys.argv
    main(run_once=run_once)
