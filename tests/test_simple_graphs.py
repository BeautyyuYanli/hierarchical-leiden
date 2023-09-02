"""Test the Louvain and Leiden algorithms on simple graphs."""

import networkx as nx

from community_detection.leiden import leiden
from community_detection.louvain import louvain
from community_detection.quality_metrics import CPM, Modularity, QualityMetric
from community_detection.utils import freeze

# Below are a few tests written for simple graphs (currently only ones for the (5,2) barbell graph),
# which are small enough for the results to be deterministic and traceable by a human.

BARBELL_PARTS = freeze([{0, 1, 2, 3, 4}, {5, 6}, {7, 8, 9, 10, 11}])


def test_louvain_barbell_modularity() -> None:
    """
    Test the Louvain algorithm with modularity as the quality function on a (5,2) barbell graph.

    This graph consists of two complete graphs K_5, connected by a path of length 2.
    """
    G = nx.generators.barbell_graph(5, 2)

    𝓗: QualityMetric[int]  # Type annotation for 𝓗 below
    𝓗 = Modularity(1)
    𝓠 = louvain(G, 𝓗)

    assert 𝓠.as_set() == BARBELL_PARTS


def test_leiden_barbell_modularity() -> None:
    """
    Test the Leiden algorithm with modularity as the quality function on a (5,2) barbell graph.

    This graph consists of two complete graphs K_5, connected by a path of length 2.
    """
    G = nx.generators.barbell_graph(5, 2)

    𝓗: QualityMetric[int]  # Type annotation for 𝓗 below
    𝓗 = Modularity(1.5)
    𝓠 = leiden(G, 𝓗)

    assert 𝓠.as_set() == BARBELL_PARTS


def test_louvain_barbell_cpm() -> None:
    """
    Test the Louvain algorithm with CPM as the quality function on a (5,2) barbell graph.

    This graph consists of two complete graphs K_5, connected by a path of length 2.
    """
    G = nx.generators.barbell_graph(5, 2)

    𝓗: QualityMetric[int]  # Type annotation for 𝓗 below
    # The following resolution parameter for the CPM was found using binary serach on the interval [0.95, 1.05].
    𝓗 = CPM(0.9999999999999986)
    𝓠 = louvain(G, 𝓗)

    assert 𝓠.as_set() == BARBELL_PARTS


def test_leiden_barbell_cpm() -> None:
    """
    Test the Leiden algorithm with CPM as the quality function on a (5,2) barbell graph.

    This graph consists of two complete graphs K_5, connected by a path of length 2.
    """
    G = nx.generators.barbell_graph(5, 2)

    𝓗: QualityMetric[int]  # Type annotation for 𝓗 below
    𝓗 = CPM(0.9999999999999986)
    𝓠 = leiden(G, 𝓗)

    assert 𝓠.as_set() == BARBELL_PARTS
