from datetime import datetime
import matplotlib.pyplot as pyplot
import RPi.GPIO as GPIO
import re
import sys

RECEIVED_SIGNAL = []
RECEIVE_PIN = 23
STORED_EXCEPTION = None # Terminate on CTRL,C
MAX_BUFFER = 80000
START_PATTERN = "000111"

def get_command(out):

    final = ''

    # proceso de marcado para separar tokens
    out = "s"+out+"s"
    out = out.replace(START_PATTERN, 'ss')

    # substrings entre marcadores, candidados a ser codigos validos
    decoded = re.findall('s(.*?)s', out)

    #print len(decoded)

    # filtrado y decodificacion
    #  - vacios y ruido: hay menos del 10% de 1's (hay ruido y otras senales tomadas por el receptor$
    #  - 1: hay mas del 25% de 1's pero menos del 39% (media 32+-7)
    #  - 0: hay mas del 58% de 1's pero menos del 72% (media 65)
    #  - ? rangos intermedios no se puede decidir
    for code in decoded:
        if len(code) > 0:
            ones = code.count('1')
            rate = float(ones) / float(len(code))
            if 0.25 < rate < 0.39:
                final += '1'
            elif 0.58 < rate < 72:
                final += '0'

    a_on = '1111111111111010101011101'
    a_off = '1111111111111010101010111'
    b_on = '1111111111101110101011101'
    b_off = '1111111111101110101010111'
    c_on = '1111111111101011101011101'
    c_off = '1111111111101011101010111'
    d_on = '1111111111101010111011101'
    d_off = '1111111111101010111010111'

    if final.count(a_on) > 0:
        print "a_on"
    if final.count(a_off) > 0:
        print "a_off"
    if final.count(b_on) > 0:
        print "b_on"

    del decoded
    return
# /get_command()


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RECEIVE_PIN, GPIO.IN)

    print '**Started recording**'
    i = 0
    while True:
        try:
            RECEIVED_SIGNAL.insert(i, GPIO.input(RECEIVE_PIN))
            i += 1
            if i > MAX_BUFFER:
                # process current buff
                #print '**Processing results**'
                out = ''.join(map(str, RECEIVED_SIGNAL))
                get_command(out)
                del out
                del RECEIVED_SIGNAL[:]
                i = 0 # back to fill the buffer again
            if STORED_EXCEPTION:
                break
        except KeyboardInterrupt:
            STORED_EXCEPTION = sys.exc_info()
    

    print "Cleanup" 
    GPIO.cleanup()

    if STORED_EXCEPTION:
        raise STORED_EXCEPTION[0], STORED_EXCEPTION[1], STORED_EXCEPTION[2]

    sys.exit()

