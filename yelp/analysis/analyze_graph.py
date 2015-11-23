__author__ = 'yan.cui'

# network components distribution

# friends of friends, number of non-unique friends, and number of unique friends

# average degree of neighbors against degrees

# percentage against neighbor's degree

# which one is more effective? tip or review?

# how location affect users on yelp, we have location of business, how many uses cross

from import_json_to_neo4j import yelp_graph

def persons_versus_users():
    # match(n:User) return count(n)
    # match(n:Person) return count(n)

    # the number of users and number of person are the same(366715)
    # which means no users only bring by
    # other people, but no detailed information.
    # This shows they polish the data themselves
    # total number of users cannot be just 360000, for sure
    pass

def friends_on_average():
    # match(n:User)-[r:knows]->() return count(r)
    # all knows relationship count: 2576179
    # note it has direction
    # on average, each user has 2576179.0 / 366715.0 = 7.025016702343782 ~= 7 friends
    pass

def friends_count_distribution():
    # match(n:User) where not (n)-[:knows]->() return count(n)
    # 0 friends 192621
    # distribution
    # match(n:User)-[r:knows]->() with n.user_id as uid, count(r) as relations order by relations desc
    # with relations as relations, count(relations) as cnt return relations, cnt order by relations

    # verify
    # match(n:User)-[r:knows]->() with n.user_id as uid, count(r) as relations order by relations desc
    # with relations as relations, count(relations) as cnt return sum(cnt)
    # 174094 + 192621 = 366715

    # kind of standard power law
    pass

def stars_distribution():
    # match(n:User) where n.average_stars <= 1 return count(n)  20460
    # match(n:User) where n.average_stars > 1 and n.average_stars <= 2 12853
    # match(n:User) where n.average_stars > 2 and n.average_stars <= 3 42972
    # match(n:User) where n.average_stars > 3 and n.average_stars <= 4 150634
    # match(n:User) where n.average_stars > 4 and n.average_stars <= 5 139796

    # users with high stars dominate
    pass

def component_numbers():
    # Users with no friends 192621
    # match (n:User) where (n)-[:knows]-()
    # with collect(n) as nodes
    # with reduce(graphs = [], n in nodes |
     #  case when
     #  ANY (g in graphs where shortestPath( (n)-[*]-(g) ) )
     #  then graphs
     #  else graphs + [n]
     #  end ) as result unwind result as ret return count(ret)  2434 components
    pass

def component_distribution():

    pass

def get_random_nodeid():
    return yelp_graph.cypher.execute("MATCH(m:User) with m as node, rand() as r return node.user_id as nid order by r limit 1")

def get_distance(uid1, uid2):
    return yelp_graph.cypher.execute("MATCH (m:User),(n:User) where m.user_id={nodeid1} and n.user_id={nodeid2} " +
                              "with shortestPath((m)-[*]-(n)) as path return length(path) as len",
                            {"nodeid1" : uid1, "nodeid2" : uid2})
def hop_distance_distribution():
    # create random node
    # match(m:User) with m as node, rand() as r return id(node) order by r limit 1
    # shortest path between two nodes
    # match(m:Test),(n:Test) where id(m)=39609 and id(n)=39608
    # with shortestPath((m)-[*]-(n)) as path return length(path)
    experiment, inf, MAX_ITERARIONS = 0, 32767, 10000
    dist = {}
    for index in range(MAX_ITERARIONS):
        id1, id2 = get_random_nodeid(), get_random_nodeid()
        assert len(id1) == 1 and len(id2) == 1
        dis = get_distance(id1[0].nid, id2[0].nid)
        leng = dis[0].len
        if leng == None:
            leng = inf
        try:
            dist[leng] = dist[leng] + 1
        except:
            dist[leng] = 1

        experiment = experiment + 1
        if experiment % 10 == 0:
            print experiment

    with open("hop_distribution.csv", "w") as file:
        sum = 0
        for key in sorted(dist.keys()):
            sum += dist[key]
            file.write(str(key) + "," + str(float(sum)/float(MAX_ITERARIONS)) + "\n")
        file.close()


