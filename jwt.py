import os

user_01 = os.environ['AUTH_EXEC_PRODUCER']
user_02 = os.environ['AUTH_CASTING_DIRECTOR']
user_03 = os.environ['AUTH_CASTING_ASSISTANT']

casting_assistant_and_above = [user_01, user_02, user_03]
casting_director_and_above = [user_01, user_02]
exec_producer = [user_01]