import sys
from pathlib import Path
import depthai as dai
import requests
from PIL import Image

from datetime import datetime

token = "TOKEN"
chat_id = "CHAT_ID"
ENABLE = False
save_dict = {
    'image': None,
    'timestamp':  datetime.now()
}

def send_message(text):

   url = f"https://api.telegram.org/bot{token}/sendMessage"
   params = {
      "chat_id": chat_id,
      "text": text,
   }
   resp = requests.get(url, params=params)

   # Throw an exception if Telegram API fails
   resp.raise_for_status()


send_message("Bot initalized")


def send_photo(chat_id, file_opened):
   method = "sendPhoto"
   params = {'chat_id': chat_id}
   files = {'photo': file_opened}
   resp = requests.post(f"https://api.telegram.org/bot{token}/" + method, params, files=files)
   return resp

# Get argument first
nnPath = Path('models/mobilenet-ssd_openvino_2021.2_6shave.blob')
if len(sys.argv) > 1:
    nnPath = sys.argv[1]

if not Path(nnPath).exists():
    import sys
    raise FileNotFoundError(f'Required file/s not found, please run "{sys.executable} install_requirements.py"')

# MobilenetSSD label texts
labelMap = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
            "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
nn = pipeline.create(dai.node.MobileNetDetectionNetwork)
xoutRgb = pipeline.create(dai.node.XLinkOut)
nnOut = pipeline.create(dai.node.XLinkOut)

xoutRgb.setStreamName("rgb")
nnOut.setStreamName("nn")

# Properties
camRgb.setPreviewSize(300, 300)
camRgb.setInterleaved(False)
camRgb.setFps(40)
# Define a neural network that will make predictions based on the source frames
nn.setConfidenceThreshold(0.5)
nn.setBlobPath(nnPath)
nn.setNumInferenceThreads(2)
nn.input.setBlocking(False)

# Linking
nn.passthrough.link(xoutRgb.input)

camRgb.preview.link(nn.input)
nn.out.link(nnOut.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queues will be used to get the rgb frames and nn data from the outputs defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    qDet = device.getOutputQueue(name="nn", maxSize=4, blocking=False)

    while True:
        inRgb = qRgb.get()
        inDet = qDet.get()

        if inDet is not None:
            for detection in inDet.detections:
                if detection.label == 15:
                    now = datetime.now()  # Now
                    duration_in_minutes = abs(now - save_dict['timestamp']).total_seconds() / 60.0
                    if duration_in_minutes > 1 and inRgb != None:
                        # print("dif")

                        image = Image.fromarray(inRgb.getCvFrame(), 'RGB')
                        image.save('temp.png', 'PNG')

                        save_dict['timestamp'] = now

                        send_photo(chat_id, open("temp.png", 'rb'))
                    # print(detection.label)
