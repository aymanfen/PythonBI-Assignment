from bokeh.io import curdoc,show
from bokeh.models import ColumnDataSource, Select, TabPanel, Tabs
from bokeh.plotting import figure
from bokeh.layouts import column, row
import pandas as pd

# Load and preprocess the data
data = pd.read_csv("Datasets/ProdAgri.csv")
data.columns = data.columns.str.strip()
data['Occurrence'] = data['Occurrence'].astype(str)

years = list(data['Occurrence'].unique())

# Dashboard1

#datasources and plots
start_year_select = Select(title="Start Year", value=years[0], options=years)
end_year_select = Select(title="End Year", value=years[-1], options=years)

sum_valeur = data.groupby('Occurrence')['Valeur'].sum().reset_index()
sum_median_source = ColumnDataSource(sum_valeur)

sum_median_plot = figure(title="Sum of Valeur by Year", x_axis_label='Year', y_axis_label='Valeur')
sum_median_plot.line('Occurrence', 'Valeur', legend_label='Sum', color='blue', line_width=2, source=sum_median_source)

#update date
def get_filiere_data(start_year, end_year):
    filtered_data = data[(data['Occurrence'] >= start_year) & (data['Occurrence'] <= end_year)]
    return filtered_data.groupby('Filière')['Valeur'].sum().reset_index()

initial_start_year = start_year_select.value
initial_end_year = end_year_select.value
filiere_data = get_filiere_data(initial_start_year, initial_end_year)
filiere_source = ColumnDataSource(filiere_data)

bar_plot = figure(x_range=filiere_data['Filière'], title="Sum of Valeur by Filière", x_axis_label='Filière', y_axis_label='Sum Valeur')
bar_plot.vbar(x='Filière', top='Valeur', width=0.5, source=filiere_source, color="firebrick")
bar_plot.xaxis.major_label_orientation = 1.0  

#update plots
def update_plots(attr, old, new):
    start_year = start_year_select.value
    end_year = end_year_select.value

    filtered_sum_valeur = sum_valeur[(sum_valeur['Occurrence'] >= start_year) & (sum_valeur['Occurrence'] <= end_year)]
    sum_median_source.data = dict(filtered_sum_valeur)
    
    updated_filiere_data = get_filiere_data(start_year, end_year)
    filiere_source.data = dict(updated_filiere_data)
    bar_plot.x_range.factors = list(updated_filiere_data['Filière'])

start_year_select.on_change('value', update_plots)
end_year_select.on_change('value', update_plots)

dashboard1_layout = row(column(start_year_select, end_year_select), sum_median_plot, bar_plot)
dashboard1 = TabPanel(child=dashboard1_layout, title="Générale")

# Dashboard2

#datasources and plots
filliere_select = Select(title="Filière", value=data['Filière'].unique()[0], options=list(data['Filière'].unique()))

filliere_sum_valeur_plot = figure(title="Sum of Valeur by Year for Selected Filière", x_axis_label='Year', y_axis_label='Sum Valeur')
filliere_bar_data=data.groupby("Occurrence")['Valeur'].sum().reset_index()
filliere_sum_valeur_source = ColumnDataSource(data=dict(Occurrence=[], Valeur=[]))
filliere_sum_valeur_line = filliere_sum_valeur_plot.line('Occurrence', 'Valeur', source=filliere_sum_valeur_source, line_width=2)

filliere_bar_plot = figure(title="Count of Valeur of Selected Filière by Year", x_axis_label='Year', y_axis_label='Sum Valeur')
filliere_bar_source = ColumnDataSource(data=dict(Occurrence=[], Valeur=[]))
filliere_bar_plot.vbar(x='Occurrence', top='Valeur', source=filliere_bar_source, color="green")

#update plots
def update_dashboard2(attr, old, new):
    selected_filliere = filliere_select.value
    filtered_data = data[data['Filière'] == selected_filliere]
    
    # Update line plot
    filliere_sum_valeur_data = filtered_data.groupby('Occurrence')['Valeur'].sum().reset_index()
    filliere_sum_valeur_source.data = dict(Occurrence=filliere_sum_valeur_data['Occurrence'], Valeur=filliere_sum_valeur_data['Valeur'])
    
    # Update bar plot
    filliere_bar_data = filtered_data.groupby('Occurrence')['Valeur'].count().reset_index()
    #filliere_bar_source.data = dict(Occurrence=filliere_bar_data['Occurrence'], Valeur=filliere_bar_data['Valeur'])
    filliere_bar_source.data = dict(Occurrence=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021], Valeur=filliere_bar_data['Valeur'])
    
    
filliere_select.on_change('value', update_dashboard2)

dashboard2_layout = row(filliere_select, filliere_sum_valeur_plot, filliere_bar_plot)
dashboard2 = TabPanel(child=dashboard2_layout, title="Détails Filières")


# Dashboard3

#datasources and plots
produit_select = Select(title="Produit", value=data['Produit'].unique()[0], options=list(data['Produit'].unique()))


produit_sum_valeur_plot = figure(title="Sum of Valeur by Year for Selected Produit", x_axis_label='Year', y_axis_label='Sum Valeur')
produit_sum_valeur_source = ColumnDataSource(data=dict(Occurrence=[], Valeur=[]))
produit_sum_valeur_line = produit_sum_valeur_plot.line('Occurrence', 'Valeur', source=produit_sum_valeur_source, line_width=2)


produit_bar_plot = figure(title="Count of Valeur of Selected Produit by Year", x_axis_label='Year', y_axis_label='Sum Valeur')
produit_bar_source = ColumnDataSource(data=dict(Occurrence=[], Valeur=[]))
produit_bar_plot.vbar(x='Occurrence', top='Valeur', source=produit_bar_source, color="orange")

#update plots
def update_dashboard3(attr, old, new):
    selected_produit = produit_select.value
    filtered_data = data[data['Produit'] == selected_produit]
    
    # Update line plot
    produit_sum_valeur_data = filtered_data.groupby('Occurrence')['Valeur'].sum().reset_index()
    produit_sum_valeur_source.data = dict(Occurrence=produit_sum_valeur_data['Occurrence'], Valeur=produit_sum_valeur_data['Valeur'])
    
    # Update bar plot
    produit_bar_data = filtered_data.groupby('Occurrence')['Valeur'].count().reset_index()
    produit_bar_source.data = dict(Occurrence=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021], Valeur=produit_bar_data['Valeur'])

produit_select.on_change('value', update_dashboard3)

dashboard3_layout = row(produit_select, produit_sum_valeur_plot, produit_bar_plot)
dashboard3 = TabPanel(child=dashboard3_layout, title="Détails Produit")



# Combine all Dashboards
tabs = Tabs(tabs=[dashboard1, dashboard2, dashboard3])


# Add the tabs to the current document
curdoc().add_root(tabs)
