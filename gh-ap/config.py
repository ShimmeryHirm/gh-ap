from environs import Env

env = Env()
env.read_env()

TOKEN = env.str('GITHUB_TOKEN')

IGNORE_FOLDER = ("Debug", 'vs', '.sln', '.vcx', 'cmake-build')
MIN_DIFF = 80
MAX_THREADS = 50
