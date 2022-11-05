from environs import Env

env = Env()
env.read_env()

IGNORE_FOLDER = ("Debug", 'vs', '.sln', '.vcx', 'cmake-build')
MIN_DIFF = 80
TOKEN = env.str('GITHUB_TOKEN')
