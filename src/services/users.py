users = set()

def add_user(user_id: int):
    users.add(user_id)

def get_users():
    return list(users)