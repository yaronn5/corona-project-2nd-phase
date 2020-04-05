
import os
from random_word import RandomWords
r = RandomWords()

os.system("git add *")
os.system("git commit -m " + "aaa") #r.get_random_word())
os.system("git push")
os.system("git push heroku master")

