
### Model Description and Justification

In this task, we aimed to predict whether **User A** would recommend **Game B**. Given the imbalanced nature of our dataset, where the majority of data points represent positive recommendations, our model choice and preprocessing strategy were crucial for ensuring robust and fair performance across classes.

#### Data Imbalance Challenge and Preprocessing

The primary challenge we encountered was the severe class imbalance, with significantly more positive recommendations than negative ones. This imbalance risked biasing the model towards over-predicting the majority class. To address this, we explored various resampling techniques:

1. **SMOTE (Synthetic Minority Oversampling Technique):** Created synthetic samples for the minority class to balance the dataset.
2. **Undersampling:** Reduced the majority class size to match the minority class.
3. **SMOTEENN (Combination of SMOTE and Edited Nearest Neighbors):** Combines oversampling and noise removal, which provided the best results by improving the minority class representation and removing borderline or noisy samples.

After preprocessing the data with SMOTEENN, we achieved a balanced dataset for training and proceeded to model selection.

#### Model Selection

We evaluated several machine learning algorithms to identify the one that best fit our task:

1. **K-Nearest Neighbors (KNN)**
2. **Logistic Regression** 
3. **Gradient Boosting**
4. **XGBoost**
5. **Support Vector Machine (SVM)** 
6. **Random Forest** 

Random Forest was ultimately chosen as our final model after the test on each algorithm.

#### Optimization and Evaluation

To optimize the model, we used the following strategies:

1. **Number of Neighbors (`n_neighbors`)**: We experimented with different values for `n_neighbors` and found that a value of **150** produced the best results.
2. **Weighting (`weights`)**: We used the `uniform` weighting method, where all neighbors contribute equally to the prediction, as it performed adequately given the nature of the data.

#### Challenges Encountered

- **Data Imbalance:** Initially, models were biased towards the majority class, but the combination of SMOTEENN and class weight balancing addressed this effectively.
- **Scalability:** One of the challenges we encountered with KNN was scalability, particularly with larger datasets. Since KNN requires calculating the distance between a test sample and every training sample, the computational cost can grow exponentially with the size of the dataset. To mitigate this, we used a reduced dataset by splitting the data into training and test sets, and applied SMOTEENN to balance the classes.
- **Overfitting:** KNN is prone to overfitting, especially when the number of neighbors is small. However, by choosing an appropriate value of `n_neighbors` (150 in our case), we were able to strike a balance between underfitting and overfitting. 

#### Strengths and Weaknesses of Models Compared

| Model                   | Strengths                                                    | Weaknesses                                                   |
| ----------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **KNN**                 | Simple and interpretable; works well for small datasets.     | Sensitive to class imbalance; computationally expensive for large datasets. |
| **Logistic Regression** | Easy to implement and interpretable.                         | Struggles with non-linear relationships; limited performance on complex datasets. |
| **Gradient Boosting**   | Captures complex patterns; good performance on imbalanced datasets. | Long training times; sensitive to hyperparameter tuning.     |
| **XGBoost**             | Highly efficient and powerful; good handling of missing values and class imbalance. | Computationally intensive; prone to overfitting without careful tuning. |
| **SVM**                 | Effective for small datasets; robust to outliers.            | Scalability issues for large datasets; sensitive to noise.   |
| **Random Forest**       | Handles imbalance well; robust against noise; interpretable through feature importance. | Relatively slower predictions compared to simpler models; potential overfitting with large trees. |
