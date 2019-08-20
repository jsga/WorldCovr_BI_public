# WorldCovr retention metrics dashboard

This repository contains the code necessary to create a dashboard that displays customer retentions metrics and results in a synthetic and visual manner.

Access the dashboard alive [here](https://worldcover-bi-public.herokuapp.com/).

The dashboard contains simulated data and any resemblance with real data is not intended at all.

## The dashboard

The dashboard is built using a Plotly-dash framework. Dash is a framework for building quick and good-looking analytical web applications. It is built on top of Flask, it can be easily customised and embedded anywhere.

The app is structured as follows:

- `app.py` is the main file. The skeleton of the app and the callbacks are defined here.
- `pages/` folder containing a file for each page. The layout of each page is defined here.
- `utils/` collection of scripts used for data preparation, plotting and layout.
- `data/` contains the data input in csv format.
- `asserts/` contains css files and image files
- `requirements.txt`list of python required packages



### Access the dashboard online [here](https://worldcover-bi-public.herokuapp.com/) 

The app is freely hosted on Heroku and available via [this link](https://worldcover-bi-public.herokuapp.com/). Please keep in mind the speed of the response might not be as fast as if the app was hosted on a premium service hosting. Heroku has been configured so that the dashboard re-builds automatically when the master branch is pushed.


### Run the app locally

1. Clone or download the repository `git clone https://github.com/jsga/WorldCovr_BI_public .`
2. Place the provided csv files in folder `data/`
3. Make sure your terminal is located in the main folder of the app
4. Create a Python3 virtualenv `virtualenv -p python3 .venv`
5. Activate the virtualenv `source .venv/bin/activate`
6. Install the requirements `pip install -r requirements.txt`
7. Run the app: `python3 app.py`
8. Open your browser and visit [http://127.0.0.1:8050/](http://127.0.0.1:8050/). Enjoy!


## List of future work

Future work splits into two possible sub-tasks: data analytics and dashboard development.

From the **data analysis** point of view, the future tasks are:

- Calculate and display further customer metrics:
    - Churn rate
    - Customer lifetime value
    - Cost of acquiring a customer
- Use the available data to create a machine learning model that predicts the customer churn. Then, inspect this model and gain insights from churned customers and their common characteristics. We could also predict the number of future customers and assess the uncertainty.
- Design a statistical experiment (marketing campaign, or a customer survey) to define what marketing strategy works best.
- Season is placed in 2 different tables inside the database. This is not ideal, changing it should be considered. If the two columns refer to a different type of season it should be noted somewhere.

In terms of **software development**, some of the possible future tasks are:

- Fetch real-time data from database
- Save state of the app via url. This would make the app really easy to share between collaborators.
- Create unity tests to make sure all elements function correctly and that inputs to functions are defined correctly.
- Assess whether the app should be contained inside a docker image.


There are various **questions** that I believe they are not completely relevant for this exercise, however, they would be if the analysis was done as a real business case:

- Some rows, like _gender_, have a lot of missing values (61%). Can we find information from customers from somewhere else?
- I did not consider the row _"status"_ in community_payout. I should find out more on the meaning of it.
- Column "date_issued" in customer_policy indicates that Worldcover receives a payment. What then means date_priced?
- What happened in 2018 to gain so many customers at once?
- Besides the region: is the subregion a relevant factor?
