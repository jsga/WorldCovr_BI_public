import dash_html_components as html
import dash_core_components as dcc


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.A(
                        html.Img(
                            src=app.get_asset_url("logo.png"),
                            className="logo"
                            ),
                        href="https://www.worldcovr.com/",
                        ),

                    html.A([
                        html.Button("About", id="learn-more-button"),
                        ],
                        href="http://jsaezgallego.com/en/",
                        ),
                    ],
                className="row",
                ),
            html.Div(
                [
                    html.Div(
                        [html.H5("WorldCover customer analysis")],
                        className="seven columns main-title",
                        ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/full-view",
                                className="full-view-link",
                                )
                            ],
                        className="five columns",
                        ),
                    ],
                className="twelve columns",
                style={"padding-left": "0"},
                ),
            ],
        className="row",
        )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link("Retention analysis", href="/overview", className="tab first"),
            dcc.Link("Comments and Conclusions", href="/comments-conclusions", className="tab"),
            dcc.Link("Future work prediction model", href="/prediction-model", className="tab"),
            ],
        className="row all-tabs",
        )
    return menu
