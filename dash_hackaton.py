### PROJET DASH MORITZ ###

import dash
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np  # pip install dash (version 2.0.0 or higher)
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.CYBORG])

colors = {
    'background': '#000000', 
    'text': '#7FDBFF'
}

# on clear un peu et on fait des moyennes
df = pd.read_csv("D:\Cours_2021-2022\Semestre_3\dashboard_moritz\CLAUDE_DILETTA_ROUSSEAU.csv")
df['INNOVATION']= (df['UTILITE_INNOVATION'] + df['INFORMATION_INNOVATION'])/2
df['INTERET_PARTICIPANT'] = (df['INTERET_PARTICIPANT1'] + df['INTERET_PARTICIPANT2'])/2
df['NETWORKING']= (df['NETWORKING1'] + df['NETWORKING2'] + df['NETWORKING3'] + df['NETWORKING4'] + df['NETWORKING5'])/5
df['SELF_IMPROVEMENT'] = (df['SELF_IMPROVEMENT1']+df['SELF_IMPROVEMENT2'])/2
df.drop(df.iloc[:, 0:19], inplace=True, axis=1)
df = df.drop('Network ID', axis=1)
df['SATISFACTION_GLOBAl']= round(df['SATISFACTION_GLOBAl']/2)


#______________________________________________________________________________________
# App layout
app.layout = html.Div([

    html.H1("Dashboard Hackaton", style={'text-align': 'center', 'color': '#7FDBFF', 'font-size': 35}),
    html.Br(),
    


        html.Div([
            html.Div(id='container_variables'), #1
            
            dcc.Checklist(                      #2
                id='lst_vrbl',
                options=[
                         #{'label': x, 'value': x, 'disabled':False}
                         #for x in df.columns[8:13]
                         {'label' : 'Innovation', 'value' : 'INNOVATION'},
                         {'label' : 'Interet personnel', 'value' : 'INTERET_PARTICIPANT'},
                         {'label' : 'Networking', 'value' : 'NETWORKING'},
                         {'label' : 'Amélioration Personnelle', 'value' : 'SELF_IMPROVEMENT'},
                ],
                style={'color': '#7FDBFF' , 'font-size': 20},
                inputStyle={"margin-right": "5px", "margin-left": "10px"},
                value=df.columns[8:13],
                inline = True
            ),
        ]),
        html.Br(),
        
        html.Div(id='container_sex'),       #3
        
        dcc.Checklist(                      #4
            id = 'lst_sex',
            options=[
                {'label' : "Homme", 'value' : 1},
                {'label' : 'Femme', 'value' : 0}],
            style={'color': '#7FDBFF' , 'font-size': 20},
            inputStyle={"margin-right": "5px", "margin-left": "10px"},
            value=[0,1]),
        html.Br(),
        
        html.Div(id='container_cat'),       #5
        
        dcc.Checklist(                      #6
            id = 'lst_cat',
            options=[
                {'label' : "Etudiant", 'value' : '15-25 ans/étudiant'},
                {'label' : 'Professionnel', 'value' : '26 ans et plus /Pro'}],
            style={'color': '#7FDBFF' , 'font-size': 20},
            inputStyle={"margin-right": "5px", "margin-left": "10px"},
            value=['15-25 ans/étudiant','26 ans et plus /Pro']),
        html.Br(),

        html.Div([
            dcc.Graph(id='graph'),      #7
        html.Br(),
        
        html.Div(id='container_note'),      #8
        html.Br(),
        
        dcc.RangeSlider(0, 10,              #9
                        id = 'slider_note',
                        value=[0, 10],
                        step =1,
                tooltip={"placement": "bottom", "always_visible": True})
    ]),

])
    
#______________________________________________________________________________________
# variables dans les graph
@app.callback(
    [Output(component_id='container_variables', component_property='children'), #1
     Output(component_id='container_sex', component_property='children'),       #3
     Output(component_id='container_cat', component_property='children'),       #5
     Output(component_id='container_note', component_property='children'),      #8
     Output(component_id='graph', component_property='figure'),                 #7
     ],
    [Input(component_id='lst_vrbl', component_property='value'),                #2
     Input(component_id='lst_sex', component_property='value'),                 #4
     Input(component_id='lst_cat', component_property='value'),                 #6
     Input(component_id='slider_note', component_property='value'),            #9
     ]            
)

#def update_graph(lst_vrbl, lst_sex, lst_cat, slider_note):
def update_graph(lst_vrbl, lst_sex, lst_cat, slider_note):

    container = "Selectionnez les motivations des participants" #: {}".format(lst_vrbl)
    container2 = "Selectionnez le sexe des participants" #+ str(lst_sex)
    container3 = "Selectionnez la catégorie socioprofessionnelle des participants"  #:{}".format(lst_cat)
    container4 = "Selectionnez l'intervalle de la note moyenne donnée par le participant" # : {}".format(lst_vrbl)

    dff = df.copy()
    dff = dff[dff["GENRE"].isin(lst_sex)]
    dff = dff[dff["CATEGORIE_PRO"].isin(lst_cat)]
    dff = dff[dff["SATISFACTION_GLOBAl"].isin(range(slider_note[0],slider_note[1]+1))]
    dff = dff.groupby(dff['SATISFACTION_GLOBAl'], as_index=False)[lst_vrbl].mean()
    

    fig = px.bar(dff, x ='SATISFACTION_GLOBAl', y = lst_vrbl ,
                 barmode="group")
    fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
            )
    #fig = px.bar(dff, x='INNOVATION', y='SATISFACTION_GLOBAl')

    return container, container2, container3, container4, fig
    #return [go.Figure(data=fig)]
    #return container, container2, container3, container4, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
