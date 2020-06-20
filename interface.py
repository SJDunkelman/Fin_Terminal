"""
Finnhub API Command Line Interface.
For full documentation see: https://finnhub.io/docs/api

S. Dunkelman (https://www.dunkelman.co)

Distributed under a __ license.
See license.txt for full terms & conditions.
"""

import re
import time
import requests
import argparse
import math as m
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from timeit import default_timer as timer

class DataVendor(object):
    def __init__(self, *args, **kwargs):
        if args is None:
            print("Need base URL for API!")
            raise ValueError
        else:
            url = "https://"
            for argument in args:
                url += argument + '/'
        self.url = url
        
        self.set_request_limit(**kwargs)
        
    def set_request_limit(self, **kwargs):
        """
        Should be overridden by child class, if not then no limit is assumed
        """
        self.request_limit = None
                
class FinnHub(DataVendor):
    def __init__(self,account_type):
        """
        Future improvements will include scraping API version from docs.
        Example:
        
        ## Get documentation from website
        documentation = 'https://finnhub.io/docs/api'
        temp_request = requests.get(documentation)
        soup = BeautifulSoup(temp_request.text, 'html.parser')
        
        ## Get latest base URL for API
        api_base = re.search(r'(?<=code\\u003e\/)(...\/..)(?=\\u003c\/code)',soup)
        """
        super().__init__('finnhub.io','api/v1',account_type=account_type)
        
        
    def set_request_limit(self,**kwargs):
        """
        Arguments:
            account_type        = 'f'ree / 'b'asic / 's'tandard / 'p'rofessional / 'u'ltimate
        """
        if kwargs['account_type'] == 'f':
            self.request_limit = 30
        elif kwargs['account_type'] ==  'b':
            self.request_limit = 150
        elif kwargs['account_type'] ==  's':
            self.request_limit = 300
        elif kwargs['account_type'] ==  'p':
            self.request_limit = 700
        elif kwargs['account_type'] ==  'u':
            self.request_limit = 900
        

class Interface():
    def __init__(self,args,data_vendor='finnhub'):

        
        if data_vendor == 'finnhub':
            pass
    

            
    def iteration(self):
        pass
        
        
        
if __name__ == '__main__':
    ## Command Line Interface
    parser = argparse.ArgumentParser(description='Interface for streaming data using FinnHub API.')
    
    # Add class arguments
    parser.add_argument('-p', action='store',dest='plan',help='plan type: (f)ree/(s)tandard/(p)rofessional/(u)ltimate')
    parser.add_argument('-key', action='store',dest='api_key',help='user generated api key')
    parser.add_argument('-s', action='store',dest='start',help='start date: DD/MM/YYYY')
    parser.add_argument('-x', action='store',dest='exchange',help='enter "-exchanges" to view options')
    parser.add_argument('-f', action='store',dest='finish',help='final date: DD/MM/YYYY')
    parser.add_argument('-tzn', action='store',dest='timezone',help='timezone')
    
    # Add execution arguments
    parser.add_argument('-exchanges', action='store_true',dest='exchanges',help='exchange options')
    parser.add_argument('-candles', action='store_true',dest='candles',help='candle price data')
    parser.add_argument('-financials', action='store_true',dest='financials',help='financial statement data')
    
    
    # Parse Arguments
    args = parser.parse_args()