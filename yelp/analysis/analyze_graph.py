__author__ = 'yan.cui'

# network components distribution

# network hop distance distribution

# friends of friends, number of non-unique friends, and number of unique friends

# average degree of neighbors against degrees

# percentage against neighbor's degree

# when fans number is larger, compliments activity and votes should be more active
# which mechanism is more effective? votes or compliments?

# which one is more effective? tip or review?

# how location affect users on yelp

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
    # MATCH (n)
    # WITH COLLECT(n) as nodes
    # RETURN REDUCE(graphs = [], n in nodes |
    #   case when
    #     ANY (g in graphs WHERE shortestPath( (n)-[*]-(g) ) )
    #     then graphs
    #     else graphs + [n]
    #     end )
    pass