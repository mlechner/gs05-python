# -*- coding: utf-8 -*-

class Record:
    def __init__(self, recordstring):
        self.record_string = recordstring
        self.data = {}
        self.set_data_from_recordstring()

    def set_data_from_recordstring(self):
        split_string = self.record_string.split(" ")
        split_data = {}
        for val in split_string:
            k, v = val.split(":")
            split_data[k] = v
        # convert strings to numeric values
        self.data = {
            "lowdose": int(split_data["N"], 16),
            "highdose": int(split_data["H"], 16),
            "echo": int(split_data["E"], 16),
            "coincidence": bool(split_data["K"]),
            "highvoltage": bool(split_data["S"]),
            "temperature": split_data["T"]
        }

    def get_lowdose_from_recordstring(self):
        self.record_string.split(" ")[0].split(":")
