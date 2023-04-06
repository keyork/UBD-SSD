import os
import time
import sys
from cfg import THRESHOLD

module_path = os.path.abspath(os.path.join(".."))
if module_path not in sys.path:
    sys.path.append(module_path)

import torch
from torch.autograd import Variable
import numpy as np
import cv2

if torch.cuda.is_available():
    torch.set_default_tensor_type("torch.cuda.FloatTensor")

from ssd import build_ssd


net = build_ssd("test", 300, 5)

net.load_state_dict(
    torch.load("./weights_ours/ssd300_VOC_86000.pth", map_location=torch.device("cpu"))
)
device = torch.device("cpu")
net = net.to(device)

print("Load weights successfully!!!")

for i in range(1):
    while True:
        try:
            image = cv2.imread("../temp.jpg")
        except:
            continue
        start = time.time()
        try:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        except:
            continue
        x = cv2.resize(image, (300, 300)).astype(np.float32)
        x -= (104.0, 117.0, 123.0)
        x = x.astype(np.float32)
        x = x[:, :, ::-1].copy()

        x = torch.from_numpy(x).permute(2, 0, 1)
        with torch.no_grad():
            xx = x.unsqueeze(0)

            y = net(xx)
        end = time.time()

        print("fps = " + str(1 / (end - start)))

        from data import VOC_CLASSES as labels

        top_k = 10

        detections = y.data
        # scale each detection back up to the image
        scale = torch.Tensor(rgb_image.shape[1::-1]).repeat(2)

        is_empty = True
        for i in range(detections.size(1)):
            j = 0
            while detections[0, i, j, 0] >= THRESHOLD:
                score = detections[0, i, j, 0]
                label_name = labels[i - 1]
                display_txt = "%s: %.2f" % (label_name, score)
                pt = (detections[0, i, j, 1:] * scale).cpu().numpy()
                coords = (pt[0], pt[1]), pt[2] - pt[0] + 1, pt[3] - pt[1] + 1
                if label_name == "volleyball":
                    color = (146, 61, 146)
                if label_name == "football":
                    color = (0, 255, 25)
                if label_name == "basketball":
                    color = (253, 208, 0)
                if label_name == "balloon":
                    color = (215, 0, 64)
                cv2.rectangle(
                    rgb_image,
                    (int(pt[0]), int(pt[1])),
                    (int(pt[2]), int(pt[3])),
                    color,
                    4,
                )
                cv2.putText(
                    rgb_image,
                    display_txt,
                    (int(pt[0]), int(pt[1]) - 10),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.5,
                    color,
                    2,
                )

                j += 1
                f = open("../temp.txt", "w")
                if label_name:
                    if not label_name == "balloon":
                        f.write(label_name[0])
                        is_empty = False
                    else:
                        f.write("e")
                else:
                    f.write("e")
                f.close()
        if is_empty:
            f = open("../temp.txt", "w")
            f.write("e")
            f.close()
        # cv2.imshow("imshow", cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB))
        # cv2.waitKey(1)
        save_path = "./result.jpg"
        cv2.imwrite(save_path, cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB))
