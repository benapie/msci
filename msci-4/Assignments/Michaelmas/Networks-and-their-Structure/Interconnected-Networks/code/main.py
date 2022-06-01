from itertools import permutations
from random import shuffle


def int_to_binary_string(i: int, d: int) -> str:
    """
    Converts an integer to a binary string.
    :param i: integer to convert.
    :param d: number of binary digits to use.
    :return: binary string representing the integer i.
    """
    if i >= 2 ** d:
        raise ValueError(f"{d} binary digits is not enough to represent {i}!")
    return bin(i)[2:][::-1].ljust(d, '0')


def flip_ith_digit(x: str, i: int):
    """
    Takes a binary string and flips the ith bit (starting from 0).
    :param x: the binary string.
    :param i: the bit to flip.
    :return: the binary string with the ith bit flipped.
    """
    if i >= len(x) or i < 0:
        raise ValueError(f"i out of bounds: 0 <= {i} < {len(x)}")
    y = x[0:i]
    if x[i] == '0':
        y += '1'
    else:
        y += '0'
    y += x[i + 1:]
    return y


def build_adjacency_dict(n: int,
                         faulty_nodes: list[str],
                         faulty_channels: list[tuple[str, str]]) -> dict[str, list[str]]:
    """
    Builds an adjacency list of a hypercube with specified missing nodes and channels.
    :param n: dimension of the hypercube (Q_n).
    :param faulty_nodes: the missing nodes.
    :param faulty_channels: the missing channels.
    :return: an adjacency list.
    """

    def get_neighbours(x: str) -> list[str]:
        """
        Returns the neighbours of an element of a hypercube (given in scope).
        :param x: the element of the hypercube.
        :return: the neighbours of x.
        """
        if x in faulty_nodes:
            raise ValueError(f'Node {n} does not exist (faulty node).')
        neighbour_list = []
        for i in range(len(x)):
            neighbour = flip_ith_digit(x, i)
            if neighbour in faulty_nodes:
                continue
            if (x, neighbour) in faulty_channels:
                continue
            neighbour_list.append(neighbour)
        return neighbour_list

    adjacency_dict = {}
    for i in range(2 ** n):
        node_label = int_to_binary_string(i, n)
        if node_label in faulty_nodes:
            continue
        adjacency_dict[node_label] = get_neighbours(node_label)
    return adjacency_dict


def bfs(adjacency_list, source, destination):
    """
    Simple BFS algorithm.
    :param adjacency_list: adjacency list of a graph.
    :param source: a source node.
    :param destination: a destination node.
    :return: the path from the source node to the destination node.
    """
    visited = []
    queue = [[source]]
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in visited:
            neighbours = adjacency_list[node]
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                if neighbour == destination:
                    return new_path
            visited.append(node)
    return []


def attempt_minimal_path(n: int, source: str, destination: str, faulty_nodes: list[str],
                         faulty_channels: list[tuple[str, str]]) -> list[str]:
    """
    Iterates through all paths as if the hypercube had no faulty channels or nodes and see if any are valid in the
    faulty hypercube. It is stochastic but will always terminate and is correct.
    :param n: the dimension of the hypercube.
    :param source: the source node.
    :param destination: the destination node.
    :param faulty_nodes: the faulty nodes.
    :param faulty_channels: the faulty channels.
    :return: [source] if no 'minimal' path found, a minimal path otherwise.
    """
    # first generate dimensions in which they differ
    differing_dimensions = []
    for i, (a, b) in enumerate(zip(source, destination)):
        if a != b:
            differing_dimensions.append(i)
    for permutation in permutations(differing_dimensions):
        path = [source]
        witness = True
        for dim in permutation:
            next_node = flip_ith_digit(path[len(path) - 1], dim)
            if next_node in faulty_nodes:
                witness = False
                break
            if (path[len(path) - 1], next_node) in faulty_channels:
                witness = False
                break
            path.append(flip_ith_digit(path[len(path) - 1], dim))
        if witness:
            return path
        else:
            # do again but randomise the permutation, significantly cuts down average time to find..
            perm_rand = list(permutation)
            shuffle(perm_rand)
            rand_path = [source]
            witness_rand = True
            for dim_rand in perm_rand:
                next_node = flip_ith_digit(rand_path[len(rand_path) - 1], dim_rand)
                if next_node in faulty_nodes:
                    witness_rand = False
                    break
                if (rand_path[len(rand_path) - 1], next_node) in faulty_channels:
                    witness_rand = False
                    break
                rand_path.append(flip_ith_digit(rand_path[len(rand_path) - 1], dim_rand))
            if witness_rand:
                return rand_path
    return [source]


def route_to_route_list(route):
    return [[int(digit) for digit in node] for node in route]


def faulty_hypercube_routing(n: int,
                             source: list[object],
                             destination: list[object],
                             faulty_nodes: list[list[object]],
                             faulty_channels: list[tuple[list[object], list[object]]]) -> list[list[int]]:
    # convert input to strings
    source = ''.join(str(elem) for elem in source)
    destination = ''.join(str(elem) for elem in destination)
    faulty_nodes = [''.join(str(elem) for elem in faulty_node) for faulty_node in faulty_nodes]
    faulty_channels = [
        (''.join(str(elem) for elem in faulty_channel[0]), ''.join(str(elem) for elem in faulty_channel[1])) for
        faulty_channel in faulty_channels]
    # trivial case
    if source == destination:
        return route_to_route_list([source])

    attempted_minimal_path = attempt_minimal_path(n, source, destination, faulty_nodes, faulty_channels)
    if len(attempted_minimal_path) > 0:
        return route_to_route_list(attempted_minimal_path)
    # If we are here, no 'minimal' path is possible.. so now we BFS...
    adjacency_dict = build_adjacency_dict(n, faulty_nodes, faulty_channels)
    route = bfs(adjacency_dict, source, destination)
    return route_to_route_list(route)


def bubblesort_routing(n: int, source: list[object], destination: list[object]) -> list[list[int]]:
    source = [str(elem) for elem in source]
    destination = [str(elem) for elem in destination]
    if source == destination:
        return route_to_route_list([source])

    def compare(x: str, y: str):
        return destination.index(x) < destination.index(y)

    working_node = source.copy()
    path = [source]
    for i in range(n - 1):
        for j in range(n - i - 1):
            if compare(working_node[j + 1], working_node[j]):
                working_node[j], working_node[j + 1] = working_node[j + 1], working_node[j]
                path.append(working_node.copy())
                if working_node == destination:
                    return route_to_route_list(path)
