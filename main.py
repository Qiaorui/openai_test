import speech_recognition as sr
import subprocess

from pynput import keyboard


def say(text):
    subprocess.call(['say', text])

#say("开始测试")


def another_test():
    say('测试2')


def listen_for_transcript():
    r = sr.Recognizer()
    r.pause_threshold = 2
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("开始监听")
        audio = r.listen(source)
        print('完成监听')
        transcript = r.recognize_google(audio, language='zh-CN')
        print('GOOGLE版本')
        print(transcript)
        transcript = r.recognize_whisper(audio)
        print('whisper版本')
        print(transcript)


def on_press(key):
    if key == keyboard.Key.space:
        listen_for_transcript()
    if key == keyboard.Key.enter:
        another_test()
    if key == keyboard.Key.esc:
        exit()
    else:
        print(key)


if __name__ == '__main__':
    print('程序开始')
    with keyboard.Listener(
            on_press=on_press) as listener:
        listener.join()
    print('监听开始')