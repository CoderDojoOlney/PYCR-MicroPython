# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal
# setup UART on USB

import micropython
micropython.alloc_emergency_exception_buf(100)

from machine import UART
import os
uart = UART(0, baudrate=115200)
os.dupterm(uart)
print ('UART initialised')
#uart.irq(trigger=UART.RX_ANY, wake=machine.IDLE)
	
from machine import Pin
from machine import Timer

led_out = Pin('GP16', mode=Pin.OUT)
tim = Timer(1, mode=Timer.PERIODIC)
tim_a = tim.channel(Timer.A, freq=5)
# The slowest frequency the timer can run at is 5Hz
# so we divide the frequency down to toggle the LED
# BUT the callback function doesn't appear to have been developed
# Worth trying again as it is now included in the documentation
	
tim_a.irq(handler=lambda t:led_out.toggle(), trigger=Timer.TIMEOUT)	# Toggle LED on Timer interrupt

#btn_in = Pin('GP17', mode=Pin.IN, pull=Pin.PULL_UP)


# Connect to my WiFi
import machine
from network import WLAN
wlan = WLAN() 					# get current object, without changing the mode

# Settings for TP-LINK home network
KEY = ''
IP = '192.168.1.253'			# WiPy Fixed IP address
GATEWAY = '192.168.1.1'			# IP address of gateway
DNS = '192.168.1.1'				# IP address of DNS
NETMASK = '255.255.255.0'		# Netmask for this subnet

if machine.reset_cause() != machine.SOFT_RESET:
	print('Switching to Wifi Device Mode')
	wlan.init(WLAN.STA)
	wlan.ifconfig(config=(IP, NETMASK, GATEWAY, DNS))
	
if not wlan.isconnected():
	print('Attempting to connect to WiFi', end=' ')
	nets = wlan.scan()
	for net in nets:
		if net.ssid == 'Robotmad':
			KEY = 'mou3se43'
			break
		elif net.ssid == 'CoderDojo':
			KEY = 'coderdojo'
			break
	if KEY != '':
		print(net.ssid, end=" ")
		wlan.connect(net.ssid, auth=(net.sec, KEY), timeout=10000)
	if wlan.isconnected():
		print('Connected')
		tim_a.freq(10)
		wlan.irq(trigger=WLAN.ANY_EVENT, wake=machine.SLEEP)
	else :
		wlan.init(WLAN.AP, ssid='wipy-wlan', auth=(WLAN.WPA2, 'www.wipy.io'), channel=5, antenna=WLAN.INT_ANT)
		print('Failed - setting up as AP wipy-wlan')	
		tim.deinit()					# Cancel timer that was flashing the LED
		led_out(True)					# True = LED Off

#print(wlan.ifconfig())
print('Done.')
#machine.sleep()
	


