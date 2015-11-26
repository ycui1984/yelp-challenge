# yelp-data-challenge

SETUP

1. the raw data can be acquired at `http://www.yelp.com/dataset_challenge`, 
download and put into `./dataset/yelp` folder

2. install Neo4j database, and remove security checking
by setting `dbms.security.auth_enabled=false` in `neo4j-server.properties` under 
`/usr/local/Cellar/neo4j/2.2.5/libexec/conf`

3. restart neo4j
neo4j start

4. import dataset by executing `python import_json_to_neo4j.py`
Be patient, on my mac laptop, it takes roughly two weeks to import all user 
data, optimize importing performance by REST API and bulk commit is considered 
as future work as we focus on data analysis right now 
