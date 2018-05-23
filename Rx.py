from datetime import datetime
import matplotlib.pyplot as pyplot
import RPi.GPIO as GPIO
import re

RECEIVED_SIGNAL = [[], []]  #[[time of reading], [signal reading]]
MAX_DURATION = 5
RECEIVE_PIN = 23

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RECEIVE_PIN, GPIO.IN)
    cumulative_time = 0
    beginning_time = datetime.now()
    print '**Started recording**'
    while cumulative_time < MAX_DURATION:
        time_delta = datetime.now() - beginning_time
        RECEIVED_SIGNAL[0].append(time_delta)
        RECEIVED_SIGNAL[1].append(GPIO.input(RECEIVE_PIN))
        cumulative_time = time_delta.seconds
    print '**Ended recording**'
    print len(RECEIVED_SIGNAL[0]), 'samples recorded'
    GPIO.cleanup()

    print '**Processing results**'
    out = ''.join(map(str,RECEIVED_SIGNAL[1]))

    final = ''

    # agrego marcadores para procesar tokens
    # el comienzo de un codigo es el cambio de una serie de 0's a una serie de 1's
    start = '0000011111'

    # proceso de marcado para separar tokens
    out = "s"+out+"s"
    out = out.replace(start, 'ss')

    # substrings entre marcadores, candidados a ser codigos validos
    decoded = re.findall('s(.*?)s', out)

    # filtrado y decodificacion
    #  - vacios y ruido: hay menos del 10% de 1's (hay ruido y otras senales tomadas por el receptor RF)
    #  - 1: hay mas del 25% de 1's pero menos del 39% (media 32+-7)
    #  - 0: hay mas del 58% de 1's pero menos del 72% (media 65)
    #  - ? rangos intermedios no se puede decidir
    for code in decoded:
        if len(code) == 0:
            print "lenth 0 avoided"
        else:
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

    if final.count(a_on) > 2:
        print "a_on"
    elif final.count(a_off) > 2:
        print "a_off"


#    for i in range(len(RECEIVED_SIGNAL[0])):
##         print RECEIVED_SIGNAL[1][i]
#        RECEIVED_SIGNAL[0][i] = RECEIVED_SIGNAL[0][i].seconds + RECEIVED_SIGNAL[0][i].microseconds/1000000.0

#    print '**Plotting results**'
#    pyplot.plot(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1])
#    pyplot.axis([0, MAX_DURATION, -1, 2])
#    pyplot.show()

