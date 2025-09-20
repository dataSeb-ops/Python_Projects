# Mobile App Market Analysis: Google Play vs. App Store

This project analyzes mobile app data from both the Google Play Store and the Apple App Store, focusing on free apps for an English-speaking audience.  
The goal is to clean, explore, and compare datasets from the two major platforms to identify trends and ultimately recommend app genres likely to succeed across both markets.  

---

## 📊 Dataset Sources

- **Google Play Store Apps Dataset (Kaggle)**  
  [Link](https://www.kaggle.com/datasets/lava18/google-play-store-apps)  
  Contains metadata for apps in the Google Play store, including ratings, installs, reviews, size, category, and pricing.

- **Apple App Store Apps Dataset (Kaggle)**  
  [Link](https://www.kaggle.com/datasets/ramamet4/app-store-apple-data-set-10k-apps)  
  Contains metadata for iOS apps, including ratings, reviews, category, and pricing.

---

## 🗂 Project Structure

mobile_app_analysis/
│
├── data_raw/ # CSVs with raw data
│ ├── googleplaystore.csv
│ ├── AppleStore.csv
│
├── mobile_app_analysis.ipynb # Jupyter notebook with full analysis
├── mobile_app_analysis.py # Python script alternative to Jupyter notebook
└── README.md


---

## ⚙️ Methods

- **Data Cleaning:**  
  - Handled missing values and duplicates.  
  - Converted installs, ratings, and reviews to numeric format.  

- **Exploratory Analysis:**  
  - Distribution of app ratings and reviews.  
  - Most common/popular app categories.  

- **Cross-Platform Comparison:**  
  - Identified genres with strong presence and engagement on both platforms.
  - This helps developers understand what types of apps will perform well in both markets.

---

## 📈 Key Findings

- **User Behavior:** Free apps dominate both stores, but paid apps on iOS are relatively more common.  
- **Ratings & Engagement:** Genres like *Games* and *Entertainment* draw the highest number of installs/reviews.  
- **Cross-Platform Trend:** Genres such as *Productivity* and *Lifestyle* maintain steady popularity across both stores, suggesting good long-term viability.  

---

## ✅ Recommendation

Based on trends in both datasets, the **“Lifestyle / Productivity”** genre shows strong engagement and consistent ratings on both iOS and Android.  
This makes it a promising category for developers seeking cross-platform success.  

---

## 🔮 Future Work

- Include financial performance (e.g., in-app purchases, revenue if data available).  
- Expand analysis to newer datasets (post-2023).  
- Explore regional breakdowns to see if preferences differ by market.  

---

## ▶️ How to Reproduce

1. Clone this repo:  
   ```bash
   git clone https://github.com/dataSeb-ops/Python_Projects/mobile-app-analysis.git
2. To run the analysis, either
   - Open mobile_app_analysis.ipynb in Jupyter and run all cells, **OR**
   - Execute the Python script mobile_app_analysis.py using your preferred method

___
  
📎 License
Dataset is provided by Kaggle. Analysis © 2025 Briana Sebastian.
