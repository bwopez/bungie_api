from helper_functions import steam_checker, endpoint_to_Response
import pprint
# important starter information
pp = pprint.PrettyPrinter()


### api functions

# GET BUNGIE.NET USER BY ID
## grabbing matthew's membershipId
# needs bungie.net ID
def membership_ID():
    matthew_link = "/User/GetBungieNetUserById/15882728/".format()
    matthew_Response = endpoint_to_Response(matthew_link)
    matthew_MID = matthew_Response["membershipId"]
    
    return matthew_MID


## GET MEMBERSHIPS BY ID
## grabbing membershipType
# needs membership ID
def membership_type():
    mem_link = "/User/GetMembershipsById/{}/254/".format(matthew_MID)
    mem_Response = endpoint_to_Response(mem_link)
    ## getting membershipType for matthew
    steam_user = steam_checker(mem_Response["destinyMemberships"])
    matthew_MT =steam_user["membershipType"]
    pp.pprint(mem_Response)

    return matthew_MT


## SEARCH DESTINY PLAYER
## testing out searching for a player endpoint
# needs membership type, display name
def search_destiny_player():
    SDP_link = "/Destiny2/SearchDestinyPlayer/{}/{}/".format(matthew_MT, "matthuwu")
    SDP_Response = endpoint_to_Response(SDP_link)
    # pp.pprint(SDP_Response)

    return SDP_Response


## GET PROFILE
# needs membership Type, destiny membership id
def get_profile():
    # TODO: find destiny membership id
    # TODO: still not working 7/31/2020
    # pain
    mt = "254"
    dmid = "4611686018503400629"
    GP_link = "/Destiny2/{}/Profile/{}/".format(mt, dmid)
    GP_Response = endpoint_to_Response(GP_link)
    pp.pprint(GP_Response)


## getting character
# needs membershipType, destinyMembershipId, characterId
def get_character():
    # TODO: finish this
    GC_link = "/Destiny2/{}/Profile/{}/Character/{}/".format(matthew_MT, "4611686018437293480", matthew_CID)


## testing out activity history
# need membershipType, destinyMemberhipId, characterId
def get_activity_history():
    GAH_link = "/Destiny2/{}/Account/{}/Character/{}/Stats/Activities/".format("2", "4611686018437293480", "2305843009267529341")
    GAH_Response = endpoint_to_Response(GAH_link)

    return GAH_Response


def get_activity_hashes(activities):
    activity_hashes = []
    for activity in activities:
        activity_hashes.append(activity["activityDetails"]["directorActivityHash"])

    print(activity_hashes)
    return activity_hashes


def get_destiny_entity_definition(entity_type, hash_identifier):
    GDED_link = "/Destiny2/Manifest/{}/{}/".format(entity_type, hash_identifier)
    GDED_Response = endpoint_to_Response(GDED_link)

    return GDED_Response


## testing out carnage report
# CR_endpoint = requests.get("/Destiny2/Stats/PostGameCarnageReport/{activityId}/".format(activity_id), headers=HEADERS)
# CR_endpoint_json = CR_endpoint.json()
# pp.pprint(CR_endpoint_json["Response"])


if __name__ == "__main__":
    # matthew_MID = membership_ID()
    # matthew_MT = membership_type()
    # dmid_maybe = search_destiny_player()

    # print(matthew_MID, matthew_MT)
    # get_profile()

    # pp.pprint(get_activity_history()["activities"])
    history = get_activity_history()["activities"]
    activity_hashes = get_activity_hashes(history)
    for activity in activity_hashes:
        pp.pprint(get_destiny_entity_definition("DestinyActivityDefinition", activity)["displayProperties"])

    # pp.pprint(helper_functions.thing()["Response"]["activities"][0])
