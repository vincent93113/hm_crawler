import pygame as pg
import speech_recognition as sr


def voice_to_text(duration=5):
    pg.mixer.music.load("./tmp/siri.mp3")
    pg.mixer.music.play(loops=0)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("請開始說話:")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=duration)
    try:
        Text = r.recognize_google(audio, language="zh-TW")
    except sr.UnknownValueError:
        Text = "無法翻譯"
    except sr.RequestError as e:
        Text = "無法翻譯{0}".format(e)
    return Text
