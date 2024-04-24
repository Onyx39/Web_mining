"""
TODO doctring
"""

import warnings

import matplotlib.pyplot as plt
import networkx as nx
import requests
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

def get_links(url):
    """
    TODO doctring
    """

    # print(url, '\n')
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    return links

def build_graph(start_url, max_depth=2):
    """
    TODO doctring
    """

    graph = nx.Graph()
    visited = set()

    def explore(url, depth):
        if depth > max_depth or url in visited:
            return
        visited.add(url)
        links = get_links(url)
        for link in links:
            graph.add_edge(url, link)
            explore(link, depth + 1)

    explore(start_url, 0)
    return graph

def visualize_graph(graph):
    """
    TODO doctring
    """

    pos = nx.spring_layout(graph)
    color_map = ['red'] + ['blue']*(len(pos) -1)
    nx.draw(graph, pos, with_labels=False, node_size=30, node_color=color_map)
    plt.show()

if __name__ == "__main__":
    user_url = input("Entrez l'URL du site web : ")
    user_depth = int(input("Entrez la profondeur maximale de la cartographie : "))
    web_graph = build_graph(user_url, user_depth)
    visualize_graph(web_graph)
