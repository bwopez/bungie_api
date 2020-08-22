import tkinter as tk
from destiny_functions import (
    membership_ID, membership_type, destiny_memberships,
    search_destiny_player, get_profile,
    get_character, get_activity_history,
    get_destiny_entity_definition, get_destiny_aggregate_activity_stats,
    add_activity_definition
)


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
            command=self.on_button
        )
        self.bungie_button.grid(row=2, column=1)
    

    def on_button(self):
        # print bungie membership id
        id = self.bungie_id_input.get()
        print(id)
        # getting the destiny membeship id
        first_membership = destiny_memberships(id)[0]
        dmid = first_membership["membershipId"]
        print(dmid)
        # find the membership type
        mt = first_membership["membershipType"]
        print(mt)
        # change membership type text
        self.bungie_membership_type["text"] = mt
        # print the profile
        profile1 = get_profile(mt, dmid)
        print(profile1)

    # TODO: make a button that gets and prints all of the activity stats to file


app = DestinyApp()
app.mainloop()
