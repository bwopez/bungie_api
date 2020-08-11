from destiny_functions import (
    membership_ID, membership_type, 
    search_destiny_player, get_profile,
    get_character, get_activity_history,
    get_destiny_entity_definition, get_destiny_aggregate_activity_stats,
    add_display_properties
)

import pprint
pp = pprint.PrettyPrinter()


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

    activity_stats = get_destiny_aggregate_activity_stats(matthewbropez_mt, matthewbropez_dmid, matthewbropez_character_id1)["activities"]
    activity_stats_and_display = add_display_properties(activity_stats) 

    activity_stats_and_display = pprint.pformat(activity_stats)
    with open("activity_stats_with_display_properties.txt", "w") as file_out:
        file_out.write(activity_stats_and_display)

    # pp.pprint(matthewbropez_character_info2)

    # pp.pprint(get_activity_history()["activities"])
    # history = get_activity_history(matthewbropez_mt, matthewbropez_dmid, matthewbropez_character_id1)["activities"]
    # activity_hashes = get_activity_hashes(history)
    # pp.pprint(history[-1])
    # for index, activity in enumerate(activity_hashes):
    #     pp.pprint(get_destiny_entity_definition("DestinyActivityDefinition", activity)["displayProperties"])
    #     pp.pprint(history[index])
    # pp.pprint(get_destiny_entity_definition("DestinyActivityDefinition", activity_hashes[-1])["displayProperties"])
