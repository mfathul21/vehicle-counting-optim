import numpy as np
import streamlit as st
import skfuzzy as fz
import torch, argparse, cv2, os, io, time
from PIL import Image
from model import fasterRCNN_resnet18
from fuzzy_logic import optim_traffic
from detect_images import count_classes, detect_img

# Define class labels
CLASSES = ['__background__', 'mobil', 'motor']
NUM_CLASSES = len(CLASSES)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
logo = Image.open("assets/logo.png")

# Construct the argument parser.
parser = argparse.ArgumentParser()
parser.add_argument('--imgsz', default=512,
                    type=int, help='image resize shape'
                    )
args = parser.parse_args(args=[])

# Streamlit app
def main():
    st.set_page_config(
        page_title="Traffic Light Optimzation",
        page_icon= logo,
        layout="wide",
        initial_sidebar_state="expanded")
    
    st.markdown("""
    <style>
    .css-2ykyy6.egzxvld0
    {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🚗 Vehicle Counting System")
    st.sidebar.header('Object Detection')

    st.markdown('---')
    device = st.sidebar.radio("What is your device", ("cpu", "cuda"))
    iou_threshold = st.sidebar.slider("Input your threshold", min_value =0.0, max_value=1.0, value = 0.25,step=0.05)
    inference_mode = st.sidebar.selectbox("Inference Mode", ["📷 Image", "📹 Video"])

    if device == 'cuda':
        if torch.cuda.is_available():
            pass
        else:
            st.warning("CUDA is not available. Switching to CPU.")
            device = 'cpu'      # Replace device to cpu because cuda not available


    frame_hold = st.empty()
    frame_hold.image("assets/black.jpg", use_column_width=True)
    mask = cv2.imread("assets/mask.png")

    # Load model
    model = fasterRCNN_resnet18(num_classes=3)
    DEVICE = device

    checkpoint = torch.load('model/best_model.pth', map_location=DEVICE)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(DEVICE).eval()
            
    mobil, motor, durasi = st.columns(3)
    # Menambahkan judul dan teks di kolom "mobil"
    with mobil:
        st.markdown("<h4 style='text-align: center; font-weight: bold;'>Mobil</h4>", unsafe_allow_html=True)
        mobil_text = st.markdown("<p style='text-align: center; font-size: 24px;'>__</p>", unsafe_allow_html=True)

    # Menambahkan judul dan teks di kolom "motor"
    with motor:
        st.markdown("<h4 style='text-align: center; font-weight: bold;'>Motor</h4>", unsafe_allow_html=True)
        motor_text = st.markdown("<p style='text-align: center; font-size: 24px;'>__</p>", unsafe_allow_html=True)

    # Menambahkan judul dan teks di kolom "durasi"
    with durasi:
        st.markdown("<h4 style='text-align: center; font-weight: bold;'>Durasi</h4>", unsafe_allow_html=True)
        durasi_text = st.markdown("<p style='text-align: center; font-size: 24px;'>__</p>", unsafe_allow_html=True)
    

    if inference_mode == "📷 Image":
        uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg"], key="image_uploader")

        if uploaded_image is not None:
            # Read the uploaded image
            image = Image.open(io.BytesIO(uploaded_image.read()))
            image = np.array(image)
            orig_image = image.copy()

            # Display the uploaded image
            frame_hold.image(orig_image, channels="RGB")

            st.sidebar.markdown(
            """
            <style>
            .stButton > button {
                width: 100%;
            }
            </style>
            """
            ,unsafe_allow_html=True
            )
            if st.sidebar.button("Detect"):
                st.sidebar.empty()
                pred_image, boxes, scores, pred_classes = detect_img(model, image, iou_threshold)
                
                # Display the detected image
                frame_hold.image(pred_image, channels="RGB")

                class_counts = count_classes(boxes, pred_classes)
                class_counts['durasi'] = f"{optim_traffic(class_counts['mobil'], class_counts['motor'])} detik"
                
                mobil_text.write(f"<p style='text-align: center; font-size: 24px;'>{class_counts['mobil']}</p>", unsafe_allow_html=True)
                motor_text.write(f"<p style='text-align: center; font-size: 24px;'>{class_counts['motor']}</p>", unsafe_allow_html=True)
                durasi_text.write(f"<p style='text-align: center; font-size: 24px;'>{class_counts['durasi']}</p>", unsafe_allow_html=True)

    elif inference_mode == "📹 Video":
        uploaded_video = st.sidebar.file_uploader("Upload a video", type=["mp4"])

        if uploaded_video is not None:
            # Save the uploaded video to a temporary file
            temp_file = 'temp.mp4'

            with open(temp_file, 'wb') as f:
                f.write(uploaded_video.read())

            video_file = open(temp_file, 'rb')
            video_bytes = video_file.read()
            frame_hold.video(video_bytes)

            st.sidebar.markdown(
            """
            <style>
            .stButton > button {
                width: 100%;
            }
            </style>
            """
            ,unsafe_allow_html=True
            )

            if st.sidebar.button("Detect"):
                bar = st.sidebar.progress(0)
                progress_text = st.sidebar.empty()
                # Call the detect_video function on the temporary video file
                video = cv2.VideoCapture(temp_file)

                # Get video properties
                frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
                frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
                frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = int(video.get(cv2.CAP_PROP_FPS))

                # Define codec and create VideoWriter object
                out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

                frame_count = 0
                total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                total_fps = 0
                prev_time = time.time()  # Initialize prev_time
                class_colors = {'mobil': (0, 255, 0), 'motor': (0, 0, 255)}

                # Read until end of video
                while video.isOpened():
                    # Capture each frame of the video
                    ret, frame = video.read()

                    if ret:
                        image = frame.copy()
                        frame_height, frame_width = frame.shape[:2]
                        frame_count += 1

                        # Add mask to image
                        mask = cv2.resize(mask, (image.shape[1], image.shape[0]))

                        # Convert the image and mask to the same data type
                        image = image.astype(np.float32)
                        mask = mask.astype(np.float32)

                        image = cv2.bitwise_and(image, mask)

                        # Preprocess the image
                        if args.imgsz is not None:
                            image = cv2.resize(image, (args.imgsz, args.imgsz))

                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
                        image /= 255.0
                        image_input = np.transpose(image, (2, 0, 1)).astype(np.float32)
                        image_input = torch.tensor(image_input, dtype=torch.float)
                        image_input = torch.unsqueeze(image_input, 0)

                        # Perform object detection
                        with torch.no_grad():
                            outputs = model(image_input.to(DEVICE))

                        # Post-process the outputs
                        outputs = [{k: v.to('cpu') for k, v in t.items()} for t in outputs]
                        if len(outputs[0]['boxes']) != 0:
                            boxes = outputs[0]['boxes'].data.numpy()
                            scores = outputs[0]['scores'].data.numpy()
                            boxes = boxes[scores >= iou_threshold].astype(np.int32)
                            draw_boxes = boxes.copy()
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

                            # Draw bounding boxes and class names on the frame
                            for j, (box, class_name, score) in enumerate(zip(filtered_boxes, filtered_pred_classes, filtered_scores)):
                                class_name = pred_classes[j]
                                score = scores[j]
                                color = class_colors.get(class_name, (0, 0, 0))

                                xmin, ymin, xmax, ymax = box

                                # Mengubah koordinat box ke ukuran asli gambar
                                xmin = int(xmin * frame_width / args.imgsz)
                                ymin = int(ymin * frame_height / args.imgsz)
                                xmax = int(xmax * frame_width / args.imgsz)
                                ymax = int(ymax * frame_height / args.imgsz)

                                # Exclude boxes with very small height or width
                                if ymax - ymin > 2 and xmax - xmin > 2:
                                    cv2.rectangle(frame,
                                                (xmin, ymin),
                                                (xmax, ymax),
                                                color,
                                                2)

                                    # Create class score text
                                    class_score_text = f"{class_name} {score:.2f}"
                                    (text_width, text_height), _ = cv2.getTextSize(class_score_text, cv2.FONT_HERSHEY_SIMPLEX, 0.80, 1)

                                    # Draw background rectangle for text
                                    cv2.rectangle(frame,
                                                (xmin, ymin - text_height),
                                                (xmin + text_width - 45, ymin),
                                                color,
                                                -1)

                                    # Draw class score text
                                    cv2.putText(frame,
                                                class_score_text,
                                                (xmin, ymin - 5),
                                                cv2.FONT_HERSHEY_SIMPLEX,
                                                0.5,
                                                (0, 0, 0),
                                                1,
                                                lineType=cv2.LINE_AA)

                            class_counts = count_classes(filtered_boxes, filtered_pred_classes)
                            class_counts['durasi'] = f"{optim_traffic(class_counts['mobil'], class_counts['motor'])} detik"

                            mobil_text.write(f"<p style='text-align: center; font-size: 24px;'>{class_counts['mobil']}</p>", unsafe_allow_html=True)
                            motor_text.write(f"<p style='text-align: center; font-size: 24px;'>{class_counts['motor']}</p>", unsafe_allow_html=True)
                            durasi_text.write(f"<p style='text-align: center; font-size: 24px;'>{class_counts['durasi']}</p>", unsafe_allow_html=True)
                            
                            # Update the progress bar
                            progress = (frame_count * 100) / total_frames
                            progress /= 100
                            bar.progress(progress)
                            progress_text.markdown(f'{int(progress * 100)}%')
                            
                            # Write the frame to the output video
                            out.write(frame)

                        # Calculate the FPS
                        fps = 1 / (1e-6 + time.time() - prev_time)
                        total_fps += fps
                        prev_time = time.time()
                    
                        # Display the frame in Streamlit
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame_hold.image(frame_rgb, channels="RGB")

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    else:
                        break

                # Release the VideoCapture and VideoWriter objects
                video.release()
                out.release()
                cv2.destroyAllWindows()

    
# Run the app
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass