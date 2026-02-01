"""
LNW Code Review Engine - Diff Analyzer Module
Parses and analyzes git diff content for vector search
"""
import json
from pr_data_utils import PullRequestDataHelper


class DiffParser:
    """Parses raw git diff content into structured data"""
    
    # File patterns to exclude from analysis
    EXCLUDED_PATTERNS = ['DAO', '.xml']
    
    @classmethod
    def parse(cls, diff_text):
        """
        Parses a git diff string into structured file changes.
        
        Args:
            diff_text: Raw git diff content
            
        Returns:
            List of tuples: (filename, added_lines, deleted_lines, parent_commit)
        """
        changes = []
        current_file = None
        additions = []
        deletions = []
        parent_commit = ""
        
        for line in diff_text.split('\n'):
            # New file detected
            if line.startswith('diff --git'):
                # Save previous file if exists and not excluded
                if current_file and not cls._should_exclude(current_file):
                    changes.append((current_file, additions, deletions, parent_commit))
                
                # Reset for new file
                current_file = line.split(' ')[-1][2:]  # Extract filename
                additions = []
                deletions = []
                parent_commit = ""
                
            elif line.startswith('@@'):
                continue  # Skip hunk headers
                
            elif line.startswith('+') and len(line) > 1:
                additions.append(line[1:])
                
            elif line.startswith('-') and len(line) > 1:
                deletions.append(line[1:])
                
            elif line.startswith("index "):
                # Extract parent commit hash
                parent_commit = line.split()[1].split("..")[0]
        
        # Don't forget the last file
        if current_file and not cls._should_exclude(current_file):
            changes.append((current_file, additions, deletions, parent_commit))
        
        return changes
    
    @classmethod
    def _should_exclude(cls, filename):
        """Check if file should be excluded from analysis"""
        return any(pattern in filename for pattern in cls.EXCLUDED_PATTERNS)


class VectorSearchHelper:
    """Helper utilities for vector similarity search"""
    
    @staticmethod
    def create_search_text(file_changes):
        """
        Converts parsed changes into text suitable for vector embedding.
        
        Args:
            file_changes: List of parsed file change tuples
            
        Returns:
            str: Minified text representation for embedding
        """
        embeddings = []
        
        for filename, additions, deletions, parent_commit in file_changes:
            entry = {
                'file_name': filename,
                'added_lines': additions,
                'deleted_lines': deletions,
                'parent_jira_id': parent_commit
            }
            embeddings.append(entry)
        
        # Minify for efficient embedding
        minified = json.dumps(embeddings)
        
        # Remove noise characters
        for char in [' ', '[', ']', "'", '"', '\\t', '{', '}']:
            minified = minified.replace(char, '')
        
        return minified.replace(':', ' ')
    
    @staticmethod
    def extract_metadata(search_result):
        """
        Extracts file metadata from vector search results.
        
        Args:
            search_result: Raw text from vector database search
            
        Returns:
            Tuple of (file_names, added_files, deleted_files, jira_ids)
        """
        file_names = []
        added_files = []
        deleted_files = []
        diff_file_names = []
        
        segments = search_result.split(',')
        
        is_adding = False
        is_deleting = False
        
        for segment in segments:
            if segment.startswith('file_name'):
                is_adding = False
                is_deleting = False
                file_names.append(segment.split('file_name ')[-1])
                
            elif segment.startswith('added_lines') and not is_adding:
                is_adding = True
                is_deleting = False
                added_files.append(segment.split('++')[-1])
                
            elif segment.startswith('deleted_lines') and not is_deleting:
                is_adding = False
                is_deleting = True
                deleted_files.append(segment.split('--')[-1])
                
            elif segment.startswith('diff_name'):
                diff_file_names.append(segment.split('diff_name ')[-1])
                break
                
            elif is_adding:
                added_files.append(segment)
            elif is_deleting:
                deleted_files.append(segment)
        
        # Resolve Jira IDs from diff files
        jira_ids = []
        if diff_file_names:
            pr_data = PullRequestDataHelper.load_data()
            for diff_file in diff_file_names:
                ids = PullRequestDataHelper.find_jira_ids(pr_data, diff_file)
                if ids:
                    jira_ids.extend(ids)
        
        return file_names, added_files, deleted_files, jira_ids
