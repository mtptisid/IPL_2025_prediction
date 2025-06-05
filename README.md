# IPL Match Predictor

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

The **IPL Match Predictor** is a web application that leverages machine learning to predict the outcomes of Indian Premier League (IPL) cricket matches. Built with Flask, it features a modern, user-friendly interface with a gradient theme, glassmorphism design, and interactive elements like confetti animations. Users can select teams, venues, and match dates to receive predictions, including winner, scores, run rates, and head-to-head statistics.

Created by **Siddharamayya**, this project showcases a blend of data science and web development. Visit [siddharamayya.in](https://siddharamayya.in) for more projects.

## Features

- **Predictive Analytics**:
  - Predicts match winner, first and second innings scores, run rates, and win probability using XGBoost models.
  - Example: Predicts Royal Challengers Bengaluru (RCB) winning over Punjab Kings (PBKS) with scores 166.62 vs. 151.05.
  - Provides head-to-head stats (e.g., RCB wins 6/10 matches vs. PBKS).
- **Modern UI**:
  - Gradient background (navy-indigo-purple) with glassmorphism cards.
  - 2x2 grid for prediction results with glow effects, gradient borders, and staggered animations.
  - Poppins font for clean typography.
  - Confetti animation on successful predictions.
  - Footer crediting Siddharamayya with a link to [siddharamayya.in](https://siddharamayya.in).
- **Interactive Form**:
  - Team selection with a swap button next to Team 2 for easy switching (e.g., RCB ↔ PBKS).
  - Venue dropdown with fallback (“No venues available” if data is missing).
  - Date picker for match scheduling.
  - Larger inputs and labels for improved usability.
- **Responsive Design**:
  - Form on left, results on right (desktop); stacks vertically on mobile.
  - Form width: 41.67% (`md:w-5/12`); results: 58.33% (`md:w-7/12`).
- **Real-Time Features**:
  - Displays current date and time (e.g., “Today: June 03, 2025, 04:12 PM IST”).
  - Updates time every minute.
- **Robust Backend**:
  - Flask app with JSON serialization fix for `float32` data.
  - Pre-trained models (`winner_model.joblib`, `first_score_model.joblib`, etc.) for predictions.
  - Data sourced from kaggle.


## Demo

### Screenshots

<img width="1437" alt="Screenshot 2025-06-03 at 3 53 03 PM" src="https://github.com/user-attachments/assets/117a293e-e8ef-4ea7-a9b3-ac6ed777bef7" />

<img width="1424" alt="Screenshot 2025-06-03 at 3 36 24 PM" src="https://github.com/user-attachments/assets/993a1041-4718-4446-9725-ba3d7f5e74b7" />

### Videos
Watch short demos showcasing the IPL Match Predictor’s interactive UI and predictions:

<div style="display: flex; gap: 25px;">
  <a href="https://www.youtube.com/shorts/K7vD_UDO03Y" target="_blank">
    <img src="https://img.youtube.com/vi/K7vD_UDO03Y/default.jpg" alt="Demo Video 1" style="width: 398px; height: 689px;">
  </a>
  <a href="https://www.youtube.com/shorts/DjZiZJXs9mE" target="_blank">
    <img src="https://img.youtube.com/vi/DjZiZJXs9mE/default.jpg" alt="Demo Video 2" style="width: 398px; height: 689px;">
  </a>
</div>

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ipl-match-predictor.git
   cd ipl-match-predictor
   ```

2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install flask pandas numpy scikit-learn xgboost joblib
   ```

4. **Verify Directory Structure**:
   Ensure the following files are in the project root:
   ```
   ipl-match-predictor/
   ├── app.py
   ├── templates/
   │   └── index.html
   ├── winner_model.joblib
   ├── first_score_model.joblib
   ├── second_score_model.joblib
   ├── team_encoder.joblib
   ├── venue_encoder.joblib
   ├── team_stats.joblib
   ├── venue_stats.joblib
   └── ipl_data.csv
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   - Access the app at `http://localhost:5000` or your Codespaces URL (e.g., `https://<your-codespace-name>-5000.app.github.dev`).

## Usage

1. **Open the App**:
   - Navigate to `http://localhost:5000` in your browser.
   - The UI displays “Today: June 03, 2025, 04:12 PM IST” and a form titled “Predict a Match”.

2. **Fill the Form**:
   - **Team 1 (Batting First)**: Select a team (e.g., Royal Challengers Bengaluru).
   - **Team 2 (Batting Second)**: Select another team (e.g., Punjab Kings). Use the swap button to switch teams.
   - **Venue**: Choose a venue (e.g., M Chinnaswamy Stadium). If no venues appear, check `app.py` or `ipl_data.csv`.
   - **Match Date**: Pick a date (e.g., 2025-06-01).
   - Click **Predict Match**.

3. **View Results**:
   - Results appear in a 2x2 grid of glassmorphism boxes with a confetti animation.
   - Example output:
     ```
     Prediction Results

     [Match Details Box]         [Predicted Scores Box]
     Teams: Royal Challengers Bengaluru (batting first) vs Punjab Kings (batting second)
     Venue: M Chinnaswamy Stadium
     Date: 2025-06-01
                                 First Innings (Royal Challengers Bengaluru): 166.62 (Run Rate: 8.33)
                                 Second Innings (Punjab Kings): 151.05 (Run Rate: 7.55)

     [Winner Prediction Box]     [Head-to-Head Stats Box]
     Winner: Royal Challengers Bengaluru
     Probability: 16%
                                 Matches: 10
                                 Royal Challengers Bengaluru Wins: 6 (Win Rate: 60%)
                                 Royal Challengers Bengaluru Avg Score vs Punjab Kings: 165.80
     ```

4. **Troubleshooting**:
   - **Venue List Empty**: Inspect `<select id="venue">` in browser source. Ensure `app.py` passes `venues`.
   - **Swap Button Fails**: Check console for JavaScript errors.
   - **No Confetti**: Verify `canvas-confetti` CDN loads.
   - **Low Probability (16%)**: The classifier may need retraining. Share `ipl_data.csv` for analysis.
   - **Errors**: Check terminal logs or UI error messages.

## Project Structure

| File/Folder                | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| `app.py`                   | Flask application with routes for home (`/`) and prediction (`/predict`).   |
| `templates/index.html`     | HTML template with Tailwind CSS, Poppins font, and `canvas-confetti` for UI.|
| `winner_model.joblib`      | XGBoost model for predicting the match winner.                             |
| `first_score_model.joblib` | Model for predicting first innings score.                                  |
| `second_score_model.joblib`| Model for predicting second innings score.                                 |
| `team_encoder.joblib`      | Encoder for team names.                                                    |
| `venue_encoder.joblib`     | Encoder for venue names.                                                   |
| `team_stats.joblib`        | Statistics for team performance.                                           |
| `venue_stats.joblib`       | Statistics for venue performance.                                          |
| `ipl_data.csv`             | Dataset for training models (teams, venues, scores, outcomes).             |

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Please ensure code follows PEP 8 and includes tests where applicable. For major changes, open an issue to discuss first.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credits

- **Creator**: Siddharamayya ([siddharamayya.in](https://siddharamayya.in))
- **Technologies**:
  - Flask for the web framework.
  - XGBoost, scikit-learn, pandas, numpy for machine learning.
  - Tailwind CSS, Poppins font, and modal for styling.

## Contact

For feedback or inquiries, visit [siddharamayya.in](https://siddharamayya.in).

---
