# mp10 ttsApp
# TTS (Text To Speech)
# pip install gTTS
# pip install playsound

from gtts import *
from playsound import playsound

text = '안녕하세요, TTS입니다.'

tts = gTTS(text=text, lang='ko', slow=False)
tts.save('./Part1/studyPython/output/hi.mp3')
print('생성 완료!')

playsound('./Part1/studyPython/output/hi.mp3')
print('음성출력 완료!')