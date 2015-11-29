from flask import Flask, jsonify
import datetime
import time
import atexit
import RPi.GPIO as GPIO
app = Flask(__name__)

# LED at Pin 7
LED = 7

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW) ## Setup GPIO Pin 7 to out (3.3V)
        
# This route will return a object in JSON format
@app.route('/')
def index():
    now = datetime.datetime.now()
    return jsonify(result='Hello World !')

# This route will turn on a LED
@app.route('/api/led/on')
def led_on():
    try:
        if ( GPIO.input(LED) == GPIO.LOW ):
            print "Turn LED 'ON' at PIN: '"+ str(LED) +"' !"
            GPIO.output(LED, True) ## Turn on GPIO pin LED, if it's off
        else:
            print "LED is already 'ON' at PIN: '"+ str(LED) +"' !"
    except:
        ## do some logging...
        GPIO.cleanup()
        print "Unexpected error: ", sys.exc_info()[0]
        
    return jsonify(led='on', pin=LED)

# This route will turn on a LED
@app.route('/api/led/off')
def led_off():
    try:
        if ( GPIO.input(LED) == GPIO.HIGH ):
            print "Turn LED 'OFF' at PIN: '"+ str(LED) +"' !"
            GPIO.output(LED, False) ## Turn off GPIO pin LED, if it's on
        else:
            print "LED is already 'OFF' at PIN: '"+ str(LED) +"' !"
    except:
        ## do some logging...
        GPIO.cleanup()
        print "Unexpected error: ", sys.exc_info()[0]
        
    return jsonify(led='off', pin=LED)

# This route will toogle some cool functions :)
@app.route('/api/led/toggle')
def toggle():
    result = 'Hello Toggle !'
    try:
        if ( GPIO.input(LED) == GPIO.HIGH ):
            print "Toggle LED ON!"
            GPIO.output(LED, False) ## Turn off GPIO pin 7, if it's on
            result = 'Pin number 7 turned off (was on)'
        else:
            print "Toggle LED OFF !"
            GPIO.output(LED, True) ## Turn on GPIO pin 7, if it's off
            result = 'Pin number 7 turned on (was off)'
    except:
        ## do some logging...
        now = datetime.datetime.now()
        GPIO.cleanup()
        print "Exception!"
        
    return jsonify(result=result, led=GPIO.input(LED), pin=LED)

# This route will toogle some cool functions :)
@app.route('/api/led/blink')
@app.route('/api/led/blink/<float:speed>/')
@app.route('/api/led/blink/<float:speed>/<int:numTimes>')
def blink(speed=0.1, numTimes=50):
    
    try:
        for i in range(0, numTimes):
            print "Iteration " + str(i+1)
            GPIO.output(LED, True) ## Turn on GPIO pin LED
            time.sleep(speed) ## Wait for sleep seconds
            GPIO.output(LED, False) ## Turn off GPIO pin LED
            time.sleep(speed) ## Wait for sleep seconds
        print " Done "
    except:
        ## do some logging...
        now = datetime.datetime.now()
        GPIO.cleanup()
        print "Exception!"
        
    return jsonify(result="Blinking", led=GPIO.input(LED), pin=LED)

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
