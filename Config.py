# -*- coding: utf-8 -*-

import configparser


class Config:
    def __init__(self, path="./config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def get_config(self):
        return self.config
