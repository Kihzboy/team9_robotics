import requests
from rplidar import RPLidar
import time


def norm_angle(angle):
    angle %= 360
    if angle > 180:
        angle -= 360
    return angle

def move_forward_after_left():
    data["L"] = 0.18
    data["R"] = 0.13
    r = requests.post(url, json = data, timeout = 10)
    print("Status:", r.status_code)

def move_forward_after_right():
    data["L"] = 0.14
    data["R"] = 0.14
    r = requests.post(url, json = data, timeout = 10)
    print("Status:", r.status_code)

def turn_right():
    data["L"] = 0.08
    data["R"] = -0.08
    r = requests.post(url, json = data, timeout = 10)
    print("Status:", r.status_code)

def turn_left():
    data["L"] = -0.10
    data["R"] = 0.10
    r = requests.post(url, json = data, timeout = 10)
    print("Status:", r.status_code)

url = "http://10.222.197.188/js"
data = {"T": 1, "L": 0.0, "R": 0.0}

PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)

SAFE_DIST = 280

try:
    while True:
        scan = next(lidar.iter_scans())
        front = []
        right = []
    	
        for (_, angle, distance) in scan:
        
            angle = norm_angle(angle)
            
            if -15 <= angle <= 15:
                front.append(distance)
            elif 65 <= angle <= 115:
                right.append(distance)
        
        front_min = min(front) if front else 9999
        right_min = min(right) if right else 9999
        
        #----
        #for i in right:
            #print(f'{i}')
            
        #----
        
        lidar.stop()
        lidar.stop_motor()

        if right_min > SAFE_DIST:
            turn_right()
            time.sleep(3)
            move_forward_after_right()
            pass
        elif front_min > SAFE_DIST:
            move_forward_after_left()
            pass
        else:
            turn_left()
            pass

        time.sleep(3)
        lidar.start_motor()
            
except KeyboardInterrupt:
    pass
finally:
    lidar.stop()
    lidar.disconnect()
