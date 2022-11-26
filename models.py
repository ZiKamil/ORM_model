from orm import OrmModel
from fields import OrmInteger, OrmFloat, OrmText


class SomeTable(OrmModel):
    pk = OrmInteger(primary_key=True, autoincrement=True)
    some_field_1 = OrmText()
    some_field_2 = OrmInteger()
    some_field_3 = OrmFloat()
