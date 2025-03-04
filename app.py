#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:39:51 2025

@author: rfp437
"""

from dash import Dash, html, dcc, callback, Output, Input#, State, Patch
import plotly.express as px
import pandas as pd
import numpy as np
import copy

import dash_bootstrap_components as dbc

import measles_single_population as msp

df = pd.read_csv('TX_MMR_vax_rate.csv')
df = df.loc[df['age_group'] == 'Kindergarten'].copy()


school_selector_text =  html.H4(
        'Alternatively, select vaccination rate based on reported school district value', #' and age group',
        style={'display':'inline-block','margin-right':20, 'margin-left':5})

initial_county = 'Travis'
county_dropdown = html.Div(
    [
        dbc.Label("Select a County", html_for="county_dropdown"),
        dcc.Dropdown(
            id="county-dropdown",
            options=sorted(df["County"].unique()),
            value=initial_county,
            clearable=False,
            maxHeight=600,
            optionHeight=50
        ),
    ],  className="mb-4",
    style={'width': '70%'}
)


# df there should depend on the selected county
df_county = df.loc[df['County'] == initial_county]
school_options = sorted(df_county["School District or Name"].unique())
initial_school = 'AUSTIN ISD'

if initial_school not in school_options:
    initial_school = school_options[0]

school_dropdown = html.Div(
    [
        dbc.Label("Select a School District", html_for="school_dropdown"),
        dcc.Dropdown(
            id="school-dropdown",
            options=school_options,
            value=initial_school,
            clearable=False,
            maxHeight=600,
            optionHeight=50
        ),
    ],  className="mb-4",
    style={'width': '70%'}
)

## Base parameters selection
# If using county and school selector this should be selected automatically
vaccination_rate_label = html.H4(
    'Vaccination Rate',
    style={'display':'inline-block','margin-right':5, 'margin-left':25})
vaccination_rate_selector = dcc.Input(
            id='vax_rate',
            type='number',
            placeholder='Vaccination rate (%)',
            value=85
        )

I0_label = html.H4(
    'Number initially infected',
    style={'display':'inline-block','margin-right':5, 'margin-left':25})
I0_selector = dcc.Input(
            id='I0',
            type='number',
            placeholder='Initial infections',
            value=1.0,
        )

school_size_label = html.H4(
    'School size',
    style={'display':'inline-block','margin-right':5, 'margin-left':5})
school_size_selector = dcc.Input(
            id='school_size',
            type='number',
            placeholder='School size',
            value=500,
        )

## More advanced parameter selection
R0_label = html.H4(
    'Reproduction number (R0)',
    style={'display':'inline-block','margin-right':20, 'margin-left':25})
R0_selector = dcc.Input(
            id='R0',
            type='number',
            placeholder='Reproductive number',
            value=15.0,
        )

latent_period_label = html.H4(
    'Latent period duration',
    style={'display':'inline-block','margin-right':20, 'margin-left':25})
latent_period_selector = dcc.Input(
            id='latent_period',
            type='number',
            placeholder='Latent period (days)',
            value=10.5,
        )

infectious_period_label = html.H4(
    'Infectious period duration',
    style={'display':'inline-block','margin-right':20, 'margin-left':25})
infectious_period_selector = dcc.Input(
            id='infectious_period',
            type='number',
            placeholder='Infectious period (days)',
            value=8.0,
        )

empty_text = html.Div(html.P(
        [' ---', '']))
effective_reproduction_number = dcc.Textarea(
        id='effective_reproduction_number',
        value='Effective reproduction number: ',
        style={'width': '80%', 'height': 30},
    )
outbreak_over_20 = dcc.Textarea(
        id='outbreak_over_20',
        value='Probability of 20 or more cases without intervention: 71%',
        style={'width': '80%', 'height': 30},
    )
cases_expected_over_20 = dcc.Textarea(
        id='cases_expected_over_20',
        value='Expected total number of infections without intervention if outbreak exceeds 20 cases: 1882 cases',
        style={'width': '80%', 'height': 30},
    )

app = Dash(
    prevent_initial_callbacks = 'initial_duplicate')

app.layout = html.Div([
    html.Div(children=[
            html.Div([
                school_size_label,
                school_size_selector], 
                style={'display':'inline-block'}),#, 'border': '1px solid black'}),
            html.Div([
                vaccination_rate_label,
                vaccination_rate_selector], 
                style={'display':'inline-block'}),#, 'border': '1px solid black'}),
            html.Div([
                I0_label,
                I0_selector], 
                style={'display':'inline-block'}),#, 'border': '1px solid black'}),
            html.Div([
                R0_label,
                R0_selector], 
                style={'display':'inline-block'}),#, 'border': '1px solid black'}),
            html.Div([
                latent_period_label,
                latent_period_selector], 
                style={'display':'inline-block'}),#, 'border': '1px solid black'}),
            html.Div([
                infectious_period_label,
                infectious_period_selector], 
                style={'display':'inline-block'}),#, 'border': '1px solid black'}),
            school_selector_text,
            county_dropdown,
            school_dropdown,
            #age_dropdown,
            empty_text,
            effective_reproduction_number,
            outbreak_over_20,
            cases_expected_over_20
            ], style={'padding': 10, 'flex': 1}),
        html.Div(children=[
            dcc.Graph(id="spaghetti_plot")
            ], style={'padding': 10, 'flex': 1}
            )
        ], style={'display': 'flex', 'flexDirection': 'column'}# 'row'}
        )


@callback(
    [Output('spaghetti_plot', 'figure'),
     Output('effective_reproduction_number', 'value'),
     Output('outbreak_over_20', 'value'),
     Output('cases_expected_over_20', 'value')
     ],
    [Input('school_size', 'value'),
     Input('vax_rate', 'value'),
     Input('I0', 'value'),
     Input('R0', 'value'),
     Input('latent_period', 'value'),
     Input('infectious_period', 'value')]
)
def update_graph(school_size, vax_rate, I0, R0, latent_period, infectious_period):
    
    if school_size is None:
        school_size = 500
        
    if vax_rate is None:
        vax_rate = 0
        
    if I0 is None:
        I0 = 1
        
    if R0 is None:
        R0 = 15
        
    if latent_period is None:
        latent_period = 10.5
        
    if infectious_period is None:
        infectious_period = 8
    
    R0 = max(R0, 0)
    # latent_period = max(latent_period, 1.0)
    # infectious_period = max(infectious_period, 1.0)
    
    # Update parameters, run simulations
    n_sim = 200
    params = copy.deepcopy(msp.params)
    params['population'] = [int(school_size)]
    params['vaccinated_percent'] = [0.01 * float(vax_rate)]
    params['I0'] = [int(I0)]
    params['R0'] = float(R0)
    params['incubation_period'] = float(latent_period)
    params['infectious_period'] = float(infectious_period)
    stochastic_sim = msp.StochasticSimulations(
        params, n_sim, print_summary_stats=False, show_plots=False)
    
    # Graph
    df_spaghetti_incidence = stochastic_sim.df_spaghetti_incidence
    df_spaghetti_infected = stochastic_sim.df_spaghetti_infected
    df_spaghetti_infected_ma = stochastic_sim.df_spaghetti_infected_ma
    index_sim_closest_median = stochastic_sim.index_sim_closest_median
    
    # light_grey = px.colors.qualitative.Pastel2[-1]
    light_grey = 'rgb(220, 220, 220)'
    # light_grey = 'rgb(232, 232, 232)'
    color_map = {
        x: light_grey
        for x in df_spaghetti_infected['simulation_idx'].unique()
        }
    color_map[index_sim_closest_median] = 'rgb(0, 153, 204)'
    
    nb_curves_displayed = 20
    possible_idx = [
        x for x in df_spaghetti_infected['simulation_idx'].unique()
        if x != index_sim_closest_median
        ]
    sample_idx = np.random.choice(possible_idx, nb_curves_displayed, replace=False)
    
    # df_plot = pd.concat([
    #     df_spaghetti_infected.loc[df_spaghetti_infected['simulation_idx'].isin(sample_idx)],
    #     df_spaghetti_infected.loc[df_spaghetti_infected['simulation_idx'] == index_sim_closest_median]
    #     ])
    
    df_plot = pd.concat([
        df_spaghetti_infected_ma.loc[df_spaghetti_infected_ma['simulation_idx'].isin(sample_idx)],
        df_spaghetti_infected_ma.loc[df_spaghetti_infected_ma['simulation_idx'] == index_sim_closest_median]
        ])
    
    fig = px.line(
        df_plot,
        x='day',
        y='number_infected_7_day_ma',
        color='simulation_idx',
        color_discrete_map=color_map
        # alpha=0.1
        )
    fig.update_layout(showlegend=False)
    
    # Incidence test
    df_plot = pd.concat([
        df_spaghetti_incidence.loc[df_spaghetti_incidence['simulation_idx'].isin(sample_idx)],
        df_spaghetti_incidence.loc[df_spaghetti_incidence['simulation_idx'] == index_sim_closest_median]
    ])

    fig = px.line(
        df_plot,
        x='day',
        y='number_incidence',
        color='simulation_idx',
        color_discrete_map=color_map
        # alpha=0.1
    )
    fig.update_layout(showlegend=False)
    
    # Summary statistics
    Rt = params['R0'] * (1 - 0.01 * float(vax_rate))
    effective_reproduction_number = 'Effective reproduction number: ' + '{:.2f}'.format(Rt)
    p_20_pct = '{:.0%}'.format(stochastic_sim.probability_20_plus_cases)
    outbreak_over_20 = 'Probability of 20 or more cases without intervention: ' + p_20_pct
    
    # What uncertainty should we display for outbreak size
    outbreak_size_uncertainty_displayed = '95' # '90' '95' 'range' 'IQR'

    if stochastic_sim.expected_outbreak_size == 'NA':
        expected_outbreak_size_str = stochastic_sim.expected_outbreak_size
    else:
        expected_outbreak_size_str = str(int(stochastic_sim.expected_outbreak_size)) + ' cases'
        
        if outbreak_size_uncertainty_displayed == '90':
            quantile_lb = 5
            quantile_ub = 95
            range_name = '90% CI'            
        elif outbreak_size_uncertainty_displayed == '95':
            quantile_lb = 2.5
            quantile_ub = 97.5
            range_name = '95% CI'
        elif outbreak_size_uncertainty_displayed == 'range':
            quantile_lb = 0
            quantile_ub = 100
            range_name = 'range'
        elif outbreak_size_uncertainty_displayed == 'IQR':
            quantile_lb = 25
            quantile_ub = 75
            range_name = 'IQR'
        
        uncertainty_outbreak_size_str = \
            ' (' + range_name + ': ' +  \
            str(int(stochastic_sim.expected_outbreak_quantiles[quantile_lb])) + ' - ' +\
            str(int(stochastic_sim.expected_outbreak_quantiles[quantile_ub])) + ')'
        expected_outbreak_size_str += uncertainty_outbreak_size_str
    
    cases_expected_over_20 = \
        'Expected total number of infections without intervention if outbreak exceeds 20 cases: ' +\
              expected_outbreak_size_str
              
    return fig, effective_reproduction_number, outbreak_over_20, cases_expected_over_20

@callback(
     [Output('school-dropdown', 'options'),
      Output('school-dropdown', 'value')#,
      # Output('age-dropdown', 'options'),
      # Output('age-dropdown', 'value')
      #Output('vax_rate', 'value', allow_duplicate = True)
      ],
     [Input('county-dropdown', 'value')],
     prevent_initial_call=True
)
def update_school_selector(county):
    df_county = df.loc[df['County'] == county]
    new_school_options = sorted(df_county["School District or Name"].unique())
    school_selected = new_school_options[0]
    
    # new_age_options = sorted(df_county["age_group"].unique())
    # age_selected = new_age_options[1]
    
    return new_school_options, school_selected#, new_age_options, age_selected


@callback(
     Output('vax_rate', 'value'),
     [Input('school-dropdown', 'value'),
      Input('county-dropdown', 'value')#,
      # Input('age-dropdown', 'value')
      ]
)
def update_school_vax_rate(school, county):#, age_group):
    df_school = df.loc[
        (df['County'] == county) & 
        (df['School District or Name'] == school)# &
        # (df['age_group'] == age_group)
        ]
    school_vax_rate_pct = df_school['MMR_Vaccination_Rate'].values[0]
    school_vax_rate = float(school_vax_rate_pct.replace('%', ''))
    
    # print('\nSchool:', school, 'in county', county)
        
    return school_vax_rate
    

if __name__ == '__main__':
    app.run(debug=True)