# Statement for enabling the development environment
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = "postgresql://catalog:Topher45%@localhost/catalog"
DATABASE_CONNECT_OPTIONS = {}

# Application threads. Sticking with standard 2
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secretTopherPotato1982"

# Secret key for signing cookies
SECRET_KEY = "secret"

# imgur api
IMGUR_SECRET_KEY = 'e09c306faee4cc6527eb9f03676a4860df612e44'
IMGUR_CLIENT_ID = '95123b1565c2a83'
