from gtts import gTTS
from subprocess import call     # MAC / LINUX
#from playsound import playsound # WINDOWS

def cria_audio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/bem_vindo.mp3')

    call(['afplay', 'audios/bem_vindo.mp3']) # OSX
    #call(['aplay', 'audios/hello.mp3'])  # LINUX
    #playsound('audios/hello.mp3')        # WINDOWS

cria_audio('Oi, eu sou a Rose.')


