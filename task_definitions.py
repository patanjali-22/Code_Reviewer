"""
LNW Code Review Engine - Task Definitions Module
Defines the tasks that agents execute during code review
"""
from crewai import Task
from textwrap import dedent


class ReviewTaskBuilder:
    """Builder class for creating code review tasks"""
    
    @staticmethod
    def build_similarity_search_task(agent, code_diff):
        """
        Creates a task to search for similar historical code changes.
        
        Args:
            agent: The AI agent to execute this task
            code_diff: The git diff content to analyze
            
        Returns:
            Task: Configured task for similarity search
        """
        return Task(
            description=dedent(f"""
                Analyze the provided git diff and search the vector database 
                to find historically similar code changes and patterns.
                
                Input Git Diff:
                {code_diff}
            """),
            agent=agent,
            expected_output="List of similar historical git differences with associated metadata"
        )
    
    @staticmethod
    def build_ticket_retrieval_task(agent, preceding_tasks):
        """
        Creates a task to retrieve Jira ticket context.
        
        Args:
            agent: The AI agent to execute this task
            preceding_tasks: List of tasks whose output provides context
            
        Returns:
            Task: Configured task for ticket retrieval
        """
        return Task(
            description=dedent("""
                Extract Jira ticket IDs from the context provided by the preceding task 
                and retrieve comprehensive details about each ticket.
                
                Expected context format:
                    File: services/src/java/com/lnw/services/core/bl/utils/ServiceUtils.java
                    Added Lines:
                      ++b/services/src/java/com/lnw/services/core/bl/utils/ServiceUtils.java
                      dataTO.setProcessed(data.isProcessed());
                      dataTO.setValidated(data.isValidated());
                    Deleted Lines:
                      --a/services/src/java/com/lnw/services/core/bl/utils/ServiceUtils.java
                        parent_jira_id abc123def
                    Related Jira: [TICKET-1, TICKET-2]
                    
                Look for ticket IDs in the 'Related Jira' field.
            """),
            agent=agent,
            expected_output='''
                Return a JSON array of ticket details with the following structure:
                [
                    {
                        "key": "LNW-1234",
                        "description": "Description of the ticket",
                        "summary": "Brief summary",
                        "commits": ["commit_hash_1", "commit_hash_2"],
                        "parent": ["PARENT-123"],
                        "children": ["CHILD-456"],
                        "status": "In Progress"
                    }
                ]
            ''',
            context=preceding_tasks
        )
