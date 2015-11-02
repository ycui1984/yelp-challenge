__author__ = 'yan.cui'

import json
from py2neo import Graph

yelp_graph = Graph()
def parse_json_object_from_file(file_name):
    file_to_handler = {"user" : handle_one_user, "business" : handle_one_bussiness,
                        "checkin" : handle_one_checkin, "review" : handle_one_review, "tip" : handle_one_tip}
    with open(file_name) as file:
        for line in file:
            while True:
                try:
                    json_object = json.loads(line)
                    break
                except:
                    line += next(file)
            been_processed = False
            for key in file_to_handler.keys():
                if file_name.find(key) != -1:
                    file_to_handler[key](json_object)
                    been_processed = True
                    break
            if been_processed == False:
                print "unknown file"

def dict_to_list(target_dict):
    ret = []
    if target_dict == {}:
        return ret
    for key in target_dict.keys():
        if not isinstance(target_dict[key], dict):
            ret.extend([key, unicode(target_dict[key])])
        else:
            key_ret = unicode(','.join(dict_to_list(target_dict[key])))
            ret.extend([key, key_ret])
    return ret

def query_by_id(user_id):
    return yelp_graph.cypher.execute("MATCH u WHERE u.user_id = {id} return u", {"id" : user_id})

def query_by_bussiness_id(business_id):
    return yelp_graph.cypher.execute("MATCH b WHERE b.business_id = {id} return b", {"id" : business_id})

def create_knows_relations(user, person):
    yelp_graph.cypher.execute("MATCH (u:Person),(p:Person) WHERE u.user_id = {user_id} AND p.user_id = {person_id} " +
                              "CREATE UNIQUE u-[:knows]->p", {"user_id" : user, "person_id" : person})

def handle_one_user(json_object):
    result_set = query_by_id(json_object["user_id"])
    votes_list, compliments_list = dict_to_list(json_object["votes"]), dict_to_list(json_object["compliments"])
    if len(result_set) == 0:
        # no such user, create node, add information
        yelp_graph.cypher.execute("CREATE (u :User :Person {yelping_since:{yelping_since}, review_count:{review_count}, " +
                                  "name:{name}, user_id:{user_id}, fans:{fans}, average_stars:{average_stars}, " +
                                  "type:{type}, elite:{elite}, votes:{votes_list}, compliments:{compliments_list}})",
                                  {"yelping_since": json_object["yelping_since"], "review_count":json_object["review_count"],
                                   "name":json_object["name"], "user_id":json_object["user_id"], "fans":json_object["fans"],
                                   "average_stars":json_object["average_stars"], "type":json_object["type"],
                                   "elite":json_object["elite"], "votes_list":votes_list, "compliments_list":compliments_list})
    else:
        # have such user, add information
        print "adding user label..."
        yelp_graph.cypher.execute("MATCH (p:Person {user_id:{user_id}}) SET p :User, p.yelping_since={yelping_since}, " +
                                  "p.review_count={review_count}, p.name={name}, p.fans={fans}, p.average_stars={average_stars}, " +
                                  "p.type={type}, p.elite={elite}, p.votes={votes_list}, p.compliments={compliments_list}",
                                  {"user_id":json_object["user_id"], "yelping_since": json_object["yelping_since"],
                                   "review_count":json_object["review_count"],"name":json_object["name"], "fans":json_object["fans"],
                                   "average_stars":json_object["average_stars"],"type":json_object["type"],
                                   "elite":json_object["elite"], "votes_list":votes_list, "compliments_list":compliments_list})

    friends = json_object["friends"]
    for person in friends:
        result = query_by_id(person)
        if len(result) == 0:
            # create person
            yelp_graph.cypher.execute("CREATE (p:Person {user_id:{user_id}})", {"user_id":person})
        create_knows_relations(json_object["user_id"], person)


def handle_one_bussiness(json_object):
    result_set = query_by_bussiness_id(json_object["business_id"])
    hours = dict_to_list(json_object["hours"])
    print hours
    attributes = dict_to_list(json_object["attributes"])
    print attributes
    assert len(result_set) == 0
    yelp_graph.cypher.execute("CREATE (b :Business {business_id:{business_id}, full_address:{full_address}, " +
                              "open:{open}, categories:{categories}, city:{city}, review_count:{review_count}, " +
                              "name:{name}, neighborhoods:{neighborhoods}, longitude:{longitude}, state:{state}, " +
                              "stars:{stars}, latitude:{latitude}, type:{type}, attributes:{attributes}, hours:{hours}})",
                              {"business_id": json_object["business_id"], "full_address": json_object["full_address"],
                               "open":json_object["open"], "categories":json_object["categories"],
                               "city":json_object["city"], "review_count":json_object["review_count"], "name":json_object["name"],
                               "neighborhoods":json_object["neighborhoods"], "longitude":json_object["longitude"],
                               "state":json_object["state"], "stars":json_object["stars"], "latitude":json_object["latitude"],
                               "type":json_object["type"], "attributes":attributes, "hours":hours})

def handle_one_checkin(json_object):
    pass

def handle_one_review(json_object):
    pass

def handle_one_tip(json_object):
    pass

def prepare_database():
    yelp_graph.cypher.execute("MATCH (n)-[r]-() DELETE n,r")
    yelp_graph.cypher.execute("MATCH (n) DELETE n")
    try:
        yelp_graph.cypher.execute("DROP CONSTRAINT ON (p:Person) ASSERT p.user_id IS UNIQUE")
    except:
        print "NO TARGET CONSTRAINT, IGNORE"
    yelp_graph.cypher.execute("CREATE CONSTRAINT ON (p:Person) ASSERT p.user_id IS UNIQUE")

if __name__ == "__main__":
    # order here is important
    prepare_database()
    file_list = ["yelp_academic_dataset_testbusiness.json"]
    for elem in file_list:
        parse_json_object_from_file("dataset/yelp/" + elem)