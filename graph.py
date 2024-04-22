import numpy as np
import matplotlib.pyplot as plt
import random
import osmnx as ox
import networkx as nx
import seaborn as sns
from gapminder import gapminder # data set

def draw_graph():
    G = nx.Graph()

    G.add_node('Gippo', title="Gippo", size=90, square="4583.3439")
    G.add_node('Kosmos', title="Kosmos", size=249, square="12579.8214")
    G.add_node('Akvarel', title="Akvarel", size=3000, square="158741.6045")
    G.add_node('Voroshil', title="Voroshil", size=300, square="15964.7606")
    G.add_node('Merkuriy', title="Merkuriy", size=27, square="1381.5588")
    G.add_node('Diamant', title="Diamant", size=81, square="3955.0650")
    G.add_node('Evropa', title="Evropa", size=507, square="25346.0893")
    G.add_node('Marmelad', title="Marmelad", size=1314, square="65734.3480")
    G.add_node('Park_House', title="Park_House", size=873, square="43752.5159")
    G.add_node('Volgorost', title="Volgorost", size=396, square="19835.2063")
    G.add_node('Ros_potrb_Nadzor', title="Ros_potrb_Nadzor", size=36, square="1729.8225")
    G.add_node('Titiovskiy', title="Titiovskiy", size=75, square="3773.7117")
    G.add_node('Selgros', title="Selgros", size=579, square="29038.4559")
    G.add_node('7_zvezd', title="7_zvezd", size=921, square="46012.6466")

    node_labelss = nx.get_node_attributes(G, 'title')  # не трогать
    sizeee = nx.get_node_attributes(G, 'size')
    squareee = nx.get_node_attributes(G, 'square')

    G.add_edge('Gippo', 'Kosmos', title='12.8 км')  # связи с весом - title
    G.add_edge('Kosmos', 'Akvarel', title='3.6')
    G.add_edge('Akvarel', 'Voroshil', title='8.16 км')
    G.add_edge('Voroshil', 'Merkuriy', title='0.36 км')
    G.add_edge('Merkuriy', 'Park_House', title='5.5 км')
    G.add_edge('Merkuriy', 'Marmelad', title='4.9 км')
    G.add_edge('Merkuriy', 'Diamant', title='1.5')
    G.add_edge('Park_House', 'Marmelad', title='1.68 км')
    G.add_edge('Park_House', 'Volgorost', title='2.43 км')
    G.add_edge('Volgorost', 'Ros_potrb_Nadzor', title='5.51 км')
    G.add_edge('Marmelad', 'Evropa', title='2.5 км')
    G.add_edge('Marmelad', 'Diamant', title='4.02 км')
    G.add_edge('Diamant', 'Evropa', title='2.5')
    G.add_edge('Evropa', 'Titiovskiy', title='6.77 км')
    G.add_edge('Titiovskiy', 'Selgros', title='0.69 км')
    G.add_edge('Selgros', '7_zvezd', title='2.62 км')

    edge_labels = nx.get_edge_attributes(G, 'title')

    pos = {
        "Gippo": (44.5346199, 48.5150528),
        "Kosmos": (44.4244982, 48.6050157),
        "Akvarel": (44.4319745, 48.6378398),
        "Voroshil": (44.473278, 48.7043622),
        "Merkuriy": (44.5051911, 48.6998551),
        "Diamant": (44.521524, 48.7077245),
        "Evropa": (44.5418894, 48.7253215),
        "Marmelad": (44.5199375, 48.7429243),
        "Park_House": (44.4975537, 48.7492608),
        "Volgorost": (44.4675729, 48.7571037),
        "Ros_potrb_Nadzor": (44.4772117, 48.8061284),
        "Titiovskiy": (44.5655284, 48.78602),
        "Selgros": (44.5707329, 48.7889167),
        "7_zvezd": (44.6051752, 48.8009422),
    }

    pos_labels = {
        "Gippo": (44.5346199, 48.5150528),
        "Kosmos": (44.4244982, 48.6050157),
        "Akvarel": (44.4319745, 48.6378398),
        "Voroshil": (44.473278, 48.7043622),
        "Merkuriy": (44.5051911, 48.6998551),
        "Diamant": (44.521524, 48.7077245),
        "Evropa": (44.5418894, 48.7253215),
        "Marmelad": (44.5199375, 48.7429243),
        "Park_House": (44.4975537, 48.7492608),
        "Volgorost": (44.4675729, 48.7571037),
        "Ros_potrb_Nadzor": (44.4772117, 48.8061284),
        "Titiovskiy": (44.5655284, 48.78602),
        "Selgros": (44.5707329, 48.7889167),
        "7_zvezd": (44.6051752, 48.8009422),
    }

    pos_area = {
        "Gippo": (44.5346199, 48.5060528),
        "Kosmos": (44.4244982, 48.5960157),
        "Akvarel": (44.4319745, 48.6288398),
        "Voroshil": (44.473278, 48.6953622),
        "Merkuriy": (44.5051911, 48.6908551),
        "Diamant": (44.521524, 48.6987245),
        "Evropa": (44.5418894, 48.7163215),
        "Marmelad": (44.5199375, 48.7339243),
        "Park_House": (44.4975537, 48.7402608),
        "Volgorost": (44.4675729, 48.7481037),
        "Ros_potrb_Nadzor": (44.4772117, 48.7971284),
        "Titiovskiy": (44.5655284, 48.77702),
        "Selgros": (44.5707329, 48.7799167),
        "7_zvezd": (44.6051752, 48.7919422),
    }

    nx.draw(G, pos=pos, node_size=[v for v in sizeee.values()])  # рисует без букв просто, заготовка

    nx.draw_networkx_labels(G, pos=pos_labels, labels=node_labelss, font_weight='light')  # за название отвечает
    nx.draw_networkx_labels(G, pos=pos_area, labels=squareee, font_weight='light')  # за площадь отвечает
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)  # вес между точками (вес дуг)

    plt.margins(0.2)
    plt.show()