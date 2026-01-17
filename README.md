###### **Movie Data Pipeline (ETL Project)**



**Overview**



This project implements a simple ETL (Extract, Transform, Load) pipeline using Python, the OMDb API, and MySQL. The pipeline extracts movie and rating data, enriches movie records using the OMDb API, transforms and cleans the data, and loads it into a relational database. The final dataset supports analytical queries for interview-style problem solving.





------------------



**Project Structure**



* etl.py : Python script that performs extract, transform, and load operations
* schema.sql : SQL file to create database tables and constraints
* queries.sql : SQL file containing analytical queries
* requirements.txt : Python dependencies
* README.md : Project documentation



------------------



**Environment Setup and Execution**



**Prerequisites**



* Python 3.8 or higher
* MySQL Server
* Valid OMDb API key





**Install Dependencies**



* Run the following command in the project directory:

  pip install -r requirements.txt



* Database Setup

  Create the database and tables by running:

  SOURCE schema.sql;



* Run the ETL Pipeline

  Execute the ETL script using:

  python etl.py



The script reads data, calls the OMDb API, handles errors, and loads valid records into MySQL.



* Run Analytical Queries

  After successful ETL execution, run:

  SOURCE queries.sql;





------------------





**Design Choices and Assumptions**



**Design Choices**



* OMDb API is used to enrich movie metadata.
* MySQL is used for structured storage and relational integrity.
* Foreign key constraints ensure valid relationships between movies and ratings.
* Error handling allows the ETL to continue when movies are not found.





**Assumptions**



* Some movies may not exist in the OMDb API.
* Missing fields such as director or ratings are expected.
* Ratings are inserted only when the corresponding movie exists.







---------------------



**Challenges and Solutions**



* OMDb Movie Not Found Errors

  Handled using conditional checks and logging so the pipeline continues without failure.



* API Retry and Timeout Issues

  Requests are limited and failed calls are skipped to prevent infinite execution.



* Foreign Key Constraint Errors

  Movies are inserted before ratings and validated before loading rating data.



* NULL Values in Query Results

  SQL functions such as COALESCE are used to handle missing values.





---------------------



**Conclusion**



This project demonstrates a complete end-to-end ETL pipeline for movie data. It integrates external API data with CSV sources, handles real-world challenges like missing or inconsistent data, and stores cleaned data in a structured relational database. The solution allows for meaningful analysis through SQL queries and showcases practical data engineering skills, including data extraction, transformation, loading, and error handling. This pipeline can be extended or scaled for larger datasets and more complex analytics in a production environment.


