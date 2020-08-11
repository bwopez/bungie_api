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
    """
    Changes the endpoint that is passed in into a workable Response

    Args:
        link (str): The link to the endpoint 

    Returns:
        endpoint_json["Response"] (dict): The Response from endpoint
    """
    x_api_key = os.environ.get("bungie_key")
    HEADERS = {"X-API-Key":x_api_key}
    starter = "https://www.bungie.net/Platform"

    endpoint = requests.get(starter + link, headers=HEADERS)
    try:
        endpoint_json = endpoint.json()

        return endpoint_json["Response"]
    except:
        return "No Response"


def get_activity_hashes(activities):
    """
    Extracts only the hashes out of the list of activities given

    Args:
        activities (list): The list of activities

    Returns:
        activity_hashes (list): The list of hashes
    """
    activity_hashes = []
    for activity in activities:
        activity_hashes.append(activity["activityDetails"]["directorActivityHash"])

    return activity_hashes
