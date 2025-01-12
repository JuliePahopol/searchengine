import sqlite3
import networkx as nx


# connect to the sQLITE database

conn = sqlite3.connect("crawled_pages.db")
cursor = conn.cursor()

# retrieve the urls of all the websites from the database
cursor.execute("SELECT url FROM pages")
urls = [row[0] for row in cursor.fetchall()]

# create an empty directed graph using networkx
graph = nx.DiGraph()

# add the nodes to the graph
for url in urls:
    graph.add_node(url)


# and add the edges to the graph
for url in urls:
    cursor.execute("SELECT outgoing_links FROM pages WHERE url = ?", (url,))
    outgoing_links = cursor.fetchone()[0].split(",")
    for link in outgoing_links:
        if link.startswith("http"):
            graph.add_edge(url, link)

# calculate pagerank of the graph
pagerank = nx.pagerank(graph)

# store the pagerank scores in the database
for url in urls:
    cursor.execute("UPDATE pages SET pagerank = ? WHERE url = ?", (pagerank[url], url))

# commit the changes
conn.commit()

# close the database connection
conn.close()
