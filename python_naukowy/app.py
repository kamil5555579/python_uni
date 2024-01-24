#poetry run bokeh serve --show .\scripts\Lab009\app.py

import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column, gridplot, layout
from bokeh.models import Slider, Div
from bokeh.transform import linear_cmap
from bokeh.palettes import all_palettes
from scipy.integrate import odeint

def model(y, t, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

y0 = 0.99, 0.01, 0
t = np.linspace(0, 100, 100)
beta, gamma = 0.2, 0.1
sol = odeint(model, y0, t, args=(beta, gamma))
S, I, R = sol.T

fig = figure(width=1000, x_axis_label='time', y_axis_label='population', aspect_ratio=2, background_fill_color='black', border_fill_color='black', outline_line_color='white', x_range=(0, 100), y_range=(0, 1))
fig.grid.visible = False

S_plot = fig.line(t, S, color='green', legend_label='S', line_width=5)
I_plot = fig.line(t, I, color='red', legend_label='I', line_width=5)
R_plot = fig.line(t, R, color='blue', legend_label='R', line_width=5)

s1 = Slider(start=0, end=1, value=0.1, step=0.05, title=r"$$\beta$$", width=300, styles={'color': 'white', 'background-color': 'black', 'font-size': '20px', 'margin': '10px'})
s2 = Slider(start=0, end=1, value=0.1, step=0.05, title=r"$$\gamma$$", width=300, styles={'color': 'white', 'background-color': 'black', 'font-size': '20px', 'margin': '10px'})

def update(attr, old, new):

    beta = s1.value
    gamma = s2.value

    sol = odeint(model, y0, t, args=(beta, gamma))
    S, I, R = sol.T

    S_plot.data_source.data['y'] = S
    I_plot.data_source.data['y'] = I
    R_plot.data_source.data['y'] = R

s1.on_change('value_throttled', update)
s2.on_change('value_throttled', update)

title = Div(text='<h1>SIR model</h1>', styles={'color': 'white', 'background-color': 'black', 'font-size': '30px'})
desc1 = Div(text=r"$$\frac{dS}{dt} = -\beta SI$$", styles={'color': 'white', 'background-color': 'black', 'margin': '10px', 'font-size': '20px'})
desc2 = Div(text=r"$$\frac{dI}{dt} = \beta SI - \gamma I$$", styles={'color': 'white', 'background-color': 'black', 'margin': '10px', 'font-size': '20px'})
desc3 = Div(text=r"$$\frac{dR}{dt} = \gamma I$$", styles={'color': 'white', 'background-color': 'black', 'margin': '10px', 'font-size': '20px'})

desc = column(desc1, desc2, desc3)

main_col = column(title, row(column(desc, s1, s2), fig), background='black', sizing_mode='stretch_both')

curdoc().add_root(main_col)
curdoc().title = 'SIR'
curdoc().theme = 'dark_minimal'
