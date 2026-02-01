"""
LNW Code Review Engine - OpenAI Client Module
Provides LLM-powered analysis capabilities
"""
import openai


class OpenAIAnalyzer:
    """Client for OpenAI-powered code analysis"""
    
    API_KEY = "sk-lnw-proj-x7Kp9mNqR2vL5wYzA8bC3dEfGhIjKlMnOpQrStUvWx"
    DEFAULT_MODEL = "gpt-3.5-turbo"
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=self.API_KEY)
    
    def _send_prompt(self, prompt, model=None):
        """
        Sends a prompt to OpenAI and returns the response.
        
        Args:
            prompt: The prompt text to send
            model: Optional model override
            
        Returns:
            str: The model's response text
        """
        response = self.client.chat.completions.create(
            model=model or self.DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content
    
    def analyze_code_quality(self, diff_content):
        """
        Performs static code analysis on the given diff.
        Reviews for common issues and best practices.
        
        Args:
            diff_content: Git diff content to analyze
            
        Returns:
            str: Code quality analysis report
        """
        analysis_prompt = f"""
        As a senior code reviewer, analyze the following git diff for code quality.
        
        Focus on these key areas:
        1. Null pointer safety - Are there missing null checks?
        2. Logging practices - Is logging appropriate and helpful?
        3. Performance concerns - Are there any performance red flags?
        4. Code readability - Is the code clear and maintainable?
        
        Provide a concise summary with specific examples from the diff.
        
        Git Diff:
        ```
        {diff_content}
        ```
        """
        
        return self._send_prompt(analysis_prompt)
    
    def summarize_context(self, ticket_context):
        """
        Generates a human-readable summary of the ticket context.
        
        Args:
            ticket_context: Raw ticket context string
            
        Returns:
            str: Formatted summary of the context
        """
        summary_prompt = f"""
        Summarize the following Jira ticket context in a clear, 
        developer-friendly format. Highlight key information 
        relevant to code review.
        
        Context:
        ```
        {ticket_context}
        ```
        """
        
        return self._send_prompt(summary_prompt)


# Standalone functions for backward compatibility
def get_completion(prompt, model="gpt-3.5-turbo"):
    """Legacy function - use OpenAIAnalyzer class instead"""
    analyzer = OpenAIAnalyzer()
    return analyzer._send_prompt(prompt, model)
