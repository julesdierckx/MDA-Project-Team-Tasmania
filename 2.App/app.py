import pandas as pd
from datetime import date
import dash
from dash import html
from dash import dcc
import plotly.express as px
import plotly.graph_objects as go
# import dash_core_components as dcc
from dash.dependencies import Input,Output

# Read test_set created in Jupyter Notebook
test=pd.read_excel(r"C:\Users\jules\OneDrive\Documenten\KU Leuven\Master of Statistics and Data Science\Modern Data Analytics (2022-2023)\test_set.xlsx")

# Rename relevant columns in test set
test.rename(columns={'result_timestamp':'Date/time',
                                     'lamax':'A-weighted maximum sound level in dB(A)',
                                     'laeq':'A-weighted equivalent continuous sound level in dB(A)',
                                     'lceq':'C-weighted equivalent continuous sound level in dB(C)',
                                     'lcpeak':'C-weighted peak sound level in dB(C)',
                                     'LC_HUMIDITY':'Relative humidity (%)',
                                     'LC_DWPTEMP':'Dew point temperature (°C)',
                                     'LC_RAD':'Solar radiation (W/m2)',
                                     'LC_RAININ':'Rain intensity (mm/h)',
                                     'LC_DAILYRAIN':'Daily rain sum (mm)',
                                     'LC_WINDDIR':'Wind direction',
                                     'LC_WINDSPEED':'Wind speed (m/s)',
                                     'LC_RAD60':'Weighted radiation during last 60 minutes (W/m2)',
                                     'LC_TEMP_QCL3':'Temperature at QCL3 (°C)',
                                     'noise_event_laeq_primary_detected_class':'Noise event class',
                                     'noise_event_laeq_primary_detected_class_pred':'Predicted noise event class',
                                     'coronavirus_measures_cum_polarity_textblob_nl':'Cumulative polarity Belgian Covid-19 measures (textblob-nl)',
                                     'coronavirus_measures_cum_polarity_textblob_en':'Cumulative polarity Belgian Covid-19 measures (textblob)',
                                     'coronavirus_measures_cum_polarity_textblob_avg':'Cumulative polarity Belgian Covid-19 measures (Average from textblob-nl and textblob)',
                                     'Classification Accuracy':'Classification accuracy'},inplace=True)

# Create 1st scatterplot
scatter_fig=px.scatter(
  title=f'Noise events by A-weighted maximum sound level in dB(A)',
  data_frame=test, 
  x='Date/time', 
  y='A-weighted maximum sound level in dB(A)',
  color='Noise event class',
  hover_data=['Predicted noise event class','Classification accuracy']
)
scatter_fig.update_traces(marker={'size':4.5})

# Create histogram
hist_fig=go.Figure()
hist_fig.add_trace(go.Histogram(x=test['Classification accuracy'],histnorm='percent',marker=dict(color=['green','red'])))
hist_fig.update_layout(title='Classification accuracy for all noise event categories',
                   yaxis=dict(title='%',tickvals=list(range(0, 101, 10))),yaxis_range=[0, 110])
# The texttemplate parameter is set to '%{y:.2f}%', which formats the y-values (percentages) with two decimal places and appends the percentage symbol (%). The textposition parameter is set to 'outside', which places the percentage counts above each bin
hist_fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')

# Create 2nd scatterplot
scatter_fig2=px.scatter(
    title="(In)correctly classified noise events for all noise event categories'",
    data_frame=test, 
    x='Date/time', 
    y='A-weighted maximum sound level in dB(A)',
    color_discrete_map={'Correctly classified':'green','Incorrectly classified':'red'},
    color='Classification accuracy',
    hover_data=['Noise event class','Predicted noise event class']
)
scatter_fig2.update_traces(
    marker={'size':4}
)

# Application
app=dash.Dash(__name__)

server=app.server

