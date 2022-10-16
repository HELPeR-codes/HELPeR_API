from blueprints.recsys_endpoints.recsys_config import  aconfig as config
from py2neo import NodeMatcher, RelationshipMatcher
from py2neo import Graph
import copy
def get_neo4jConnection():

    if  config.connection == None:
        print("connection was null")
        config.connection = Graph("neo4j://neo4j.ngrok.luozm.me:16002", auth=("neo4j", "helper"))
        return config.connection
    try:
        config.connection.run("Match () Return 1 Limit 1")
    except :
        print("no connection found / or was closed")
        config.connection =Graph("neo4j://neo4j.ngrok.luozm.me:16002", auth=("neo4j", "helper"))

    return config.connection


def get_neo4jNodeMatcher():
    node_matcher = None
    try:
        connection = get_neo4jConnection()
        node_matcher = NodeMatcher(connection)
    except:
        print("node macther cannot be initialized")

    return node_matcher

def get_neo4jRelationshipMatcher():
    node_matcher = None
    try:
        connection = get_neo4jConnection()
        node_matcher = RelationshipMatcher(connection)
    except:
        print("node macther cannot be initialized")

    return node_matcher
