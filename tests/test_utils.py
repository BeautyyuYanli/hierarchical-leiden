import networkx as nx
import pytest

from ..leiden import leiden
from ..louvain import louvain
from ..utils import Partition, freeze, recursive_size, flat, flatₚ, argmax, aggregate_graph, singleton_partition


def test_partition_creation():
    E = nx.generators.empty_graph(0)
    G = nx.generators.classic.complete_graph(5)
    H = nx.generators.barbell_graph(5, 2)

    # Check that we can create valid partitions for the graphs above
    assert Partition(E, [{}]) is not None
    assert Partition(G, [{0, 1, 2, 3, 4}]) is not None
    assert Partition(G, [{0}, {1}, {2}, {3}, {4}]) is not None
    assert Partition(H, [{0, 1, 2, 3, 4}, {5, 6}, {7, 8, 9, 10, 11}]) is not None

    # Now check that partition creation fails when given sets which don't form a partition of the graph's nodes:
    # Partition contains nodes not in the graph:
    with pytest.raises(AssertionError):
        Partition(E, [{0}])
    # Not all graph nodes are present:
    with pytest.raises(AssertionError):
        Partition(G, [{0, 1, 3, 4}])  # Missing 2
    # There is a non-empty intersection of two sets in the partition
    with pytest.raises(AssertionError):
        Partition(G, [{0, 1, 2}, {2, 3, 4}])


def test_partition_moving():
    G = nx.generators.classic.complete_graph(5)
    P = [{0, 1, 2, 3}, {4}]

    𝓟 = Partition(G, P)              # Start with the partition indicated in P and do each of the following:
    𝓠 = 𝓟.move_node(0, {})           # a) Move node 0 to its own community (i.e. nothing should change)
    𝓡 = 𝓟.move_node(0, {4})          # b) Move node 0 to the community which contains node 4
    𝓢 = 𝓟.move_node(4, {0, 1, 2, 3}) # c) Move node 0 to the community containing all other nodes

    # Now, verify that both the communities and the membership of node 4 are correct:
    assert 𝓟.node_community(4) == {4}
    assert 𝓟.as_set() == freeze([{0, 1, 2, 3}, {4}])

    assert 𝓠.node_community(4) == {4}
    assert 𝓠.as_set() == freeze([{1, 2, 3}, {4}, {0}])

    assert 𝓡.node_community(4) == {0, 4}
    assert 𝓡.as_set() == freeze([{1, 2, 3}, {0, 4}])

    assert 𝓢.node_community(4) == {0, 1, 2, 3, 4}
    assert 𝓢.as_set() == freeze([{0, 1, 2, 3, 4}])


def test_freeze():
    assert freeze([]) == set()
    assert freeze([set()]) == { frozenset(set()) }
    assert freeze([{1, 2, 3}, {4, 5}, set()]) == { frozenset({1, 2, 3}), frozenset({4, 5}), frozenset() }
    assert freeze([set(), set()]) == { frozenset(set()) }


def test_recursive_size():
    assert recursive_size([]) == 0

    assert recursive_size(42) == 1
    assert recursive_size([42]) == 1

    assert recursive_size([0, [1]]) == 2
    assert recursive_size([[[[0, [1]]]]]) == 2

    assert recursive_size([[], 1, [2], [[3]]]) == 3
    assert recursive_size([1, 2, 3]) == 3


def test_flat():
    # Note that '{}' is not an empty set, but an empty dict!
    assert flat(set()) == set()  # test the input {}
    assert flat({ 0, 1, 2, 3 }) == {0, 1, 2, 3}  # test the input {0, 1, 2, 3}

    assert flat({ frozenset( set() ) }) == set()  # test the input { set() }
    assert flat({ frozenset( frozenset( set() ) ) }) == set()  # test the input { { { } } }
    assert flat({ 0, frozenset( {1} ), frozenset( {2, frozenset({3}) } ) }) == {0, 1, 2, 3}  # test the input { 0, {1}, {2, {3}} }


def test_flat_partition():
    raise NotImplementedError()


def test_argmax():
    raise NotImplementedError()


def test_aggregate_graph():
    G = nx.generators.classic.complete_graph(5)
    communities = [{0}, {1, 2}, {3, 4}]
    𝓟 = Partition(G, communities)

    H = aggregate_graph(G, 𝓟)

    # Short sanity check: We have three nodes, representing the three communities
    # and as many edges as before (recall that the aggregate graph H is a multigraph!)
    assert len(H.nodes()) == 3
    assert len(H.edges()) == 10

    # Verify that the nodes of the aggregate graph correspond to the communities
    assert set(H.nodes()) == freeze(communities)
    # Check that the inter-community-edges are correct
    assert H.number_of_edges(frozenset({0}),    frozenset({1, 2})) == 2
    assert H.number_of_edges(frozenset({0}),    frozenset({3, 4})) == 2
    assert H.number_of_edges(frozenset({1, 2}), frozenset({3, 4})) == 4
    # Also check that self-loops for the communities are correct
    assert H.number_of_edges(frozenset({1, 2}), frozenset({1, 2})) == 1
    assert H.number_of_edges(frozenset({3, 4}), frozenset({3, 4})) == 1


def test_singleton_partition():
    E = nx.generators.empty_graph(0)
    G = nx.generators.classic.complete_graph(5)
    H = nx.generators.barbell_graph(5, 2)

    𝓟 = singleton_partition(E)
    𝓠 = singleton_partition(G)
    𝓡 = singleton_partition(H)

    assert 𝓟.as_set() == freeze([])
    assert 𝓠.as_set() == freeze([{0}, {1}, {2}, {3}, {4}])
    assert 𝓡.as_set() == freeze([ {i} for i in range(12) ])