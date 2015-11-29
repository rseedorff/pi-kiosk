from flask import Flask, jsonify
import datetime
import time
import atexit
import RPi.GPIO as GPIO
app = Flask(__name__)

#####################################################
#   Initialise GPIO Board and setup all pins        #
#####################################################

# Green LED at Pin 7
LED_GREEN = 7
LED_RED = 11
PIR = 12

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(LED_GREEN, GPIO.OUT, initial=GPIO.LOW) ## Setup GPIO Pin LED_GREEN to OUT (3.3V)
GPIO.setup(LED_RED, GPIO.OUT, initial=GPIO.LOW) ## Setup GPIO Pin LED_RED to OUT (3.3V)
GPIO.setup(PIR, GPIO.IN) ## Setup GPIO Pin PIR to IN

# Initialise PIT states
STATE_PIR_CURRENT   = 0
STATE_PIR_LAST      = 0


#####################################################
#   REST Services                                   #
#####################################################


# This route will return a object in JSON format
@app.route('/api/pir')
def pir():
    try:
        print "%s: Sensor initialisieren ..." % datetime.datetime.now()

        # wait for PIR sensor
        while (GPIO.input(PIR) == GPIO.HIGH):
            STATE_PIR_CURRENT = 0

        print "%s: Fertig! Warte auf Beweung ..." % datetime.datetime.now()

        for i in range(0, 500):
            STATE_PIR_CURRENT = GPIO.input(PIR)
            print "Iteration " + str(i+1) + " current state:" + str(STATE_PIR_CURRENT)
            
            if (STATE_PIR_CURRENT == 1 and STATE_PIR_LAST == 0 ):
                print "%s: Bewegung erkannt!..." % datetime.datetime.now()
                STATE_PIR_LAST = 1
            elif (STATE_PIR_CURRENT == 0 and STATE_PIR_LAST == 1):
                print "%s: Bewegung beendet!..." % datetime.datetime.now()
                STATE_PIR_LAST = 0

            time.sleep(0.05) ## Wait for sleep seconds
        print " Done !"
    except KeyboardInterrupt:
        print "exit ..."
        GPIO.cleanup()
    
    return jsonify(result='Hello PIR !')

# This route will return a object in JSON format
@app.route('/')
def index():
    now = datetime.datetime.now()
    return jsonify(result='Hello World !')

# This route will turn on a LED_GREEN
@app.route('/api/led/on')
def led_on():
    try:
        if ( GPIO.input(LED_GREEN) == GPIO.LOW ):
            print "Turn LED_GREEN 'ON' at PIN: '"+ str(LED_GREEN) +"' !"
            GPIO.output(LED_GREEN, True) ## Turn on GPIO pin LED_GREEN, if it's off
        else:
            print "LED_GREEN is already 'ON' at PIN: '"+ str(LED_GREEN) +"' !"
    except:
        ## do some logging...
        GPIO.cleanup()
        print "Unexpected error: ", sys.exc_info()[0]
        
    return jsonify(led='on', pin=LED_GREEN)

# This route will turn on a LED_GREEN
@app.route('/api/led/off')
def led_off():
    try:
        if ( GPIO.input(LED_GREEN) == GPIO.HIGH ):
            print "Turn LED_GREEN 'OFF' at PIN: '"+ str(LED_GREEN) +"' !"
            GPIO.output(LED_GREEN, False) ## Turn off GPIO pin LED_GREEN, if it's on
        else:
            print "LED_GREEN is already 'OFF' at PIN: '"+ str(LED_GREEN) +"' !"
    except:
        ## do some logging...
        GPIO.cleanup()
        print "Unexpected error: ", sys.exc_info()[0]
        
    return jsonify(led='off', pin=LED_GREEN)

# This route will toogle some cool functions :)
@app.route('/api/led/toggle')
def toggle():
    result = 'Hello Toggle !'
    try:
        if ( GPIO.input(LED_GREEN) == GPIO.HIGH ):
            print "Toggle LED_GREEN ON!"
            GPIO.output(LED_GREEN, False) ## Turn off GPIO pin 7, if it's on
            result = 'Pin number 7 turned off (was on)'
        else:
            print "Toggle LED_GREEN OFF !"
            GPIO.output(LED_GREEN, True) ## Turn on GPIO pin 7, if it's off
            result = 'Pin number 7 turned on (was off)'
    except:
        ## do some logging...
        now = datetime.datetime.now()
        GPIO.cleanup()
        print "Exception!"
        
    return jsonify(result=result, led=GPIO.input(LED_GREEN), pin=LED_GREEN)

# This route will toogle some cool functions :)
@app.route('/api/led/blink')
@app.route('/api/led/blink/<float:speed>/')
@app.route('/api/led/blink/<float:speed>/<int:numTimes>')
def blink(speed=0.1, numTimes=50):
    
    try:
        for i in range(0, numTimes):
            print "Iteration " + str(i+1)
            GPIO.output(LED_GREEN, True) ## Turn on GPIO pin LED_GREEN
            time.sleep(speed) ## Wait for sleep seconds
            GPIO.output(LED_GREEN, False) ## Turn off GPIO pin LED_GREEN
            time.sleep(speed) ## Wait for sleep seconds
        print " Done "
    except:
        ## do some logging...
        now = datetime.datetime.now()
        GPIO.cleanup()
        print "Exception!"
        
    return jsonify(result="Blinking", led=GPIO.input(LED_GREEN), pin=LED_GREEN)

@app.errorhandler(Exception)
def catch_all_exception_handler(error):
    GPIO.cleanup() ## On error cleanup all GPIO Pins (hard reset)!
    return 'Error', 500

def cleanup():
    GPIO.cleanup() ## On shutdown clean all GPIO Pins!
    print "Cleanup due to shutdown this server!"


if __name__ == '__main__':
    app.debug = True
    app.run()

atexit.register(cleanup)
