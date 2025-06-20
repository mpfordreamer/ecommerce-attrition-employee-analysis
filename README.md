# Solving Challenges for an Edutech Company

## Business Understanding

The Edutech company, Jaya Jaya Maju, faces a challenge in retaining its employees, with an employee **attrition** rate that needs to be understood and managed. A high attrition rate can have a significant impact on recruitment costs, productivity, and overall employee morale. Based on initial data, approximately **16.92%** of employees have experienced attrition, which is the main focus of this analysis. The Human Resources (HR) management at the Edutech company needs to understand the driving factors of attrition to design effective retention strategies and create a better work environment.

### Business Problems

The business problems to be solved through this project are:
1.  Identifying the key demographic, job-related, and behavioral factors that most influence an employee's decision to leave the company.
2.  Building a predictive model that can identify employees at high risk of attrition.
3.  Providing a basis for a dashboard tool for the HR team to continuously monitor attrition trends and risk factors, which will help in:
    *   Proactively reducing the attrition rate.
    *   Optimizing costs related to recruitment and talent loss.
    *   Improving employee satisfaction and loyalty.

### Project Scope

This project includes the following steps:
1.  **Exploratory Data Analysis (EDA)**: Understanding the `employee_data.csv` dataset, variable distributions, and initial patterns related to attrition.
2.  **Data Preparation**: Cleaning the data (handling missing values, outliers if relevant), encoding categorical features, and scaling numerical features.
3.  **Analysis of Attrition Factors**: Using statistical analysis (Cramér's V) and feature importance from machine learning models to identify key predictors.
4.  **Predictive Modeling**: Building and evaluating several classification models, with a focus on an `ExtraTreesClassifier` optimized using Optuna to predict attrition.
5.  **Preparing Output for Dashboard**: Exporting prediction results and relevant data to CSV and SQLite database formats for further visualization.
6.  **Conclusion and Recommendations**: Summarizing findings and providing strategic recommendations to the Edutech management.

### Preparation

**Data Source**: The dataset used is `employee_data.csv` provided by Dicoding, containing demographic, job, and employee satisfaction information. Link: [https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/refs/heads/main/employee/employee_data.csv](https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/refs/heads/main/employee/employee_data.csv)

**Environment Setup**:
This project was developed using Python in a Jupyter Notebook environment.
1.  **Running `notebook.ipynb`**:
    *   Ensure all dependencies and libraries listed in the `requirements.txt` file are installed in your environment. This file can be created by running `pip freeze > requirements.txt` at the end of the notebook.
    *   Run the cells in the notebook sequentially to replicate the analysis, modeling, and results. This will generate an SQLite database file in the `model/metabase.db` directory.
2.  **Running the Dashboard (using Metabase with Docker)**:
    The prediction results and feature analysis are stored in an SQLite database (`model/metabase.db`) that can be connected to Metabase.
    *   Ensure Docker is installed on your system.
    *   Pull the Metabase image (if you don't have it): `docker pull metabase/metabase:latest` (or a specific version you use, e.g., v0.46.4).
    *   Run the Metabase container with the following command from your main project directory (the one containing the `model` folder):
        ```bash
        docker run -d \
          --name dashboard_employee \
          -p 3000:3000 \
          -v ${PWD}/model:/metabase-data \
          metabase/metabase
        ```
        *   **Command Explanation:**
            *   `-d`: Runs the container in the background (detached mode).
            *   `--name dashboard_employee`: Gives the container a name.
            *   `-p 3000:3000`: Maps port 3000 on the host to port 3000 in the container.
            *   `-v ${PWD}/model:/metabase-data`: This is the important part. This command mounts the `model` directory from your current working directory (`${PWD}/model`) to the `/metabase-data` directory inside the Metabase container. Your `metabase.db` file, located at `model/metabase.db`, will be accessible from inside the container via the path `/metabase-data/metabase.db`.
    *   Access Metabase through your browser at `http://localhost:3000`.
    *   During the initial Metabase setup (or when adding a new database):
        1.  Select "Let's get set up."
        2.  Fill in the admin user information.
        3.  In the "Add your data" section, you can select "I'll add my data later" or add it immediately:
            *   Select Database type: **SQLite**.
            *   Display name: (e.g.) `Employee Attrition DB`
            *   Filename: `/metabase-data/metabase.db` (This is the path to your SQLite file *inside the Docker container*, according to the volume mapping above).
    *   Create questions and dashboards in Metabase using the `employee_predictions`, `feature_importance`, and `employee_data` (cleaned) tables from the database you just connected.

---

## Business Dashboard

The interactive dashboard built in Metabase will help the Edutech HR team to:
1.  **Monitor Attrition Rates**: View the proportion of employees predicted to attrite and compare it with actual data (if available periodically).
2.  **Analyze Key Risk Factors**:
    *   Visualize feature importance, showing factors like `OverTime`, `MaritalStatus`, and `TotalWorkingYears` as the main drivers.
    *   See the distribution of high-risk employees based on key characteristics.
3.  **Identify At-Risk Employee Segments**: Filter and view details of employees predicted to have a high probability of attrition.

To access the dashboard (after local setup as guided above):
*   **Local Access Link (Metabase via Docker):** `http://localhost:3000`
    *   After logging in and connecting the SQLite database (`model/metabase.db`, accessed as `/metabase-data/metabase.db` within Metabase), navigate to the collection or dashboard created for the Edutech employee attrition analysis.

---

## Conclusion

This project successfully identified the significant factors influencing attrition at the Edutech company and built an `ExtraTreesClassifier` model to predict employees at risk of leaving.

**Key Factors Causing Attrition:**
Based on the feature importance analysis from the `ExtraTreesClassifier` model:
1.  **`OverTime`**: This is the strongest predictor (score ~0.42), indicating that employees who frequently work overtime have a very high risk of attrition.
2.  **`MaritalStatus`**: Marital status is the second most significant predictor (score ~0.20). Further analysis from previous data showed that 'Single' status has the highest proportion of attrition.
3.  **`TotalWorkingYears`**: The employee's total working years also shows a significant contribution to the prediction (score ~0.09).
4.  Other features such as **`MonthlyIncome`** (score ~0.06) and **`Age`** (score ~0.06) also contribute moderately.

**Best Predictive Model (`ExtraTreesClassifier`):**
The `ExtraTreesClassifier` model, after hyperparameter optimization using Optuna (with best parameters: `{'n_estimators': 215, 'max_depth': 11, 'min_samples_split': 0.13399970021595703, 'min_samples_leaf': 0.04206053437992983}`), showed the following performance on the test data:
*   **Accuracy**: 74.06%
*   **Recall (for Attrition=Yes)**: 0.61 (The model successfully identified 61% of the employees who actually attrited)
*   **F1-Score (for Attrition=Yes)**: 0.44
*   **Precision (for Attrition=Yes)**: 0.35
*   **Confusion Matrix**: The model identified 22 True Positives and 135 True Negatives, with 14 False Negatives and 41 False Positives. The focus on recall (0.61) is important to minimize the risk of losing potential employees, although the precision (0.35) indicates some false positive predictions.

### Recommended Action Items (Optional)

- **Prioritize `OverTime` Management**:
    Given that `OverTime` is the dominant factor, conduct a deep evaluation of overtime policies and culture. Identify the causes of excessive overtime (workload, inefficiency, understaffing) and find solutions to reduce it. Note that simulating a reduction in overtime (from previous analysis) could increase overall accuracy but decrease the ability to detect actual attrition cases (Recall). Reduction strategies must be carefully planned.
- **Focus on `MaritalStatus`**:
    Investigate further why employees with a certain marital status (e.g., 'Single') are more prone to attrition. Consider support programs, benefits, or work flexibility that may be relevant for this segment.
- **In-depth Analysis of `TotalWorkingYears`, `MonthlyIncome`, and `Age` Factors**:
    Understand how the combination of total working years, income level, and age contributes to attrition risk. Employees with fewer total working years may need more intensive mentoring and career development programs. Review the compensation structure for `MonthlyIncome` at various experience and age levels.
- **Continuous Utilization of the Predictive Model**:
    Implement the `ExtraTreesClassifier` model as part of the HR system for proactive identification of high-risk employees. This allows for earlier and more targeted retention interventions. Use the dashboard connected to the prediction results for continuous monitoring by the HR team.

---

## Authors
-   [I  Dewa Gede Mahesta Parawangsa] - [dewamahesta2711@gmail.com]

## Version History
*   **0.1**
    *   Initial Release: Includes data analysis, feature engineering, predictive modeling with `ExtraTreesClassifier`, and preparation for dashboard integration.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
