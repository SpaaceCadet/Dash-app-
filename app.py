
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash import *
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

DF = pd.read_csv("file_namee.csv")
# pour le pyramide
MM = DF[DF.Year == 1970]
MM["fem_duc"] = 100 - MM["Percent_fem_noeduc"]
MM["percent_homme_educ"] = 100 - MM["percent_homme_noeduc"]
y_age = MM['rang_age']
x_M = MM['percent_homme_noeduc']
x_F = ((MM["Percent_fem_noeduc"] * MM["popfemale_in_thsnd"]) / MM["pop_in_thsnd"]) * (-1)
# Creating instance of the figure
figara = go.Figure()
# Adding Male data to the figure
figara.add_trace(go.Bar(y=y_age, x=x_M,
                        name='Male',
                        orientation='h', marker_color='#fab17a'))

# Adding Female data to the figure
figara.add_trace(go.Bar(y=y_age, x=x_F,
                        name='Female', orientation='h', marker_color='#f7cd68'))

# Updating the layout for our graph
figara.update_layout(
    title_font_size=22, barmode='relative',
    bargap=0, bargroupgap=0,
    xaxis=dict(tickvals=[-80, -60, -40, -20, 0,
                         20, 40, 60, 80, 100],

               ticktext=['80', '60', '40', '20', '0',
                         '20', '40', '60', '80']), plot_bgcolor='white', paper_bgcolor='white')
# fin pyramide
# let's plot some scatters
# initialisation du scatter
figuro = go.Figure()
figuro.add_trace(
    go.Scatter(x=MM['rang_age'], y=MM['percent_homme_noeduc'], name='homme_no_educ', marker_color="#fab17a"))
figuro.add_trace(go.Scatter(x=MM['rang_age'], y=MM["Percent_fem_noeduc"], name='femme_no_educ', marker_color="#f7cd68"))
figuro.update_layout(plot_bgcolor='#ffffcc')
figuro.update_layout(
    updatemenus=[
        dict(
            type = "buttons",
            direction = "left",
            buttons=list([
                dict(
                    args=["type", "bar"],
                    label="bar",
                    method="restyle"
                ),
                dict(
                    args=["type", "scatter"],
                    label="scatter",
                    method="restyle"
                )]),pad={"r": 10, "t": 10},
            showactive=True,
            x=0.11,
            xanchor="left",
            y=1.3,
            yanchor="top")])
K = DF.groupby("Year")["Percent_fem_noeduc"].mean().to_frame()
# les figures de plot qu'on doit faire

# Tracé d'evolution des classes pourcentage des femmes non éduqués chaque 5 années
# création de figure vide
figure2 = go.Figure()
for element in DF["Year"].unique().tolist():
    dff = DF[DF["Year"] == element]
    figure2.add_trace(go.Bar(x=dff["rang_age"], y=dff["Percent_fem_noeduc"], name=element))
    # creons mtn un dropdown
    # on doit definir les niveaux de visibilités
    dropdown_buttons = [
        {'label': 'All years', 'method': 'update',
         'args': [{'visible': [True, True, True, True, True, True, True, True, True]},
                  {'title': 'All years '}]},
        {'label': 1970, 'method': 'update',
         'args': [{'visible': [True, False, False, False, False, False, False, False, False]},
                  {'title': 'Année :1970'}]},
        {'label': 1975, 'method': 'update',
         'args': [{'visible': [False, True, False, False, False, False, False, False, False]},
                  {'title': 'Année :1975'}]},
        {'label': 1980, 'method': 'update',
         'args': [{'visible': [False, False, True, False, False, False, False, False, False]},
                  {'title': 'Année :1980'}]},
        {'label': 1985, 'method': 'update',
         'args': [{'visible': [False, False, False, True, False, False, False, False, False]},
                  {'title': 'Année :1985'}]},
        {'label': 1990, 'method': 'update',
         'args': [{'visible': [False, False, False, False, True, False, False, False, False]},
                  {'title': 'Année :1990'}]},
        {'label': 1995, 'method': 'update',
         'args': [{'visible': [False, False, False, False, False, True, False, False, False]},
                  {'title': 'Année :1995'}]},
        {'label': 2000, 'method': 'update',
         'args': [{'visible': [False, False, False, False, False, False, True, False, False]},
                  {'title': 'Année :2000'}]},
        {'label': 2005, 'method': 'update',
         'args': [{'visible': [False, False, False, False, False, False, False, True, False]},
                  {'title': 'Année :2005'}]},
        {'label': 2010, 'method': 'update',
         'args': [{'visible': [False, False, False, False, False, False, False, False, True]},
                  {'title': 'Année :2010'}]}]

    figure2.update_layout({
        'updatemenus': [{
            'type': "dropdown", 'x': 1.3, 'y': 1, 'showactive': True, 'active': 0,
            'buttons': dropdown_buttons}]
    })
    figure2.update_layout({'xaxis': {'title': {'text': 'Classes_age'}, 'title_font': dict(size=15)},
                           'yaxis': {'title': {'text': '%femmes non_eduqués'}, 'title_font': dict(size=17)}},
                          plot_bgcolor='white',
                          paper_bgcolor='white', font_color="black", font_family="Times New Roman", legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1, bgcolor="#ffffcc"))

