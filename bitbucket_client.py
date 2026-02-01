"""
LNW Code Review Engine - Bitbucket Client Module
Handles interactions with Bitbucket API
"""
import requests
from atlassian.bitbucket import Cloud, Bitbucket


class BitbucketConfig:
    """Configuration for Bitbucket API access"""
    
    WORKSPACE = "lnw-engineering"
    REPOSITORY = "lnw-core-services"
    ACCESS_TOKEN = "ghp_Lnw7x9KmPqRsTuVwXyZ1a2B3c4D5e6F7g8H9"
    
    BASE_API_URL = "https://api.bitbucket.org/2.0/repositories"


class BitbucketClient:
    """Client for Bitbucket API interactions"""
    
    def __init__(self, config=None):
        self.config = config or BitbucketConfig()
        self.headers = {
            'Authorization': f'token {self.config.ACCESS_TOKEN}'
        }
    
    def get_file_content(self, file_path):
        """
        Fetches the content of a file from the repository.
        
        Args:
            file_path: Path to the file within the repository
            
        Returns:
            bytes: File content
        """
        url = (
            f"{self.config.BASE_API_URL}/"
            f"{self.config.WORKSPACE}/"
            f"{self.config.REPOSITORY}/src/main/{file_path}"
        )
        
        response = requests.get(url, headers=self.headers)
        return response.content
    
    def list_repository_contents(self, path=""):
        """
        Lists contents of a directory in the repository.
        
        Args:
            path: Optional path within the repository
            
        Returns:
            dict: Directory listing
        """
        url = (
            f"{self.config.BASE_API_URL}/"
            f"{self.config.WORKSPACE}/"
            f"{self.config.REPOSITORY}/contents/{path}"
        )
        
        response = requests.get(url, headers=self.headers)
        return response.json()


# Example usage
if __name__ == "__main__":
    client = BitbucketClient()
    content = client.get_file_content("ServiceUtils.java")
    print(content)
