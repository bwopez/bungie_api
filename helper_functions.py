import requests
import os


### helper functions
def steam_checker(membership_data):
    """
    Checks to see if the passed in member has connected their account to Steam.
    If so then it returns the correct Steam information

    Args:
        membership_data (list): A python list of json bungie.net membership data

    Returns:
        cluster (dict): A python dictionary of json bungie.net Steam membership data
    """
    for cluster in membership_data:
        if "steam" in cluster["iconPath"]:
            return cluster
    
    print("Couldn't find a steam user")
    return membership_data[0]


def endpoint_to_Response(link):
    x_api_key = os.environ.get("bungie_key")
    HEADERS = {"X-API-Key":x_api_key}
    starter = "https://www.bungie.net/Platform"

    endpoint = requests.get(starter + link, headers=HEADERS)
    endpoint_json = endpoint.json()
    #pp.pprint(endpoint_json["Response"])

    return endpoint_json["Response"]


def thing():
    # I'm just testing stuff here really
    x_api_key = os.environ.get("bungie_key")
    HEADERS = {"X-API-Key":x_api_key}
    # r = requests.get("https://www.bungie.net/Platform/Destiny2/SearchDestinyPlayer/3/matthuwu/", headers=HEADERS)
    r = requests.get("https://www.bungie.net/Platform/User/GetMembershipsById/4611686018437293480/2/", headers=HEADERS)
    json = r.json()
    response = json["Response"]
    DMID = response["destinyMemberships"][1]["membershipId"]
    DMT = response["destinyMemberships"][1]["membershipType"]

    r2 = requests.get(
        # ?components=100 is needed for getting profiles
        "https://www.bungie.net/Platform/Destiny2/2/Profile/4611686018437293480/?components=100".format(DMID, DMT), 
        headers=HEADERS
    )
    json2= r2.json()

    activity_list_link = requests.get(
        "https://www.bungie.net/Platform/Destiny2/2/Account/4611686018437293480/Character/2305843009267529341/Stats/Activities/",
        headers=HEADERS
    )
    activity_list_json = activity_list_link.json()
    return activity_list_json

    # TODO: okay we got the character information and '?components=' part lets go
    ## now how do we find entityType
    # thingy = requests.get("https://www.bungie.net/Platform/Destiny2/Manifest/{entityType}/4148187374/", headers=HEADERS)
    # thingy_json = thingy.json()
    # return thingy_json


    # r = requests.get("http://www.bungie.net/Platform/Destiny2/2/Profile/4611686018437293480/", headers=HEADERS)
    # return activity_list_json["Response"]["activities"][0]
