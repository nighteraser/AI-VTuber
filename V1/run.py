from nlp import *
from prompt_maker import *
from tts import *
import time

if __name__ == '__main__':
    finish = True
    time.sleep(2)
    while finish:
        text = input('> ')

        if text == 'bye':
            break
        else:
            finish = False

        ai_answer = get_ai_answer(text)
        print('\033[1;34m'+ ai_answer + '\033[0m')

        text2speech(ai_answer)

        finish = True
    
