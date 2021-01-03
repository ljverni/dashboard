import pandas as pd
from datetime import datetime
import calendar
import numpy as np
import json
import re
import cufflinks as cf
from matplotlib.gridspec import GridSpec
from matplotlib.legend import Legend
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib import pyplot as plt
plt.style.use("seaborn")

import plotly.figure_factory as ff
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
cf.go_offline()

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv(r"C:\Users\l.verni\Desktop\test.csv")
##############################################################################
#CLEAN DATA#
############

def correct(old_word, group):
    for item in group:
        if item[0:3] in str.lower(str(old_word)):
            return item
    return group[-1]  

def clean_gp(value):
    if value == "nan":
        return 0
    else:
        value = str(value).replace("£", "")
        value = str(value).replace(",", "")
        return int(float(value))
    
df.columns= df.columns.str.lower()
df = df.apply(lambda x: x.astype(str).str.lower()).rename(columns={"lead source": "lead_source", "sales person working": "exec_working"})
sources = ["existing", "lapsed", "email", "web follow up", "call", "liveChat", "other"]
products = ["ram", "various", "server", "ssd", "hdd", "switch", "storage", "laptop", "desktop", "other"]
df["lead_source"] = df["lead_source"].apply(lambda x: correct(x, sources))
df["product"] = df["product"].apply(lambda x: correct(x, products))
df["gp"] = df["gp"].apply(lambda x: clean_gp(x))
df["outcome"] = df["outcome"].apply(lambda x: "0" if str(x) == "nan" else "1")
df["exec"] = df["exec"].apply(lambda x: x.replace(" ", ""))
df["date"] = df["date"].apply(lambda x: (datetime.strptime(x, "%d/%m/%Y")).strftime("%d/%m"))

##############################################################################
#LISTS#
#######

#DATES LIST
last_day = calendar.monthrange(int(datetime.today().strftime("%Y")), int(datetime.today().strftime("%m")))[1]
month, year = str(datetime.today().strftime("%m")), str(datetime.today().strftime("%Y"))
current_month = datetime.now().strftime("%B")
#b_days = [d.strftime("%d/%m") for d in pd.bdate_range(start="{m}/{d}/{y}".format(m = month, d = "01", y = year), end="{m}/{d}/{y}".format(m = month, d = last_day, y = year))]
b_days = [pd.bdate_range(start="{m}/{d}/{y}".format(m = month, d = "01", y = year), end="{m}/{d}/{y}".format(m = month, d = last_day, y = year)).date][0]
dates = list(df["date"].unique())
date_labels = [str(date)[8:10]+str(date)[4:7] for date in b_days]
#LEAD SOURCE LIST
sources = list(df["lead_source"].unique())
#EXECS LIST
execs = list(df["exec"].unique())
#COLORS LIST
color_dict = colors = {"mads": "#D4908B", "callum": "#A4D992", "ali": "#A1E5E5", "tom": "#9B9AD1", "karl": "#D19AD1", "luciano": "#D1D19A"}
default_colors = [color_dict[key] for key in color_dict]
#PRODUCT LIST
products = list(df["product"].unique())

##############################################################################
#QUERIES#
#########

#Quotes
quoted_total = df["outcome"].count()
quoted_total_date = df.groupby(["date"])["outcome"].count()

gp_quoted_total = df.agg({"gp":"sum"})
gp_quoted_total_date = df.groupby(["date"]).agg({"gp":"sum"})

quoted_exec = df.groupby(["exec"])["gp"].count().sort_values(ascending=False)
quoted_exec_date = df.groupby(["exec", "date"])["gp"].count().rename("quotes")

gp_quoted_exec = df.groupby(["exec"]).agg({"gp":"sum"}).sort_values(by="gp", ascending=False)
gp_quoted_exec_date = df.groupby(["exec", "date"]).agg({"gp":"sum"})


#Sales
sales_total = df[df["outcome"] == "1"]["gp"].count()
sales_total_date = df[df["outcome"] == "1"].groupby(["date"])["outcome"].count()

gp_total = df[df["outcome"] == "1"].agg({"gp":"sum"})
gp_total_date = df[df["outcome"] == "1"].groupby(["date"]).agg({"gp":"sum"})

gp_sales_exec = df[df["outcome"] == "1"].groupby(["exec"]).agg({"gp":"sum"}).sort_values(by="gp", ascending=False)
gp_sales_exec_date = df[df["outcome"] == "1"].groupby(["exec", "date"]).agg({"gp":"sum"})

