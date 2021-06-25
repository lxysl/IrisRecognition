import cv2
from util.innerCircle import innerCircle
from util.outerCircle import outerCircle
from util.visualization import displayCircle

cap = cv2.VideoCapture(1)  # 笔记本外接虹膜摄像头为1，树莓派只有一个摄像头改成0
cv2.namedWindow("take photo", 0)
cv2.resizeWindow("frame", 640, 480)  # 640*480
i = 1
path = "./photo"
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
                # 再次按q确认拍摄并保存照片
                photo_path = path + "/" + str(i) + ".jpeg"
                i = i + 1
                cv2.imwrite(photo_path, frame)
                print("Path=", photo_path)
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
