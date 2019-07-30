import dash_html_components as html
from utils.utils_layout import Header
import dash_core_components as dcc


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
                                    html.H6("Conclusions", className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.P(
                                                "From the available data we can answer the following questions:",
                                                style={"color": "#000000"}),
                                            html.Li("Do retention patterns vary by geographic zone?"
                                                    , style={"color": "#000000"}),
                                            html.P(
                                                '''Generally speaking, there is not much difference in retention rates over different regions. However, 
                                                we can roughly say there are three regional groups:'''),
                                            html.P(
                                                "  1. AH and BA: are the newest areas with customers."
                                                ),
                                            html.P(
                                                "  2. NP, UE and UW: do not have new customers, only old ones. 2018 major was really popular on this group, especially in NP. "
                                                "Most of the current customers in 2019 come from that year. However, in absolute numbers they are quite "
                                                "small. We could investigate further what makes this group and 2018 major special."
                                                ),
                                            html.P(
                                                "  3. TV: Irrelevant region with 4 new customers in total."
                                                ),

                                            html.Li(
                                                "Are retention rates and insurance premium amounts influenced by external factors, such as customers "
                                                "experiencing drought (and receiving a payout) in a prior cropping season?",
                                                style={"color": "#000000"}),
                                            html.P(
                                                "There are indeed some differences. For example, looking back at 2018 major, it is clear that customers "
                                                "that received a payment (982, 16% of them) purchased another policy in 2019 major. Amongst customers that "
                                                "did not receive a payment only 86 (1%) purchased again a policy."),
                                            html.P(
                                                "Looking at the fractions for different dates, it seems that receiving a premium has an influence: generally "
                                                "speaking, the chances of having a customer purchase again increase by 10%"),

                                            html.Li(
                                                "Do other socio-demographic factors have an influence on customer retention patterns?",
                                                style={"color": "#000000"}),
                                            html.P(
                                                '''To answer this question rigorously, a proper statistical analysis that accounts for all variables at once 
                                                should be done. See tab 'Future work: prediction model' for further information.'''
                                                ),
                                            html.P(
                                                "Generally speaking, retention rates amongst rice farmers seems the highest. Also, customers with a phone are "
                                                "more likely to purchase a policy for more than one season."
                                                )

                                            ],
                                        style={"color": "#7a7a7a"},
                                        # ),
                                        ),
                                    ],
                                className="row",
                                ),
                            html.Div(
                                [
                                    html.H6("Open questions and possible improvements", className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.P("There are some question left unanswered:", style={"color": "#000000"}),
                                            html.Li(
                                                "Churn rate is as important as retention ratios and also a popular metric. Display it too."
                                                ),
                                            html.Li(
                                                '''We have analyzed the revenue. How about the benefits? Growth measures should also take into account 
                                                the amount of premiums paid to communities.'''
                                                ),
                                            html.Li(
                                                '''What is the customer lifetime value (LTV) across different groupping variables? How about the cost of 
                                                acquiring a customer?'''
                                                ),
                                            html.Li(
                                                '''Can we design a statistical experiment (marketing campaign) to test what strategy works best? Can we send a 
                                                survey to existing customers and define some data-driven actions?'''
                                                ),

                                            ],
                                        id="reviews-bullet-pts",
                                        style={"color": "#000000"}
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
