import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from django.db.models import Avg, Count

from django_plotly_dash import DjangoDash
import plotly.express as px

from mainapp.models import Category

app = DjangoDash('SimpleExample')   # replaces dash.Dash

qs = Category.objects.exclude(parent_category=None)
qs = qs.annotate(
    order_count=Count('product__order'),
    average_price=Avg('product__order__price')
)
df = pd.DataFrame([
    {
        "name": i.name,
        "order_count": i.average_price
    } for i in qs
]
)

print("!!!!!!!!!!!")

fig = px.histogram(df, x='order_count')

app.layout = html.Div([
    dcc.RadioItems(
        id='dropdown-color',
        options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
        value='red'
    ),
    html.Div(id='output-color'),
    dcc.RadioItems(
        id='dropdown-size',
        options=[{'label': i,
                  'value': j} for i, j in [('L','large'), ('M','medium'), ('S','small')]],
        value='medium'
    ),
    html.Div(id='output-size'),

    dcc.Graph(
        id="test-graph",
        figure=fig
    )
])

@app.callback(
    dash.dependencies.Output('output-color', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value')])
def callback_color(dropdown_value):
    return "The selected color is %s." % dropdown_value

@app.callback(
    dash.dependencies.Output('output-size', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value'),
     dash.dependencies.Input('dropdown-size', 'value')])
def callback_size(dropdown_color, dropdown_size):
    return "The chosen T-shirt is a %s %s one." %(dropdown_size,
                                                  dropdown_color)