sales_exec = df[df["outcome"] == "1"].groupby(["exec"])["gp"].count().sort_values(ascending=False)
sales_exec_date = df[df["outcome"] == "1"].groupby(["exec", "date"])["gp"].count()

total_quotes_sales_date = pd.concat([quoted_total_date.rename("quotes"), sales_total_date.rename("sales")], axis=1).sort_index()
gp_sales_quotes_exec_date = df[df["outcome"] == "1"].groupby(["exec", "date"]).agg({"gp":"sum"})

sales_quotes_exec_date = pd.DataFrame(quoted_exec_date)
sales_quotes_exec_date["sales"] = sales_exec_date
sales_quotes_exec_date = sales_quotes_exec_date.apply(lambda x: x.replace(np.nan, 0)).astype(int)

#Query dictionary
sales_total = df[df["outcome"] == "1"]["gp"].count()
sales_total_date = df[df["outcome"] == "1"].groupby(["date"])["outcome"].count()

gp_total = df[df["outcome"] == "1"].agg({"gp":"sum"})
gp_total_date = df[df["outcome"] == "1"].groupby(["date"]).agg({"gp":"sum"})

gp_sales_exec = df[df["outcome"] == "1"].groupby(["exec"]).agg({"gp":"sum"}).sort_values(by="gp", ascending=False)
gp_sales_exec_date = df[df["outcome"] == "1"].groupby(["exec", "date"]).agg({"gp":"sum"})

sales_exec = df[df["outcome"] == "1"].groupby(["exec"])["gp"].count().sort_values(ascending=False)
sales_exec_date = df[df["outcome"] == "1"].groupby(["exec", "date"])["gp"].count()

total_quotes_sales_date = pd.concat([quoted_total_date.rename("quotes"), sales_total_date.rename("sales")], axis=1).sort_index()
gp_sales_quotes_exec_date = df[df["outcome"] == "1"].groupby(["exec", "date"]).agg({"gp":"sum"})

sales_quotes_exec_date = pd.DataFrame(quoted_exec_date)
sales_quotes_exec_date["sales"] = sales_exec_date
sales_quotes_exec_date = sales_quotes_exec_date.apply(lambda x: x.replace(np.nan, 0)).astype(int)

#Close ratio
close_ratio_total = int(round((sales_total / quoted_total)*100)+1)
close_ratio_exec = ((sales_exec / quoted_exec)*100).sort_values(ascending=False)
close_ratio = sales_total / quoted_total
close_ratio_xday = ((sales_total_date / quoted_total_date) * 100)
highest_ratio_day = close_ratio_xday.max()
lowest_ratio_day = close_ratio_xday.min()

#Customers
quoted_new_total_perc = "{a}{b}".format(a=int((df[(df["lead_source"] != "existing")]["lead_source"].count() / quoted_total)*100), b="%")
quoted_new_exec_perc = df[(df["lead_source"] != "existing")].groupby(["exec"])["gp"].count().sort_values(ascending=False) / df.groupby(["exec"])["gp"].count().sort_values(ascending=False)*100

sales_new_total_perc = "{a}{b}".format(a=int((df[(df["lead_source"] != "existing") & (df["outcome"] == "1")]["lead_source"].count() / sales_total)*100), b="%")
sales_new_exec_perc = df[(df["lead_source"] != "existing") & (df["outcome"] == "1")].groupby(["exec"])["gp"].count().sort_values(ascending=False) / df[df["outcome"] == "1"].groupby(["exec"])["gp"].count().sort_values(ascending=False)*100

gp_new_sales_total = df[(df["lead_source"] != "existing") & (df["outcome"] == "1")]["gp"].agg({"gp":"sum"})
gp_new_sales_exec = df[(df["lead_source"] != "existing") & (df["outcome"] == "1")].groupby(["exec"]).agg({"gp":"sum"}).sort_values(by="gp", ascending=False)

#Lead source
sales_lead_source = df[df["outcome"] == "1"].groupby(["lead_source"])["outcome"].count().sort_values(ascending=True)
gp_lead_source = df[df["outcome"] == "1"].groupby(["lead_source"]).agg({"gp":"sum"}).sort_values(by="gp", ascending=True)

sales_new_lead_source = df[(df["lead_source"] != "existing") & (df["outcome"] == "1")].groupby(["lead_source"])["outcome"].count()
gp_new_lead_source = df[(df["lead_source"] != "existing") & (df["outcome"] == "1")].groupby(["lead_source"]).agg({"gp":"sum"})

