import RPi.GPIO as GPIO
import time

buzzerPin = 11
SPEED = 1

TONES = {
    "c6": 1047,
    "b5": 998,
    "a5": 880,
    "g5": 784,
    "f5": 698,
    "e5": 659,
    'eb5': 622,
    "d5": 587,
    'c5': 523,
    'b4': 494,
    'a4': 440,
    'ab4': 415,
    'g4': 392,
    'gb4': 370,
    'f4': 349,
    'e4': 330,
    'd4': 294,
    'c4': 262
}

SONGS = {}
SONGS["boom"]= [
    ["c6", 16], ["c5", 16], ["c4", 16]
]

def setup():
    global p
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buzzerPin, GPIO.OUT)
    p = GPIO.PWM(buzzerPin, 440)

def PlayTone(p,tone):
    duration = (1./(tone[1]*0.25*SPEED))

    if tone[0] == "p":
        time.sleep(duration)
    else:
        frequency = TONES[tone[0]]
        p.ChangeFrequency(frequency)
        p.start(0.5)
        #time.sleep(duration)
        #p.stop()
def startSound(tone):
    frequency = TONES[tone[0]]
    p.ChangeFrequency(frequency)
    p.start(0.5)

def stop():
    p.stop()


def run():
    #p = GPIO.PWM(buzzerPin, 440)
    p.start(0.5)
    song = "boom"
    #print("Now Playing: ", song)
    for t in SONGS[song]:
        PlayTone(p,t)


def destroy():
    GPIO.output(buzzerPin, GPIO.HIGH)
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        run()
        GPIO.cleanup()
    except KeyboardInterrupt:
        destroy()
else:
    setup()
    