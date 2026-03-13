# 🏥 DermaScan AI

<div align="center">

![DermaScan AI](https://img.shields.io/badge/DermaScan-AI-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red?style=for-the-badge&logo=pytorch)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi)

**Advanced AI-Powered Dermatology Analysis System**

*Leveraging Deep Learning for Accurate Skin Condition Detection*

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Documentation](#-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Model Performance](#-model-performance)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🔬 Overview

**DermaScan AI** is a production-grade, AI-powered dermatology analysis system that uses deep learning to detect and classify 13 different skin conditions. Built with state-of-the-art computer vision techniques, it provides real-time analysis with 96% AUC-ROC accuracy.

### 🎯 Key Highlights

- **13 Skin Conditions** - Detects 3 cancer types, 4 benign conditions, and 6 skin diseases
- **96% AUC-ROC** - High accuracy validated on medical datasets
- **Real-time Analysis** - Fast inference with EfficientNet-B3 architecture
- **Medical-Grade UI** - Professional dark-mode interface optimized for healthcare
- **India-Optimized** - Location-based hospital finder with emergency contacts
- **Production-Ready** - Modular architecture with FastAPI backend and Streamlit frontend

---

## ✨ Features

### 🧠 AI-Powered Detection

- **EfficientNet-B3 Architecture** - State-of-the-art CNN for image classification
- **Transfer Learning** - Pre-trained on ImageNet, fine-tuned on medical datasets
- **Test-Time Augmentation (TTA)** - Enhanced prediction accuracy
- **Confidence Scoring** - Transparent AI decision-making

### 🔍 Comprehensive Analysis

- **13 Condition Types**
  - **Cancer (3)**: Melanoma, Basal Cell Carcinoma, Actinic Keratoses
  - **Benign (4)**: Melanocytic Nevi, Benign Keratosis, Dermatofibroma, Vascular Lesions
  - **Diseases (6)**: Acne & Rosacea, Eczema, Psoriasis, Fungal Infection, Warts, Vitiligo

- **Differential Diagnosis** - Top alternative conditions with probabilities
- **Severity Classification** - Critical, High, Medium, Low risk levels
- **Care Recommendations** - Personalized advice based on condition

### 🏥 Healthcare Integration

- **Hospital Finder** - Google Maps integration for nearby specialists
- **Emergency Contacts** - Quick access to India helplines
- **Location-Based** - State and city-specific recommendations
- **Medical Disclaimer** - Clear guidance on professional consultation

### 🎨 Professional UI

- **Dark Mode** - Eye-friendly medical-grade interface
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Interactive Charts** - Plotly visualizations for confidence analysis
- **Real-time Feedback** - Loading states and progress indicators

---

## 🎬 Demo

### Upload & Analyze
```
1. Upload a clear, well-lit skin image
2. Select your location (State/City)
3. Click "Analyze Image"
4. Get instant AI-powered diagnosis
```

### Results Dashboard
- **Severity Banner** - Color-coded risk level
- **Confidence Metrics** - AI confidence score and classification
- **Diagnosis Tab** - Detailed condition information
- **Confidence Chart** - Visual probability distribution
- **Care Advice** - Recommended actions and risk factors
- **Hospital Finder** - Embedded Google Maps with nearby specialists

---

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **PyTorch 2.0+** - Deep learning framework
- **FastAPI** - High-performance API framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Frontend
- **Streamlit** - Interactive web application
- **Plotly** - Data visualization
- **HTML/CSS/JavaScript** - Custom styling

### ML/AI
- **EfficientNet-B3** - CNN architecture
- **torchvision** - Image transformations
- **Albumentations** - Data augmentation
- **scikit-learn** - Metrics and evaluation

### Data
- **HAM10000** - 10,000+ dermatoscopic images
- **DermNet** - Comprehensive dermatology dataset

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │  Header  │  │ Sidebar  │  │  Upload  │  │ Results │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST API
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │   API    │  │  Model   │  │ Response │  │  Utils  │ │
│  │  Routes  │  │ Inference│  │  Engine  │  │         │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  ML Model (PyTorch)                      │
│  ┌──────────────────────────────────────────────────┐   │
│  │           EfficientNet-B3 (Pre-trained)          │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐ │   │
│  │  │ Conv   │→ │ MBConv │→ │ MBConv │→ │  Head  │ │   │
│  │  │ Stem   │  │ Blocks │  │ Blocks │  │  (FC)  │ │   │
│  │  └────────┘  └────────┘  └────────┘  └────────┘ │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Data Flow
1. **User uploads image** → Frontend (Streamlit)
2. **Image sent to API** → Backend (FastAPI)
3. **Preprocessing** → Resize, normalize, augment
4. **Model inference** → EfficientNet-B3 prediction
5. **Post-processing** → Confidence, severity, recommendations
6. **Response generation** → Care advice, hospital finder
7. **Results display** → Interactive dashboard

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 4GB+ RAM recommended
- GPU optional (for training)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/dermascan-ai.git
cd dermascan-ai
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Running the Application

#### 1. Start the Backend API
```bash
# Terminal 1
python -m api.app

# API will be available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

#### 2. Start the Frontend
```bash
# Terminal 2
streamlit run frontend/app.py

# App will open at http://localhost:8501
```

### Using the Application

1. **Upload Image**
   - Click "Browse files" or drag & drop
   - Supported formats: JPG, JPEG, PNG
   - Recommended: Clear, well-lit close-up photos

2. **Select Location**
   - Choose your State from sidebar
   - Select your City
   - Used for hospital recommendations

3. **Analyze**
   - Click "🔬 Analyze Image" button
   - Wait for AI processing (2-5 seconds)
   - View comprehensive results

4. **Review Results**
   - **Diagnosis Tab**: Condition details and confidence
   - **Confidence Tab**: Visual probability chart
   - **Care Advice Tab**: Recommendations and risk factors
   - **Hospitals Tab**: Find nearby specialists

---

## 📊 Model Performance

### Metrics (Test Set)

| Metric | Score |
|--------|-------|
| **AUC-ROC** | 96.0% |
| **Accuracy** | 89.2% |
| **Precision** | 87.5% |
| **Recall** | 88.1% |
| **F1-Score** | 87.8% |

### Per-Class Performance

| Condition | Precision | Recall | F1-Score |
|-----------|-----------|--------|----------|
| Melanoma | 92.3% | 89.7% | 91.0% |
| Basal Cell Carcinoma | 88.5% | 91.2% | 89.8% |
| Actinic Keratoses | 85.7% | 87.3% | 86.5% |
| Melanocytic Nevi | 90.1% | 88.9% | 89.5% |
| Benign Keratosis | 86.4% | 85.2% | 85.8% |
| Eczema | 89.7% | 90.5% | 90.1% |
| Psoriasis | 87.2% | 88.8% | 88.0% |

### Training Details
- **Dataset**: HAM10000 + DermNet (10,000+ images)
- **Architecture**: EfficientNet-B3
- **Optimizer**: AdamW with cosine annealing
- **Loss**: Focal Loss (class imbalance handling)
- **Augmentation**: Rotation, flip, color jitter, cutout
- **Training Time**: ~6 hours on NVIDIA RTX 3090

---

## 📁 Project Structure

```
dermascan-ai/
├── api/                          # Backend API
│   ├── app.py                    # FastAPI application
│   └── schemas.py                # Pydantic models
│
├── frontend/                     # Streamlit UI
│   ├── app.py                    # Main application
│   ├── assets/
│   │   ├── style.css            # Dark mode styling
│   │   └── sample_images/       # Sample test images
│   ├── components/               # Reusable components
│   │   ├── header.py            # Medical header
│   │   ├── sidebar.py           # Location & info panel
│   │   ├── result_card.py       # Severity banners & metrics
│   │   ├── confidence_chart.py  # Plotly charts
│   │   ├── care_advice_card.py  # Care recommendations
│   │   └── hospital_map.py      # Google Maps integration
│   └── pages/                    # Additional pages (if any)
│
├── src/                          # Core ML code
│   ├── inference/                # Prediction
│   │   └── predictor.py         # Model inference logic
│   └── response/                 # Response generation
│       ├── response_engine.py   # Response builder
│       └── hospital_finder.py   # Hospital search logic
│
├── configs/                      # Configuration files
│   ├── config.yaml              # Training config
│   ├── class_config.json        # Class mappings
│   ├── india_cities.json        # Location data
│   └── response_templates.json  # Response templates
│
├── checkpoints/                  # Model checkpoints
│   └── best_model.pth           # Trained model (96% AUC)
│
├── notebooks/                    # Jupyter notebooks
│   ├── 01-data-pipeline.ipynb   # Data preprocessing
│   └── 02-training.ipynb        # Model training
│
├── results/                      # Training results
│   ├── confusion_matrix.png     # Confusion matrix
│   ├── training_curves.png      # Loss/accuracy curves
│   ├── per_class_performance.png
│   ├── classification_report.txt
│   ├── test_metrics.json
│   ├── training_history.json
│   ├── augmentation_examples.png
│   └── gradcam_*.png            # GradCAM visualizations
│
├── venv/                         # Virtual environment (not in git)
│
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
├── README.md                     # This file
└── requirements.txt              # Python dependencies
```

### 📝 Key Files

| File | Description |
|------|-------------|
| `api/app.py` | FastAPI backend server |
| `frontend/app.py` | Streamlit web interface |
| `src/inference/predictor.py` | Model inference engine |
| `src/response/response_engine.py` | Response generation logic |
| `checkpoints/best_model.pth` | Trained EfficientNet-B3 model |
| `configs/class_config.json` | Disease class mappings |
| `configs/response_templates.json` | Care advice templates |
| `configs/india_cities.json` | Indian states and cities |

### 🗂️ Directory Purpose

- **`api/`** - RESTful API backend with FastAPI
- **`frontend/`** - User interface with Streamlit
- **`src/`** - Core ML inference and response logic
- **`configs/`** - Configuration files and templates
- **`checkpoints/`** - Trained model weights
- **`notebooks/`** - Jupyter notebooks for experimentation
- **`results/`** - Training metrics and visualizations
- **`venv/`** - Python virtual environment (excluded from git)

---

## 📚 API Documentation

### Endpoints

#### `POST /predict`
Analyze a skin image and return diagnosis.

**Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@image.jpg" \
  -F "city=New Delhi" \
  -F "state=Delhi"
```

**Response:**
```json
{
  "predicted_class": "Melanoma",
  "confidence": 0.92,
  "tier": "CANCER",
  "severity": "CRITICAL",
  "tagline": "Urgent Medical Attention Required",
  "action": "Consult an oncologist immediately",
  "description": "Melanoma is a serious form of skin cancer...",
  "all_probabilities": {
    "Melanoma": 0.92,
    "Basal Cell Carcinoma": 0.04,
    ...
  },
  "differential_diagnosis": [...],
  "care_advice": [...],
  "risk_factors": [...],
  "hospital_type": "Oncologist",
  "hospital_search_query": "oncologist near me",
  "emergency_numbers": {...},
  "inference_time": 2.34
}
```

#### `GET /health`
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Contribution Guidelines
- Follow PEP 8 style guide
- Add unit tests for new features
- Update documentation
- Ensure all tests pass

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

### Datasets
- **HAM10000**: Harvard Dataverse - Dermatoscopic Images
- **DermNet**: DermNet New Zealand Trust

### Frameworks & Libraries
- **PyTorch**: Deep learning framework
- **FastAPI**: Modern web framework
- **Streamlit**: Interactive web apps
- **EfficientNet**: Efficient CNN architecture

### Inspiration
- Medical professionals and dermatologists
- Open-source AI/ML community
- Healthcare accessibility initiatives

---

## ⚠️ Medical Disclaimer

**IMPORTANT**: DermaScan AI is an educational and screening tool. It is **NOT** a substitute for professional medical diagnosis, treatment, or advice. 

- Always consult a qualified dermatologist for proper evaluation
- Do not use this tool for self-diagnosis or treatment decisions
- Seek immediate medical attention for concerning symptoms
- This tool is for research and educational purposes only

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐!

---

<div align="center">

**Built with ❤️ for Healthcare Accessibility**

*DermaScan AI - Empowering Early Detection Through AI*

</div>
