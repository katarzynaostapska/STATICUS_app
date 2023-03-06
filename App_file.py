from dash import Dash, dcc, Output, Input, State, html, ctx
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import time as t
import matplotlib.pylab as plt
from hamopy import ham_library as ham
from hamopy.classes import Mesh, Boundary, Time, Material
from hamopy.algorithm import calcul
from hamopy.postpro import evolution

# Choice of materials and geometry
from hamopy.materials.hamstad import BM3
from hamopy.materials.standard import wood_fibre, steel, wood, spruce, glass, argon
from hamopy.materials.standard import zinc, mw_sh, mw_soft, aluminium, glue, polyiso_ins
import plotly.express as px
import plotly.graph_objects as go
#
#
# section definition
#
section_A1 = [[glass, argon, glass, mw_sh, mw_soft, zinc],
              [0.006, 0.022, 0.006, 0.03, 0.18, 0.002],
              [3, 5, 3, 5, 10, 3],
              [0.0, 0.006, 0.028, 0.034, 0.064, 0.244, 0.0246]
            ]
section_A2 = [[aluminium, polyiso_ins, aluminium, spruce, glue, spruce, glue, spruce, glue, spruce],
              [0.0355, 0.03, 0.0345, 0.04, 0.001, 0.04, 0.001, 0.04, 0.001, 0.04],
              [5, 5, 5, 4, 3, 4, 3, 4, 3, 4],
              [0.0, 0.0355, 0.0655, 0.1, 0.14, 0.141, 0.181, 0.182, 0.222, 0.223, 0.263]
            ]
#
# solving function
#
def HAM_SOLVER(section, climate_file):
    file1 = open(climate_file, "r+")
    for line in file1.readlines():
        total_time = (line.split(',')[0][0:-2])
    total_time = int(total_time)/365*30
    #
    start_t = t.time()
    #
    # mesh
    mesh = Mesh(**{
                "materials": section[0],
                "sizes": section[1],
                "nbr_elements": section[2]
                })
    # Boundary conditions
    clim_file = climate_file
    #
    #
    clim_out = Boundary('Fourier', **{"file"      : clim_file,
                              "delimiter" : ',',
                              "time"      : "Time [s]",
                              "T"         : 'Temp [C]',
                              "HR"        : 'RH [%]',
                              "h_t"       : 'h_t', # 5 W/(m2.K) surface transfer coefficient
                              "h_m"       : 'h_m', # s/m  7.7 x 10e-9 x (3.06 x u_10 - 5.44) / wood: (9.4×10−10 to 5.7×10−9 s/m)
                              "P_air"     : 0.0,#"DeltaP" # air pressure (Pa), impacting eventual air transfer in the wall. 0,
                              "g_l"       : 0.0,#'WDR [kg/m2.s]',#[kg/(m2.s)] liquid water income caused by rain
                                })

    clim_inn = Boundary('Fourier',**{"T"      : 293.15,  # 20 C inside
                              "HR"        : 0.3,     # here standard EN 15026 to implement
                              "h_t"       : 5,       # W/(m2.K)
                              "h_m"       : 7.38e-8, # [s/m] 7.45e-9 * h_t =
                              "g_l"       : 0.0,     # [kg/(m2.s)] liquid water income caused by rain
                             })
    climate = [clim_out, clim_inn]

    #
    # Initial conditions
    init = {'T': 293.15, # 20 C initial
            'HR': 0.3}

    # Time step control
    time = Time('variable', **{"delta_t"  : 1,
                          "t_max"    : int(total_time),#len(time1)*3600,
                          "iter_max" : 1000,
                          "delta_min": 1,
                          "delta_max": 2400 } )
    # Calculation
    diary_1 = 'diary_1'
    #
    results = calcul(mesh, climate, init, time, logfile= diary_1)
    #
    end_t = t.time()
    elapsed_time = (end_t - start_t) / 60  #'min'
    #
    return results, total_time, elapsed_time
#
def WET_PERIODS(result, RH_crit, section):
    x_out = section[3]
    time = np.array([i * 3600 for i in range(int(result['t'][-1] / 3600))])
    MC = np.column_stack([evolution(result, 'HR', i, time) for i in x_out])
    MC_0h = [i[0] for i in MC]
    MC_0h_st = []
    MC_0h_end = []
    for k in range(0, len(MC_0h)):
        if MC_0h[k] > RH_crit and MC_0h[k - 1] < RH_crit:
            MC_0h_st.append(k)
        if MC_0h[k] < RH_crit and MC_0h[k - 1] > RH_crit:
            MC_0h_end.append(k)
    periods_wet = [] # durations of consecutive periods with RH > RH_crit
    periods_dry = [] # durations of consecutive periods with RH < RH_crit
    for i in range(min(len(MC_0h_st), len(MC_0h_end))):
        periods_wet.append(MC_0h_end[i] - MC_0h_st[i])
    for i in range(min(len(MC_0h_st), len(MC_0h_end)) - 1):
        periods_dry.append(-MC_0h_end[i] + MC_0h_st[i + 1])
    Mean_wet_period = np.mean(periods_wet)
    Sum_wet_period = np.sum(periods_wet)
    Count_wet_period = len(periods_wet)
    Mean_dry_period = np.mean(periods_dry)
    Sum_dry_period = np.sum(periods_dry)
    Count_dry_period = len(periods_dry)
    print(MC_0h_st, MC_0h_end,periods_dry)
    return Mean_dry_period, Sum_dry_period, Count_dry_period, Mean_wet_period, Sum_wet_period, Count_wet_period
