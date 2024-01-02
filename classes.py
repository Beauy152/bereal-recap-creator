from dataclasses import dataclass

@dataclass
class Img:
    url:str
    width:int
    height:int

@dataclass
class Location:
    longitude:float
    latitude:float

@dataclass
class Memory:
    id:str
    thumbnail:Img
    primary:Img
    secondary:Img
    isLate:bool
    memoryDay:str
    location:Location | None

@dataclass
class Memories:
    data:list[Memory]
    next: None
    memoriesSynchronized: bool

@dataclass
class Response:
    status: int
    message: str
    data:Memories