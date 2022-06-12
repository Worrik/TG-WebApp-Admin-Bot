from environs import Env

env = Env()
env.read_env()

DATABASE_URL = env.str("DATABASE_URL")
TOKEN = env.str("TOKEN")
WEB_APP_URL = env.str("WEB_APP_URL")

