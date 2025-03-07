"""
Functions for calculating network statistics
"""

import networkx as nx
from typing import Dict, Tuple, Any

def calculate_node_sizes(G: nx.Graph) -> Dict[str, float]:
    """Calculate node sizes based on connections and weights"""
    sizes = {}
    for node in G.nodes():
        edges = G.edges(node, data=True)
        degree = len(edges)
        weight_sum = sum(data['weight'] for _, _, data in edges)
        sizes[node] = (degree * weight_sum) ** 0.5
    return sizes

def get_character_stats(G: nx.Graph, character: str) -> Dict[str, Any]:
    """Calculate statistics for a character"""
    edges = G.edges(character, data=True)
    stats = {
        'Connections': len(edges),
        'Total Mentions': sum(data['weight'] for _, _, data in edges),
        'Strongest Connection': max(
            ((u, v, data['weight']) for u, v, data in edges),
            key=lambda x: x[2],
            default=('None', 'None', 0)
        ),
        'Centrality': nx.degree_centrality(G)[character]
    }
    return stats 