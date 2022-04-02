from scanner import Scanner
import time

scn = Scanner()
scn.setup()
for i in range(1):
    scn.slide_reverse()
    time.sleep(1)
