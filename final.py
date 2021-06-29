class ModelNotFoundError(Exception):
    def __init__(self, model: str, id: int):
        super().__init__()
        self.model_name = model
        self.id = id


class EndProgramException(Exception):
    def __init__(self):
        super().__init__()


class City:
    def __init__(self, **kwargs):
        self.__id = kwargs.get('id')
        self.__name = kwargs.get('name')
    
    @property
    def id(self):
        return int(self.__id)
    
    @property
    def name(self):
        return self.__name

    @classmethod
    def field_names(cls) -> list:
        city = City()
        fields = city.__dict__.keys()
        return fields

    def __eq__(self, value):
        return self.id == value.id


class Path:
    def __init__(self, status: bool=False, road_name: str='', time: dict={}):
        self.__status = status
        self.road_name = road_name
        self.__time = time
    
    def __bool__(self):
        return self.__status

    @property
    def time(self) -> dict:
        return self.__time


class Road:
    def __init__(self, **kwargs):
        self.__id = kwargs.get('id')
        self.__name = kwargs.get('name')
        self.__from = kwargs.get('from')
        self.__to = kwargs.get('to')
        if kwargs.get('through'):
            self.__through = [int(x) for x in kwargs.get('through')[1:-1].split(',')]
        else:
            self.__through = None
        self.__speed_limit = kwargs.get('speed_limit')
        self.__length = kwargs.get('length')
        self.__bi_directional = kwargs.get('bi_directional')

    @property
    def id(self):
        return int(self.__id)
    
    @property
    def name(self):
        return self.__name

    @classmethod
    def field_names(cls) -> list:
        road = Road()
        fields = road.__dict__.keys()
        return fields

    def is_bi_directional(self):
        return self.__bi_directional

    def __eq__(self, value):
        return self.id == value.id

    def __calculate_time(self, src_index: int, dst_index: int) -> dict:
        hours = int(self.__length) / int(self.__speed_limit)
        minutes = hours * 60
        d = minutes // (24 * 60)
        minutes -= d * 24 * 60
        h = minutes // 60
        minutes -= 60 * h
        m = minutes
        return {'days': d, 'hours': h, 'minutes': m}

    def get_path(self, src: int, dst: int) -> Path:
        way = self.__through.copy()
        way.append(int(self.__to))
        dst_index = -1
        try:
            src_index = way.index(src)
        except ValueError:
            src_index = len(way)
        try:
            dst_index = way.index(dst)
        except ValueError:
            dst_index = -1
        if not self.is_bi_directional and src_index > dst_index:
            return Path()
        if src_index == len(way) or dst_index == -1:
            return Path()
        return Path(True, self.name, self.__calculate_time(src_index, dst_index))


class Agency:
    def __init__(self):
        self.__roads = []
        self.__cities = []
    
    def add_road(self, road: Road):
        for i in range(len(self.__roads)):
            if self.__roads[i] == road:
                self.__roads[i] = road
                break
        else:
            self.__roads.append(road)
    
    def add_city(self, city: City):
        for i in range(len(self.__cities)):
            if self.__cities[i] == city:
                self.__cities[i] = city
                break
        else:
            self.__cities.append(city)

    def delete_city(self, id: int):
        for i in range(len(self.__cities)):
            if self.__cities[i].id == id:
                self.__cities.pop(i)
                break
        else:
            raise ModelNotFoundError('City', id)
    
    def delete_road(self, id: int):
        for i in range(len(self.__roads)):
            if self.__roads[i].id == id:
                self.__roads.pop(i)
                break
        else:
            raise ModelNotFoundError('Road', id)

    def get_city_name(self, id: int) -> str:
        for city in self.__cities:
            if city.id == id:
                return city.name
        raise ModelNotFoundError('City', id)

    def get_pathes(self, src: int, dst: int) -> list:
        pathes = []
        for road in self.__roads:
            path = road.get_path(src, dst)
            if path:
                pathes.append(path)
        return pathes


class UserInterface:
    def __init__(self, agency: Agency):
        self.agency = agency
    
    def get_input(self):
        return input()
    
    def show_main_menu(self):
        print("Main Menu - Select an action:")
        print("1. Help")
        print("2. Add")
        print("3. Delete")
        print("4. Path")
        print("5. Exit")

    def show_help(self):
        print("Select a number from shown menu and enter. For example 1 is for help.")
    
    def show_add_delete_menu(self):
        print("Select model:")
        print("1. City")
        print("2. Road")

    def show_model_added_menu(self, model: str, id: int):
        print(f"{model} with id={id} added!")
        print("Select your next action")
        print(f"1. Add another {model}")
        print("2. Main Menu")

    def handle_help_cmd(self):
        self.show_help()
        self.show_main_menu()
    
    def handle_add_cmd(self):
        self.show_add_delete_menu()
        select = self.get_input()
        if select == '1':
            self.handle_add_model('City')
        elif select == '2':
            self.handle_add_model('Road')

    def handle_delete_cmd(self):
        self.show_add_delete_menu()
        select = int(self.get_input())
        if select == 1:
            self.handle_delete_model('City')
        elif select == 2:
            self.handle_delete_model('Road')

    def __get_model_fields(self, model: str) -> list:
        if model == 'City':
            return City.field_names()
        elif model == 'Road':
            return Road.field_names()

    def handle_add_model(self, model: str):
        kwargs = {}
        for field in self.__get_model_fields(model):
            if f'_{model}__' in field:
                field = field[len(f'_{model}__'):]
            print(f"{field}=?")
            kwargs[field] = self.get_input()
        if model == 'City':
            self.agency.add_city(City(**kwargs))
        elif model == 'Road':
            self.agency.add_road(Road(**kwargs))
        self.show_model_added_menu(model, kwargs['id'])
        select = int(self.get_input())
        if select == 1:
            self.handle_add_model(model)
        elif select == 2:
            self.show_main_menu()

    def handle_delete_model(self, model: str):
        id = int(self.get_input())
        try:
            if model == 'City':
                self.agency.delete_city(id)
            elif model == 'Road':
                self.agency.delete_road(id)
        except ModelNotFoundError as err:
            print(f"{err.model_name} with id {err.id} not found!")
        else:
            print(f"{model}:{id} deleted!")
        self.show_main_menu()

    def handle_path_cmd(self):
        src_id, dst_id = [int(x) for x in self.get_input().split(':')]
        src_city_name = self.agency.get_city_name(src_id)
        dst_city_name = self.agency.get_city_name(dst_id)
        pathes = self.agency.get_pathes(src_id, dst_id)
        pathes.sort(key=lambda path: path.time.values())
        for path in pathes:
            road_name = path.road_name
            dd = int(path.time['days'])
            hh = int(path.time['hours'])
            mm = int(path.time['minutes'])
            print(f"{src_city_name}:{dst_city_name} via Road {road_name}: Takes {dd:02d}:{hh:02d}:{mm:02d}")
        self.show_main_menu()

    def get_command_and_execute(self):
        select = self.get_input()
        if select == '1':
            self.handle_help_cmd()
        elif select == '2':
            self.handle_add_cmd()
        elif select == '3':
            self.handle_delete_cmd()
        elif select == '4':
            self.handle_path_cmd()
        elif select == '5':
            raise EndProgramException
        else:
            print("Invalid input. Please enter 1 for more info.")
            self.show_main_menu()

if __name__ == '__main__':
    agency = Agency()
    UI = UserInterface(agency)
    UI.show_main_menu()
    while True:
        try:
            UI.get_command_and_execute()
        except EndProgramException:
            break
