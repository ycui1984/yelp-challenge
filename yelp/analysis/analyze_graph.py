__author__ = 'yan.cui'

# which one is more effective? tip or review?

# how location affect users on yelp, we have location of business, how many uses cross

from import_json_to_neo4j import yelp_graph
import networkx as nx

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


def get_all_user_nodes_with_friends():
    return yelp_graph.cypher.execute("MATCH(n:User) where (n)-[:knows]->() return id(n) as nid")

def exist_path(nid1, nid2):
    res = yelp_graph.cypher.execute("MATCH(n:User),(m:User) where id(n)={nid1} and id(m)={nid2} " +
                                    "return shortestPath((n)-[*]-(m)) as path", {"nid1": nid1, "nid2":nid2})
    return True if len(res) > 0 and res[0].path != None else False

def component_distribution():
    res = get_all_user_nodes_with_friends()
    assert(len(res)) != 0
    graphs, cnt = [], []
    progress = 0
    for node in res:
        found = False
        for indexg in range(len(graphs)):
            if exist_path(node.nid, graphs[indexg]):
                cnt[indexg] += 1
                found = True
                break
        if found == False:
            graphs.append(node.nid)
            cnt.append(1)
        progress += 1
        try:
            if progress % int(float(len(res)) * 0.01) == 0:
                print str(progress)+"\n"
        except:
            print str(progress)+"\n"

    print "number of components:", len(cnt)
    component_table = {}
    for elem in sorted(cnt):
        try:
            component_table[elem] += 1
        except:
            component_table[elem] = 1
    with open("component_distribution.csv", "w") as file:
        for key in sorted(component_table.keys()):
            file.write(str(key)+","+str(component_table[key])+"\n")


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

    # cal the expected avg distance
    # 0.0001 + (0.0016-0.0001)*2 + (0.033-0.0016)*3 + (0.1176 - 0.033)*4 + (0.1799 - 0.1176)*5 + (0.2036-0.1799)*6 + (0.2093-0.2036)*7 + (0.2101-0.2093)*8
    # / 0.2101 = 4.453593526891956 ~= 4.5
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
    # match(n:User) return sum(toInt(n.votes[1]))   10949028    funny
    # match(n:User) return sum(toInt(n.votes[3]))   21628724    useful
    # match(n:User) return sum(toInt(n.votes[5]))   12241310    cool
    # which may indicate the yelp graph is effective as useful votes dominate
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

def get_nodes_with_degree(k):
    return yelp_graph.cypher.execute("MATCH(n:User)-[r:knows]->() with n as node, count(r) as relations " +
                                     "where relations={r} return id(node) as nid", {"r" : k})
    #return yelp_graph.cypher.execute("MATCH(n:Test)-[r:testknow]->() with n as node, count(r) as relations " +
    #                                 "where relations={r} return id(node) as nid", {"r" : k})

def get_all_friends(n):
    return yelp_graph.cypher.execute("MATCH(n:User)-[r:knows]->(m:User) where id(n)={uid} return id(m) as nid",
                                     {"uid" : n.nid})
    #return yelp_graph.cypher.execute("MATCH(n:Test)-[r:testknow]->(m:Test) where id(n)={uid} return id(m) as nid",
    #                                {"uid" : n.nid})

def has_knows_relation(n1, n2):
    nid1, nid2 = n1.nid, n2.nid
    ret = yelp_graph.cypher.execute("MATCH(n:User)-[r:knows]->(m:User) where id(n)={nid1} and id(m)={nid2} return r",
                                    {"nid1":nid1, "nid2":nid2})
    #ret = yelp_graph.cypher.execute("MATCH(n:Test)-[r:testknow]->(m:Test) where id(n)={nid1} and id(m)={nid2} return r",
    #                                {"nid1":nid1, "nid2":nid2})

    if len(ret) > 0 and ret[0].r != None:
        return True
    return False

def calculate_relationships(n):
    all_friend_nodes = get_all_friends(n)
    ret = 0
    if len(all_friend_nodes) <= 1:
        return 0
    for index in range(len(all_friend_nodes)-1):
        sindex = index + 1
        while sindex < len(all_friend_nodes):
            if has_knows_relation(all_friend_nodes[index], all_friend_nodes[sindex]):
                ret += 1
            sindex += 1
        #if index % 50 == 0:
        #    print index
    return ret

def calculate_avg_friendships(nodes):
    if len(nodes) == 0:
        return 0
    sum = 0
    for n in nodes:
        sum += calculate_relationships(n)
    print "DEBUG:"
    print sum, len(nodes)
    return float(sum) / float(len(nodes))

def avg_clustering_coefficient():
    # 2,    0.195167588676
    # 5,    0.155161590328
    # 10,   0.145253521581
    # 20,   0.13691887742
    # 50,   0.130709321566
    # 100,  0.12884914721
    # 200,  0.0783115577889
    # 1000, 0.0437697697698
    # 3830, 0.00587191196496

    # largest degree is 3830  total should smaller than 5000 by yelp policy
    degrees = [2, 5, 10, 20, 50, 100, 200, 1000, 3830]
    for elem in degrees:
        nodes = get_nodes_with_degree(elem)
        print str(elem) + str(",") + str(len(nodes))
        print str(elem) + str(",") + str(float(2*calculate_avg_friendships(nodes))/float(elem*(elem-1)))

def construct_networkx_graph(friends):
    if len(friends) <= 1:
        return nx.Graph()
    G = nx.Graph()
    for index in range(len(friends)-1):
        sindex = index + 1
        while sindex < len(friends):
            if has_knows_relation(friends[index], friends[sindex]):
                G.add_edge(friends[index].nid, friends[sindex].nid)
            sindex += 1
        if index % 50 == 0:
            print index
    return G