sales_new_lead_source_exec = df[(df["lead_source"] != "existing") & (df["outcome"] == "1")].groupby(["exec", "lead_source"])["outcome"].count()
gp_new_lead_source_exec = df[(df["lead_source"] != "existing") & (df["outcome"] == "1")].groupby(["exec", "lead_source"]).agg({"gp":"sum"})

gp_existing_lead_source = df[(df["lead_source"] == "existing") & (df["outcome"] == "1")].groupby(["lead_source"]).agg({"gp":"sum"})
gp_existing_new_lead_source = gp_existing_lead_source.reset_index().append({"lead_source": "new", "gp": df[(df["lead_source"] != "existing") & (df["outcome"] == "1")].agg({"gp": "sum"}).values[0]}, ignore_index=True).set_index(["lead_source"])["gp"]

sales_existing_lead_source = df[(df["lead_source"] == "existing") & (df["outcome"] == "1")].groupby(["lead_source"]).agg({"gp":"count"}).rename(columns={"gp" : "sales"}).reset_index()
sales_existing_new_lead_source = pd.concat([sales_existing_lead_source, pd.DataFrame(data={"lead_source": ["new"], "sales": [sales_new_lead_source.sum()]})], ignore_index=True).set_index(["lead_source"])["sales"]

#Execs dataframe
df_execs_a = df.groupby(["exec"]).agg({"gp": ["count", "sum", "min", "max", "mean"]}).rename(columns={"gp": "quotes", "count": "quotes_count", "sum": "quotes_sum", "min": "quotes_min", "max": "quotes_max", "mean": "quotes_mean"})

df_execs_b = df[df["outcome"] == "1"].groupby(["exec"]).agg({"gp": ["count", "sum", "min", "max", "mean"]}).rename(columns={"gp": "sales", "count": "sales_count", "sum": "sales_sum", "min": "sales_min", "max": "sales_max", "mean": "sales_mean"})

df_execs_master = pd.concat([df_execs_a, df_execs_b], axis=1)
df_execs_master.columns = df_execs_master.columns.droplevel(0)

df_execs_master["close_ratio"] = round((df_execs_master["sales_count"] / df_execs_master["quotes_count"])*100, 2)
#df_execs_master.columns.set_levels(["quotes_count], level=1, inplace=True)


df_execs_dict = {}
for exec in df["exec"].unique():
    frame = df[df["exec"]==exec].reset_index(drop=True)
    df_execs_dict[exec] = frame
    
##############################################################################
#Analytics#
###########

#Daily quotes & sales
df1 = total_quotes_sales_date.reset_index()
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df1.date, y=df1.quotes, mode="lines+markers", name="Quotes", line={"color": "#85C6B0", "width": 2, "dash": "dashdot"}))
fig1.add_trace(go.Scatter(x=df1.date, y=df1.sales, mode="lines+markers", name="Sales", line={"color": "#006D5B", "width": 2}))
fig1.update_layout(
    hovermode="closest",
    title=f"Daily quotes & sales - {current_month}",
    title_font_family="Playfair",
    title_font_size=20,
    xaxis={"showline": True, "showgrid": False, "tickfont":{"family": "Playfair"}, "tickvals": [i for i in range(0, len(date_labels))],
        "ticktext": date_labels},
    yaxis={"showline": True, "showgrid": False, "tickfont":{"family": "Playfair"}},
    legend={"font":{"family": "Playfair"}},
    margin={"t":50}
)

#Daily GP
df2 = gp_total_date.reset_index()
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=df2.date, y=df2.gp, hovertemplate="%{y:$.2f}<extra></extra>"))

fig2.update_traces(marker_color="#55AFB7", marker_line_color="rgb(8,48,107)", marker_line_width=1.5, opacity=0.6)

fig2.update_xaxes(color="rgb(8,48,107)")

fig2.update_layout(
    autosize=False,
    width=700,
    height=200,
    margin={"l":5, "r": 5, "t": 50, "b": 50},
    plot_bgcolor="rgba(0,0,0,0)",
    hovermode="closest",
    title=f"Daily GP - {current_month}",
    title_font_family="Playfair",
    title_font_size=20,
    xaxis={"showgrid": False, "tickfont":{"family": "Playfair"}, "tickvals": [i for i in range(0, len(date_labels))],
        "ticktext": date_labels, "zeroline": False},
    yaxis={"showticklabels": False, "showgrid": False, "tickfont":{"family": "Playfair"}, "zeroline": False}
)

#Lead source & new customers
df3_sales = sales_lead_source.reset_index()
df3_gp = gp_lead_source.reset_index()
df3_ex_sales = sales_existing_new_lead_source.reset_index()
df3_ex_gp = gp_existing_new_lead_source.reset_index()

