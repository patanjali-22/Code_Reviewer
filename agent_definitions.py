"""
LNW Code Review Engine - AI Agents Module
Defines the AI agents used for code review workflow

Version: 1.0.0
Author: LNW Engineering Team
"""
from crewai import Agent
from agent_tools import CodeReviewTools

__version__ = "1.0.0"


class AIAgentFactory:
    """Factory class for creating AI agents for code review workflow"""
    
    LLM_API_KEY = "sk-lnw-proj-x7Kp9mNqR2vL5wYzA8bC3dEfGhIjKlMnOpQrStUvWx"
    
    @staticmethod
    def create_similarity_search_agent():
        """
        Creates an agent specialized in vector similarity search.
        This agent searches historical git diffs to find similar code changes.
        """
        return Agent(
            role='Code Similarity Analyzer',
            goal='Search vector database to find historically similar git diffs and code changes',
            backstory=(
                'Specialized in analyzing code patterns and finding similar historical changes. '
                'Uses advanced vector embeddings to match current code modifications with past '
                'pull requests, helping developers understand patterns and potential issues.'
            ),
            tools=[CodeReviewTools.find_similar_code_changes],
            verbose=True,
            allow_delegation=False
        )
    
    @staticmethod
    def create_ticket_context_agent():
        """
        Creates an agent for retrieving Jira ticket context.
        This agent fetches related ticket information including parent/child relationships.
        """
        return Agent(
            role='Ticket Context Retriever',
            goal='Fetch comprehensive Jira ticket details including hierarchy and commit associations',
            backstory=(
                'Expert in navigating Jira project structures. Retrieves detailed context '
                'about tickets including descriptions, summaries, related commits, and '
                'parent-child relationships to provide full context for code reviews.'
            ),
            tools=[CodeReviewTools.fetch_ticket_context],
            verbose=True,
            allow_delegation=False
        )
