from helper_functions import (steam_checker, endpoint_to_Response, 
    get_activity_hashes)


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
    # pp.pprint(MT_Response)

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
    # pp.pprint(GP_Response)

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
    # pp.pprint(GDED_Response)

    return GDED_Response


# needs membership type, destiny membership id, character id
def get_destiny_aggregate_activity_stats(membership_type, destiny_membership_id, character_id):
    GDAAS_link = "/Destiny2/{}/Account/{}/Character/{}/Stats/AggregateActivityStats/".format(membership_type, destiny_membership_id, character_id)
    GDAAS_Response = endpoint_to_Response(GDAAS_link)
    # pp.pprint(GDAAS_Response)

    return GDAAS_Response


def add_display_properties(activity_stats):
    for index, activity in enumerate(activity_stats):
        temp = activity_stats[index]
        temp_hash = temp["activityHash"]
        definition = get_destiny_entity_definition("DestinyActivityDefinition", temp_hash)
        if (type(definition) != type("")):
            temp["displayProperties"] = definition["displayProperties"]
        else:
            temp["displayProperties"] = "No Display Properties"

        activity_stats[index] = temp

    return activity_stats



## testing out carnage report
# CR_endpoint = requests.get("/Destiny2/Stats/PostGameCarnageReport/{activityId}/".format(activity_id), headers=HEADERS)
# CR_endpoint_json = CR_endpoint.json()
# pp.pprint(CR_endpoint_json["Response"])