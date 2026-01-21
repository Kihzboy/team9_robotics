import requests
from rplidar import RPLidar
import time


def norm_angle(angle):
    angle %= 360
    if angle > 180:
        angle -= 360
    return angle

def move_forward():
    data["L"] = 0.15
    data["R"] = 0.15
    r = requests.post(url, json = data, timeout = 10)
    print("Status:", r.status_code)

def turn_right():
    data["L"] = 0.10
    data["R"] = -0.10
    r = requests.post(url, json = data, timeout = 10)
    print("Status:", r.status_code)

def turn_left():
    data["L"] = -0.10
    data["R"] = 0.10
    r = requests.post(url, json = data, timeout = 10)
    print("Status:", r.status_code)

def emergency_stop():
    stop = {"T": 0}
    r = requests.post(url, json = stop, timeout = 10)
    print("Stop. Status:", r.status_code)

def decision_right():
    turn_right()
    time.sleep(2)
    move_forward()
    time.sleep(2)
    turn_left()
    time.sleep(2)
    move_forward()

def decision_left():
    turn_left()
    time.sleep(2)
    move_forward()
    time.sleep(2)
    turn_right()
    time.sleep(2)
    move_forward()

url = "http://10.222.197.188/js"
data = {"T": 1, "L": 0.0, "R": 0.0}

PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)

SAFE_DIST = 500

try:
    while True:
        scan = next(lidar.iter_scans())
        front = []
        right = []
        left = []
    	
        for (_, angle, distance) in scan:
        
            angle = norm_angle(angle)
            
            if -15 <= angle <= 15:
                front.append(distance)
            elif 60 <= angle <= 120:
                right.append(distance)
            elif -120 <= angle <= -60:
                left.append(distance)
        
        front_min = min(front) if front else 9999
        right_min = min(right) if right else 9999
        left_min = min(left) if left else 9999
        
        #----
        #for i in right:
            #print(f'{i}')
            
        #----
        
        lidar.stop()
        lidar.stop_motor()

        if front_min < SAFE_DIST:
            emergency_stop()
            time.sleep(2)
            if right_min >= left_min:
                decision_right()
            else:
                decision_left()
            pass

        time.sleep(2)
        lidar.start_motor()
        move_forward()
            
except KeyboardInterrupt:
    pass
finally:
    lidar.stop()
    lidar.disconnect()
