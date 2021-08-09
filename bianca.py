from gtts import gTTS
import speech_recognition as sr
from subprocess import call         # MAC / LINUX
#from playsound import playsound    # WINDOWS
from requests import get
from bs4 import BeautifulSoup
import webbrowser as browser
from paho.mqtt import publish


##### CONFIGURAÇÕES #####
hotword = 'rose'

with open('rosie-python-assistente-fe02a8d39c53.json') as credenciais_google:
    credenciais_google = credenciais_google.read()

##### LISTAGEM DOS COMANDOS #####
'''
NOTÍCIAS                    Últimas notícias
TOCA <NOME DO ÁLBUM>        Reproduz o álbum no spotify player web
TEMPO AGORA                 Informações sobre temperatura e condição Climática
TEMPERATURA HOJE            Informações sobre mínima e máxima
LIGA/DESATIVA BUNKER        Controla iluminação do escritório
'''

##### FUNÇÕES PRINCIPAIS #####

def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o Comando: ")
            audio = microfone.listen(source)
            try:
                trigger = microfone.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-BR')
                trigger = trigger.lower()

                if hotword in trigger:
                    print('COMANDO: ', trigger)
                    responde('feedback')
                    executa_comandos(trigger)
                    break

            except sr.UnknownValueError:
                print("Google not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger

def responde(arquivo):
    call(['afplay', 'audios/' + arquivo + '.mp3'])

def cria_audio(mensagem):
    tts = gTTS(mensagem, lang='pt-br')
    tts.save('audios/mensagem.mp3')
    print('ROSIE: ', mensagem)
    call(['afplay', 'audios/mensagem.mp3'])     # OSX
    #call(['aplay', 'audios/mensagem.mp3'])     # LINUX
    #playsound('audios/mensagem.mp3')           # WINDOWS


def executa_comandos(trigger):

    if 'notícias' in trigger:
        ultimas_noticias()

    elif 'toca' in trigger and 'bee gees' in trigger:
        playlists('bee_gees')

    elif 'toca' in trigger and 'taylor davis' in trigger:
        playlists('taylor_davis')

    elif 'tempo agora' in trigger:
        previsao_tempo(tempo=True)

    elif 'temperatura hoje' in trigger:
        previsao_tempo(minmax=True)

    elif 'liga o bunker' in trigger:
        publica_mqtt('office/iluminacao/status', '1')

    elif 'desativa o bunker' in trigger:
        publica_mqtt('office/iluminacao/status', '0')

    else:
        mensagem = trigger.strip(hotword)
        cria_audio(mensagem)
        print('C. INVÁLIDO', mensagem)
        responde('comando_invalido')


##### FUNÇÕES COMANDOS #####

def ultimas_noticias():
    site = get('https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt')
    noticias = BeautifulSoup(site.text, 'html.parser')
    for item in noticias.findAll('item')[:2]:
        mensagem = item.title.text
        cria_audio(mensagem)

def playlists(album):
    if album == 'bee_gees':
        browser.open('https://open.spotify.com/track/33ALuUDfftTs2NEszyvJRm')
    elif album == 'taylor_davis':
        browser.open('https://open.spotify.com/track/3MKep4BfEwSlAHuFJrA9aV')

def previsao_tempo(tempo=False, minmax=False):
    site = get('http://api.openweathermap.org/data/2.5/weather?id=3451190&APPID=111111111111111&units=metric&lang=pt')
    clima = site.json()
    temperatura=clima['main']['temp']
    minima=clima['main']['temp_min']
    maxima=clima['main']['temp_max']
    descricao=clima['weather'][0]['description']
    if tempo:
        mensagem = f'No momento fazem {temperatura} graus com: {descricao}'
    elif minmax:
        mensagem = f'Mínima de {minima} e máxima de {maxima} graus'
    cria_audio(mensagem)


def publica_mqtt(topic, payload):
    publish.single(topic, payload=payload, qos=1, retain=True, hostname='m10.cloudmqtt.com', port=12892, client_id='rosie', auth={'username': 'xxxxxxxx', 'password': 'xxxxxxxx'})
    if payload == '1':
        mensagem = 'Bunker Ligado!'
    elif payload == '0':
        mensagem = 'Bunker Desligado!'
    cria_audio(mensagem)


def main():
    while True:
        monitora_audio()

main()




