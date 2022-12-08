import dash
import pandas as pd
import numpy as np
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

app = Dash(__name__)
df = pd.read_csv('fossil-fuel-co2-emissions.csv')
temp = pd.read_csv("annual.csv")

external_stylesheets = [
    {
       
        "href": "https://fonts.googleapis.com/css2?"
        "family=Ubuntu:wght@300&display=swap",
        "rel":"stylesheet", 
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Climate Dashboard"

#--------------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    children=[
    html.Div(
       children = [
           html.H1("CO2 EMISSION BY NATION DASHBOARD",className='header-title'),
           html.P(
                    children="Analyze the carbon emissions"
                    " of different nations and "
                    " global temperature anomalies",
                    className="header-description",
                ),
          ],
           className="header", 
         ), 
    
     html.Div(
     children = [
      html.Div(
          children = [
            html.Div(children = "Country" , className ="menu-title"),
            dcc.Dropdown(id="slct_country",
                 options=[
                          {"label": region, "value": region}
                            for region in np.sort(df.Country.unique())
                            ],
                 multi=True,
                 value=None,
                 className = "dropdown",
                 ),
               ]
            ),  
       
    html.Div(
    children =[
       html.Div(children = "Type" , className = "menu-title"),
       dcc.Dropdown(id="slct_data",
                options=[{"label": data, "value": data}
                        for data in df.columns[2:]
                            ],
                 multi=False,
                 value="Total",
                 className = "dropdown",
                 ),
               ],
             ),  
            ],
           className = "menu",
         ),  

       
    html.Div(id='output_container', children=[],style={'color': '#000','text-align':'center','padding': '20px 0 0 10px'}),
    html.Br(),
    html.Div(children =[
      html.Div(
      children = dcc.Graph(id='co2_graph', figure={}
               ),
               className ="card",
             ),
      html.Div(children = dcc.Graph(id='world_temp', figure={}
              ),
               className = "card",
             ),
      html.Div(children = dcc.Graph(id='world_plot', figure={}
             ),
              className = "card",
            ),
           ],
             className = "wrapper",
         ),
       ]
    )      


    


# ------------------------------------------------------------------------------
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='co2_graph', component_property='figure'),
     Output(component_id='world_temp', component_property='figure'),
     Output(component_id='world_plot', component_property='figure')],
    [Input(component_id='slct_country', component_property='value'),
     Input(component_id='slct_data', component_property='value')],
    
)
def update_charts(region, data):
    dff = df.copy()
    fig = go.Figure()
    
    container = "The countries selected are "
    if region != None:
      for i in region :
          container = container + str(i) + " "
          ds = dff[dff.Country == i]
          fig.add_trace(go.Scatter(x= ds["Year"], y= ds[data],
                     mode='lines',
                     name=i) )  
    fig.update_layout(
            title = "Carbon emissions by Country in million metric tons of C",
            title_x = 0.5,
            font_family="Courier New",
            font_color="black",
            title_font_family="Times New Roman",
            title_font_color="black",
            margin= dict(l=60, r=60, t=50, b=50),
            legend_title ="Country",
            yaxis = dict(
            title = str(data) + " value" ,zeroline=True,
            
      showline = True),
             xaxis = dict(
      title = "Year",zeroline=True,
      showline = True
)  
 ),
    
    #_______________________________________________________________
    
   
     
    fig2 = go.Figure()
    for i in ["GISTEMP","GCAG"]:
       ds = temp[temp.Source == i]
       fig2.add_trace(go.Scatter(x=ds["Year"], y=ds['Mean'],
                    mode='lines',
                    name=i))
    
    
    
    
    
    fig2.update_layout(height = 600,title = "Average global mean temperature anomalies in degrees Celsius relative to a base period:GISTEMP: 1951-1980 GCAG : 20th century average",title_x = 0.5 )   
    #fig2.layout.plot_bgcolor = '#fff'        
    #fig2.layout.paper_bgcolor = '#F2F2F2'
    fig2.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='black')
    fig2.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='black')
    #fig2.add_annotation(text="GISTEMP: 1951-1980 <br> GCAG : 20th century average (base period)")
   #___________________________________________________________________
    
    fig1 = px.choropleth(df,animation_frame="Year", locationmode='country names',
        locations='Country', animation_group="Country",
           color=data, hover_name="Total" ,width=1250,height=800,title = "World Carbon Emissions by " + str(data) +" (million metric tons of C)",
           )
    
    #fig1.layout.paper_bgcolor = '#ceaf87'
    #fig1.layout.plot_bgcolor = '#ceaf87'
    fig1.update_layout(title_x=0.5)
    fig1["layout"].pop("updatemenus") # optional, drop animation buttons

    return container,fig,fig2,fig1























if __name__ == '__main__':
    app.run_server(debug=True)

