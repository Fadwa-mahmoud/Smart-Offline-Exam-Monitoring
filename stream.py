import streamlit as st
import requests
from PIL import Image
import pandas as pd


st.set_page_config(
    page_title="ExamGuard AI",
    page_icon="🛡️",
    layout="wide"
)
st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

/* Tabs styling */

.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
}


.stTabs [data-baseweb="tab"] {
    color: white;
    font-size: 18px;
    font-weight: bold;
}


.stTabs [aria-selected="true"] {
    color: #00E5FF;
    background-color: #1E1E1E;
}
.main-title {
    font-size: 32px;
    font-weight: 700;
    color: white;
    letter-spacing: 1px;
}


.card {
    background: #1E1E1E;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
/* Upload text */
.stFileUploader label {
    color: white !important;
    font-size: 18px;
}


/* Upload box */
.stFileUploader section {
    background-color: #1E1E1E !important;
    border: 1px solid #444 !important;
}


/* Uploaded file name */
.stFileUploader small {
    color: white !important;
}


/* Button */
.stButton button {
    background-color: #1E1E1E;
    color: white;
    border: 1px solid #555;
    border-radius: 10px;
    font-weight: bold;
}


/* Metrics */
[data-testid="stMetricLabel"] {
    color: white !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
}

/* Titles */
h1, h2, h3 {
    color: white !important;
}
.stFileUploader div[data-testid="stFileUploaderDropzone"] {
    background-color: #1E1E1E !important;
}


.stFileUploader div[data-testid="stFileUploaderDropzone"] * {
    color: white !important;
}


/* Browse files button */
.stFileUploader button {
    background-color: #000000 !important;
    color: white !important;
    border: 1px solid #555 !important;
}
.stAlert {
    color: white !important;
}

.stAlert p {
    color: white !important;
}
/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #111827 !important;
}


[data-testid="stSidebar"] * {
    color: white !important;
}


[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
}
/* File uploader help text */

.stFileUploader small {
    color: white !important;
}
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] small {
    color: white !important;
}
[data-testid="stFileUploaderDropzone"] p {
    color: white !important;
}

[data-testid="stFileUploaderDropzone"] span {
    color: white !important;
}

[data-testid="stFileUploaderDropzone"] small {
    color: white !important;
}
/* Top header background */

[data-testid="stHeader"] {
    background-color: #0E1117 !important;
}

[data-testid="stToolbar"] {
    background-color: #0E1117 !important;
}
/* Dataframe header */

[data-testid="stDataFrame"] th {
    color: black !important;
    background-color: white !important;
}


/* Dataframe cells */

[data-testid="stDataFrame"] td {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


API_URL = "http://127.0.0.1:8000"


st.markdown(
    '<div class="main-title">ExamGuard AI</div>',
    unsafe_allow_html=True
)

st.write(
    "AI Powered Offline Exam Monitoring System"
)

with st.sidebar:

    st.title("🛡️ Control Panel")

    try:

        health = requests.get(
            f"{API_URL}/health"
        ).json()

        st.success("🟢 API Online")

        if health["model_loaded"]:
            st.success("🤖 YOLO Model Loaded")
        else:
            st.error("🤖 Model Not Loaded")


    except:

        st.error("🔴 API Offline")

    st.write("📌 System: ExamGuard AI")
    st.divider()

    st.info(
        "Offline Exam Cheating Detection"
    )


tab1, tab2, tab3 = st.tabs(
    [
        "🏠 Home",
        "🔍 Analyze",
        "📋 History"
    ]
)
with tab1:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
                <div class="card">

                <h3>API Status</h3>

                <p>🟢 Online</p>

                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                """
                <div class="card">

                <h3>AI Model</h3>

                <p>🤖 YOLO Active</p>

                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                """
                <div class="card">

                <h3>Database</h3>

                <p>🗄️ SQLite Connected</p>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        st.markdown(
            "### About System"
        )

        st.write(
            """
            ExamGuard AI is an intelligent exam monitoring
            system that uses YOLO object detection to analyze
            suspicious behaviors and calculate risk levels.
            """
        )

        st.markdown(
            "### Features"
        )

        st.write(
            """
            ✅ YOLO Object Detection

            ✅ Risk Score Analysis

            ✅ Detection History Storage
            """
        )


with tab2:

    st.header("🔍 Exam Analysis")

    uploaded_file = st.file_uploader(
        "Upload Exam Image",
        type=["jpg", "jpeg", "png"]
    )


    if uploaded_file:

        image = Image.open(uploaded_file)
        if st.button("🚀 Analyze Exam"):
            files = {
                "file": uploaded_file.getvalue()
            }
            response = requests.post(
                f"{API_URL}/predict",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }
            )


            result = response.json()
            # Display YOLO result image

            result_image_path = result["image_path"]

            result_image = Image.open(result_image_path)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Original")

                st.image(
                    image,
                    width=400
                )

            with col2:
                st.subheader("YOLO Detection")

                st.image(
                    result_image,
                    width=400
                )


            st.success("Analysis Completed")

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    "### 🚨 Exam Status"
                )

                if result["risk_score"] > 0:
                    st.error(result["exam_status"])
                else:
                    st.success(result["exam_status"])

            with col2:
                st.markdown(
                    "### 📊 Risk Score"
                )

                risk = result["risk_score"]

                st.progress(
                    risk / 100
                )

                st.write(
                    f"{risk}% Risk Level"
                )

            st.divider()

            st.markdown(
                "### 🎯 Detection Details"
            )

            detections = result["detections"]

            if len(detections) > 0:

                df = pd.DataFrame(detections)

                df.index += 1

                st.dataframe(
                    df,
                    use_container_width=True
                )

                st.info(
                    f"Total detected objects: {len(detections)}"
                )

            else:

                st.success(
                    "No suspicious objects detected"
                )

with tab3:

    st.header("📋 Analysis History")


    response = requests.get(
        f"{API_URL}/history"
    )


    data = response.json()

    records = data["records"]


    if len(records) > 0:

        df = pd.DataFrame(
            records,
            columns=[
                "ID",
                "Image Name",
                "Image Path",
                "Status",
                "Risk Score",
                "Detections",
                "Date"
            ]
        )
        df["ID"] = range(1, len(df) + 1)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )



    else:

        st.info(
            "No analysis history found"
        )