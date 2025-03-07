"""
CharacterNetwork class for building and managing character networks
"""

import networkx as nx
from collections import Counter
import re
import time
from typing import Dict, Set
from ..api.wiki_api import WikiAPI

class CharacterNetwork:
    def __init__(self, wiki_api: WikiAPI):
        self.wiki_api = wiki_api
        self.G = nx.Graph()
        self.characters = set()
    
    def count_character_mentions(self, text: str, characters: Set[str]) -> Dict[str, int]:
        """Count mentions of characters in text"""
        mentions = Counter()
        for character in characters:
            pattern = rf'\b{re.escape(character)}\b'
            mentions[character] = len(re.findall(pattern, text, re.IGNORECASE))
        return mentions
    
    def build_network(self):
        """Build the character network"""
        self.characters = self.wiki_api.get_all_characters()
        
        for character in self.characters:
            print(f"Processing {character}...")
            history = self.wiki_api.get_character_history(character)
            mentions = self.count_character_mentions(history, self.characters)
            
            for mentioned_char, count in mentions.items():
                if mentioned_char != character and count > 0:
                    if self.G.has_edge(mentioned_char, character):
                        current_weight = self.G[mentioned_char][character]['weight']
                        self.G[mentioned_char][character]['weight'] = max(current_weight, count)
                    else:
                        self.G.add_edge(character, mentioned_char, weight=count)
            
            time.sleep(1)  # Rate limiting 