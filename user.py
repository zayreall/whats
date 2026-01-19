class User:
    def __init__(self, user_id, name, email, password, role, status):
        self.__user_id = user_id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__role = role
        self.__status = status

    # Accessors
    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_role(self):
        return self.__role

    def get_status(self):
        return self.__status

    # Mutators
    def set_role(self, role):
        self.__role = role

    def set_status(self, status):
        self.__status = status
