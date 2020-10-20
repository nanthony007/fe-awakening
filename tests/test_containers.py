from fe_awakening import containers


def test_driver():
    username = "neo4j"
    password = "nick0709"

    graph = containers.App("bolt://localhost:7687", user=username, password=password)
    x = graph.close()
    assert x == None
