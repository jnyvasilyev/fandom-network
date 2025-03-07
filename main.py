"""
Main script for building and visualizing character networks from Fandom wikis
"""

from src.api.wiki_api import WikiAPI
from src.network.graph import CharacterNetwork
from src.visualization.interactive import NetworkVisualizer
from src.utils.cache import Cache
import argparse

def main():
    parser = argparse.ArgumentParser(description='Build and visualize a character network from a Fandom wiki')
    parser.add_argument('wiki_domain', help='The domain of the wiki (e.g., "harrypotter")')
    parser.add_argument('--cache-dir', default='.cache', help='Directory to store cached data')
    parser.add_argument('--clear-cache', action='store_true', help='Clear the cache before starting')
    args = parser.parse_args()
    
    # Initialize components
    cache = Cache(args.cache_dir)
    if args.clear_cache:
        cache.clear()
    
    wiki_api = WikiAPI(args.wiki_domain)
    network = CharacterNetwork(wiki_api)
    
    # Try to load network from cache
    cached_network = cache.get('network')
    if cached_network:
        print("Loading network from cache...")
        network.G = cached_network
    else:
        print("Building network...")
        network.build_network()
        cache.set('network', network.G)
    
    # Get character images
    print("Getting character images...")
    image_urls = {}
    for character in network.characters:
        cached_image = cache.get(f'image_{character}')
        if cached_image:
            image_urls[character] = cached_image
        else:
            image_url = wiki_api.get_character_image(character)
            cache.set(f'image_{character}', image_url)
            image_urls[character] = image_url
    
    # Create visualization
    print("Creating visualization...")
    visualizer = NetworkVisualizer(network.G, image_urls)
    fig = visualizer.create_visualization()
    fig.show()

if __name__ == "__main__":
    main() 