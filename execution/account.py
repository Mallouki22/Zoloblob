"""
Account Manager
"""

from mt5.client import MT5Client


class AccountManager:

    def __init__(self):

        self.client = MT5Client()

        self.client.initialize()


    def info(self):

        return self.client.account_info()


    def balance(self):

        return self.info().balance


    def equity(self):

        return self.info().equity


    def margin(self):

        return self.info().margin


    def free_margin(self):

        return self.info().margin_free