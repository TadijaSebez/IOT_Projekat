import RPi.GPIO as GPIO
import time
import threading


def loop(dht):
    GPIO.setmode(GPIO.BCM)
    while True:
        code, humidity, temperature = dht.detect_values()
        dht.callback(humidity, temperature, code)
        time.sleep(0.5)
        if dht.should_stop():
            break

class DHT:

    def __init__(self, config, stop_event, callback):
        self.stop_event = stop_event
        self.callback = callback

        self.DHTLIB_OK = 0
        self.DHTLIB_ERROR_CHECKSUM = -1
        self.DHTLIB_ERROR_TIMEOUT = -2
        self.DHTLIB_INVALID_VALUE = -999
        
        self.DHTLIB_DHT11_WAKEUP = 0.020
        self.DHTLIB_TIMEOUT = 0.0001
        
        self.humidity = 0
        self.temperature = 0

        self.pin = config["pin"]
        self.bits = [0, 0, 0, 0, 0]

    def readSensor(self,pin,wakeupDelay):
        mask = 0x80
        idx = 0
        self.bits = [0,0,0,0,0]
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(wakeupDelay)
        GPIO.output(pin,GPIO.HIGH)
        #time.sleep(40*0.000001)
        GPIO.setup(pin,GPIO.IN)
        
        loopCnt = self.DHTLIB_TIMEOUT
        t = time.time()
        while(GPIO.input(pin) == GPIO.LOW):
            if((time.time() - t) > loopCnt):
                #print ("Echo LOW")
                return self.DHTLIB_ERROR_TIMEOUT
        t = time.time()
        while(GPIO.input(pin) == GPIO.HIGH):
            if((time.time() - t) > loopCnt):
                #print ("Echo HIGH")
                return self.DHTLIB_ERROR_TIMEOUT
        for i in range(0,40,1):
            t = time.time()
            while(GPIO.input(pin) == GPIO.LOW):
                if((time.time() - t) > loopCnt):
                    #print ("Data Low %d"%(i))
                    return self.DHTLIB_ERROR_TIMEOUT
            t = time.time()
            while(GPIO.input(pin) == GPIO.HIGH):
                if((time.time() - t) > loopCnt):
                    #print ("Data HIGH %d"%(i))
                    return self.DHTLIB_ERROR_TIMEOUT		
            if((time.time() - t) > 0.00005):	
                self.bits[idx] |= mask
            #print("t : %f"%(time.time()-t))
            mask >>= 1
            if(mask == 0):
                mask = 0x80
                idx += 1	
        #print (self.bits)
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,GPIO.HIGH)
        return self.DHTLIB_OK
    
    def readDHT11(self):
        rv = self.readSensor(self.pin,self.DHTLIB_DHT11_WAKEUP)
        if (rv is not self.DHTLIB_OK):
            self.humidity = self.DHTLIB_INVALID_VALUE
            self.temperature = self.DHTLIB_INVALID_VALUE
            return rv
        self.humidity = self.bits[0]
        self.temperature = self.bits[2] + self.bits[3]*0.1
        sumChk = ((self.bits[0] + self.bits[1] + self.bits[2] + self.bits[3]) & 0xFF)
        if(self.bits[4] is not sumChk):
            return self.DHTLIB_ERROR_CHECKSUM
        return self.DHTLIB_OK

    def detect_values(self):
        code = self.readDHT11()
        return code, self.humidity, self.temperature
    
    def should_stop(self):
        return self.stop_event.is_set()

    def start(self):
        t = threading.Thread(target=loop, args=(self,))
        t.start()
        return t
