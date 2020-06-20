"""
Finnhub API request actions.
For full documentation see: https://finnhub.io/docs/api

S. Dunkelman

<LICENSE>
"""
import pytz
import requests
import pandas as pd
from datetime import datetime
from datetime import timezone

## Helper functions
def date_to_unix(date):
    dt = datetime.strptime(date, '%Y-%m-%d')
    utc_unix = int(dt.replace(tzinfo=timezone.utc).timestamp())
    return utc_unix

class Action(object):
    """
    api_key         = User generated key
    asset           = Stock/forex/crypto
    req_category    = Specific request type
    dates_flag      = Time series data
    exchange        = Exchange for converting date to unix timestamp.
                      Scrapes from API if not provided
    
    """
    def __init__(self,
                 api_key,
                 asset,
                 req_category,
                 dates_flag=False,
                 start_date=None,
                 end_date=None,
                 exchange=None,
                 base='https://finnhub.io/api/v1',
                 **kwargs):
        
        ## Base attributes for API
        self.api_key = api_key
        self.asset = asset
        self.req_category = req_category
        self.base = base
        self.dates_flag = dates_flag
        
        ## Additional inherited attributes for specific API call
        if kwargs is None:
            self.args = None
        else:
            self.args = kwargs
            
        ## Process ticker to uppercase
        if 'symbol' in self.args:
           self.args['symbol'] = self.args['symbol'].upper() 
        
        ## Set date parameters if flagged
        if self.dates_flag:
            ## Set timezone if exchange provided
#                if any(exchange == a for a in )
            if start_date and end_date:
                self.start_date = date_to_unix(start_date)
                self.end_date = date_to_unix(end_date)
            
            else:
                print("Need dates")
                raise ValueError
        
        ## Generate URL for API request
        try:
            self.url = self.generate_url()
        except:
            print("Incomplete arguments")
            raise ValueError
    
    def get_exchange(self):
        """
        Called within initialisation of any child class that uses UNIX date
        without providing exchange.
        Recursively calls generate URL then returns geography of exchange 
        """
        raise NotImplementedError("Must override exchange")
#    
    def generate_url(self):
        url  = self.base + '/' + self.asset + '/' + self.req_category +'?'
        
        ## Add action specific parameters
        if self.args:
            for variable,argument in self.args.items():
                url += variable + '=' + argument + '&'
        
        ## Add period dates if action is time series
        if self.dates_flag:
            url += 'from='+str(self.start_date)+'&to='+str(self.end_date)+'&'
        
        ## Add user generated API Key
        url += 'token='+self.api_key
        
        return url
    
    def execute(self):
        r = requests.get(self.url)
        result = pd.DataFrame.from_dict(r.json())
        return result
        
    
class Candles(Action):
    """
    Arguments (in order):
        symbol          = Security ticker
        resolution      = Frequency of data
        adjusted        = Adjusted price data
        start_date      = Start date of period
        end_date        = Last date of period
        
        Dates must be in YYYY=MM-DD format
        
    """
    def __init__(self,start_date,end_date,**kwargs):
        super().__init__(start_date=start_date,
                         end_date=end_date,
                         req_category='candles',
                         dates_flag=True,
                         **kwargs)

class Exchanges(Action):
    def __init__(self,**kwargs):
        super().__init__(req_category='exchange',
                         **kwargs)
        
    def get_exchange(self):
        ## Call on Exchanges class method get_geography
        ## Extract exchange and compare with geographies
        pass

class Profile(Action):
    def __init__(self,**kwargs):
        super().__init__(asset='stock',
                         req_category='profile',
                         dates_flag=True,
                         **kwargs)
        
    def get_exchange(self):
        ## Call on Exchanges class method get_geography
        ## Extract exchange and compare with geographies
        pass
    
#    
#class Candles(Action):
#    def __init(self,ticker,resolution,start_date,final_date,api_key):
#        Action.__init__(self,
#                        api_weight=25,
#                        asset='stock',
#                        req_category = 'candles',
#                        api_key = api_key,
#                        symbol = ticker,
#                        resolution = resolution)
#        '''
#        NEED TO INSERT 'FROM' INTRO ARGS -> PROTECTED KEYWORD
#        in Action base class use bool var = if action uses dates
#        store args as list
#        insert 'from' and 'to' into key list
#        iterate over key list to create new dict for args
#        '''
#        
#class Financials(Action):
#    def __init(self,ticker,start_date,final_date,record,api_key):
#        super().__init__(api_weight=25,
#                         base='candle?', 
#                         args={'symbol':ticker,
#                               'from':start_date,
#                               'to':final_date,
#                               'token':api_key})
#
#class Universe(Action):
#    def __init(self,exchange,api_key):
#        super().__init__(api_weight=25,
#                         asset='stock',
#                         req_category = 'exchange',
#                         api_key = api_key,
#                         args={})
#
#class Exchanges(Action):
#    def __init(self,asset,api_key,req_category):
#        Action.__init__(self,
#                        api_weight=1,
#                        asset=asset,
#                        req_category = 'exchange',
#                        api_key = api_key)