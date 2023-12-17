from pathlib import Path
from openai import OpenAI
import os
import configparser
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import time

def generate_and_play_speech(text):
    # 设置环境变量以隐藏 pygame 欢迎信息
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

    # 读取 API 密钥
    # keyfile = open("key.txt", "r")
    # key = keyfile.readline()
    config = configparser.ConfigParser()
    relative_path = "../../config/config.ini"
    file_path = (Path(__file__).parent / relative_path).resolve()
    config.read(file_path)

    api_key = config['API_KEYS']['IMG_VIOSION_KEY']

    client = OpenAI(api_key=api_key)

    # 设置语音文件路径
    relative_path = "../../tmp/tmp.mp3"
    speech_file_path = (Path(__file__).parent / relative_path).resolve()
    print(speech_file_path)
    # 使用 OpenAI 创建语音
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",  # 可以选择 'onyx', 'nova' 等
        input=text
    )
    response.stream_to_file(speech_file_path)

    # 初始化播放器
    # pygame.mixer.init()

    # 延迟播放
    # time.sleep(2)  # 在播放前暂停

    # 播放音频
    pygame.mixer.music.load(speech_file_path)
    pygame.mixer.music.play()

    # 等待音乐播放完成
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # 确保音乐播放完全释放文件
    pygame.mixer.music.unload()

    return speech_file_path

# 驱动代码
if __name__ == "__main__":
    generate_and_play_speech("手機的媽媽是誰？手機螢幕")
