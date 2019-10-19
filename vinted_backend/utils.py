from sqlalchemy import create_engine
from dateutil.parser import parse
import math

def create_connection(host:str, pw:str, db:str, user:str):
    """
    A method to create a connection using sqlalchemy
    """
    engine = create_engine(f"mysql+pymysql://{user}:{pw}@{host}/{db}")
    return(engine)

def parse_date(date_str):
    """
    A method to parse date strings
    """    
    try:
        return parse(date_str)
    except:
        return None   

def check_if_nan(var):
    """
    A method to parse strings from csv to database
    """        
    if not isinstance(var, str): 
        if math.isnan(var):
            var = None
    return var   

          