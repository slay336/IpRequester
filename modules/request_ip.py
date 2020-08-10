# -*- coding: utf-8 -*-

import requests


class IpGetter:
    url = 'https://api.ipify.org?format=json'

    def get_ip(self):
        return requests.get(self.url).json()