def real_degeneracy(node):
    friends = get_all_friends(node)
    print "construct graph"
    G = construct_networkx_graph(friends)
    print "calculate core number"
    core_list = nx.core_number(G)
    ret = 0
    for key in core_list.keys():
        ret = max(ret, core_list[key])
    return ret

def cal_avg_degeneracy(nodes):
    if len(nodes) == 0:
        return 0
    sum = 0
    for n in nodes:
        sum += real_degeneracy(n)
    print "DEBUG:" + str(sum) + "," + str(len(nodes))
    return float(sum) / float(len(nodes))

def avg_degeneracy():
    # 2,    0.195167588676
    # 5,    0.840502208789
    # 10,   1.74731650711
    # 20,   3.1734197731
    # 50,   6.73513513514
    # 100,  12.5081967213
    # 200,  16.4
    # 1000, 53.0
    # 3830, 50.0

    degrees = [2, 5, 10, 20, 50, 100, 200, 1000, 3830]
    for elem in degrees:
        nodes = get_nodes_with_degree(elem)
        print str(elem) + str(",") + str(cal_avg_degeneracy(nodes))

def cal_unique_friend_of_friend(n):
    ret = yelp_graph.cypher.execute("match(n:User)-[:knows]->(m:User)-[:knows]->(q:User) where id(n)={uid} and id(q)<>{uid} return count(distinct(q)) as cnt",
                                    {"uid" : n.nid})
    #ret = yelp_graph.cypher.execute("match(n:Test)-[:testknow]->(m:Test)-[:testknow]->(q:Test) where id(n)={uid} and id(q)<>{uid} return count(distinct(q)) as cnt",
    #                                {"uid" : n.nid})
    assert len(ret) > 0 and ret[0].cnt != None
    return ret[0].cnt

def cal_nonunique_friend_of_friend(n):
    ret = yelp_graph.cypher.execute("match(n:User)-[:knows]->(m:User)-[:knows]->(q:User) where id(n)={uid} and id(q)<>{uid} return count(q) as cnt",
                                    {"uid" : n.nid})
    #ret = yelp_graph.cypher.execute("match(n:Test)-[:testknow]->(m:Test)-[:testknow]->(q:Test) where id(n)={uid} and id(q)<>{uid} return count(q) as cnt",
    #                                {"uid" : n.nid})
    assert len(ret) > 0 and ret[0].cnt != None
    return ret[0].cnt

def cal_friend_of_friend(n, unique):
    if unique == True:
        return cal_unique_friend_of_friend(n)
    return cal_nonunique_friend_of_friend(n)

def cal_avg_friend_of_friend(nodes, unique):
    if len(nodes) == 0:
        return 0
    sum = 0
    for n in nodes:
        sum += cal_friend_of_friend(n, unique)
    return float(sum) / (float)(len(nodes))

def avg_friends_of_friends(unique=True):
    #2,     279.728278555
    #5,     731.413275982
    #10,    1419.42413693
    #20,    2920.25526742
    #50,    6890.26486486
    #100,   11660.1639344
    #200,   18052.6
    #1000,  38189.0
    #3830,  61114.0

    #2,     288.005165962
    #5,     803.487677284
    #10,    1696.20365535
    #20,    3987.73338736
    #50,    12437.4918919
    #100,   28778.1967213
    #200,   56126.4
    #1000,  224701.0
    #3830,  347004.0

    degrees = [2, 5, 10, 20, 50, 100, 200, 1000, 3830]
    for elem in degrees:
        nodes = get_nodes_with_degree(elem)
        print str(elem) + str(",") + str(cal_avg_friend_of_friend(nodes, unique))

def cal_degree(n):
    ret = yelp_graph.cypher.execute("match(n:User)-[r:knows]->() where id(n)={uid} return count(r) as cnt",
                                    {"uid" : n.nid})
    #ret = yelp_graph.cypher.execute("match(n:Test)-[r:testknow]->() where id(n)={uid} return count(r) as cnt",
    #                                {"uid" : n.nid})
    assert len(ret) > 0 and ret[0].cnt != None
    return ret[0].cnt

def cal_friend_degrees(n):
    all_friend_nodes = get_all_friends(n)
    if len(all_friend_nodes) == 0:
        return 0
    sum = 0
    for n in all_friend_nodes:
        sum += cal_degree(n)
    return float(sum) / float(len(all_friend_nodes))

def cal_avg_degrees_of_friends(nodes):
    if len(nodes) == 0:
        return 0
    sum = 0
    for n in nodes:
        sum += cal_friend_degrees(n)
    return float(sum) / float(len(nodes))

def avg_degrees():
    # 2,145.002501627
    # 5,161.697442455
    # 10,170.620278503
    # 20,200.386628849
    # 50,249.749837838
    # 100,288.781967213
    # 200,281.632
    # 300,350.291111111
    # 400,259.12
    # 1000,225.701
    # 3830,91.6015665796
    degrees = [2,5,10,20,50,100,200,300,400,1000,3830]
    for elem in degrees:
        nodes = get_nodes_with_degree(elem)
        print str(elem) + str(",") + str(len(nodes))
        print str(elem) + str(",") + str(cal_avg_degrees_of_friends(nodes))

if __name__ == "__main__":
    # hop_distance_distribution()
    # component_distribution()

    #avg_degrees()
    #avg_clustering_coefficient()
    avg_degeneracy()
    avg_friends_of_friends(True)
    avg_friends_of_friends(False)

