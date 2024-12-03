
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

### Additions to Baseline
#### **Predictive Tasks**
1. temporal features
2. helpful/funny

#### **Model**
1. temporal features
Based on the baseline model, we integrated temporal features on the basis of the baseline to better capture the temporal dynamic characteristics of user behavior. First, in the data preprocessing stage, we extracted the time information of the comments from the user comment data and parsed it into datetime format for more accurate time calculation. Then, in feature engineering, for each comment, we additionally constructed a "time interval" feature, which is calculated as the absolute time difference between the comment time and the specified reference time. This feature can reflect the relationship between the comment time and the target time point. After constructing the test set, to ensure feature independence, we removed the "time interval" feature because it is mainly used to calculate sample weights rather than directly input into the prediction features of the model. In the model training stage, we calculated the temporal weight of each data according to the formula np.exp(-time_span / 365), where time_span is the time interval (in days), and the calculated weight value is stored in an array called timeWeight. In this way, we adjusted the time sensitivity of the sample importance so that samples closer to the reference time have a greater weight in the model. Finally, when training the model, we pass the timeWeight array into the model as the sample_weight parameter, so that the model can dynamically adjust the influence of the sample according to the weight. By integrating the time weight, the model can better capture the characteristics of user behavior changing over time, and significantly improve the prediction accuracy of whether the user will recommend a certain game.
2. helpful/funny
In addition to this improvement, we have also made an attempt in another direction, in which we tried to introduce weights (hereinafter referred to as HF weights) based on the helpful and funny information in user comments. First, in the data preprocessing stage, we extracted the numerical information of the helpful and funny fields from the user comment data. For example, the helpful field may mean "15 out of 20 people (75%) think this comment is helpful", while the funny field may mean "5 people think this comment is funny". Then, in the feature engineering stage, we calculated the HF weight according to the formula w = helpful + i * funny, where i is the weight factor used to balance the importance of helpful and funny. The calculated HF weight is added to the dataset as a new feature. After constructing the test set, we removed the "HF weight" feature because it is mainly used as a weight for the sample rather than a prediction feature directly input into the model. In the model training stage, for each set of input features X and target variable y, we store the HF weight in an array called helpfulWeight to record the importance of each sample. Finally, when training the model, we pass this weight array as the sample_weight parameter to the model, so that it can dynamically adjust the influence of the sample according to the HF weight of the comment. By introducing the HF weight, the model can more effectively understand which comments are more valuable for the prediction task, thereby improving the prediction effect of user recommendation behavior.