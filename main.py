from helper_functions import steam_checker, endpoint_to_Response, get_activity_hashes

import pprint
# important starter information
pp = pprint.PrettyPrinter()


### api functions

# GET BUNGIE.NET USER BY ID
## grabbing matthew's bungie membershipId
# needs bungie.net ID
def membership_ID(bungie_membership_id):
    GBNUID_link = "/User/GetBungieNetUserById/{}/".format(bungie_membership_id)
    GBNUID_Response = endpoint_to_Response(GBNUID_link)
    BMID = GBNUID_Response["membershipId"]
    # pp.pprint(GBNUID_Response)
    
    return BMID


## GET MEMBERSHIPS TYPE BY Bungie Membership ID
## grabbing membershipType
# needs bungie membership ID
def membership_type(bungie_membership_id):
    MT_link = "/User/GetMembershipsById/{}/254/".format(bungie_membership_id)
    MT_Response = endpoint_to_Response(MT_link)
    ## getting membershipType for matthew
    steam_user = steam_checker(MT_Response["destinyMemberships"])
    user_MT =steam_user["membershipType"]
    pp.pprint(MT_Response)

    return user_MT


## SEARCH DESTINY PLAYER
## testing out searching for a player endpoint
# needs membership type, display name
def search_destiny_player(membership_type, display_name):
    SDP_link = "/Destiny2/SearchDestinyPlayer/{}/{}/".format(membership_type, display_name)
    SDP_Response = endpoint_to_Response(SDP_link)
    # pp.pprint(SDP_Response)

    return SDP_Response


## GET PROFILE
# needs membership Type, destiny membership id
def get_profile(membership_type, destiny_membership_id):
    # solved. needed ?components=100 to get profiles for this endpoint
    GP_link = "/Destiny2/{}/Profile/{}/?components=100".format(membership_type, destiny_membership_id)
    GP_Response = endpoint_to_Response(GP_link)
    # pp.pprint(GP_Response)

    return GP_Response


## getting character
# needs membershipType, destinyMembershipId, characterId
def get_character(membership_type, destiny_membership_id, character_id):
    # SOLVED: needed "?components=200" for character summary
    GC_link = "/Destiny2/{}/Profile/{}/Character/{}/?components=200".format(membership_type, destiny_membership_id, character_id)
    GC_Response = endpoint_to_Response(GC_link)

    # pp.pprint(GC_Response)
    return GC_Response


## testing out activity history
# need membershipType, destinyMemberhipId, characterId
def get_activity_history(membership_type, destiny_membership_id, character_id):
    GAH_link = "/Destiny2/{}/Account/{}/Character/{}/Stats/Activities/".format(membership_type, destiny_membership_id, character_id)
    GAH_Response = endpoint_to_Response(GAH_link)

    return GAH_Response


# need entity type, hash identifier
def get_destiny_entity_definition(entity_type, hash_identifier):
    GDED_link = "/Destiny2/Manifest/{}/{}/".format(entity_type, hash_identifier)
    GDED_Response = endpoint_to_Response(GDED_link)

    return GDED_Response


## testing out carnage report
# CR_endpoint = requests.get("/Destiny2/Stats/PostGameCarnageReport/{activityId}/".format(activity_id), headers=HEADERS)
# CR_endpoint_json = CR_endpoint.json()
# pp.pprint(CR_endpoint_json["Response"])


if __name__ == "__main__":
    # unique_name = "15882728"
    # matthew_BMID = membership_ID(unique_name)
    # matthew_MT = membership_type(matthew_BMID)
    destiny_player = search_destiny_player("3", "matthuwu")

    matthuwu, matthewbropez = destiny_player
    matthuwu_mt = matthuwu["membershipType"]
    matthuwu_dmid = matthuwu["membershipId"]

    matthewbropez_mt = matthewbropez["membershipType"]
    matthewbropez_dmid = matthewbropez["membershipId"]

    # print(matthew_MID, matthew_MT)
    # profile = get_profile(matthuwu_mt, matthuwu_dmid)
    # matthuwu_character_id = profile["profile"]["data"]["characterIds"][0]
    # print(matthuwu_character_id)
    # matthuwu_character = get_character(matthuwu_mt, matthuwu_dmid, matthuwu_character_id)

    profile2 = get_profile(matthewbropez_mt, matthewbropez_dmid)
    matthewbropez_character_id1, matthewbropez_character_id2 = profile2["profile"]["data"]["characterIds"]
    matthewbropez_character_info1 = get_character(matthewbropez_mt, matthewbropez_dmid, matthewbropez_character_id1)
    matthewbropez_character_info2 = get_character(matthewbropez_mt, matthewbropez_dmid, matthewbropez_character_id2)

    # pp.pprint(matthewbropez_character_info2)

    # pp.pprint(get_activity_history()["activities"])
    history = get_activity_history(matthewbropez_mt, matthewbropez_dmid, matthewbropez_character_id1)["activities"]
    activity_hashes = get_activity_hashes(history)
    for activity in activity_hashes:
        pp.pprint(get_destiny_entity_definition("DestinyActivityDefinition", activity)["displayProperties"])