fig3a = make_subplots(rows=1, cols=2,subplot_titles=("Sales by lead source", "Profit by lead source"))
                    
fig3a.add_trace(go.Bar(x=df3_sales.outcome, y=df3_sales.lead_source, orientation="h", name=""), row=1, col=1)
fig3a.update_traces(marker_color="#006D5B", marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6, row=1, col=1)

fig3a.add_trace(go.Bar(x=df3_gp.gp, y=df3_gp.lead_source, orientation="h", name=""), row=1, col=2)
fig3a.update_traces(marker_color="#55AFB7", marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6, row=1, col=2)

fig3a.update_layout(
    showlegend=False,
    font_family="Playfair",
    autosize=False,
    margin={"t":50, "b":50, "r":5, "l":5},
    width=600,
    height=200,
    yaxis={"showline": False, "showgrid": False},
    xaxis={"showline": False, "showgrid": False, "showticklabels":False},
    plot_bgcolor="rgba(0,0,0,0)",
)


fig3b = make_subplots(rows=1, cols=2,subplot_titles=("Total sales existing & new customers", "Total profit existing & new customers"))

fig3b.add_trace(go.Bar(x=df3_ex_sales.lead_source, y=df3_ex_sales.sales, name=""), row=1, col=1)
fig3b.update_traces(marker_color="#006D5B", marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6, row=1, col=1)

fig3b.add_trace(go.Bar(x=df3_ex_gp.lead_source, y=df3_ex_gp.gp, name=""), row=1, col=2)
fig3b.update_traces(marker_color="#55AFB7", marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6, row=1, col=2)

fig3b.update_layout(
    showlegend=False,
    font_family="Playfair",
    autosize=False,
    margin={"t":50, "b":50, "r":5, "l":5},
    width=600,
    height=200,
    yaxis={"showline": False, "showgrid": False, "showticklabels":False},
    xaxis={"showline": False, "showgrid": False},
    plot_bgcolor="rgba(0,0,0,0)",
)

#Target
df4 = int(gp_total)
values = [df4, int(50000-df4)]
labels = ["Current GP", "GP left to target"]
fig4 = px.pie(names=labels, values=values, color_discrete_sequence=px.colors.sequential.Tealgrn, hole=.6)

fig4.update_traces(showlegend=False, textinfo="none")

fig4.update_layout(
    autosize=False,
    width=150,
    height=200,
    margin={"l":40, "r":0, "t":5, "b":5}
)

#Execs
df5_sales = sales_exec_date.to_frame().reset_index().rename(columns={"gp": "sales"}).drop(columns="date")
df5_gp = gp_sales_exec_date.reset_index()

fig5 = make_subplots(rows=2, cols=1, subplot_titles=("Sales - Execs", "GP - Execs"), vertical_spacing = 0.2)

fig5.add_trace(go.Box(x=df5_sales.exec, y=df5_sales.sales, name=""), row=1, col=1)
fig5.update_traces(marker_color="#55AFB7", marker_line_color='rgb(8,48,107)', marker_line_width=1.5, row=1, col=1)

fig5.add_trace(go.Box(x=df5_gp.exec, y=df5_gp.gp, name=""), row=2, col=1)
fig5.update_traces(marker_color="#006D5B", marker_line_color='rgb(8,48,107)', marker_line_width=1.5, row=2, col=1)

fig5.update_layout(
    autosize=False,
    width=700,
    height=200,
    margin={"l":30, "r": 50, "t": 50, "b": 20},
    hovermode="closest",
    title_font_size=20,
    showlegend=False,
    font_family="Playfair",
    yaxis={"showline": False, "showgrid": False, "showticklabels":False},
    xaxis={"showline": False, "showgrid": False, "showticklabels":False},
    plot_bgcolor="rgba(0,0,0,0)",
)

#Execs ranking

df6 = gp_sales_exec.reset_index().sort_values(by="gp", ascending=True)
fig6 = px.bar(df6, x=df6.gp, y=df6.exec, color="gp", color_continuous_scale=px.colors.sequential.Tealgrn, hover_name="exec", hover_data={"gp":True, "exec":False}, orientation="h")


fig6.update_traces(opacity=0.6)

fig6.update_layout(
    width=500,
    height=200,
    hovermode="closest",
    title=f"Total Profit - Execs - {current_month}",
    title_font_family="Playfair",
    title_font_size=20,
    xaxis={"visible": False, "showticklabels": False, "title": "", "showline": True, "showgrid": False, "tickfont":{"family": "Playfair"}},
    yaxis={"title": "", "showline": True, "showgrid": False, "tickfont":{"family": "Playfair"}},
    margin={"l":0, "r":30, "b":10, "t": 50},
    coloraxis_showscale=False,
    plot_bgcolor="rgba(0,0,0,0)"
    )


