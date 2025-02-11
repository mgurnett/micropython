from datetime import datetime
from sys import stderr

now = datetime.now()
message = f'{now:%M:%S} LOGGED'
#44:29 LOGGED

print (message, file=stderr)# - prints in RED
print('Hello world', file=stderr)

with open ('logs.txt', 'a') as file:
    print (message, file=file)

#This will append ('a') to a log file

num: float = 5087654.34
print (f'{num: ,.2%}')
# 508,765,434.00%

