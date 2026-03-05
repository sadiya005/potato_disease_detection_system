# 🌿 LeafGuard – Potato Leaf Disease Detection System

**LeafGuard** is an end-to-end **deep learning–based potato leaf disease detection system** designed to identify plant diseases from leaf images. The project simulates a real-world **agri-tech AI solution**, covering everything from **model training** to **real-time deployment** using modern tools.

---

## 📌 Project Overview

The objective of LeafGuard is to help farmers and agricultural stakeholders **detect potato plant diseases early** using images of leaves. Early detection enables timely treatment, reduces crop loss, and improves yield.

This project demonstrates a complete **computer vision deployment pipeline**, including:

- Image-based disease classification using deep learning  
- FastAPI for model inference  
- Interactive web interface for users  
- Containerized deployment using Docker  

---

## 🛠️ Project Workflow

### 1️⃣ Dataset & Preprocessing
- Used a **potato leaf disease dataset** (healthy, early blight, late blight)
- Image resizing and normalization
- Dataset split into training and validation sets

### 2️⃣ Model Training
- Built a **CNN-based deep learning model** using **TensorFlow / Keras**
- Trained on labeled potato leaf images
- Optimized for accuracy and generalization
- Final trained model saved for inference

### 3️⃣ Model Evaluation
- Evaluated model performance on validation data
- Verified predictions on unseen images
- Ensured stable inference before deployment

### 4️⃣ Backend API (FastAPI)
- Developed a **FastAPI backend** to serve predictions
- Accepts image uploads via API endpoints
- Returns predicted disease class with confidence
- Designed for real-time inference

### 5️⃣ Frontend (Streamlit)
- Built an interactive **Streamlit web application**
- Users can take or upload leaf images
- Displays predicted disease and result instantly
- Simple, farmer-friendly interface

### 6️⃣ Deployment
- Containerized the entire application using **Docker**
- Single container running:
  - FastAPI backend
  - Streamlit frontend
- Deployed on **Render**
- Accessible via browser without local setup
- Live deployment link: [https://leafguard-full.onrender.com/]
---

## 🔍 Key Insights
- Deep learning–based potato leaf disease classification  
- Supports image upload and real-time camera capture  
- Displays prediction confidence and handles low-confidence cases  
- FastAPI backend for model inference  
- Streamlit-based interactive and mobile-friendly frontend  
- Dockerized application ready for cloud deployment  
 

---

## 🧰 Tools & Technologies

- **Python**
- **TensorFlow / Keras** – Deep Learning
- **NumPy, Pillow** – Image processing
- **FastAPI** – Backend API
- **Streamlit** – Interactive UI
- **Docker** – Containerization
- **Render** – Cloud deployment

---

## 🚀 Use Cases
- Early disease detection for farmers using leaf images  
- Mobile-friendly crop health monitoring via browser-based camera input  
- Decision support tool for smart agriculture systems  
- Educational demonstration of deep learning in agriculture  
- Foundation for scalable deployment in agri-tech platforms  
  

---

## 🔮 Future Enhancements
- Expand classification to multiple crop types and diseases  
- Improve model robustness using additional field images and augmentation  
- Add multilingual support for wider farmer accessibility  
- Integrate weather and soil data for richer decision support  
- Optimize inference for low-bandwidth and low-resource environments  
 

---

## 👩‍💻 Author

**Sadiya Sajid**  

🔗 [LinkedIn](https://www.linkedin.com/in/sadiyasajid/)

---

## 🎯 Why This Project Matters

LeafGuard showcases a **real-world AI application in agriculture**, covering the complete journey from **data and model development** to **production-ready deployment**. It highlights how deep learning-based models can support sustainable farming and smarter crop management.
