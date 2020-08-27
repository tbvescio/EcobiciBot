import time, datetime, csv, os
import requests, tweepy

#   TWITTER API
CONSUMER_KEY = os.environ['consumer_key']
CONSUMER_SECRET = os.environ['consumer_secret'] 
ACCESS_TOKEN = os.environ['access_token'] 
ACCESS_SECRET = os.environ['access_secret'] 
URL = os.environ['url'] 
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)    
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
API = tweepy.API(AUTH)

INTERVAL = 900

def get_data():
    response = requests.get(URL)
    response = response.json()

    bloq = 0
    disp = 0
    for x in range(0, len(response["data"]["stations"])): # va de 0 a la cantidad de entradas de 'stations'
        #x se usa como indice para saber cual parsear 
        disp = disp + response["data"]["stations"][x]["num_bikes_available"] 
        bloq = bloq + response["data"]["stations"][x]["num_bikes_disabled"]
    return bloq, disp

def main():
    while True:
        try:
            bloq, disp = get_data()
            print(bloq)
            print(disp)
            API.update_status(f"Disponibles: {disp} Bloquedas: {bloq}")
            time.sleep(INTERVAL) #waits 15 minutes
        except KeyboardInterrupt:
            exit()
        except:
            print("error")


if __name__ == "__main__":
    main()

    
   
 

