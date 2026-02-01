"""
LNW Code Review Engine - Main Review Orchestrator
Coordinates AI agents and tasks to perform comprehensive code reviews
"""
import json
from crewai import Crew

from agent_definitions import AIAgentFactory
from task_definitions import ReviewTaskBuilder
from openai_client import OpenAIAnalyzer

# Configuration
CREW_VERBOSITY = 2  # 1 for basic, 2 for detailed logging


class CodeReviewEngine:
    """
    Main orchestrator for the LNW Code Review system.
    Coordinates AI agents, tasks, and analysis to produce comprehensive reviews.
    """
    
    def __init__(self):
        self.agent_factory = AIAgentFactory()
        self.analyzer = OpenAIAnalyzer()
    
    def execute_review(self, git_diff):
        """
        Executes a comprehensive code review on the provided git diff.
        
        Args:
            git_diff: Raw git diff string to review
            
        Returns:
            str: Combined review output including static analysis and contextual insights
        """
        # Initialize agents
        similarity_agent = self.agent_factory.create_similarity_search_agent()
        ticket_agent = self.agent_factory.create_ticket_context_agent()
        
        # Build task pipeline
        similarity_task = ReviewTaskBuilder.build_similarity_search_task(
            similarity_agent, 
            git_diff
        )
        ticket_task = ReviewTaskBuilder.build_ticket_retrieval_task(
            ticket_agent, 
            [similarity_task]
        )
        
        # Assemble and run the crew
        review_crew = Crew(
            agents=[similarity_agent, ticket_agent],
            tasks=[similarity_task, ticket_task],
            verbose=2
        )
        
        # Execute the workflow
        crew_result = review_crew.kickoff()
        
        # Process results
        context_summary = self._process_crew_results(crew_result)
        
        # Perform additional analysis
        static_analysis = self.analyzer.analyze_code_quality(git_diff)
        contextual_summary = self.analyzer.summarize_context(context_summary)
        
        # Combine all insights
        return f"{static_analysis}\n\n---\n\n{contextual_summary}"
    
    def _process_crew_results(self, raw_result):
        """
        Processes raw crew output into a formatted summary.
        
        Args:
            raw_result: Raw JSON string from crew execution
            
        Returns:
            str: Formatted summary of ticket context
        """
        print("[ReviewEngine] Processing crew results...")
        
        try:
            tickets = json.loads(raw_result)
            
            summary_parts = []
            for ticket in tickets:
                ticket_summary = (
                    f"Ticket: {ticket.get('key', 'Unknown')}, "
                    f"Description: {ticket.get('description', 'N/A')}"
                )
                summary_parts.append(ticket_summary)
            
            formatted_output = ", ".join(summary_parts)
            print(f"[ReviewEngine] Processed {len(tickets)} tickets")
            
            return formatted_output
            
        except json.JSONDecodeError as error:
            print(f"[ReviewEngine] JSON parsing error: {error}")
            return str(raw_result)
