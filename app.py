from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from ultralytics import YOLO
from API.database import create_database, save_history, get_history,clear_history
import shutil
import os
app = FastAPI(
    title="🛡️ ExamGuard AI API",
    description="Offline Exam Cheating Detection System using YOLO",
    version="1.0",
    docs_url=None
)
create_database()
import sqlite3

conn = sqlite3.connect("API/examguard.db")
cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
)

print(cursor.fetchall())

conn.close()
@app.get("/docs", include_in_schema=False)
def custom_docs():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ExamGuard AI API</title>

        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui.css">

        <style>
            body {
                background-color: #121212;
            }

            .swagger-ui {
                filter: invert(0.9) hue-rotate(180deg);
            }
        </style>

    </head>

    <body>

        <div id="swagger-ui"></div>

        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui-bundle.js"></script>

        <script>
            SwaggerUIBundle({
                url: "/openapi.json",
                dom_id: "#swagger-ui"
            })
        </script>

    </body>
    </html>
    """)


model = YOLO("API/best.pt")

@app.get("/")
def home():
    return {
        "project": "ExamGuard AI",
        "status": "Running",
        "model": "YOLO",
        "message": "Offline Exam Monitoring API is ready"
    }


@app.get("/health")
def health():
    return {
        "api_status": "online",
        "model_loaded": True
    }


@app.post("/predict")
def predict(file: UploadFile = File(...)):

    image_path = "temp.jpg"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = model(image_path)

    annotated_image = results[0].plot()

    detections = []

    for r in results:
        for box in r.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            detections.append({
                "object": model.names[class_id],
                "confidence": round(confidence * 100, 2)
            })

    suspicious_objects = [
        "Cheating",
        "Hand-Suspiciousmove"
    ]

    suspicious_count = 0

    for d in detections:
        if d["object"] in suspicious_objects:
            suspicious_count += 1

    risk_score = min(suspicious_count * 40, 100)

    if suspicious_count > 0:
        status = "⚠️ Cheating Suspicion Detected"
    else:
        status = "✅ Normal Exam Behavior"
    output_path = "API/annotated.jpg"
    from PIL import Image
    Image.fromarray(annotated_image).save(output_path)
    save_history(
        file.filename,
        output_path,
        status,
        risk_score,
        str(detections)
    )
    if os.path.exists(image_path):
        os.remove(image_path)

    return {
        "exam_status": status,
        "risk_score": risk_score,
        "total_detections": len(detections),
        "detections": detections,
        "image_path": output_path
    }
@app.get("/history")
def history():

    data = get_history()

    return {
        "records": data
    }
@app.delete("/clear-history")
def delete_history():

    clear_history()

    return {
        "message": "History cleared successfully"
    }