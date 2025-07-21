# 🌱 LeafGuard AI

**AI-Powered Plant Disease Detection & Analysis**

*Protecting crops with intelligent monitoring*

---

## 🚀 Overview

LeafGuard AI is an advanced plant disease detection system that uses machine learning to analyze plant leaf images and provide comprehensive disease analysis. The system combines deep learning models with Grad-CAM visualization to deliver accurate disease classification, severity estimation, and detailed PDF reports.

### ✨ Key Features

- 🔍 **Advanced Disease Detection**: Multi-class plant disease classification
- 📊 **Severity Estimation**: AI-powered disease severity analysis
- 🗺️ **Visual Heatmaps**: Grad-CAM visualization for explainable AI
- 📋 **Detailed Reports**: Professional PDF reports with treatment advice
- 💾 **Database Storage**: Persistent storage of analysis results
- 📤 **Batch Processing**: Handle multiple images simultaneously
- 🌐 **Web Interface**: User-friendly Streamlit frontend

---

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **AI/ML**: PyTorch, HuggingFace Transformers (DINOv2)
- **Database**: SQLite with SQLAlchemy ORM
- **Visualization**: Grad-CAM, OpenCV
- **Reports**: FPDF for PDF generation

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PlantDiseaseSpotter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your dataset** (optional)
   - Organize plant images in folders by disease type
   - Run the training script to create your custom model

4. **Start the backend server**
   ```bash
   cd src
   python api.py
   ```

5. **Start the frontend application**
   ```bash
   cd frontend
   streamlit run app.py
   ```

---

## 🎯 Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:8501`
2. Upload one or multiple plant leaf images
3. Wait for AI analysis to complete
4. Download detailed PDF reports with disease information and treatment advice

### API Endpoints

- `POST /predict/` - Upload image for disease analysis
- `GET /results/` - Retrieve stored analysis results
- `GET /health` - Health check endpoint

---

## 📊 Model Information

### Supported Diseases

The system can detect various plant diseases including:
- Bacterial spot
- Early blight
- Late blight
- Leaf mold
- Septoria leaf spot
- Spider mites
- Target spot
- Yellow leaf curl virus
- Mosaic virus
- And many more...

### Model Architecture

- **Feature Extraction**: DINOv2 (Vision Transformer)
- **Classification**: K-Nearest Neighbors on extracted features
- **Visualization**: Grad-CAM for explainable AI
- **Severity Estimation**: Custom algorithm based on disease characteristics

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///leafguard_ai.db
MODEL_PATH=model.pth
FEATURES_PATH=features.pkl
LABELS_PATH=labels.pkl
```

### Model Training

To train your own model:

1. Organize your dataset in the `data/` directory
2. Run the training script:
   ```bash
   python src/train_model.py
   ```
3. The trained model will be saved as `model.pth`

---

## 🚀 Deployment

### Local Development

1. Start the backend:
   ```bash
   cd src && python api.py
   ```

2. Start the frontend:
   ```bash
   cd frontend && streamlit run app.py
   ```

3. Access the application at `http://localhost:8501`

### Production Deployment

For production deployment, consider:
- Using a production WSGI server (Gunicorn)
- Setting up reverse proxy (Nginx)
- Using a production database (PostgreSQL)
- Implementing authentication and rate limiting

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues and pull requests.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Plant disease datasets and research community
- Open-source AI/ML libraries
- Agricultural research institutions

---

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting guide

---

**🌱 LeafGuard AI** - *Protecting crops with intelligent monitoring*

*Built with ❤️ for the agricultural community* 