def fans_distribution():
    # match (n:User) where n.fans = 0 return count(n) 271709
    # match (n:User) where n.fans > 0 and n.fans <= 100 return count(n)  94518
    # match (n:User) where n.fans > 100 and n.fans <= 200 return count(n) 332
    # match (n:User) where n.fans > 200 and n.fans <= 300 return count(n) 71
    # match (n:User) where n.fans > 300 and n.fans <= 400 return count(n) 25
    #                              > 400 and <=500                        18
    #                              > 500 and <=600                        10
    #                              > 600 and <=700                         7
    #                              > 700 and <= 800                        8
    #                              > 800 and <= 900                        1
    #                              > 900 and <= 1000                       2
    #                              > 1000                                  7
    pass

def elite_distribution():
    # match(n:User) where n.elite=[] return count(n)  341414
    # most are not elite users
    # match(n:User) where n.elite<>[] return avg(n.fans) = 16.3822773803407 ~= 16
    # match(n:User) where n.elite<>[] return avg(n.review_count) = 245.09220979407928 ~= 245
    # match(n:User) where n.elite<>[] return avg(n.avg_stars) = 3.7801367534879953
    # match(n:User) where n.elite<>[] return avg(toInt(n.votes[1]) + toInt(n.votes[3]) + toInt(n.votes[5])) = 1336.1507845539702
    # match(n:User) where n.elite<>[] return count(n) 25301
    # match(n:User) where n.elite<>[] and n.compliments<>[] return count(n) 25244
    # match(n:User) where n.elite<>[] and n.yelping_since =~ "2004-.*" return count(n)  22
    # 2004 22    / 51       =   0.43137254901960786
    # 2005 357   / 691      =   0.516642547033285
    # 2006 1525  / 3974     =   0.3837443381982889
    # 2007 3120  / 10676    =   0.29224428624953164
    # 2008 4198  / 19390    =   0.21650335224342446
    # 2009 4631  / 32968    =   0.140469546226644
    # 2010 4649  / 50722    =   0.09165648042269627
    # 2011 3571  / 69210    =   0.05159659008813755
    # 2012 1926  / 63897    =   0.03014226020000939
    # 2013 977   / 63483    =   0.015389946914922105
    # 2014 325   / 50505    =   0.006435006435006435
    # 2015 0     / 1148
    # elite is effective
    pass

def review_count_distribution():
    # match(n:User) where n.review_count=0 return count(n) 7
    # match(n:User) where n.review_count > 0 and review_count <= 100 return count(n) 338773
    # match(n:User) where n.review_count > 100 and review_count <= 200 return count(n) 15094
    # match(n:User) where n.review_count > 200 and review_count <= 300 return count(n) 5846
    # match(n:User) where n.review_count > 300 and review_count <= 400 return count(n) 2818
    # match(n:User) where n.review_count > 400 and review_count <= 500 return count(n) 1563
    # match(n:User) where n.review_count > 500 return count(n) 2614
    pass

def votes_distribution():
    # match(n:User) where toInt(n.votes[1]) + toInt(n.votes[3]) + toInt(n.votes[5]) = 0 return count(n) 56420
    # match(n:User) return  max(toInt(n.votes[1]) + toInt(n.votes[3]) + toInt(n.votes[5])) 100319
    # match(n:User) where toInt(n.votes[1]) + toInt(n.votes[3]) + toInt(n.votes[5]) > 0 and toInt(n.votes[1]) +
    # toInt(n.votes[3]) + toInt(n.votes[5]) <= 1000 return count(n) 302842
    # > 1000 and <=2000 3842
    # > 2000 and <= 3000 1350
    # > 3000 and <= 4000 665
    # > 4000 and <= 5000  410
    # > 5000 1186
    pass

def compliments_distribution():
    # match(n:User) where n.compliments=[] return count(n)  223476  most users will not write compliments
    # match(n:User) where n.votes[1]="0" and n.votes[3] = "0" and n.votes[5] = "0" return count(n) 56420 which
    # is much smaller than the number of users do not write compliments, indicates most people just want to
    # write a simple votes instead of compliments(compliments show more details of the comments)
    pass

def user_increase_ratio():
    # analyze the yelp-since field
    # match(n:User) where n.yelping_since =~ '2004-.*' return count(n) 51
    # match(n:User) where n.yelping_since =~ '2005-.*' return count(n) 691
    # "2006" 3974
    # "2007" 10676
    # "2008" 19390
    # "2009" 32968
    # "2010" 50722
    # "2011" 69210
    # "2012" 63897
    # "2013" 63483
    # "2014" 50505
    # "2015" 1148
    pass

if __name__ == "__main__":
    hop_distance_distribution()

