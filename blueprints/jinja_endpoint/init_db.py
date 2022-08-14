import py2neo
from py2neo import database as db
from py2neo import Graph,  NodeMatcher, cypher
from py2neo import GraphService
connection = Graph("bolt://localhost:7687", password='jaidjaid')
from neo4j import (
    GraphDatabase,
    basic_auth,
)
import os


url = os.getenv("NEO4J_URI", "neo4j+s://localhost")
username = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "jaidjaid")
neo4j_version = os.getenv("NEO4J_VERSION", "4")
database = os.getenv("NEO4J_DATABASE", "neo4j")

port = os.getenv("PORT", 6001)

driver = GraphDatabase.driver(url, auth=basic_auth(username, password))

