import cv2
import time
import paho.mqtt.client as mqtt
from util.feature import generateFeatureDataset
from util.contrast import contrast
from util.innerCircle import innerCircle
from util.outerCircle import outerCircle
from util.visualization import displayCircle

# HOST = "120.55.55.230"
# PORT = 1883
# topic = "mqtt"

# client = mqtt.Client()
# client.connect(HOST, PORT, 60)

cap = cv2.VideoCapture(1)  # 笔记本外接虹膜摄像头为1，树莓派只有一个摄像头改成0
cv2.namedWindow("frame", 0)
cv2.resizeWindow("frame", 640, 480)  # 640*480


def fullname(name):
    fullName = ''
    if name == '1':
        fullName = "fullName of 1"
    elif name == '2':
        fullName = "fullName of 2"
    elif name == '3':
        fullName = "fullName of 3"
    elif name == '4':
        fullName = "fullName of 4"
    elif name == '5':
        fullName = "fullName of 5"
    return fullName


while 1:
    # 实时显示内外圆
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    try:
        inner = innerCircle(frame)
        outer_x, outer_y, outer_r = inner
        inner_x, inner_y, inner_r = outerCircle(frame, inner)
        frame_show = displayCircle(frame, outer_x, outer_y, outer_r, inner_x, inner_y, inner_r)
    except:
        frame_show = frame
    else:
        frame_show = frame_show
    cv2.imshow("frame", frame_show)
    keyboard_k = cv2.waitKey(1)
    if keyboard_k == ord('q'):
        # 按q拍摄
        while 1:
            keyboard_k = cv2.waitKey(1)
            if keyboard_k == ord('q'):
                # 再次按q确认拍摄并进行检测
                try:
                    name, side, scores = contrast(frame)
                    print(name, side, scores)
                    # ret = client.publish(topic, fullname(name) + side, 0)
                    # print(ret)
                    # print("send ", fullname(name), " to server!")
                    break
                except:
                    print("未检测到，请重新拍摄！")
                    break
            if keyboard_k == ord('r'):
                # 不满意按r重拍
                break
    if keyboard_k == ord('b'):
        # 按b退出
        print("break")
        break
cap.release()
cv2.destroyAllWindows()
