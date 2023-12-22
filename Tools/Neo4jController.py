'''
Author: Suez_kip 287140262@qq.com
Date: 2023-12-21 14:53:47
LastEditTime: 2023-12-22 13:19:20
LastEditors: Suez_kip
Description: 
'''
from py2neo import Graph, Node, Relationship, NodeMatcher

graph = Graph(r'http://localhost:7474/', auth=("neo4j", "12345678"), name = 'neo4j')
graph.create(Node('Person', name = "suez_kip"))
graph.create(Node('Person', name = 'Alan'))
matcher = NodeMatcher(graph)

match = matcher.match('Person') # 查询结点
for node in match:
    print(node)
print(list(match))