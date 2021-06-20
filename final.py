class City:
    def __init__(self, *args, **kwargs):
        self.__id = kwargs.get('id')
        self.__name = kwargs.get('name')
    
    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name

    @classmethod
    def field_names(cls) -> list:
        city = City({})
        fields = city.__dict__.keys()
        del(city)
        return fields


class Road:
    def __init__(self, *args, **kwargs):
        self.__id = kwargs.get('id')
        self.__name = kwargs.get('name')
        self.__from = kwargs.get('from')
        self.__to = kwargs.get('to')
        self.__through = kwargs.get('through')
        self.__speed_limit = kwargs.get('speed_limit')
        self.__length = kwargs.get('length')
        self.__bi_directional = kwargs.get('bi_directional')
    
    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name

    @classmethod
    def field_names(cls) -> list:
        road = Road({})
        fields = road.__dict__.keys()
        del(road)
        return fields

    def is_bi_directional(self):
        return self.__bi_directional

class Agency:
    def __init__(self):
        self.__roads = []
        self.__cities = []
    
    def add_road(self, road: Road):
        self.__roads.append(road)
    
    def add_city(self, city: City):
        self.__cities.append(city)

class UserInterface:
    def __init__(self):
        self.agency = Agency()
    
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

    def handle_help_cmd(self):
        self.show_help()
    
    def handle_add_cmd(self):
        self.show_add_delete_menu()
        select = int(self.get_input())
        if select == 1:
            self.handle_add_city()
        elif select == 2:
            self.handle_add_road()

    def handle_delete_cmd(self):
        self.show_add_delete_menu()
        select = int(self.get_input())
        if select == 1:
            self.handle_delete_city()
        elif select == 2:
            self.handle_delete_road()

    def handle_path_cmd(self):
        pass
    
    def exit(self):
        pass

    def handle_add_city(self):
        kwargs = {}
        for field in City.field_names():
            if '_City__' in field:
                field = field[7:]
            print(f"{field}=?", end='')
            kwargs[field] = self.get_input()
        self.agency.add_city(City(kwargs))
