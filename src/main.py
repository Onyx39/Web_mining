"""
TODO doctring
"""

import warnings

# import matplotlib.pyplot as plt
from pyvis.network import Network
import networkx as nx
import requests
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

# ATTENTION 3 MINIMUM
TAILLE_URL = 4

STOP_URL = ("https://www.linkedin.com/")


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
            # print(href.split("/"))
            href_list = href.split("/")
            if len(href_list) >= TAILLE_URL :
                new_href = ""
                for i in range(TAILLE_URL) :
                    new_href += href_list[i] + "/"
            else :
                new_href = href

            # if not new_href.startswith("https://www.linkedin.com/") :
            links.append(new_href)
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

def visualize_graph(graph, start_url):
    """
    TODO doctring
    """

    net = Network(height="750px", width="100%", notebook=True)

   # Ajouter les nœuds avec des couleurs personnalisées
    for node in graph.nodes():
        # Vérifier si c'est le nœud de départ (initial) pour le colorer en rouge
        if node == start_url:
            net.add_node(node, label=node, color='red')
        # Vérifier si un nœud a plus de 5 voisins pour le colorer en vert
        elif len(list(graph.neighbors(node))) > 5:
            net.add_node(node, label=node, color='green')
        else:
            net.add_node(node, label=node)

    # Ajouter les arêtes du graphe
    for edge in graph.edges():
        net.add_edge(edge[0], edge[1])

    # Générer et afficher l'interactivité
    net.show("graph.html")

    # Imprimer les nœuds triés par nombre de voisins dans l'ordre décroissant
    sorted_nodes = sorted(graph.nodes(), key=lambda node: len(list(graph.neighbors(node))), reverse=True)
    print("\nNœuds triés par nombre de voisins (ordre décroissant) :")
    for node in sorted_nodes:
        num_neighbors = len(list(graph.neighbors(node)))
        print(f"{node} : {num_neighbors} voisins")

if __name__ == "__main__":
    user_url = input("Entrez l'URL du site web : ")
    user_depth = int(input("Entrez la profondeur maximale de la cartographie : "))
    web_graph = build_graph(user_url, user_depth)
    visualize_graph(web_graph, user_url)
