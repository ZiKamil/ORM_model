class OrmInteger:
    def __init__(self, primary_key=False, autoincrement=False):
        self.primary_key = primary_key
        self.autoincrement = autoincrement

    def get_primary_key(self):
        return self.primary_key

    def get_autoincrement(self):
        return self.autoincrement


class OrmText:
    def __init__(self, primary_key=False):
        self.primary_key = primary_key

    def get_primary_key(self):
        return self.primary_key


class OrmFloat:
    def __init__(self, primary_key=False):
        self.primary_key = primary_key

    def get_primary_key(self):
        return self.primary_key
