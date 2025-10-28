

# # Hashing utility function
# def hash_password(password: str) -> str:
#     """Hash a password for storing."""
#     import bcrypt

#     # Hash a password for the first time, with a randomly-generated salt
#     hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
#     return hashed.decode("utf-8")