# tracé de pourcentage de femme non éduqués pour chaque année
figure1 = px.bar(x=DF["Year"].unique().tolist(), y=K["Percent_fem_noeduc"])
figure1.update_layout({'xaxis': {'title': {'text': 'Années'}, 'title_font': dict(size=13)},
                       'yaxis': {'title': {'text': '%de femmes non eduqués'}, 'title_font': dict(size=13)}},
                      plot_bgcolor='white',
                      paper_bgcolor='white', font_color="black", font_family="Times New Roman")

figure1.update_traces(marker_color='#fab17a')
figure1.update_traces(hovertemplate='Year: %{x} <br>Pourcentage: %{y}')
figure1.add_trace(go.Scatter(x=DF["Year"].unique().tolist(), y=K["Percent_fem_noeduc"], name='Tendance'))
figure1.update_layout(hovermode="x unified")
figure1.update_layout(
    hoverlabel=dict(
        bgcolor="#f8c86c",
        font_size=11,
        font_family="Rockwell"
    )
)

figure3 = px.scatter(data_frame=DF, x='Percent_pop_noeduc', y="pop_in_thsnd", color="rang_age")

external_scripts = [
    {'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js',
     'integrity': 'sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM',
     'crossorigin': 'anonymous'},
    {
        'src': 'https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js',
        'integrity': 'sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js',
        'integrity': 'sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF',
        'crossorigin': 'anonymous'
    }]

external_stylesheets = [
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC',
        'crossorigin': 'anonymous'
    }
]

