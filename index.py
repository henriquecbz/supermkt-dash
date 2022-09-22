from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

app = Dash(__name__)

df_data = pd.read_csv("supermarket_sales.csv")
df_data["Date"] = pd.to_datetime(df_data["Date"])

cities = df_data["City"].unique()

#============ Layout ==========#
app.layout = html.Div(children=[    
    html.H5("Cidades", id='available-cities'),
    dcc.Checklist(options= cities, value= cities, id='check_city'),
    html.Hr(),
    html.H5("Variável de análise", id= 'variables'),
    dcc.RadioItems(options=["gross income","Rating"], value='Rating', id='main_variable'),
    html.Hr(),
    
    dcc.Graph(id='city_fig'), 
    dcc.Graph(id='payment_fig'),
    dcc.Graph(id='income_per_product')
])

#============ Callbacks ========#
@app.callback([
        Output('city_fig','figure'),  
        Output('payment_fig','figure'),
        Output('income_per_product','figure'),
        ],
        [
        Input('check_city','value'),
        Input('main_variable','value'),
        ])
def render_graphs(cities, main_variable):

    operation = np.sum  if main_variable == "gross income" else np.mean
    df_filtered = df_data[df_data["City"].isin(cities)]

    df_city = df_filtered.groupby("City")[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby("Payment")[main_variable].apply(operation).to_frame().reset_index()
    df_product_income = df_filtered.groupby(["Product line","City"])[main_variable].apply(operation).to_frame().reset_index()

    fig_city = px.bar(df_city, x = "City", y = main_variable)
    fig_payment = px.bar(df_payment, y = "Payment", x = main_variable, orientation="h")
    fig_product_inome = px.bar(df_product_income, x = main_variable, y = 'Product line', color ="City", orientation="h")

    fig_city.update_layout(margin= dict(l=0,r=0,t=20,b=20), height= 200)
    fig_payment.update_layout(margin= dict(l=0,r=0,t=20,b=20), height= 200)
    fig_product_inome.update_layout(margin= dict(l=0,r=0,t=20,b=20), height= 500)
   
    return fig_city,fig_payment,fig_product_inome

#============ Server ========#
if __name__ == '__main__':
    app.run_server(debug=True)





