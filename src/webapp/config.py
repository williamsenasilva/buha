import os

SECRET_KEY = os.environ.get('BUHA_SECRET_KEY') or ("BUHA" + str(os.urandom(32)))
PORT = int(os.environ.get('PORT', 5000))