#
#
# build components
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
server = app.server
title = dcc.Markdown(children='Mould predictive tool for STATICUS facade: demo')
####
choice_1 = dcc.Markdown(children='Choose section:')
dropdown_section = dcc.Dropdown(options=['A1', 'A2'],
                                value='A1',
                                clearable=False)
section_choice = dcc.Markdown(children='Analysis will be performed on section:')
section = dcc.Markdown(children='')
#####
choice_2 = dcc.Markdown(children='Choose location:')
dropdown_location = dcc.Dropdown(options=['Oslo', 'Trondheim', 'Trømso'],
                                value='Trondheim',
                                clearable=False)
location_choice = dcc.Markdown(children='Analysis will be performed in:')
location = dcc.Markdown(children='')
#####
choice_3 = dcc.Markdown(children='Choose year:')
dropdown_year = dcc.Dropdown(options=['2020', '2021', '2022', 'Reference year'],
                                value='Reference year',
                                clearable=False)
year_choice = dcc.Markdown(children='Analysis will be performed for year:')
year = dcc.Markdown(children='')
####
button = dbc.Button('SOLVE', id='solution')
button_output = dcc.Markdown(children='solution empty')       #html.Div(className='mt-4')
figure_time = dcc.Graph(id='figure_time')
mould_statistics = dcc.Markdown(children='')
# Layout
app.layout = dbc.Container([title,
                            dbc.Row([
                                dbc.Col(choice_1, width=4), dbc.Col(choice_2, width=4), dbc.Col(choice_3, width=4)
                                ]),
                            dbc.Row([
                                dbc.Col(dropdown_section, width=4), dbc.Col(dropdown_location, width=4), dbc.Col(dropdown_year, width=4)
                                ]),
                            dbc.Row([
                                dbc.Col(section_choice, width=4), dbc.Col(location_choice, width=4), dbc.Col(year_choice, width=4)
                                ]),
                            dbc.Row([
                                dbc.Col(section, width=4), dbc.Col(location, width=4), dbc.Col(year, width=4)
                                ]),
                            button,
                            button_output,
                            dbc.Row([
                                dbc.Col(figure_time, width=12)
                                ]),
                            mould_statistics
                            ], fluid=True)

# app callback
@app.callback(
    Output(section, component_property='children'),
    Output(location, component_property='children'),
    Output(year, component_property='children'),
    Output(button_output, component_property='children'),
    Output('figure_time', 'figure'),
    Output(mould_statistics, component_property='children'),
    Input(dropdown_section, component_property='value'),
    Input(dropdown_location, component_property='value'),
    Input(dropdown_year, component_property='value'),
    Input(button, 'n_clicks'),
    #State('', 'value'),
    prevent_initial_call=True,

)
def update_title(user_input1, user_input2, user_input3, button):
    if ctx.triggered:
        button_output == 'solve'
        if user_input1 == 'A1':
            section_input = section_A1
        else:
            section_input = section_A2
        if user_input2 == 'Oslo':
            file_name = 'assets\climate_OSLO_'
        elif user_input2 == 'Trondheim':
            file_name = 'assets\climate_TRD_'
        elif user_input2 == 'Trømso':
            file_name = 'assets\climate_TROMSO_'
        if user_input3 == 'Reference year':
            file_name = file_name+'OSLOMET.txt'
        else:
            file_name = file_name+user_input3+'.txt'
        print('file_name', file_name)
        results = HAM_SOLVER(section_input, 'assets\climate_TRD_OSLOMET.txt')
        result = results[0]
        total_time = results[1]
        fig_r = go.Figure()
        dashes = ['solid', 'dash', 'dot', 'solid', 'dash', 'dot', 'solid', 'dash', 'dot']
        colors = ['red', 'green', 'grey', 'blue', 'black', 'yellow', 'pink', 'magenta', 'darkgrey', 'pink']
        print(int(int(total_time) / 3600))
        time = np.array([i * 3600 for i in range(int(int(total_time) / 3600))])
        x_out = section_input[3] #[0.0, 0.01, 0.0355, 0.05, 0.1, 0.14, 0.16, 0.02]
        temp = np.column_stack([evolution(result, 'T', i, time) for i in x_out])
        MC = np.column_stack([evolution(result, 'HR', i, time) for i in x_out])
        for i in range(len(x_out)):
            fig_r.add_trace(go.Scatter(x=time / 3600 / 24, y=[k[i] for k in MC], mode='lines',
                                       name=str(x_out[i]),
                                       #line=dict(color=colors[i], width=2, dash=dashes[i])
                                       ))
        fig_r.add_trace(go.Scatter(x=time / 3600 / 24, y=[0.8 for i in time], mode='lines', name='critical RH=0.8 '))
        fig_r.add_trace(
            go.Scatter(x=time / 3600 / 24, y=[0.3 for i in time], mode='lines', name='inner RH=' + str(0.3)))
        fig_r.update_layout(title=user_input1+' section in '+user_input2+' in '+user_input3, template='plotly_white')
        mould_stats = WET_PERIODS(result, 0.8, section_input)
        print(mould_stats[1], type(mould_stats))
    return user_input1, user_input2, user_input3, f" \n simulation solved in {results[2]} min", fig_r, \
           f" {mould_stats[2]} dry periods of mean duration {round(mould_stats[0],1)} hours and total dry time" \
           f" {mould_stats[1]} hours,\n {mould_stats[5]} wet periods" \
           f" of mean duration {round(mould_stats[3],1)} hours and total wet time of {mould_stats[4]} hours" \
           f" ({round(mould_stats[4]/total_time*3600*100,1)} % of total simulation time) "
# run app
if __name__=='__main__':
    app.run_server(port=8051)
