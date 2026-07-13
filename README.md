# Smart-Offline-Exam-Monitoring
# 🎓 AI-Based Smart Exam Monitoring System

## Overview
An AI-powered exam monitoring system that uses Computer Vision and Deep Learning to automatically detect suspicious behaviors during exams and help reduce cheating.

The system analyzes exam images and identifies different behaviors using a YOLO-based Object Detection model.

## Project Features
- Real-time cheating behavior detection
- Phone usage detection
- Hand movement monitoring
- Cheating paper detection
- Saving screenshots of detected suspicious cases
- User-friendly interface for monitoring results

## Detected Classes
The YOLO model detects 5 different classes:

- 📝 **Cheating**
- ✋ **Hand-Normalmove**
- ✅ **Non-Cheating**
- 📄 **Cheating-Paper**
- 📱 **Phone**

## 🧠 AI Model
- Model: **YOLOv8 Object Detection**
- Task: **Object Detection**
- Input: Exam images
- Output: Detected objects with bounding boxes and confidence scores

## 🛠️ Technologies Used
- Python
- YOLOv8 (Ultralytics)
-Computer Vision
-FastAPI
-Streamlit

## 🔄 System Pipeline
1. Collect and prepare dataset
2. Annotate images with bounding boxes
3. 🏋️ Train YOLOv8 model
4. Evaluate model performance
5. Integrate model with API
6. 🖥️ Build Streamlit interface
7. 📸 Store detected cheating screenshots

