class User:
    def __init__(self, uid):
        self.id = uid

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    @staticmethod
    def get(user_id):
        return User(user_id)