app: Dash = dash.Dash(__name__, meta_tags=[{'name': 'viewport', 'content': 'width=device-width initial-scale=1.0'}],
                      external_scripts=external_scripts,
                      external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div(
    children=[
        dbc.Nav(
            html.Div(children=[
                html.Img(
                    src="/assets/poo.png",
                    style={'height': '100px', 'width': '120px'}),
                html.H4(html.P("VISUAL INSIGHT", style={'margin': '0px -69px 16px 0px'})),
                html.A("contact", href="mailto:yahyasgh9@gmail.com",
                       style={'display': 'inline-block', 'color': 'black', 'margin': '0 -408px 0 0'}),
                html.A("Webpage", href="http://ensao.ump.ma/", target="_blank",
                       style={'display': 'inline-block', 'color': 'black'})],
                className='container-fluid'),
            className="navbar navbar-expand-lg navbar-light", style={'background-color': '#FBAB7E',
                                                                     'background-image': 'linear-gradient(62deg, #FBAB7E 0%, #F7CE68 100%)',
                                                                     'height': '80px', 'position': '-webkit-sticky',
                                                                     'position': 'sticky'
                , 'top': '0', 'z-index': '3', 'text-align': 'center'}),
        html.Section(className="sidebar", id="sidebar", children=[
            html.Div(className="sidebar-main", children=[
                html.Div(className="sidebar-user",
                         children=[
                             html.Div(className="sidebar-menu",
                                      children=[html.I(html.B(html.U(html.P("GRAPH I :")), style={'color': '#fbaf7b'})),
                                                html.I(html.B(html.P("PLOT TYPE:")),
                                                       style={'color': 'white', 'font-size': 13}),
                                                dcc.Dropdown(id='title_dd', options=[{'label': 'Bar chart',
                                                                                      'value': 'Bar chart'},
                                                                                     {'label': 'Pie chart',
                                                                                      'value': 'Pie chart'}],
                                                             style={'color': 'black', 'font-style': 'italic'}),
                                                html.I(
                                                    html.B(html.U(html.P("GRAPH III :")), style={'color': '#fbaf7b'})),
                                                html.I(html.B(html.P("YEARS:")),
                                                       style={'color': 'white', 'font-size': 13}),
                                                dcc.Dropdown(id='title_d2', options=[{'label': '1975', 'value': 1975},
                                                                                     {'label': '1980', 'value': 1980},
                                                                                     {'label': '1985', 'value': 1985},
                                                                                     {'label': '1990', 'value': 1990},
                                                                                     {'label': '1995', 'value': 1995},
                                                                                     {'label': '2000', 'value': 2000},
                                                                                     {'label': '2005', 'value': 2005},
                                                                                     {'label': '2010', 'value': 2010}],
                                                             style={'color': 'black', 'font-style': 'italic'})

                                                ])])])],
                     style={'top': '80px', 'width': '200px'}),
        html.Section(id="MasterPage", children=[html.Div(className="container", children=[html.Div(className="row",
                                                                                                   children=[html.Div(
                                                                                                       className="col-md-12 text-center",
                                                                                                       children=[
                                                                                                           html.Div(
                                                                                                               children=[
                                                                                                                   html.Div(
                                                                                                                       children=[
                                                                                                                           html.U(
                                                                                                                               html.B(
                                                                                                                                   html.P(
                                                                                                                                       "I/Pourcentage des femmes non éduqués chaque 5 années: "))),
                                                                                                                           dcc.Graph(
                                                                                                                               id='example-graph',
                                                                                                                               figure=figure1,
                                                                                                                               style={
                                                                                                                                   'width': '900px',
                                                                                                                                   'height': '500px',
                                                                                                                                   'margin': '0 0 0 100px'})]),
                                                                                                                   html.Div(
                                                                                                                       children=[
                                                                                                                           html.U(
                                                                                                                               html.B(
                                                                                                                                   html.P(
                                                                                                                                       "II/Pourcentage des femmes non éduqués par Classe: "))),
                                                                                                                           dcc.Graph(
                                                                                                                               figure=figure2,
                                                                                                                               style={
                                                                                                                                   'width': '900px',
                                                                                                                                   'height': '500px',
                                                                                                                                   'margin': '0 0 0 1OOpx'})]),
                                                                                                                   html.Div(
                                                                                                                       children=[
                                                                                                                           html.U(
                                                                                                                               html.B(
                                                                                                                                   html.P(
                                                                                                                                       "III/Comparaison de femmes non éduqués avec les hommes non éduqués: "))),
                                                                                                                           dcc.Graph(
                                                                                                                               id='sec_ex',
                                                                                                                               figure=figara)]),
                                                                                                                   html.Div(
                                                                                                                       children=[
                                                                                                                           html.U(
                                                                                                                               html.B(
                                                                                                                                   html.P(
                                                                                                                                       "Scatters:"))),
                                                                                                                           dcc.Graph(
                                                                                                                               id='sec_ex1',
                                                                                                                               figure=figuro)])])

                                                                                                       ])])])])
    ])

app.title="ENSAO_VISUAL"
@app.callback(Output(component_id='example-graph', component_property='figure'),
              Input(component_id='title_dd', component_property='value'))
def interactive_graphs(selection):
    title = selection
    if selection == 'Pie chart':
        fig = px.pie(values=K["Percent_fem_noeduc"].tolist(), names=DF["Year"].unique().tolist(), title='Pie Chart',
                     color_discrete_sequence=px.colors.sequential.Redor)
        fig.update_layout({'xaxis': {'title_font': dict(size=13)}}, plot_bgcolor='white', paper_bgcolor='white',
                          font_color="black", font_family="Times New Roman")
        fig.update_traces(hovertemplate='Year: %{label} <br>Percentage: %{value}')
        return fig
    else:
        return figure1


@app.callback(Output(component_id='sec_ex', component_property='figure'),
              Input(component_id='title_d2', component_property='value'))
def interactive_graph(seelection):
    titlez = seelection
    if seelection:
        kk = DF[DF.Year == seelection]
        kk["fem_duc"] = 100 - kk["Percent_fem_noeduc"]
        kk["percent_homme_educ"] = 100 - kk["percent_homme_noeduc"]
        y_ag = kk['rang_age']
        x_MM = kk['percent_homme_noeduc']
        x_FF = ((kk["Percent_fem_noeduc"] * kk["popfemale_in_thsnd"]) / kk["pop_in_thsnd"]) * (-1)
        # Creating instance of the figure
        figario = go.Figure()
        # Adding Male data to the figure
        figario.add_trace(go.Bar(y=y_age, x=x_MM,
                                 name='Male',
                                 orientation='h', marker_color='#fab17a'))

        # Adding Female data to the figure
        figario.add_trace(go.Bar(y=y_ag, x=x_FF,
                                 name='Female', orientation='h', marker_color='#f7cd68'))

        # Updating the layout for our graph
        figario.update_layout(
            title_font_size=22, barmode='relative',
            bargap=0, bargroupgap=0,
            xaxis=dict(tickvals=[-80, -60, -40, -20, 0,
                                 20, 40, 60, 80, 100],

                       ticktext=['80', '60', '40', '20', '0',
                                 '20', '40', '60', '80']), plot_bgcolor='white', paper_bgcolor='white')
        return figario
    else:
        return figara


@app.callback(Output(component_id='sec_ex1', component_property='figure'),
              Input(component_id='title_d2', component_property='value'))
def my_interactive2(myselect):
    if myselect:
        UU = DF[DF.Year == myselect]
        UU["fem_duc"] = 100 - UU["Percent_fem_noeduc"]
        UU["percent_homme_educ"] = 100 - UU["percent_homme_noeduc"]
        figurio = go.Figure()
        figurio.add_trace(
            go.Scatter(x=UU['rang_age'], y=UU['percent_homme_noeduc'], name='homme_no_educ', marker_color="#fab17a"))
        figurio.add_trace(
            go.Scatter(x=UU['rang_age'], y=UU["Percent_fem_noeduc"], name='femme_no_educ', marker_color="#f7cd68"))

        figurio.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    direction="left",
                    buttons=list([
                        dict(
                            args=["type", "bar"],
                            label="bar",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "scatter"],
                            label="scatter",
                            method="restyle"
                        )]), pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.11,
                    xanchor="left",
                    y=1.3,
                    yanchor="top")],plot_bgcolor='#ffffcc')
        return figurio
    else:
        return figuro

if __name__ == '__main__':
    app.run_server(port=8080,debug=False)
