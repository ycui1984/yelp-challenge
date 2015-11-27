# yelp-data-challenge

SETUP

1. the raw data can be acquired at `http://www.yelp.com/dataset_challenge`, 
download and put into `./dataset/yelp` folder

2. install Neo4j database, and remove security checking
by setting `dbms.security.auth_enabled=false` in `neo4j-server.properties` under 
`/usr/local/Cellar/neo4j/2.2.5/libexec/conf`

3. setup the database 
use my neo4j database by downloading `https://www.dropbox.com/s/0i7f2fusf2fe4bk/graph.db.tar.gz?dl=0`, extracting in /usr/local/Cellar/neo4j/2.2.5/libexec/data/graph.db/
or after start neo4j, you can import dataset by executing `python import_json_to_neo4j.py`
Be patient though, on my mac laptop, it takes roughly two weeks to import all user 
data, optimize importing performance by REST API and bulk commit is considered 
as future work as we focus on data analysis.

4. start neo4j by `neo4j start`

5. run analysis script in yelp/analysis folder, or you can create your own analysis program to get new insights.
