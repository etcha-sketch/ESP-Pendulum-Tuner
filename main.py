# MicroPython ESP Pendulum Tuner
# Author: Etcha-Sketch
# https://github.com/etcha-sketch

# Import required libraries
from machine import Pin
import time

# Create custom classes since micropython time does not support the performance timer.
class TimerError(Exception):
  """Exception used to report errors in Timer class"""

class Timer:
  def __init__(self):
    self._start_time = None

  def start(self):
    """Start a new timer"""
    if self._start_time is not None:
      raise TimerError(f"Timer is alread running. Use .stop() to stop it or .restart() to restart it")
    self._start_time = time.ticks_ms()

  def stop(self):
    """Stop the running timer, and return the elapsed time"""
    if self._start_time is None:
      raise TimerError(f"Timer is not running. Use .start() to start it")
    elapsed_time = (time.ticks_diff(time.ticks_ms(), self._start_time))/1000
    self._start_time = None
    return elapsed_time
    
  def restart(self):
    """Restart a running timer to zero"""
    if self._start_time is None:
      raise TimerError(f"Timer is not running. Use .start() to start it")
    self._start_time = None
    self._start_time = time.ticks_ms()
    
  def value(self):
    """Return current timer value in seconds"""
    if self._start_time is None:
      raise TimerError(f"Timer is not running. Use .start() to start it")
    elapsed_time = (time.ticks_diff(time.ticks_ms(), self._start_time))/1000
    return elapsed_time

# Define variables
led = Pin(2, Pin.OUT)
sensor = Pin(12, Pin.IN, Pin.PULL_UP)
samples = 0
maxSamples = 5
allSamples = 0
noSwingDetected = 0

mainTimer = Timer()

print("Sleeping for 3 seconds, start the pendulum.")
time.sleep(3)
print("Starting counter")
mainTimer.start()

# Start collecting 60s samples until the max samples have been reached.
while samples < maxSamples:
  samples+=1
  ctMinute = 0
  mainTimer.restart()
  print("STARTING SAMPLE", samples)
  
  # Run the collection for 60 seconds.
  while mainTimer.value() < 60:
    first = sensor.value()
    # Sleep for a short period to compare sensor state.
    time.sleep(0.01)
    second = sensor.value()
    if first and not second:
      ctMinute+=1
  print("  Pendulum pass count: ", ctMinute )
  if ctMinute == 0:
    print("  Pendulum swing not detected!")
    noSwingDetected = 1
  else:
    # Divide swing count by 120 since a pendulum at the bottom of the swing would pass over the sensor twice a second.
    swingTime = (120/ctMinute)
    print("  Pendulum timing: ", swingTime, "s" )
    allSamples += swingTime
    
print("")
if noSwingDetected == 0:
  print("Average over", samples, "samples:", (allSamples/samples), "s")
else:
  print("Some smaples did not have swings detected, no summary available.")


