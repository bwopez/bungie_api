import tkinter as tk
from destiny_functions import (
    membership_ID, membership_type, destiny_memberships,
    search_destiny_player, get_profile,
    get_character, get_activity_history,
    get_destiny_entity_definition, get_destiny_aggregate_activity_stats,
    add_activity_definition,
)
from helper_functions import (
    format_character_response, write_to_file, strip_the_json,
)

import pprint
pp = pprint.PrettyPrinter()

import json


class DestinyApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.bungie_id_label = tk.Label(self, text="bungie.net ID")
        self.bungie_id_label.grid(row=0, column=0)

        self.bungie_id_input = tk.Entry(self)
        self.bungie_id_input.grid(row=0, column=1)

        self.bungie_membership_type_label = tk.Label(self, text="bungie membership type")
        self.bungie_membership_type_label.grid(row=1, column=0)

        self.bungie_membership_type = tk.Label(self)
        self.bungie_membership_type.grid(row=1, column=1)

        self.bungie_button = tk.Button(
            self,
            text="print bungie stuff",
            command=self.load_personal_info
        )
        self.bungie_button.grid(row=2, column=1)

        self.matthews_bmid = tk.Label(self, text="15882728")
        self.matthews_bmid.grid(row=3, column=1)

        self.OptionList = ["Choose your character", "character1", "character2", "character3"]
        self.variable = tk.StringVar(self)
        self.variable.set(self.OptionList[0])
        self.dropdown_list = tk.OptionMenu(self, self.variable, *self.OptionList)
        self.dropdown_list.configure(state="disabled")
        self.dropdown_list.grid(row=0, column=2)

        self.character_information_button = tk.Button(
            self,
            text="print character information",
            command=self.load_character_information,
        )
        self.character_information_button.configure(state="disabled")
        self.character_information_button.grid(row=2, column=2)

        self.activities_file_name = tk.Entry(self)
        self.activities_file_name.configure(state="disabled")
        self.activities_file_name.grid(row=1, column=3)

        self.print_activities_to_file_button = tk.Button(
            self,
            text="print activities to file",
            command=self.activities_to_file,
        )
        self.print_activities_to_file_button.configure(state="disabled")
        self.print_activities_to_file_button.grid(row=2, column=3)

        self.strip_the_json_button = tk.Button(
            self,
            text="make the data kaggle readable",
            command=self.decompress_the_json
        )
        self.strip_the_json_button.configure(state="disabled")
        self.strip_the_json_button.grid(row=2, column=4)


    def refresh_characters(self, character_list):
        """
        Refresh the character list

        Args:
            self
            character_list (list): The list of characters to put into the list

        Returns:
            None
        """
        self.variable.set("")
        self.dropdown_list["menu"].delete(0, "end")
        character_list.insert(0, "Choose your character")

        new_choices = character_list
        self.variable.set(character_list[0])
        for choice in new_choices:
            self.dropdown_list["menu"].add_command(label=choice, command=tk._setit(self.variable, choice))


    def load_personal_info(self):
        """
        Loads the information for the specific bungie.net user

        Args:
            self

        Returns:
            None
        """
        # print bungie membership id
        self.current_id = self.bungie_id_input.get()
        print("current bungie.net id: ", self.current_id)
        # getting the destiny membeship id
        first_membership = destiny_memberships(self.current_id)[0]
        self.current_dmid = first_membership["membershipId"]
        print("current destiny membership id: ", self.current_dmid)
        # find the membership type
        self.current_mt = first_membership["membershipType"]
        print("current membership type: ", self.current_mt)
        # change membership type text
        self.bungie_membership_type["text"] = self.current_mt
        # print the profile
        self.current_profile = get_profile(self.current_mt, self.current_dmid)
        pp.pprint(self.current_profile)

        # enable the things
        self.dropdown_list.configure(state="active")
        self.character_information_button.configure(state="active")

        # this is just grabbing the character IDs from the profile
        self.refresh_characters(self.current_profile["profile"]["data"]["characterIds"])


    def load_character_information(self):
        """
        Loads the character information for the chosen Destiny 2 character

        Args:
            self

        Returns:
            None
        """
        self.current_cid = self.variable.get()

        # TODO: 3. maybe cache a character response so that we won't need to make another api call if we don't need to

        if self.current_cid == "Choose your character":
            pp.pprint("Please choose your character")

            self.print_activities_to_file_button.configure(state="disabled")
            self.activities_file_name.configure(state="disabled")
            self.strip_the_json_button.configure(state="disabled")
        else:
            response = get_character(self.current_mt, self.current_dmid, self.current_cid)

            # TODO: 2. make something so that a human can read the Character stats and not a computer hash
            new_response = format_character_response(response)
            pp.pprint(new_response)

            self.print_activities_to_file_button.configure(state="normal")
            self.activities_file_name.configure(state="normal")
            self.strip_the_json_button.configure(state="normal")


    # make a button that gets and prints all of the activity stats to file
    def activities_to_file(self):
        """
        Save the Destiny aggregate activity stats to a file

        Args:
            self

        Returns:
            None
        """
        activity_stats = get_destiny_aggregate_activity_stats(self.current_mt, self.current_dmid, self.current_cid)["activities"]
        activity_stats_and_definition = add_activity_definition(activity_stats)

        file_name = self.activities_file_name.get()
        # activity_stats_and_definition = pprint.pformat(activity_stats)
        write_to_file(file_name, activity_stats_and_definition, True)


    # TODO: make a button that strips all of the stuff and formats it into kaggle readable
    def decompress_the_json(self):
        file_name = self.activities_file_name.get()
        strip_the_json(file_name)


    # variables
    current_id = ""
    current_dmid = ""
    current_mt = ""
    current_profile = []
    current_cid = ""


app = DestinyApp()
app.mainloop()
