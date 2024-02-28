# Analysis and Implementation of Flipkart Product Dataset Using Airflow

>This project leverages Airflow for workflow orchestration, Elasticsearch for data storage and retrieval, and Kibana for visualization purposes. The dataset used in this project originates from an E-commerce company and includes product details from both Flipkart and Amazon. The primary objective of this project is to explore potential correlations between discount percentage and product ratings. This project is developed to accomplish milestone 3 of the FTDS Hacktiv8 program. 

**Project Overview**:
1. Project Objective:
   The objective of this project is to implement Airflow for data processing and visualization using Kibana. Specifically, the project aims to explore potential correlations between discount percentages and product ratings sourced from an E-commerce company's dataset.

2. Airflow Process:
   The Airflow workflow entails the extraction of data from PostgreSQL, storing it in a CSV file, performing data preprocessing tasks such as renaming columns, handling missing and duplicate values, and ensuring correct data types. The cleaned data is then uploaded to Elasticsearch for storage and analysis using Kibana for visualization. This process is scheduled to run daily at 6:30 AM (WIB).

3. Great Expectation:
   To ensure data and code quality within Airflow, testing is conducted using Great Expectation with several tests to validate data integrity and pipeline functionality.

4. Analysis and Visualization:
   Cleaned data is visualized and analyzed to uncover insights and answer the project objective regarding the correlation between discount percentages and product ratings. Kibana facilitates the visualization and analysis process, enabling stakeholders to gain valuable insights from the dataset.

>The project combines Airflow's workflow orchestration capabilities with Elasticsearch's data storage and retrieval functionalities, complemented by Kibana's powerful visualization tools, to streamline data processing and analysis workflows while ensuring data quality and integrity through testing with Great Expectation.

For visualization, you can explore the "Image" folder, which contains screenshots captured from Kibana. These screenshots offer a visual representation of the data analysis and insights derived from the dataset using various visualization techniques in Kibana. Feel free to browse through the images to gain a better understanding of the analyzed data and its insights.

Dataset source :  https://www.kaggle.com/datasets/san2deep/flipkart-product-dataset