class User:
    def __init__(self, user_id, first_name, last_name, gender, membership, status, remarks):
        self.__user_id = user_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__membership = membership
        self.__status = status
        self.__remarks = remarks

    def get_user_id(self): return self.__user_id
    def get_first_name(self): return self.__first_name
    def get_last_name(self): return self.__last_name
    def get_gender(self): return self.__gender
    def get_membership(self): return self.__membership
    def get_status(self): return self.__status
    def get_remarks(self): return self.__remarks

    @classmethod
    def from_database_row(cls, row):
        return cls(
            user_id=row[0],
            first_name=row[1],
            last_name=row[2],
            gender=row[3],
            membership=row[4],
            status=row[5],
            remarks=row[6]
        )
