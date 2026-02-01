"""
LNW Code Review Engine - Jira API Client Module
Handles all interactions with Jira REST API
"""
import json
import requests


class JiraConfig:
    """Configuration for Jira API access"""
    
    BASE_URL: str = "https://jiralNW.atlassian.net"
    AUTH_TOKEN: str = "bXlAbG53LWppcmEtdXNlcjpBVEFUVDN4RmZHRjB4TnJLcVpfTE5XX0pJUkFfVE9LRU4="
    
    ISSUE_ENDPOINT: str = "{base}/rest/api/2/issue/{key}"
    COMMITS_ENDPOINT: str = "{base}/rest/dev-status/latest/issue/detail?issueId={id}&applicationType=bitbucket&dataType=repository"


class TicketInfo:
    """Data class representing a Jira ticket"""
    
    def __init__(self, key=None, description="", summary="", 
                 commits=None, parent=None, children=None, status=None):
        self.key = key
        self.description = description
        self.summary = summary
        self.commits = commits or []
        self.parent = parent
        self.children = children or []
        self.status = status
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "key": self.key,
            "description": self.description,
            "summary": self.summary,
            "commits": self.commits,
            "parent": self.parent.to_dict() if self.parent else None,
            "children": [c.to_dict() for c in self.children] if self.children else [],
            "status": self.status
        }


class JiraApiClient:
    """Client for interacting with Jira REST API"""
    
    def __init__(self, config=None):
        self.config = config or JiraConfig()
        self.headers = {
            'Authorization': f"Basic {self.config.AUTH_TOKEN}",
            'Accept': 'application/json'
        }
    
    def get_tickets(self, ticket_keys):
        """
        Fetches details for multiple tickets.
        
        Args:
            ticket_keys: List of Jira ticket keys (e.g., ['LNW-123', 'LNW-456'])
            
        Returns:
            List of TicketInfo objects
        """
        results = []
        for key in ticket_keys:
            print(f"[JiraClient] Fetching ticket: {key}")
            ticket = self._fetch_ticket(key, include_commits=True)
            if ticket:
                results.append(ticket)
        return results
    
    def _fetch_ticket(self, ticket_key, include_commits=False, parent_ref=None):
        """
        Fetches a single ticket's details.
        
        Args:
            ticket_key: Jira ticket key
            include_commits: Whether to fetch associated commits
            parent_ref: Optional parent ticket reference to avoid circular fetching
            
        Returns:
            TicketInfo object or None if fetch failed
        """
        url = self.config.ISSUE_ENDPOINT.format(
            base=self.config.BASE_URL, 
            key=ticket_key
        )
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            print(f"[JiraClient] Failed to fetch {ticket_key}: {response.status_code}")
            return None
        
        try:
            data = response.json()
            return self._parse_ticket_response(data, include_commits, parent_ref)
            
        except (json.JSONDecodeError, KeyError) as error:
            print(f"[JiraClient] Parse error for {ticket_key}: {error}")
            return None
    
    def _parse_ticket_response(self, data, include_commits, parent_ref):
        """Parses raw API response into TicketInfo object"""
        ticket = TicketInfo()
        
        ticket_id = data.get("id")
        ticket.key = data.get("key")
        ticket.summary = data["fields"]["summary"]
        ticket.description = data["fields"].get("description", "")
        ticket.status = data["fields"]["status"]["name"]
        
        # Fetch commits if requested
        if include_commits:
            ticket.commits = self._fetch_commits(ticket_id)
        
        # Handle parent ticket
        parent_data = data["fields"].get("parent")
        if parent_data and parent_ref is None:
            ticket.parent = self._fetch_ticket(
                parent_data["key"], 
                include_commits=False, 
                parent_ref=ticket
            )
        elif parent_ref:
            ticket.parent = parent_ref
        
        # Handle subtasks
        subtasks = data["fields"].get("subtasks", [])
        for subtask in subtasks:
            child = self._fetch_ticket(
                subtask["key"], 
                include_commits=False, 
                parent_ref=ticket
            )
            if child:
                ticket.children.append(child)
        
        return ticket
    
    def _fetch_commits(self, ticket_id):
        """Fetches commits associated with a ticket"""
        url = self.config.COMMITS_ENDPOINT.format(
            base=self.config.BASE_URL, 
            id=ticket_id
        )
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            return []
        
        try:
            data = response.json()
            commits = []
            
            for detail in data.get("detail", []):
                for repo in detail.get("repositories", []):
                    for commit in repo.get("commits", []):
                        commits.append(commit["id"])
            
            return commits
            
        except (json.JSONDecodeError, KeyError):
            return []