app.layout=html.Div(
    children=[
        html.Div(
            className='header',
            children=[
                html.Img(src=dash.get_asset_url('KUL_logo2.png'),className='logoUL',style={'margin':'0px','height':'125px','position':'absolute','top':'0','left':'0'}),
                html.H1("Project Modern Data Analytics: Team Tasmania (2022-2023)",className='title',style={'text-align':'center'}),
                html.H2("A novel approach to urban noise event modelling and predicting in Leuven",className='title2.1',style={'text-align':'center','marginBottom':'0'}),
                html.H2("using sound level statistics, meteo data and NLP sentiment from Belgian Covid-19 measures",className='title2.2',style={'text-align':'center','margin':'0'}),
                html.Img(src=dash.get_asset_url('LC_logo.jpg'),className='logoUR',style={'margin':'0px','height':'125px','position':'absolute','top':'0','right':'0'}),
            ]
        ),
        html.H3("Select a variable and date and click on a point on the graph:",style={'margin-top':'75px'}),
        html.Div(
            className='controls',
            style={'display':'flex','align-items':'center'},
            children=[
                dcc.Dropdown(
                    id='yaxis_dd',
                    options=[
                        {'label':'A-weighted maximum sound level in dB(A)','value':'A-weighted maximum sound level in dB(A)'},
                        {'label':'A-weighted equivalent continuous sound level in dB(A)','value':'A-weighted equivalent continuous sound level in dB(A)'},
                        {'label':'C-weighted equivalent continuous sound level in dB(C)','value':'C-weighted equivalent continuous sound level in dB(C)'},
                        {'label':'C-weighted peak sound level in dB(C)','value':'C-weighted peak sound level in dB(C)'},
                        {'label':'Relative humidity (%)','value':'Relative humidity (%)'},
                        {'label':'Dew point temperature (°C)','value':'Dew point temperature (°C)'},
                        {'label':'Solar radiation (W/m2)','value':'Solar radiation (W/m2)'},
                        {'label':'Rain intensity (mm/h)','value':'Rain intensity (mm/h)'},
                        {'label':'Daily rain sum (mm)','value':'Daily rain sum (mm)'},
                        {'label':'Wind direction','value':'Wind direction'},
                        {'label':'Wind speed (m/s)','value':'Wind speed (m/s)'},
                        {'label':'Weighted radiation during last 60 minutes (W/m2)','value':'Weighted radiation during last 60 minutes (W/m2)'},
                        {'label':'Temperature at QCL3 (°C)','value':'Temperature at QCL3 (°C)'}
                    ],
                    value='A-weighted maximum sound level in dB(A)',
                    style={'display':'inline-block','width':'400px'}
                ),
                dcc.DatePickerRange(
                    id='date_picker_range',
                    initial_visible_month=date(2022,1,1),
                    min_date_allowed=date(2022,1,1),
                    max_date_allowed=date(2022,12,31),
                    start_date=date(2022,1,1),
                    end_date=date(2022,12,31),
                    display_format='YYYY-MM-DD',
                    style={'display':'inline-block','margin-left':'25px'}
                ),
            ]
        ),
        html.Div(
            className='charts',
            children=[
                dcc.Graph(
                    id='scatter_fig',
                    figure=scatter_fig
                ),
                html.Div(
                    className='side-by-side',
                    children=[
                        dcc.Graph(
                            id='hist_fig',
                            figure=hist_fig,
                            style={'display':'inline-block','width':'45%'}
                        ),
                        dcc.Graph(
                            id='scatter_fig2',
                            figure=scatter_fig2,
                            style={'display':'inline-block','width':'55%'}
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            className='footer',
            children=[
                html.Img(src=dash.get_asset_url('LC_logo2.png'),className='logoBL',style={'margin':'0px','width':'125px','position':'relative','bottom':'0','right':'0'}),
                html.P(
                    style={'width':'250px','text-align':'left'},
                    children=[
                        'Jules Dierckx, r0722530',
                        html.Br(),
                        "Master Statistics and Data Science",
                        html.Br(),
                        "June 29, 2023"
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    Output(component_id='scatter_fig', component_property='figure'),
    Output(component_id='hist_fig', component_property='figure'),
    Output(component_id='scatter_fig2', component_property='figure'),
    Input(component_id='yaxis_dd', component_property='value'),
    Input(component_id='scatter_fig', component_property='clickData'),
    Input(component_id='date_picker_range',component_property='start_date'),
    Input(component_id='date_picker_range',component_property='end_date')
)

def update_plots(input_yaxis,clickData,start_date,end_date):
    yaxis_filter='A-weighted maximum sound level in dB(A)'
    click_noise_event='all noise event categories'
    specific_noise_event_testdata=test.copy(deep=True)
    if input_yaxis:
        yaxis_filter=input_yaxis
    if clickData:
        click_noise_event=clickData['points'][0]['customdata'][0]
        specific_noise_event_testdata=test.loc[test['Noise event class']==click_noise_event].copy(deep=True)
    scatter_fig=px.scatter(title=f'Noise events by {yaxis_filter}',data_frame=test,x='Date/time',y=yaxis_filter,color='Noise event class',hover_data=['Predicted noise event class','Classification accuracy'],custom_data=['Noise event class'])
    scatter_fig.update_traces(marker={'size':4.5})
    scatter_fig.update_layout(xaxis=dict(range=[start_date,end_date])),

    hist_fig=go.Figure()
    if click_noise_event in ['Music non-amplified','Nature elements - Wind']:
        hist_fig.add_trace(go.Histogram(x=specific_noise_event_testdata['Classification accuracy'],histnorm='percent',marker=dict(color='red')))
    else:
        hist_fig.add_trace(go.Histogram(x=specific_noise_event_testdata['Classification accuracy'],histnorm='percent',marker=dict(color=['green','red'])))
    hist_fig.update_layout(title=f"Classification accuracy for '{click_noise_event}'",
                           yaxis=dict(title='%',tickvals=list(range(0, 101, 10))),yaxis_range=[0, 110])
    hist_fig.update_xaxes(categoryorder='array', categoryarray= ['Correctly classified','Incorrectly classified'])
    # The texttemplate parameter is set to '%{y:.2f}%', which formats the y-values (percentages) with two decimal places and appends the percentage symbol (%). The textposition parameter is set to 'outside', which places the percentage counts above each bin
    hist_fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')

    scatter_fig2 = px.scatter(
        title=f"(In)correctly classified noise events for {click_noise_event}",
        data_frame=specific_noise_event_testdata, 
        x='Date/time', 
        y=yaxis_filter,
        color_discrete_map={'Correctly classified':'green','Incorrectly classified':'red'},
        color='Classification accuracy',
        hover_data=['Noise event class','Predicted noise event class']
    )
    scatter_fig2.update_traces(marker={'size':4})   
    scatter_fig2.update_layout(xaxis=dict(range=[start_date,end_date])),

    return scatter_fig,hist_fig,scatter_fig2

if __name__ == '__main__':
    app.run_server(debug=True)