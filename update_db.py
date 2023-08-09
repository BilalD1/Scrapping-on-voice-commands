from db import DBhelper
from cluster import Cluster
from scrappers import Scrapers
import os

import os

def copy_file(source_file, destination_file):
    with open(source_file, "r") as f:
        data = f.read()

    with open(destination_file, "w") as f:
        f.write(data)


os.remove("sentences.txt")
os.rename("sentences2.txt","sentences.txt")
copy_file("sentences.txt", "sentences2.txt")

clus = Cluster()
db_helper = DBhelper()
scrap = Scrapers()
clus.clustering()

links_to_scrap = clus.scrap_clusters()
length = clus.num_clusters
for i in range(length):
    links_scrapped = scrap.run_scraper(links_to_scrap[i])
    print("total links scrapped: ",len(links_scrapped))
    db_helper.delete_table(i)
    print("table " + str(i) +": deleted")
    db_helper.create_table(links_scrapped, i)
    print("Table created " + str(i))

del scrap
del db_helper
del clus