from classes import Memories,Memory
from consts import MEMORIES_URL

from datetime import datetime
from dataclass_wizard import fromdict
from json import loads,load
import requests

def str_to_date(s:str):
    return datetime.strptime(s,'%Y-%m-%d').date()

def path_to_date(s:str):
    stripped_str = s.split('/')[-1]
    stripped_str = stripped_str.split('.')[0]
    return datetime.strptime(stripped_str,'%Y-%m-%d').date()

def filter_memories(memories_feed:Memories,filter_year:int) -> list[Memory]:    
    return [memory for memory in memories_feed.data 
            if str_to_date(memory.memoryDay).year == filter_year]
    

def fetch_user_memories(base_url:str,user_token:str) -> Memories:
    res = requests.get(url=base_url+MEMORIES_URL,
                       headers={
                           'token':user_token
                       })
    
    if not res.status_code == 200:
        print("-----------")
        print(res)
        print(res.content)
        raise ConnectionError(f"Failed to fetch memories feed.")
    
    body = loads(res.content)

    memoriesFeed = fromdict(
        Memories,
        body.get('data'))
    
    return memoriesFeed

