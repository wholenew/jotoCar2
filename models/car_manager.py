import logging
#import socket
import sys
# import time
import pigpio
# import serial
# import smbus

from models.base import Singleton
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

R_PWM = 26
R_IN1 = 20
R_IN2 = 21
L_PWM = 17
L_IN1 = 27
L_IN2 = 22
frequency = 200
maxPwm = 255

class CarManager(metaclass=Singleton):
  
  def __init__(self, servo=4):
        # self.response = None
        self.pi = pigpio.pi()
        # self.servo = servo
        # self.bus = smbus.SMBus(1)
        # self.address = 0x04

        self.pi.set_mode(R_IN1, pigpio.OUTPUT)
        self.pi.set_mode(R_IN2, pigpio.OUTPUT)
        self.pi.set_mode(L_IN1, pigpio.OUTPUT)
        self.pi.set_mode(L_IN2, pigpio.OUTPUT)

        self.pi.set_PWM_frequency(R_PWM, frequency)
        self.pi.set_PWM_range(R_PWM,maxPwm)
        self.pi.set_PWM_frequency(L_PWM, frequency)
        self.pi.set_PWM_range(L_PWM, maxPwm)

  def send_command(self, command):
      # logger.info({'action': 'send_command', 'command': command})
      code = 's'
      r_pwm = 255
      l_pwm = 255
  
      if command=='forward':
        r_pwm = 255
        l_pwm = 255
        code='f'
     
      elif command=='back':
        r_pwm = 255
        l_pwm = 255        
        code='b'
      elif command=='right':
        r_pwm = 200
        l_pwm = 255
        code='r'
      elif command=='left':
        r_pwm = 255
        l_pwm = 200
        code='l'
      elif command=='stop':
        r_pwm = 0
        l_pwm = 0
        code='s'

      if code=='f':
          r_in1 = 1
          r_in2 = 0
          l_in1 = 1
          l_in2 = 0
          print('f') 
      elif code=='b':
          r_in1 = 0
          r_in2 = 1
          l_in1 = 0
          l_in2 = 1
          print('b')
      elif code=='r':
          r_in1 = 1
          r_in2 = 0
          l_in1 = 1
          l_in2 = 0
          print('r')
      elif code=='l':
          r_in1 = 1
          r_in2 = 0
          l_in1 = 1
          l_in2 = 0
          print('l')
      elif code=='s':
          r_in1 = 1
          r_in2 = 1
          l_in1 = 1
          l_in2 = 1
          #print('s')
      self.pi.set_PWM_dutycycle(R_PWM, r_pwm)
      self.pi.set_PWM_dutycycle(L_PWM, l_pwm)
      self.pi.write(R_IN1, r_in1)
      self.pi.write(R_IN2, r_in2)
      self.pi.write(L_IN1, l_in1)
      self.pi.write(L_IN2, l_in2)
      #  self.pi.set_servo_pulsewidth(self.servo, pwm)
      # self.bus.write_byte(self.address, ord(code))
      # time.sleep(3)

      # return self.response

  def forward(self):
      return self.send_command('forward')

  def back(self):
      return self.send_command('back')

  def left(self):
      return self.send_command('left')

  def right(self):
      return self.send_command('right')
  
  def stop(self):
      return self.send_command('stop')
