# Fake Job Predictor
This Python machine learning model predicts whether a job posting is fake or not. I used the Employment Scam Aegean Dataset (EMSCAD)  https://www.kaggle.com/datasets/amruthjithrajvr/recruitment-scam to train my model.

Demo pictures: https://drive.google.com/drive/folders/1WVsrN53hPrcKOtXrnT5_sUK6bhepNv4V?usp=share_link

# Problem
College students and early career graduates search the job market for opportunities but unfortunately come across fraudulent job postings (via social media platforms, advertisements, job sites, and electronic communication) that present as legitimate. Although they the scammer job posts seem real, they have the ill intention of taking the personal information and perhaps money from innocent job seekers. 

# Process, Research, and Interpreting Data
Two algorithms were tested- Naive Bayes algorithm and Decision Tree Classifier algorithm. First, the data was cleaned. I removed missing data, html tags (from the web scrapping), and removed irrelevant columns. Next, I began created a pie chart visualizing the percentage of job postings that were fraudulent and the percentage of real ones.

<img width="640" height="498" alt="image" src="https://github.com/user-attachments/assets/d2b9f102-416f-4068-94ac-af69d26a21f9" />

Luckily, the dataset had an equal representation of both cases.

Then, I made a bar chart visualizing the top 10 countries with the most job postings. United States has a substantial amount of job postings than any other country.

<img width="1014" height="786" alt="image" src="https://github.com/user-attachments/assets/4d2534b4-fd8b-426c-976b-ed1945861455" />

Then, I made a bar chart visualizing the amount of job postings for every experience level. Mid-senior and entry level job postings were the highest among the other experience levels. Surprisingly, the number of internships were low. 

<img width="1005" height="837" alt="image" src="https://github.com/user-attachments/assets/77fb70f5-03c1-4551-b64a-0048de45a885" />

Finally, I made WordClouds to see the most common words used in the job postings. 

<img width="794" height="524" alt="image" src="https://github.com/user-attachments/assets/920f1b67-a28e-4aa2-9843-25055fff7604" />

# Model Evualuation

1. Multinomial Naive Bayes - This is a popular algorithm that relies on probability to make its categorical decisions on text data.
Classification Accuracy: 0.8961538461538462
Confusion Matrix:

<img width="785" height="602" alt="image" src="https://github.com/user-attachments/assets/d887e616-ba47-401c-86d7-29fc3b4658d8" />

2. Decision tree Classifier - This algorithm operates on set "rules" to categorize text data.
Classification Accuracy: 0.8384615384615385
Confusion Matrix:

<img width="785" height="602" alt="image" src="https://github.com/user-attachments/assets/9492400c-6094-40c4-b2f4-1673afcca168" />

# Conclusion
I used the Multinomial Naive Bayes algorithm for the web app because its classification accuracy is 89.62%, whereas the Decision Tree Classifier algorithim was only 83.85% accurate. 

# Tech Stack Used
- Numpy
- Pandas
- Matplotlib
- Imbalanced-learn
- Wordcloud
- Natural Language Toolkit
- Multinomial Naive Bayes (scikit-learn)
- Decision tree classifier (scikit-learn)
- Flask










