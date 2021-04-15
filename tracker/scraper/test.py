from datetime import datetime, timedelta
import re

strin = "NY Times, Sunday, April 11, 2021"
x = (list(filter(None, re.split('\s|,', strin))))


date = x[3] + " " + x[4] + " " + x[5]
print(date)

dt = datetime.strptime(date,"%B %d %Y")

print(dt)




timer = "(07:14)"

colons = timer.count(":")
timer = timer[1:(len(timer)-1)]

if(colons == 1):
    times = timer.split(":")
    delta = timedelta(hours = 0, minutes = int(times[0]), seconds = int(times[1]))
    print(delta)
elif(colons == 2):
    times = timer.split(":")
    delta = timedelta(hours = int(times[0]), minutes = int(times[1]), seconds = int(times[2]))
    print(delta)
    