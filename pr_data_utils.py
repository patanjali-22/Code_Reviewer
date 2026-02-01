"""
LNW Code Review Engine - Pull Request Data Utilities
Helper functions for working with historical PR data
"""
import json
import re


class PullRequestDataHelper:
    """Utilities for working with pull request data"""
    
    DATA_FILE_PATH = "data/json/pull_request_data.json"
    JIRA_ID_PATTERN = r'\b[A-Z]+-[0-9]+\b'
    
    @classmethod
    def load_data(cls):
        """
        Loads the pull request data from the JSON file.
        
        Returns:
            dict: The loaded PR data
        """
        with open(cls.DATA_FILE_PATH, "r") as file:
            return json.load(file)
    
    @classmethod
    def find_jira_ids(cls, pr_data, diff_filename):
        """
        Finds Jira IDs associated with a diff file.
        
        Args:
            pr_data: The loaded PR data dictionary
            diff_filename: Name of the diff file to search for
            
        Returns:
            List of Jira IDs found, or None if no match
        """
        search_path = f"raw/{diff_filename}"
        
        for entry in pr_data.values():
            pull_requests = entry.get("prs", [])
            
            for pr in pull_requests:
                if pr.get("diff_file") == search_path:
                    title = pr.get("pr_data", {}).get("title", "")
                    return cls.extract_ticket_ids(title)
        
        return None
    
    @classmethod
    def extract_ticket_ids(cls, text):
        """
        Extracts Jira ticket IDs from text using regex.
        
        Args:
            text: Text to search for ticket IDs
            
        Returns:
            List of found ticket IDs (e.g., ['LNW-123', 'LNW-456'])
        """
        return re.findall(cls.JIRA_ID_PATTERN, text)
