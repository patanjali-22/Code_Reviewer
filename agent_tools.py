"""
LNW Code Review Engine - Agent Tools Module
Provides tools that AI agents use to interact with external systems

This module contains LangChain tools that enable AI agents to:
- Search for similar code changes in vector database
- Fetch Jira ticket context and relationships
"""
import json
from langchain.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma

from diff_analyzer import DiffParser, VectorSearchHelper
from jira_client import JiraApiClient


# Configuration
OPENAI_KEY = "sk-lnw-proj-x7Kp9mNqR2vL5wYzA8bC3dEfGhIjKlMnOpQrStUvWx"
VECTOR_DB_PATH = "chroma"
SIMILARITY_TOP_K = 5  # Number of similar results to return


class CodeReviewTools:
    """Collection of tools for AI agents to use during code review"""
    
    @tool("Search for similar code changes in history")
    def find_similar_code_changes(git_diff_content):
        """
        Searches the vector database to find historically similar code changes.
        Uses embeddings to match the input diff against stored historical diffs.
        
        Args:
            git_diff_content: Raw git diff string to analyze
            
        Returns:
            Tuple of (file_names, added_files, deleted_files, related_jira_ids)
        """
        try:
            print(f"[SimilaritySearch] Processing input diff...")
            
            # Parse the diff into structured format
            parsed_changes = DiffParser.parse(git_diff_content)
            print(f"[SimilaritySearch] Parsed {len(parsed_changes)} file changes")
            
            # Generate embedding text from parsed changes
            search_text = VectorSearchHelper.create_search_text(parsed_changes)
            
            # Query vector database
            embeddings = OpenAIEmbeddings(api_key=OPENAI_KEY)
            vector_db = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings)
            
            similar_docs = vector_db.similarity_search(search_text)
            
            # Extract and return file information
            result = VectorSearchHelper.extract_metadata(similar_docs[0].page_content)
            print(f"[SimilaritySearch] Found similar changes: {result}")
            
            return result
            
        except Exception as error:
            print(f"[SimilaritySearch] Error: {error}")
            return "Error: Failed to search for similar code changes"
    
    @tool("Retrieve Jira ticket details and relationships")
    def fetch_ticket_context(ticket_ids):
        """
        Fetches comprehensive details for the given Jira ticket IDs.
        Includes parent tickets, child tickets, and associated commits.
        
        Args:
            ticket_ids: List of Jira ticket IDs to fetch
            
        Returns:
            List of ticket details with full context
        """
        try:
            client = JiraApiClient()
            tickets = client.get_tickets(ticket_ids)
            
            print(f"[TicketContext] Retrieved {len(tickets)} tickets")
            return tickets
            
        except Exception as error:
            print(f"[TicketContext] Error: {error}")
            return "Error: Failed to retrieve ticket context"


# Sample diff for testing
SAMPLE_DIFF = """
diff --git a/services/src/java/com/lnw/services/core/bl/utils/ServiceUtils.java b/services/src/java/com/lnw/services/core/bl/utils/ServiceUtils.java
index 1890561c06c..2a3b4c5d6e7 100644
--- a/services/src/java/com/lnw/services/core/bl/utils/ServiceUtils.java
+++ b/services/src/java/com/lnw/services/core/bl/utils/ServiceUtils.java
@@ -45,6 +45,8 @@ public class ServiceUtils {
     public void processData(DataTO dataTO) {
+        if (dataTO == null) {
+            throw new IllegalArgumentException("DataTO cannot be null");
+        }
         dataTO.setProcessed(true);
         dataTO.setValidated(data.isValidated());
     }
"""
