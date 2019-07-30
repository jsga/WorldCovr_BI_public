import dash_html_components as html
from utils.utils_layout import Header


def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 6
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Customer retention prediction model", className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.P(
                                                '''This is an experimental feature that I would add if I had the time. The basic idea is to predict whether a 
                                                customer will churn (stop using our service) or not. Building a model that predicts such events could be 
                                                useful for several reasons:'''),
                                            html.P(
                                                '''   1. We could take into account all significant factors at once, considering interactions between them. 
                                                For example, gender and phone together.'''),
                                            html.P('''   2. We could predict the number customers we will retain on the upcoming season.'''),
                                            html.P(
                                                '''   3. We could obtain an estimation of the uncertainty of the number of future customers and perform 
                                                worst-case situation analysis, etc.'''),
                                            html.P(
                                                '''   4. We could inspect the model and identify which features are common to the customers that churn. Once 
                                                the key factors of customers retention are identified, we could target our marketing efforts in those 
                                                features.''')
                                            ],
                                        # style={"color": "#7a7a7a"},
                                        ),
                                    ],
                                className="row",
                                ),
                            html.Div(
                                [   html.Br([]),
                                    html.H6("Modeling steps", className="subtitle padded"),


                                    html.Div(
                                        [html.P(''' The steps I would follow to achieve the machine learning model are the following:'''),
                                         html.Li(
                                             '''Gather relevant data. Can we find more characteristics of our customers than just gender and income level?'''),
                                         html.Li('''Visualize the data. Make sure all columns are understood and contain no errors.'''),
                                         html.Li(
                                             '''Model-building. Start with a simple logit model and iterate until a decent level of accuracy is achieved. Use 
                                             a cross-validation schema to make sure we are not overfitting.'''),
                                         html.Li(
                                             '''Learn insights from the model itself and the outcome. What are the features statistically significant? How do 
                                             changes in such features affect the probability of a customer to churn?'''),
                                         html.Li(
                                             '''Display model outcomes in a dashboard, share the results and suggest some specific data-driven actions. The 
                                             model could be used via an API if needed by other members of the organization.'''),
                                         ],
                                        id="reviews-bullet-pts",
                                        ),
                                    ],
                                className="row",
                            ),
                        ],
                        className="row ",
                    )
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
