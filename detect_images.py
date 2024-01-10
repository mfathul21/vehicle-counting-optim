import cv2
import torch 
import numpy as np
import streamlit as st
import argparse
from model import fasterRCNN_resnet18

# Define class labels
CLASSES = ['__background__', 'mobil', 'motor']
NUM_CLASSES = len(CLASSES)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Construct the argument parser.
parser = argparse.ArgumentParser()
parser.add_argument('--imgsz', default=512,
                    type=int, help='image resize shape'
                    )
args = parser.parse_args(args=[])


def count_classes(boxes, pred_classes):
    class_counts = {class_name: 0 for class_name in CLASSES[1:]}
    for class_name in pred_classes:
        if class_name in class_counts:
            class_counts[class_name] += 1
    return class_counts

def detect_img(model, image, threshold=0.30):
    progress_bar = st.sidebar.progress(0)
    progress_text = st.sidebar.empty()

    # Preprocess the image
    mask = cv2.imread("assets/mask.png")
    orig_image = image.copy()

    # Add mask to image
    mask = cv2.resize(mask, (image.shape[1], image.shape[0]))

    # Convert the image and mask to the same data type
    image = image.astype(np.float32)
    mask = mask.astype(np.float32)
    
    image = cv2.bitwise_and(image, mask)
    orig_height, orig_width = orig_image.shape[:2]  # Menyimpan ukuran asli gambar
    if args.imgsz is not None:
        image = cv2.resize(image, (args.imgsz, args.imgsz))
        #orig_image = cv2.resize(orig_image, (args.imgsz, args.imgsz))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
    image /= 255.0
    image_input = np.transpose(image, (2, 0, 1)).astype(np.float32)
    image_input = torch.tensor(image_input, dtype=torch.float)
    image_input = torch.unsqueeze(image_input, 0)
    
    # Predictions
    with torch.no_grad():
        outputs = model(image_input)
    
    # Post-process the outputs
    boxes = outputs[0]['boxes'].data.numpy()
    scores = outputs[0]['scores'].data.numpy()
    boxes = boxes[scores >= threshold].astype(np.int32)
    pred_classes = [CLASSES[i] for i in outputs[0]['labels'].cpu().numpy()]

    # Filter out boxes with the same coordinates
    filtered_boxes = []
    filtered_pred_classes = []
    filtered_scores = []
    seen_coordinates = set()
    for box, class_name, score in zip(boxes, pred_classes, scores):
        coordinates = tuple(box.tolist())
        if coordinates not in seen_coordinates:
            filtered_boxes.append(box)
            filtered_pred_classes.append(class_name)
            filtered_scores.append(score)
            seen_coordinates.add(coordinates)
    

    for i, (box, class_name, score) in enumerate(zip(filtered_boxes, filtered_pred_classes, filtered_scores)):
        xmin, ymin, xmax, ymax = box.tolist()

        # Mengubah koordinat box ke ukuran asli gambar
        xmin = int(xmin * orig_width / args.imgsz)
        ymin = int(ymin * orig_height / args.imgsz)
        xmax = int(xmax * orig_width / args.imgsz)
        ymax = int(ymax * orig_height / args.imgsz)

        class_id = CLASSES.index(class_name)
        color = COLORS[class_id]

        # Exclude boxes with very small height or width
        if ymax - ymin > 2 and xmax - xmin > 2:
            cv2.rectangle(orig_image,
                            (xmin, ymin),
                            (xmax, ymax),
                            color[::-1], 
                            2)
        
            # Create class score text
            class_score_text = f"{class_name} {score:.2f}"
            (text_width, text_height), _ = cv2.getTextSize(class_score_text, cv2.FONT_HERSHEY_SIMPLEX, 0.80, 1)
            
            # Draw background rectangle for text
            cv2.rectangle(orig_image,
                        (xmin, ymin - text_height),
                        (xmin + text_width - 45, ymin),
                        color[::-1],
                        -1)
            
            # Draw class score text
            cv2.putText(orig_image, 
                        class_score_text, 
                        (xmin, ymin - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, 
                        (0, 0, 0), 
                        1, 
                        lineType=cv2.LINE_AA)

        # Mengupdate nilai progress setiap iterasi
        progress = (i + 1) / len(filtered_boxes)
        progress_bar.progress(progress)
        progress_text.markdown(f'{int(progress * 100)}%')
        st.sidebar.markdown('')

    return orig_image, filtered_boxes, filtered_scores, filtered_pred_classes