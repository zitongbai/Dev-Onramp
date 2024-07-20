import cv2

from ultralytics import YOLO

# 加载预训练好的yolo模型
model = YOLO("yolov8n.pt")

video = cv2.VideoCapture(0)
fps = video.get(cv2.CAP_PROP_FPS)
print(fps)
size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print(size)
while True:
    ret, frame = video.read()
    
    results = model(frame, stream=True)
    for i, result in enumerate(results):
        img = result.plot()

    cv2.imshow("result", img)
    # 如果检测到按键，就退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()