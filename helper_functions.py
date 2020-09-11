import requests
import os
import json


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


def format_character_response(response):
    """
    A helper function to format a character response and put it into the destiny_api_globals.json file

    Args:
        response (list): The response that holds the character information to be translated

    Returns:
        None
    """
    with open("destiny_api_globals.json") as f:
        data = json.load(f)
        character_stats_dict = {}
        for stat in response["character"]["data"]["stats"].keys():
            stat_name = data["DestinyCharacterStats"][stat]["name"]
            character_stats_dict[stat_name] = response["character"]["data"]["stats"][stat]

        response["character"]["data"]["stats"] = character_stats_dict
        
    return response


def write_to_file(file_name, data, is_json):
    """
    A function that writes the data passed into the function to a named file

    Args:
        file_name (str): The name of the file
        data (str): The data to write to file
        is_json (bool): A way to differentiate if the file should be written as .json or .txt

    Returns:
        None
    """
    if is_json:
        with open(file_name + ".json", "w") as file_out:
            json.dump(data, file_out)
    else:
        with open(file_name + ".txt", "w") as file_out:
            file_out.write(data)
        
    print("finished writing.")


def strip_the_json(file_name):
    with open("{}{}".format(file_name, ".json")) as file_in:
        data = json.load(file_in)


        temp = []
        for subset in data:
            new_dict = {}
            # activity mode types
            # display properties:
                # 1. name
                # 2. description
            if subset["activityDefinition"] == "No Activity Definition":
                new_dict["name"] = "No name"
                new_dict["description"] = "No description"
                new_dict["activityModeTypes"] = []
            else:
                new_dict["name"] = subset["activityDefinition"]["displayProperties"]["name"]
                new_dict["description"] = subset["activityDefinition"]["displayProperties"]["description"]
                if "activityModeTypes" in subset["activityDefinition"].keys():
                    new_dict["activityModeTypes"] = subset["activityDefinition"]["activityModeTypes"]
                else:
                    new_dict["activityModeTypes"] = []

            # activity hash
            # move all values out of values
                # take information out of 'basic'
                # remove displaValue
                # remove statId OR remove activityId
                # ONLY use value
            new_dict["activityHash"] = subset["activityHash"]
            for key in subset["values"].keys():
                new_dict[key] = subset["values"][key]["basic"]["value"]

            temp.append(new_dict)

        with open("{}_cleanedish{}".format(file_name, ".json"), "w") as file_out:
            json.dump(temp, file_out)

    print("'{}{}' is now kaggle readable".format(file_name, ".json"))


if __name__ == "__main__":
    strip_the_json("titan2_but_json")