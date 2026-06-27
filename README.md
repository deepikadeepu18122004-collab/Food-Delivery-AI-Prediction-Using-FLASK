# Food Delivery AI Prediction Using FLASK

A machine learning-powered Flask web application that predicts food delivery times based on various factors like traffic conditions, weather, vehicle type, and distance.

## Features

- **Real-time Delivery Time Prediction**: Predict delivery time using ML model
- **Multiple Input Parameters**: 
  - Distance
  - Traffic Condition (Dense, Moderate, Light)
  - Weather (Sunny, Rainy, Cloudy)
  - Vehicle Type (Bike, Car, Scooter)
- **User-Friendly Interface**: Interactive web interface built with HTML, CSS, and JavaScript
- **Delivery History**: Track and view previous delivery predictions
- **Persistent Database**: SQLite database to store prediction history

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Machine Learning**: scikit-learn
- **Data Processing**: Pandas, NumPy
- **Database**: SQLite3
- **Model Storage**: Joblib (for ML model serialization)

## Project Structure

```
Food-Delivery-AI-Prediction-Using-FLASK/
├── app.py                 # Main Flask application
├── database.py            # Database management
├── requirement.txt        # Python dependencies
├── model/
│   ├── predictor.py       # ML prediction logic
│   ├── preprocessing.py   # Data preprocessing
│   └── model.pkl          # Trained ML model
├── static/
│   ├── script.js          # Frontend JavaScript
│   └── style.css          # Frontend styling
├── templates/
│   ├── index.html         # Home page
│   ├── result.html        # Prediction result page
│   └── history.html       # Delivery history page
├── scaler.pkl             # Feature scaling model
├── traffic_encoder.pkl    # Traffic condition encoder
├── vehicle_encoder.pkl    # Vehicle type encoder
├── weather_encoder.pkl    # Weather condition encoder
└── README.md              # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Important: Model Files

The trained ML model files (*.pkl) are large files not included in the repository. You have two options:

**Option 1: Download Pre-trained Model Files**
- Download the model files from the [GitHub Releases](https://github.com/deepikadeepu18122004-collab/Food-Delivery-AI-Prediction-Using-FLASK/releases)
- Extract them to the project root directory
- Files needed:
  - `model.pkl` (102+ MB)
  - `scaler.pkl`
  - `traffic_encoder.pkl`
  - `vehicle_encoder.pkl`
  - `weather_encoder.pkl`

**Option 2: Train the Model Locally**
- If you have training data, you can run the model training script (not included in this repo)
- The trained models will be saved as .pkl files in the project root

### Steps

1. Clone the repository
```bash
git clone https://github.com/deepikadeepu18122004-collab/Food-Delivery-AI-Prediction-Using-FLASK.git
cd Food-Delivery-AI-Prediction-Using-FLASK
```

2. **Download or prepare model files** (see Important section above)

3. Create a virtual environment
```bash
python -m venv venv
```

4. Activate the virtual environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

5. Install dependencies
```bash
pip install -r requirement.txt
```

## Usage

1. Run the Flask application
```bash
python app.py
```

2. Open your web browser and navigate to
```
http://localhost:5000/
```

3. Enter the delivery parameters:
   - Distance (in km)
   - Traffic Condition
   - Weather Condition
   - Vehicle Type

4. Click "Predict" to get the estimated delivery time

5. View prediction history on the History page

## Features Explained

### Prediction Model
- Uses a trained machine learning model to predict delivery times
- Considers multiple factors that affect delivery time:
  - Distance traveled
  - Traffic conditions
  - Weather conditions
  - Vehicle type

### Database
- Stores all prediction history
- Can be accessed through the History page
- Useful for analyzing prediction patterns

### User Interface
- Responsive design
- Easy-to-use form
- Real-time prediction results
- Visual feedback and animations

## API Endpoints

- `GET /` - Home page
- `POST /predict` - Make a prediction (API endpoint)
- `GET /history` - View delivery history
- `POST /clear_history` - Clear prediction history

## Configuration

The application runs on:
- **Host**: localhost (127.0.0.1)
- **Port**: 5000
- **Debug Mode**: Enabled (for development)

To change these settings, modify `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## Machine Learning Model Details

The model is trained on delivery data with the following features:
- Distance (continuous)
- Traffic Condition (categorical: Dense, Moderate, Light)
- Weather (categorical: Sunny, Rainy, Cloudy)
- Vehicle Type (categorical: Bike, Car, Scooter)

The model uses preprocessing and scaling to normalize inputs before prediction.

## Future Enhancements

- Add more features (time of day, restaurant location, etc.)
- Implement user authentication
- Add delivery partner integration
- Real-time GPS tracking
- Advanced analytics dashboard
- Mobile app version
- API rate limiting
- Caching mechanisms

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.

## Author

Created by: deepikadeepu18122004-collab

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**Live Application**: http://localhost:5000/

**Repository**: https://github.com/deepikadeepu18122004-collab/Food-Delivery-AI-Prediction-Using-FLASK
