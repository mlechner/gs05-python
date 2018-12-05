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
        bittemp = split_data["T"][0], split_data["T"][1:3], split_data["T"][3:5], split_data["T"][5:]
        temperature = float(str(bittemp[0]) + str(int(bittemp[1], 16)) + '.' + str((int(bittemp[2], 16)*100)/256))
        # convert strings to numeric values
        self.data = {
            "lowdose": int(split_data["N"], 16),
            "highdose": int(split_data["H"], 16),
            "echo": int(split_data["E"], 16),
            "coincidence": bool(int(split_data["K"])),
            "highvoltage": bool(int(split_data["S"])),
            "temperature": temperature
        }
