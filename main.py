from models import SomeTable
from orm import BaseManager, OrmModel


if __name__ == '__main__':

    """if there are database settings, then these settings are applied, 
    if not, then by default sqlite3"""

    bd = BaseManager
    bd.set_connection()
    bd.migrations(bd)

    print(SomeTable.objects.select("some_field_1", "some_field_2", "some_field_3"))

    table_data = [
        {"some_field_1": "Iphone", "some_field_2": 2020, "some_field_3": 60000.50},
        {"some_field_1": "Xiaomi", "some_field_2": 2020, "some_field_3": 35000.50}
    ]
    SomeTable.objects.bulk_insert(rows=table_data)
    print(SomeTable.objects.select("pk", "some_field_1", "some_field_2", "some_field_3"))
    print(SomeTable.objects.filter("some_field_1", "some_field_2", "some_field_3", some_field_1='Iphone'))

    SomeTable.objects.update(
        pk=1,
        new_data={'some_field_2': 2019, 'some_field_3': '59555.55'}
    )
    print(SomeTable.objects.select("some_field_1", "some_field_2", "some_field_3"))

    SomeTable.objects.delete()
    print(SomeTable.objects.select("some_field_1", "some_field_2", "some_field_3"))
