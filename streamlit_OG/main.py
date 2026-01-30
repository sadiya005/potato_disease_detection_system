import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"


# -------------------- Page Config --------------------
st.set_page_config(
    page_title="LeafGuard: Potato Health Monitor",
    layout="centered",
    page_icon="🥔"
)

# -------------------- Title --------------------
st.markdown(
    "<h1 style='text-align:center; color:green;'>LeafGuard: Potato Health Monitor</h1>",
    unsafe_allow_html=True
)
st.caption("Tip: Use a clear photo of a single potato leaf")

# -------------------- Image Input --------------------
col1, col2 = st.columns(2)

with col1:
    camera_file = st.camera_input("📸 Take a photo")

with col2:
    uploaded_file = st.file_uploader(
        "📁 Upload from gallery",
        type=["jpg", "jpeg", "png"]
    )

image = uploaded_file if uploaded_file else camera_file

# -------------------- Image Preview & File Size Validation --------------------
if image:
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
    if image.size > MAX_FILE_SIZE:
        st.error("⚠️ File too large! Please upload an image under 5MB.")
    else:
        st.markdown("<br>", unsafe_allow_html=True)

        # Center image
        img_col1, img_col2, img_col3 = st.columns([1, 2, 1])
        with img_col2:
            st.image(image, caption="Uploaded Image", width=320)

        st.markdown("<br>", unsafe_allow_html=True)

        # Center Predict Button
        btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
        with btn_col2:
            predict = st.button("🔍 Predict Disease", use_container_width=True)

        # -------------------- Prediction --------------------
        if predict:
            with st.spinner("Analyzing leaf... 🌿"):
                try:
                    # Determine content type dynamically
                    ext = image.name.split(".")[-1].lower()
                    content_type = f"image/{'jpeg' if ext in ['jpg', 'jpeg'] else 'png'}"
                    files = {
                        "file": (
                        image.name if hasattr(image, "name") else "image.jpg",
                        image.getvalue(),
                        content_type
                        )
                    }

                    # Send request to FastAPI
                    response = requests.post(API_URL, files=files)
                    if response.status_code != 200:
                        st.error(f"API Error {response.status_code}: {response.text}")
                        st.stop()
                    data = response.json()

                    cls = data.get("class", "Unknown")
                    conf = data.get("confidence", 0)
                    sugg = data.get("suggestions", [])
                    warning = data.get("warning")

                    # -------------------- Color Cards --------------------
                    if cls == "Healthy":
                        bg = "#4CAF50"  # green
                        icon = "✅"
                    elif cls == "Early Blight":
                        bg = "#FF9800"  # orange
                        icon = "⚠️"
                    else:
                        bg = "#F44336"  # red
                        icon = "🛑"

                    st.markdown(
                        f"""
                        <div style="
                            background-color:{bg};
                            color:white;
                            padding:18px;
                            border-radius:12px;
                            text-align:center;
                            margin-top:15px;
                        ">
                            <h3>{icon} {cls}</h3>
                            <p style="font-size:16px;">
                                Confidence: <b>{conf*100:.2f}%</b>
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # -------------------- Suggestions --------------------
                    if sugg:
                        with st.expander("💡 Suggestions"):
                            for s in sugg:
                                st.write(f"- {s}")

                    if warning:
                        st.warning(warning)

                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Cannot connect to FastAPI. Make sure it's running on port 8000.")
                except requests.exceptions.HTTPError as http_err:
                    st.error(f"HTTP error from FastAPI: {http_err}")
                except Exception as e:
                    st.error(f"Prediction failed: {e}")

# -------------------- Footer --------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Made with ❤️ by Sadiya Sajid | LeafGuard v1.0</p>",
    unsafe_allow_html=True
)