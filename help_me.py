import snowboydecoder
import sys
import signal
from mailing import emergency_mail

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

def detected():
    emergency_mail(寄件者email, 寄件者密碼, 收件者email, 內容)
    
if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=detected,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
