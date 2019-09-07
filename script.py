import requests, tweepy, time, config, datetime, csv
import matplotlib.pyplot as plt
import pandas as pd



#   twitter api
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

def save_data(disp, bloq):
    timestamp = datetime.datetime.now()
    data = [timestamp, disp, bloq]

    with open('data.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
    csvFile.close()

    return True

def get_graph():
    d = pd.read_csv('data.csv')
    time = d['TIME']
    disp = d['DISPONIBLE']
    bloq = d['BLOQUEADA']
    plt.plot(time, disp)
    plt.plot(time, bloq)
    plt.xlabel('Tiempo')
    plt.ylabel('Bicicletas')
    plt.legend(["Bloqueadas", "Disponibles"])
    plt.xticks(time, ['5/9/2019'])
    plt.savefig('plot.png')

    return 'plot.png'

last_id = 1170111344563097600

while True:

    bloq, disp = get_data()
    #api.update_status(f"Disponibles: {disp} Bloquedas: {bloq}")
    save_data(disp, bloq)

    mentions = api.mentions_timeline(last_id, tweet_mode='extended')
    print(last_id)
    for mention in reversed(mentions):
        print(str(mention.id) + " -- " + mention.full_text)
        last_id = mention.id

        if 'grafico!' in mention.full_text.lower():
            print("mentioned in a tweet!")
            msg = "@" + mention.user.screen_name 
            api.update_with_media(get_graph(),msg, mention.id )
 
   #dev note 1170111344563097600

    time.sleep(600) #espera 10 minutos




    
   
 

