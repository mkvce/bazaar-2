class City:
    def __init__(self, id: int, name: str):
        self.__id = id
        self.__name = name
    
    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name
    

class Road:
    def __init__(self, id: int, name: str, start: int, to: int, through: list, speed_limit: int, length: int, bi_directional: bool):
        self.__id = id
        self.__name = name
        self.start = start
        self.to = to
        self.through = through
        self.speed_limit = speed_limit
        self.length = length
        self.bi_directional = bi_directional
    
    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name

class Agency:
    def __init__(self):
        self.__roads = []
        self.__cities = []
    
    def add_road(self, road: Road):
        self.__roads.append(road)
    
    def add_city(self, city: City):
        self.__cities.append(city)
