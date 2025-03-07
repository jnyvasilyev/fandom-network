"""
NetworkVisualizer class for creating interactive network visualizations
"""

import plotly.graph_objects as go
import networkx as nx
import numpy as np
from typing import Dict, List, Tuple
from ..network.stats import calculate_node_sizes, get_character_stats

class NetworkVisualizer:
    def __init__(self, G: nx.Graph, image_urls: Dict[str, str]):
        self.G = G
        self.image_urls = image_urls
        
    def create_visualization(self):
        """Create an interactive network visualization"""
        pos = nx.spring_layout(self.G, k=1/np.sqrt(len(self.G.nodes())), iterations=50)
        node_sizes = calculate_node_sizes(self.G)
        
        # Create edge traces
        edge_trace = self._create_edge_trace(pos)
        
        # Create node traces
        node_trace = self._create_node_trace(pos, node_sizes)
        
        # Create figure
        fig = self._create_figure(edge_trace, node_trace)
        
        # Add images
        self._add_images(fig, pos)
        
        return fig
    
    def _create_edge_trace(self, pos: Dict) -> go.Scatter:
        """Create the edge trace for the visualization"""
        edge_x, edge_y = [], []
        edge_weights = []
        
        for edge in self.G.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_weights.append(edge[2]['weight'])
            
        return go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(
                width=np.array(edge_weights) / max(edge_weights) * 5,
                color='#888'
            ),
            hoverinfo='none',
            mode='lines'
        )
    
    def _create_node_trace(self, pos: Dict, node_sizes: Dict) -> go.Scatter:
        """Create the node trace for the visualization"""
        node_x, node_y = [], []
        node_text = []
        
        for node in self.G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            # Get character stats
            stats = get_character_stats(self.G, node)
            
            # Prepare hover text
            hover_text = f"""
            <b>{node}</b><br>
            Connections: {stats['Connections']}<br>
            Total Mentions: {stats['Total Mentions']}<br>
            Strongest Connection: {stats['Strongest Connection'][1]} ({stats['Strongest Connection'][2]} mentions)<br>
            Centrality: {stats['Centrality']:.3f}
            """
            node_text.append(hover_text)
        
        return go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition='top center',
            marker=dict(
                size=[node_sizes[node] * 10 for node in self.G.nodes()],
                color='lightblue',
                line_width=2,
                line_color='black'
            )
        )
    
    def _create_figure(self, edge_trace: go.Scatter, node_trace: go.Scatter) -> go.Figure:
        """Create the figure with layout settings"""
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title='Character Network (Hover for details)',
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[
                    dict(
                        text="Character Network",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002
                    )
                ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='white'
            )
        )
        
        # Add hover label styling
        fig.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Arial"
            )
        )
        
        return fig
    
    def _add_images(self, fig: go.Figure, pos: Dict):
        """Add character images to the visualization"""
        for node, (x, y) in pos.items():
            if node in self.image_urls and self.image_urls[node]:
                fig.add_layout_image(
                    dict(
                        source=self.image_urls[node],
                        xref="x",
                        yref="y",
                        x=x,
                        y=y,
                        sizex=0.1,
                        sizey=0.1,
                        sizing="contain",
                        opacity=1,
                        layer="above"
                    )
                ) 