"""
WikiAPI class for interacting with Fandom wikis
"""

import requests
import time
from typing import Dict, Set, Optional

class WikiAPI:
    def __init__(self, wiki_domain: str):
        self.base_url = f"https://{wiki_domain}.fandom.com/api.php"
    
    def _make_request(self, params: Dict) -> Dict:
        """Make an API request with error handling"""
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return {}
    
    def get_all_characters(self) -> Set[str]:
        """Get all character pages from the wiki"""
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": "Category:Characters",
            "cmlimit": "500"
        }
        
        response = self._make_request(params)
        if response and 'query' in response:
            return {page['title'] for page in response['query']['categorymembers']}
        return set()
    
    def get_character_history(self, character: str) -> str:
        """Get the character's story content from their wiki page"""
        params = {
            "action": "parse",
            "page": character,
            "format": "json",
            "prop": "sections|text",
            "section": "0"
        }
        
        response = self._make_request(params)
        if not response or 'parse' not in response:
            return ""
        
        sections = response['parse']['sections']
        target_section = None
        
        # List of possible section names that might contain character information
        story_section_keywords = [
            'history',
            'biography',
            'plot',
            'story',
            'background',
            'life',
            'overview',
            'description',
            'character history',
            'personal history',
            'role',
            'narrative'
        ]
        
        # First pass: look for exact matches
        for section in sections:
            section_title = section['line'].lower()
            if any(keyword == section_title for keyword in story_section_keywords):
                target_section = section['index']
                break
        
        # Second pass: look for partial matches if no exact match was found
        if target_section is None:
            for section in sections:
                section_title = section['line'].lower()
                if any(keyword in section_title for keyword in story_section_keywords):
                    target_section = section['index']
                    break
        
        # If we found a relevant section, get its content
        if target_section is not None:
            params['section'] = target_section
            response = self._make_request(params)
            if response and 'parse' in response:
                return response['parse']['text']['*']
            
        # If no specific section was found, return the main content
        params['section'] = '0'
        response = self._make_request(params)
        if response and 'parse' in response:
            return response['parse']['text']['*']
        
        return ""
    
    def get_character_image(self, character: str) -> str:
        """Get character image URL from wiki"""
        params = {
            "action": "query",
            "format": "json",
            "titles": character,
            "prop": "pageimages",
            "pithumbsize": 100
        }
        
        response = self._make_request(params)
        if response and 'query' in response and 'pages' in response['query']:
            page = next(iter(response['query']['pages'].values()))
            if 'thumbnail' in page:
                return page['thumbnail']['source']
        return "" 