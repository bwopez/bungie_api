from helper_functions import (steam_checker, endpoint_to_Response, 
    get_activity_hashes)

import pprint
pp = pprint.PrettyPrinter()


### api functions

# GET BUNGIE.NET USER BY ID
## grabbing matthew's bungie membershipId
# needs bungie.net ID
def membership_ID(bungie_membership_id):
    # TODO: maybe refactor this to get just the Response?
    """
    Gets just the Bungie Membership ID

    Args:
        bungie_membership_id (str): The bungie membership ID of the selected user

    Returns:
        BMID (str): The bungie membership ID of the selected user
    """
    GBNUID_link = "/User/GetBungieNetUserById/{}/".format(bungie_membership_id)
    GBNUID_Response = endpoint_to_Response(GBNUID_link)
    BMID = GBNUID_Response["membershipId"]
    # pp.pprint(GBNUID_Response)
    print(type(BMID))
    
    return BMID


## GET MEMBERSHIPS TYPE BY Bungie Membership ID
## grabbing membershipType
# needs bungie membership ID
def membership_type(bungie_membership_id):
    """
    Gets the membership type for the specific bungie member

    Args:
        bungie_membership_id (str): The specific bungie membership ID of the selected user

    Returns:
        user_MT (str): The bungie membership type of the selected user
    """
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
    """
    Searches for the Destiny Player

    Args:
        membership_type (str): Which console the player is on. 1 = Xbox, 2 = PSN, 3 = Steam, 254 = Bungie
        display_name (str): The display name of the player

    Returns:
        SDP_Response (list): The Response from the endpoint
    """
    SDP_link = "/Destiny2/SearchDestinyPlayer/{}/{}/".format(membership_type, display_name)
    SDP_Response = endpoint_to_Response(SDP_link)
    # pp.pprint(SDP_Response)

    return SDP_Response


## GET PROFILE
# needs membership Type, destiny membership id
def get_profile(membership_type, destiny_membership_id):
    """
    Gets profile information of a specific member based on console and destiny membership id

    Args:
        membership_type (str): Which console the player is on. 1 = Xbox, 2 = PSN, 3 = Steam, 254 = Bungie
        destiny_membership_id (str): The Destiny Membership ID for the player

    Returns:
        GP_Response (list): The Response from the endpoint
    """
    GP_link = "/Destiny2/{}/Profile/{}/?components=100".format(membership_type, destiny_membership_id)
    GP_Response = endpoint_to_Response(GP_link)
    pp.pprint(GP_Response)

    return GP_Response


## getting character
# needs membershipType, destinyMembershipId, characterId
def get_character(membership_type, destiny_membership_id, character_id):
    """
    Gets the Destiny 2 character information of a player

    Args:
        membership_type (str): Which console the player is on. 1 = Xbox, 2 = PSN, 3 = Steam, 254 = Bungie
        destiny_membership_id (str): The Destiny Membership ID for the player
        character_id (str): The Character ID for the player's specific character

    Returns: 
        GC_Response (list): The Response from the endpoint
    """
    # SOLVED: needed "?components=200" for character summary
    GC_link = "/Destiny2/{}/Profile/{}/Character/{}/?components=200".format(membership_type, destiny_membership_id, character_id)
    GC_Response = endpoint_to_Response(GC_link)

    # pp.pprint(GC_Response)
    return GC_Response


## testing out activity history
# need membershipType, destinyMemberhipId, characterId
def get_activity_history(membership_type, destiny_membership_id, character_id):
    """
    Gets the activity history for a specific Destiny 2 character

    Args:
        membership_type (str): Which console the player is on. 1 = Xbox, 2 = PSN, 3 = Steam, 254 = Bungie
        destiny_membership_id (str): The Destiny Membership ID for the player
        character_id (str) : The Character ID for the player's specific character

    Returns:
        GAH_Response (list): The Response from the endpoint
    """
    GAH_link = "/Destiny2/{}/Account/{}/Character/{}/Stats/Activities/".format(membership_type, destiny_membership_id, character_id)
    GAH_Response = endpoint_to_Response(GAH_link)

    return GAH_Response


# need entity type, hash identifier
def get_destiny_entity_definition(entity_type, hash_identifier):
    """
    Gets the Destiny 2 entity definition

    Args:
        entity_type (str): What kind of entity
        hash_identifier (str): The hash that the entity has

    Returns:
        GDED_Response (list): The Response from the endpoint
    """
    GDED_link = "/Destiny2/Manifest/{}/{}/".format(entity_type, hash_identifier)
    GDED_Response = endpoint_to_Response(GDED_link)
    pp.pprint(GDED_Response)

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
    # for activity in activity_hashes:
    #     pp.pprint(get_destiny_entity_definition("DestinyActivityDefinition", activity)["displayProperties"])
