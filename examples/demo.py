def secret_function(password):
    secret_key = "super_secret_key_12345"
    if password == secret_key:
        return "Access granted!"
    else:
        return "Access denied!"
