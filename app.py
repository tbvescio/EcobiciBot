import requests, tweepy, time, config

consumer_key = config.consumer_key
consumer_secret = config.consumer_secret 
access_token = config.access_token
access_secret = config.access_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)    
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def get_data():
    response = requests.get(config.url)
    response = response.json()

    bloq = 0
    disp = 0
    for x in range(0, len(response["data"]["stations"])): # va de 0 a la cantidad de entradas de 'stations'

        #x se usa como indice para saber cual parsear 
        disp = disp + response["data"]["stations"][x]["num_bikes_available"] 
        bloq = bloq + response["data"]["stations"][x]["num_bikes_disabled"]

    return bloq, disp


while True:

    bloq, disp = get_data()
    api.update_status(f"Disponibles: {disp} Bloquedas: {bloq}")
    time.sleep(120) #espera 2 minutos




    
   
 