#Execs share

df7 = df6
fig7 = px.pie(names=df7.exec, values=df7.gp, color_discrete_sequence=px.colors.sequential.Tealgrn)

fig7.update_traces(textinfo="none")

fig7.update_layout(
    legend={"x": 1.1 ,"y": 0.49},
    autosize=False,
    width=300,
    height=200,
    margin={"l":5, "r":20, "b":10, "t": 10},
    )

#Execs stats
df8 = df_execs_master[["sales_count", "sales_sum", "quotes_count", "close_ratio"]].transpose().sort_index(ascending=True)

fig8 = ff.create_annotated_heatmap(z=df8.values.tolist(), x=df8.columns.tolist(), y= df8.index.tolist(), colorscale="Tealgrn")

fig8.update_layout(
    title_text="Execs stats",
    autosize=False,
    width=420,
    height=200,
    margin={"l":5, "r":0, "b":5, "t":50}
    )

#Team stats

fig9 = go.Figure()

fig9.add_trace(go.Indicator(
    mode = "number",
    value = gp_total[0],
    delta = {"reference": 50000},
    domain = {'x': [0, 0.5], 'y': [0.70, 1]},
    number = {"prefix": "£"},
    title = {"text": "Total profit"}
    ))


fig9.add_trace(go.Indicator(
    mode = "number",
    value = sales_total,
    domain = {'x': [0, 0.5], 'y': [0, 0.30]},
    title = {"text": "Total sales"}
    ))

fig9.add_trace(go.Indicator(
    mode = "number",
    value = quoted_total,
    domain = {'x': [0.5, 1], 'y': [0.70, 1]},
    title = {"text": "Total quotes"}
    ))

fig9.add_trace(go.Indicator(
    mode = "number",
    value = close_ratio_total,
    domain = {'x': [0.5, 1], 'y': [0, 0.30]},
    number = {"suffix": "%"},
    title = {"text": "Close ratio"}
    ))

fig9.update_layout(
    grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
    autosize=False,
    width=225,
    height=200,
    margin={"l":25, "r":0, "b":50, "t":50},
    font_size=5,
    font_color="#74AF9B",
    font_family="Playfair"
    )

##############################################################################
#DASHBOARD#
###########


app.layout = html.Div([
        dbc.Row(
            [
                dbc.Col(html.Div(dcc.Graph(figure=fig4)), width=2, style={"border-right-width":"5px" ,"border-right-radius": "5px", "border-right-color":"#E0FFF1", "border-right-style":"solid"}),
                dbc.Col(html.Div(dcc.Graph(figure=fig2)), width=7, style={"border-right-width":"5px" ,"border-right-radius": "5px", "border-right-color":"#E0FFF1", "border-right-style":"solid"}),
                dbc.Col(html.Div(dcc.Graph(figure=fig9)), width=3, style={"border-right-width":"30px" ,"border-right-radius": "5px", "border-right-color":"#E0FFF1", "border-right-style":"solid"}),
                ], 
            ),
        
        dbc.Row(
            [
                dbc.Col(html.Div(dcc.Graph(figure=fig3a)), width=6, style={"border-width":"20px" ,"border-radius": "5px", "border-color":"#E0FFF1", "border-style":"solid"}),
                dbc.Col(html.Div(dcc.Graph(figure=fig3b)), width=6, style={"border-width":"20px" ,"border-radius": "5px", "border-color":"#E0FFF1", "border-style":"solid"})
                ], 
            ), 
            
        dbc.Row(
            [
                dbc.Col(html.Div(dcc.Graph(figure=fig6)), width=4.5, style={"border-right-width":"20px" ,"border-right-radius": "5px", "border-right-color":"#E0FFF1", "border-right-style":"solid"}),
                dbc.Col(html.Div(dcc.Graph(figure=fig8)), width=4.5, style={"border-right-width":"20px" ,"border-right-radius": "5px", "border-right-color":"#E0FFF1", "border-right-style":"solid"}),
                dbc.Col(html.Div(dcc.Graph(figure=fig7)), width=3, style={"border-right-width":"20px" ,"border-right-radius": "5px", "border-right-color":"#E0FFF1", "border-right-style":"solid"}),
                ],
            ),
        ])  
    





app.run_server(debug=True, use_reloader=False)



