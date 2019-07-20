import logging
import socket
import sys
import time
import pigpio
import serial
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
frequency = 300
maxPwm = 255

class CarManager(metaclass=Singleton):
  
  def __init__(self, servo=4):
        self.response = None
        self.pi = pigpio.pi()
        self.servo = servo
        # self.bus = smbus.SMBus(1)
        self.address = 0x04

        self.pi.set_mode(R_IN1, pigpio.OUTPUT)
        self.pi.set_mode(R_IN2, pigpio.OUTPUT)
        self.pi.set_mode(L_IN1, pigpio.OUTPUT)
        self.pi.set_mode(L_IN2, pigpio.OUTPUT)

        self.pi.set_PWM_frequency(R_PWM,  self.frequency)
        self.pi.set_PWM_range(R_PWM,  self.maxPwm)
        self.pi.set_PWM_frequency(L_PWM, self.frequency)
        self.pi.set_PWM_range(L_PWM, self.maxPwm)


        self.set_PWM_dutycycle(R_PWM, 125)
        self.set_PWM_dutycycle(L_PWM, 125)
        self.pi.write(R_IN1, 1)
        self.pi.write(R_IN2, 1)
        self.pi.write(L_IN1, 1)
        self.pi.write(L_IN2, 1)
        time.sleep(10);

  def send_command(self, command):
      logger.info({'action': 'send_command', 'command': command})
      code = ''
      if command=='forward':
        code='f'
        pwm=1450
      elif command=='back':
        code='b'
        pwm =1450
      elif command=='right':
        code='r'
        pwm =500
      elif command=='left':
        code='l'
        pwm =2350
      elif command=='stop':
        code='s'
        pwm =1450


      self.pi.set_servo_pulsewidth(self.servo, pwm)
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
