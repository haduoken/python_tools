import yaml
import math
from numpy.linalg import norm
import numpy as np
from numpy import arccos, array, dot, pi, cross

from collections import deque, namedtuple

# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def distance_numpy(A, B, P):
    """ segment line AB, point P, where each one is an array([x, y]) """
    if all(A == P) or all(B == P):
        return 0
    if arccos(dot((P - A) / norm(P - A), (B - A) / norm(B - A))) > pi / 2:
        return norm(P - A)
    if arccos(dot((P - B) / norm(P - B), (A - B) / norm(A - B))) > pi / 2:
        return norm(P - B)
    return norm(cross(A - B, A - P)) / norm(B - A)


def make_edge(start, end, cost):
    return Edge(start, end, cost)


class Graph:
    def __init__(self, edges=None):
        if edges is None:
            self.edges = []
            return
            # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))
        
        self.edges = [make_edge(*edge) for edge in edges]
    
    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )
    
    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs
    
    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)
    
    def add_edge(self, n1, n2, cost, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))
        
        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))
    
    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))
        
        return neighbours
    
    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()
        
        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex
        
        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path


graph = Graph([
    ("a", "b", 7), ("a", "c", 9), ("a", "f", 14), ("b", "c", 10),
    ("b", "d", 15), ("c", "d", 11), ("c", "f", 2), ("d", "e", 6),
    ("e", "f", 9)])

print(graph.dijkstra("a", "e"))


def calculate_dis(a, b):
    return math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2)


class Navigation:
    def __init__(self, file):
        self.graph = Graph()
        self.nodes = []
        self.edges = []
        with open(file, 'r') as f:
            map_yaml = yaml.load(f)
            node_cnt = 0
            cnt = 0
            for lane in map_yaml['Lanes']:
                
                point_from = lane['points'][0]['point']
                for n in self.nodes:
                    if calculate_dis(n, point_from) < 0.5:
                        point_from.append(n[2])
                        break
                if len(point_from) == 2:
                    point_from.append(str(cnt))
                    self.nodes.append(point_from)
                cnt += 1
                
                point_to = lane['points'][1]['point']
                for n in self.nodes:
                    if calculate_dis(n, point_to) < 0.5:
                        point_to.append(n[2])
                        break
                if len(point_to) == 2:
                    point_to.append(str(cnt))
                    self.nodes.append(point_to)
                cnt += 1
                dis = calculate_dis(point_from, point_to)
                if lane['direction_attr'] == 'BiDirection':
                    self.graph.add_edge(point_from[2], point_to[2], dis, both_ends=True)
                elif lane['direction_attr'] == 'Forward':
                    self.graph.add_edge(point_from[2], point_to[2], dis, both_ends=False)
                elif lane['direction_attr'] == 'Backward':
                    self.graph.add_edge(point_to[2], point_from[2], dis, both_ends=False)
    
    def serach(self, pose_from, pose_to):
        shortest_to_map = 99999
        for edge in self.edges:
            length = distance_numpy(edge[0], edge[1], pose_from)
            shortest_to_map = length if length < shortest_to_map else shortest_to_map
        if shortest_to_map > 1:
            return False, None
        
        shortest_to_map = 99999
        for edge in self.edges:
            length = distance_numpy(edge[0], edge[1], pose_to)
            shortest_to_map = length if length < shortest_to_map else shortest_to_map
        if shortest_to_map > 1:
            return False, None
        
        shortest_to_node = 9999
        node_name_from = 'None'
        for n in self.nodes:
            dis = calculate_dis(n, pose_from)
            if shortest_to_node > dis:
                node_name_from = n[2]
                shortest_to_node = dis
        
        self.graph.add_edge(node_name_from, 'from', shortest_to_node, False)
        
        shortest_to_node = 9999
        node_name_to = 'None'
        for n in self.nodes:
            dis = calculate_dis(n, pose_to)
            if shortest_to_node > dis:
                node_name_to = n[2]
                shortest_to_node = dis
        
        self.graph.add_edge(node_name_to, 'to', shortest_to_node, False)
        
        print(self.graph.dijkstra('from', 'to'))
