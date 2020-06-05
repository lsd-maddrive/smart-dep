import cv2
from PIL import Image
import WiderFacesTest as WFT
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import json


def TestModel(model, type="MT"):
    """Return predicted boxes """
    wft = WFT.WiderFaceTest()
    wft.download_files()
    pred = dict()
    for arg in wft.test_generate():
        img = cv2.imread(arg["path"]+arg["image_name"], 0)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        oder = [1, 0, 3, 2]
        if type == "MT":
            boxes, probs = model.detect(frame)
        else:
            pass

        if boxes is not None:
            pred[arg["image_name"]] = {"boxes":[x[oder].tolist() for x in boxes], "scores":probs.tolist()}
        else:
            pred[arg["image_name"]] = {"boxes":[], "scores":[]}

    with open('predictions.json', 'w') as f:
        json.dump(pred, f, indent=4)

def SingleImageExample(folder, img_name, model):
    # Load a single image and display
    img = cv2.imread('WiderFacesTest/images/'+ folder + img_name, 0)
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)

    # Visualize
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.imshow(frame)
    ax.axis('off')

    with open("WiderFacesTest/WiderFacesTest.json", "r") as f:
        data = json.load(f)

    boxes = data[img_name]["bboxes"]
    if boxes is not None:
        for box in boxes:
            width = box[3] - box[1]
            height = box[2] - box[0]
            rect = patches.Rectangle((box[1], box[0]), width, height, linewidth=1, edgecolor='g', facecolor='none')
            ax.add_patch(rect)



    # Detect face
    boxes, probs, landmarks = model.detect(frame, landmarks=True)
    if boxes is not None:
        for box, landmark in zip(boxes, landmarks):
            #ax.scatter(*np.meshgrid(box[[0, 2]], box[[1, 3]]))
            ax.scatter(landmark[:, 0], landmark[:, 1], c='r', s=4)
            width = box[2]-box[0]
            height = box[3]-box[1]
            rect = patches.Rectangle((box[0],box[1]),width,height,linewidth=1,edgecolor='r',facecolor='none')
            ax.add_patch(rect)
    fig.show()

def FacialCrops(folder, img_name, model):
    # Load a single image and display
    img = cv2.imread('WiderFacesTest/images/'+ folder + img_name, 0)
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)

    plt.figure(figsize=(12, 8))
    plt.imshow(frame)
    plt.axis('off')
    plt.show()

    # Detect face
    faces = model(frame)
    # Visualize
    if len(faces)>1:
        fig, axes = plt.subplots(1, len(faces))
        for face, ax in zip(faces, axes):
            ax.imshow(face.permute(1, 2, 0).int().numpy())
            ax.axis('off')
            fig.show()
    elif len(faces):
        plt.figure(figsize=(2,2))
        plt.imshow(faces[0].permute(1, 2, 0).int().numpy())
        plt.axis('off')
        plt.show()
