def check(user: str | None):
    return False if user is None else user == "Pranoy"

print(check("Pranoy"))