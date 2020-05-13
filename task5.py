import requests
from urllib.parse import quote
import json
from datetime import datetime, date
import numpy as np # install numpy before use it
import matplotlib.pyplot as plt # also matplotlib
import math

group_id = "eminem24" # here u set group id

server = "https://api.vk.com/method/groups.getMembers?group_id="

token = "" # token

def get_cnt():
    global server, group_id, token
    url = server + str( group_id ) + "&offset=0&fields=bdate&v=5.27&access_token=" + token
    response = requests.get( url )
    cnt = json.loads( requests.get( url ).text )
    return cnt["response"]["count"]

def send_req( offset ):
    global server, group_id, token
    url = server + str( group_id ) + "&offset=" + str( offset ) + "&fields=bdate&v=5.27&access_token=" + token
    response = requests.get( url )
    return requests.get( url ).text

def age( born ):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def parse_month( born ):
    if( len( born ) > 5 ):
        born = datetime.strptime( born, "%d.%m.%Y" )
    else:
        born = datetime.strptime( born, "%d.%m" )
    
    return born.month

def rm_y_from_bday( born ):
    if( len( born ) > 5 ):
        born = datetime.strptime( born, "%d.%m.%Y" )
    else:
        born = datetime.strptime( born, "%d.%m" )
    return str( born.day ) + "." + str( born.month )

def has_duplicates( lst ):
    unq = set( lst )
    if len( unq ) != len( lst ):
        return True
    return False

def bday_paradox( n ):
    return 1000 - 1000 * math.factorial(365) / (math.factorial(365 - n) * 365**n)


req = 0 # request number
 
limit = 1000 # cuz u can get only 1000 users per request

map = [0] * 12 # chart, гистограмма

months = ( 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec' )

cnt = get_cnt() # > offset + limit

tmp_cnt = 0 # task 4
sub_group = [] # task 4, save members id
coincidence = 0
loop_len = 0

while True:
    
    offset = req * limit

    if( cnt < offset + limit ):
        break
    
    members = json.loads( send_req( offset ) )["response"]["items"]

    for member in members:
        try:
            bdate = member["bdate"]
        except:
            continue

        if( len( bdate ) > 0 ):
            #map[int( age( datetime.strptime( bdate, "%d.%m.%Y" ) ) )] += 1
            #print( member["id"] , bdate, parse_month( bdate )  ) 
            map[int( parse_month( bdate ) ) - 1] += 1 # save for chart

            
            sub_group.append( rm_y_from_bday( bdate ) )  
            
            tmp_cnt += 1
            if tmp_cnt == 50:
                if has_duplicates( sub_group ) == True:
                    coincidence += 1
                loop_len += 1
                sub_group = [] # clear var
                tmp_cnt = 0
                

    req += 1



print( "task 4:" )

for n in range(3, 50):
    print( 0.1 * bday_paradox( n ) )


print( "probability: " , coincidence / loop_len * 100 )




# chart
y_pos = np.arange( len( months ) )
plt.bar( y_pos, map )

plt.xticks( y_pos, months, color='orange' )
plt.yticks( color='orange' )

plt.show()

# /chart


