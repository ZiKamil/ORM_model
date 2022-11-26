import sqlite3


class BaseManager:
    connection = None

    @classmethod
    def set_connection(cls):
        connection = sqlite3.connect('sqlite_python.db')
        cls.connection = connection

    @classmethod
    def get_cursor(cls):
        return cls.connection.cursor()

    def __init__(self, model_class):
        self.model_class = model_class
        self.database = None

    def migrations(self):
        cursor = self.get_cursor()
        # TODO: вместо sqlite_master, брать значение из config файла
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        available_table = [i[-1] for i in cursor.fetchall()]
        classes = OrmModel.__subclasses__()
        for i in classes:
            if i.__name__ in available_table:
                return
            fields = ""
            for k, v in i.__dict__.items():
                if k == '__doc__' or k == '__module__':
                    continue
                fields += k + " "
                if v.__class__.__name__ == "OrmInteger":
                    fields += "INTEGER"
                if v.__class__.__name__ == "OrmText":
                    fields += "TEXT"
                if v.__class__.__name__ == "OrmFloat":
                    fields += "REAL"
                if v.get_primary_key():
                    fields += " PRIMARY KEY "
                    if v.__class__.__name__ == "OrmInteger" and v.get_autoincrement():
                        fields += "AUTOINCREMENT, "
                    else:
                        fields += ", "
                else:
                    fields += ", "
            fields = fields.strip()[:-1]
            query = f"CREATE TABLE {i.__name__} ({fields})"
            cursor.execute(query)

    def filter(self, *field_names, **filter_params):
        fields_format = ', '.join(field_names)
        if filter_params:
            filter_params = ', '.join([f"{field_name} = '{value}'" for field_name, value in filter_params.items()])
            query = f"SELECT {fields_format} FROM {self.model_class.__name__} WHERE {filter_params}"
        else:
            query = f"SELECT {fields_format} FROM {self.model_class.__name__}"

        cursor = self.get_cursor()
        cursor.execute(query)

        model_objects = list()
        result = cursor.fetchall()

        for row_values in result:
            keys, values = field_names, row_values
            row_data = dict(zip(keys, values))
            model_objects.append(self.model_class(**row_data))

        return model_objects

    def bulk_insert(self, rows: list):
        field_names = rows[0].keys()
        assert all(row.keys() == field_names for row in rows[1:])

        fields_format = ", ".join(field_names)

        params = ""
        for row in rows:
            row_values = [row[field_name] for field_name in field_names]
            params += f'{tuple(row_values)}, '
        params = params.strip()[:-1]

        query = f"INSERT INTO {self.model_class.__name__} ({fields_format}) " \
                f"VALUES {params}"

        cursor = self.get_cursor()
        cursor.execute(query)

    def update(self, new_data: dict, **filter_params):
        field_names = new_data.items()
        filter_params = ', '.join([f"{field_name} = '{value}'" for field_name, value in filter_params.items()])
        placeholder_format = ', '.join([f'{field_name} = {value}' for field_name, value in field_names])
        query = f"UPDATE {self.model_class.__name__} SET {placeholder_format} WHERE {filter_params}"

        cursor = self.get_cursor()
        cursor.execute(query)

    def delete(self, **filter_params):
        filter_params = ', '.join([f"{field_name} = '{value}'" for field_name, value in filter_params.items()])
        query = f"DELETE FROM {self.model_class.__name__} WHERE {filter_params}"

        cursor = self.get_cursor()
        cursor.execute(query)


class MetaModel(type):
    manager_class = BaseManager

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()


class OrmModel(metaclass=MetaModel):
    def __init__(self, **row_data):
        for field_name, value in row_data.items():
            setattr(self, field_name, value)

    def __repr__(self):
        attrs_format = ", ".join([f'{field}={value}' for field, value in self.__dict__.items()])
        return f"<{self.__class__.__name__}: ({attrs_format})>"
