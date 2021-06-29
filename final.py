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
        self.__country = kwargs.get('country')
    
    @property
    def id(self):
        return int(self.__id)
    
    @property
    def name(self):
        return self.__name

    @property
    def country_id(self):
        return int(self.__country)

    @classmethod
    def field_names(cls) -> list:
        city = City()
        fields = city.__dict__.keys()
        return fields

    def export(self):
        dump = ''
        for value in self.__dict__.values():
            dump += value + '\n'
        return dump

    def __eq__(self, value):
        return self.id == value.id


class Country:
    def __init__(self, **kwargs):
        self.__id = kwargs.get('id')
        self.__name = kwargs.get('name')
    
    @property
    def id(self):
        return int(self.__id)

    @property
    def name(self):
        return self.__name

    def __eq__(self, value):
        return self.id == value.id

    @classmethod
    def field_names(cls) -> list:
        country = Country()
        fields = country.__dict__.keys()
        return fields

    def export(self):
        dump = ''
        for value in self.__dict__.values():
            dump += value + '\n'
        return dump



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
            self.__through = [int(x) for x in kwargs.get('through')[1:-1].replace(' ','').split(',')]
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

    def export(self):
        dump = ''
        for value in self.__dict__.values():
            dump += value + '\n'
        return dump

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
        self.__cities = []
        self.__roads = []
        self.__countries = []
    
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

    def add_country(self, country: Country):
        for i in range(len(self.__countries)):
            if self.__countries[i] == country:
                self.__countries[i] = country
                break
        else:
            self.__countries.append(country)

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

    def delete_country(self, id: int):
        for i in range(len(self.__countries)):
            if self.__countries[i].id == id:
                self.__countries.pop(i)
                break
        else:
            raise ModelNotFoundError('Country', id)

    def get_city_name(self, id: int) -> str:
        for city in self.__cities:
            if city.id == id:
                return city.name
        raise ModelNotFoundError('City', id)

    def get_country_name(self, id: int):
        for country in self.__countries:
            if country.id == id:
                return country.name
        raise ModelNotFoundError('Country', id)

    def get_country_of_city_name(self, id: int):
        for city in self.__cities:
            if city.id == id:
                return self.get_country_name(city.country_id)
        raise ModelNotFoundError('City', id)


    def get_pathes(self, src: int, dst: int) -> list:
        pathes = []
        for road in self.__roads:
            path = road.get_path(src, dst)
            if path:
                pathes.append(path)
        return pathes

    def export(self):
        ADD = '2'
        CITY = '1'
        ROAD = '2'
        COUNTRY = '3'
        ADD_ANOTHER = '1'
        DONE = '2'
        with open('dump.txt', 'w') as dump:
            if self.__cities:
                dump.write(ADD)
                dump.write('\n')
                dump.write(CITY)
                dump.write('\n')
                for city in self.__cities[:-1]:
                    dump.write(city.export())
                    dump.write(ADD_ANOTHER)
                dump.write(self.__cities[-1].export())
                dump.write(DONE)
            if self.__roads:
                dump.write(ADD)
                dump.write('\n')
                dump.write(ROAD)
                dump.write('\n')
                for road in self.__roads[:-1]:
                    dump.write(road.export())
                    dump.write(ADD_ANOTHER)
                dump.write(self.__roads[-1].export())
                dump.write(DONE)
            if self.__countries:
                dump.write(ADD)
                dump.write('\n')
                dump.write(ROAD)
                dump.write('\n')
                for country in self.__countries[:-1]:
                    dump.write(country.export())
                    dump.write(ADD_ANOTHER)
                dump.write(self.__countries[-1].export())
                dump.write(DONE)


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
        print("5. Export")
        print("6. Exit")

    def show_help(self):
        print("Select a number from shown menu and enter. For example 1 is for help.")
    
    def show_add_delete_menu(self):
        print("Select model:")
        print("1. City")
        print("2. Road")
        print("3. Country")

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
        elif select == '3':
            self.handle_add_model('Country')


    def handle_delete_cmd(self):
        self.show_add_delete_menu()
        select = int(self.get_input())
        if select == 1:
            self.handle_delete_model('City')
        elif select == 2:
            self.handle_delete_model('Road')
        elif select == 3:
            self.handle_delete_model('Country')

    def __get_model_fields(self, model: str) -> list:
        if model == 'City':
            return City.field_names()
        elif model == 'Road':
            return Road.field_names()
        elif model == 'Country':
            return Country.field_names()
        

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
        elif model == 'Country':
            self.agency.add_country(Country(**kwargs))
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
            elif model == 'Country':
                self.agency.delete_country(id)
        except ModelNotFoundError as err:
            print(f"{err.model_name} with id {err.id} not found!")
        else:
            print(f"{model}:{id} deleted!")
        self.show_main_menu()

    def handle_path_cmd(self):
        src_id, dst_id = [int(x) for x in self.get_input().split(':')]
        src_city_name = self.agency.get_city_name(src_id)
        src_country_name = self.agency.get_country_of_city_name(src_id)
        dst_city_name = self.agency.get_city_name(dst_id)
        dst_country_name = self.agency.get_country_of_city_name(dst_id)
        pathes = self.agency.get_pathes(src_id, dst_id)
        pathes.sort(key=lambda path: path.time.values())
        for path in pathes:
            road_name = path.road_name
            dd = int(path.time['days'])
            hh = int(path.time['hours'])
            mm = int(path.time['minutes'])
            print(f"{src_country_name}-{src_city_name}:{dst_country_name}-{dst_city_name} via Road {road_name}: Takes {dd:02d}:{hh:02d}:{mm:02d}")
        self.show_main_menu()

    def handle_export_cmd(self):
        self.agency.export()
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
            self.handle_export_cmd()
        elif select == '6':
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
