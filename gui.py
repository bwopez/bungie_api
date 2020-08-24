import tkinter as tk
from destiny_functions import (
    membership_ID, membership_type, destiny_memberships,
    search_destiny_player, get_profile,
    get_character, get_activity_history,
    get_destiny_entity_definition, get_destiny_aggregate_activity_stats,
    add_activity_definition
)

import pprint
pp = pprint.PrettyPrinter()


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

        # this one
        self.OptionList = ["character1", "character2", "character3"]
        self.variable = tk.StringVar(self)
        self.variable.set(self.OptionList[0])
        self.dropdown_list = tk.OptionMenu(self, self.variable, *self.OptionList)
        self.dropdown_list.grid(row=0, column=2)
        # self.character_label = tk.Label(self)
        # self.character_label.grid(row=0, column=2)

        # self.character_input = tk.Entry(self)
        # self.character_input.grid(row=1, column=2)

        self.character_information_button = tk.Button(
            self,
            text="load character information",
            command=self.load_character_information
        )
        self.character_information_button.grid(row=2, column=2)

        # self.refresh_button = tk.Button(
        #     self,
        #     text="refresh the character list",
        #     command=self.refresh_characters
        # )
        # self.refresh_button.grid(row=3, column=2)


    def refresh_characters(self, character_list):
        self.variable.set("")
        self.dropdown_list["menu"].delete(0, "end")

        new_choices = character_list
        # new_choices = ["titan1", "warlock2", "maybe no hunter"]
        self.variable.set(new_choices[0])
        for choice in new_choices:
            self.dropdown_list["menu"].add_command(label=choice, command=tk._setit(self.variable, choice))


    def load_personal_info(self):
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

        # self.character_label["text"] = self.current_profile["profile"]["data"]["characterIds"]
        self.refresh_characters(self.current_profile["profile"]["data"]["characterIds"])


    def load_character_information(self):
        # self.current_cid = self.character_input.get()
        self.current_cid = self.variable.get()

        pp.pprint(get_character(self.current_mt, self.current_dmid, self.current_cid))


    # TODO: make a button that gets and prints all of the activity stats to file


    # variables
    current_id = ""
    current_dmid = ""
    current_mt = ""
    current_profile = []
    current_cid = ""


app = DestinyApp()
app.mainloop()
