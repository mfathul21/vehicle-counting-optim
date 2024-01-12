# Traffic Light Optimization using Vehicle Counting & Fuzzy Logic

## Project Description

This project aims to optimize traffic light control at intersections by leveraging object detection, specifically using a modified Faster R-CNN model with a ResNet-18 backbone. The optimization is achieved through the integration of vehicle counting and fuzzy logic to dynamically adjust traffic light timings based on real-time traffic conditions.

## Features

- Object Detection: Utilizes a Faster R-CNN model with a ResNet-18 backbone to detect and count vehicles at intersections.
- Fuzzy Logic: Implements fuzzy logic to make dynamic decisions for optimizing traffic light timings.
- Real-time Adaptation: The system adapts traffic light timings in real-time based on the detected vehicle count.

## Dataset Sources

Collected data from <a href=https://cctv.jogjakota.go.id/home>https://cctv.jogjakota.go.id</a> then annotate with roboflow and augmentation. Dataset have 2 class, it is motorcycle and car

## Model Output

The trained model outputs can be found in the `model/` directory. Below are the links to download the model files:

- [Best Trained Model](https://drive.google.com/drive/folders/1L419RCGY0zDCPojnsGmZsjhzgsRS1UyS?usp=sharing): The best-performing model after training.

## Usage

1. **Installation:**
   - Clone the repository: `git clone https://github.com/your_username/traffic-light-optimization.git`
   - Install dependencies: `pip install -r requirements.txt`
   - Download model from google drive in README.md file

2. **Run the Application:**
   - Navigate to the project directory: `cd traffic-light-optimization`
   - Run the application: `python app.py`

3. **Input:**
   - Provide input images or videos to the application.

4. **Output:**
   - The application will display the optimized traffic light control and relevant statistics.

## Contributors

- Your Name (@your_username)
- Collaborator Name (@collaborator_username)

## License

This project is licensed under the [MIT License](LICENSE).
