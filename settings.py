DEBUG = True
PORT = 8080

SECRET_KEY = "secret"
WTF_CSRF_ENABLED = True

PASSWORDS = {
    "draylin@gmail.com": "$pbkdf2-sha256$29000$9h5DiNGa8/6f8957T0kppQ$MWPbeXnAfIxIdEokfqt7JyhxSlQvvWw8DFd0m0jsy7Y",
}

USERS = ["draylin@gmail.com"]
USER_NAMES = {
    "draylin@gmail.com":"Aylin"
}
