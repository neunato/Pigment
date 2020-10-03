from mss import mss
from sys import argv

with mss() as sct:
   sct.shot(output=argv[1])
