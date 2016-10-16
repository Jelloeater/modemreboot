import RPi.GPIO as GPIO
import time
import pyping
import logging
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)

logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
level=logging.DEBUG)

def modem_off():
    GPIO.output(17,GPIO.HIGH)

def modem_on():
    GPIO.output(17,GPIO.LOW)

def modem_reboot():
    modem_off()
    logging.info("Modem Rebooting")
    time.sleep(120)
    modem_on()
    logging.info("Modem Rebooted")

def check_wan():
    if pyping.ping("8.8.8.8").ret_code == 0:
        return True
    else:
        return False

def main():
    FAIL_COUNT = 0
    while True:
        logging.debug ("Fail Count = " + str(FAIL_COUNT))
        if check_wan() is False:
            FAIL_COUNT += 1
            logging.error ("Fail Count = " + str(FAIL_COUNT))
        else:
            FAIL_COUNT = 0
        time.sleep(30)
        if FAIL_COUNT > 10:
            modem_reboot()
            break

#RUN MAIN
modem_on()
while True:
    main()
