from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Select, Panel, Tabs
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.transform import dodge
import pandas as pd

# Load and preprocess the data
data = pd.read_csv("Datasets/ProdAgri.csv")
data.columns = data.columns.str.strip()
data['Occurrence'] = data['Occurrence'].astype(str)

# Initial year selection
years = list(data['Occurrence'].unique())
start_year_select = Select(title="Start Year", value=years[0], options=years)
end_year_select = Select(title="End Year", value=years[-1], options=years)

# Data source for the line plot
sum_valeur = data.groupby('Occurrence')['Valeur'].sum().reset_index()
median_valeur = data.groupby('Occurrence')['Valeur'].median().reset_index()

sum_median_source = ColumnDataSource(sum_valeur)
median_source = ColumnDataSource(median_valeur)

# Sum and median plot
sum_median_plot = figure(title="Sum & Median of Valeur by Year", x_axis_label='Year', y_axis_label='Valeur')
sum_median_plot.line('Occurrence', 'Valeur', legend_label='Sum', color='blue', line_width=2, source=sum_median_source)
sum_median_plot.line('Occurrence', 'Valeur', legend_label='Median', color='green', line_width=2, source=median_source)

# Data source for the bar plot
def get_filiere_data(start_year, end_year):
    filtered_data = data[(data['Occurrence'] >= start_year) & (data['Occurrence'] <= end_year)]
    return filtered_data.groupby('Filière')['Valeur'].sum().reset_index()

initial_start_year = start_year_select.value
initial_end_year = end_year_select.value
filiere_data = get_filiere_data(initial_start_year, initial_end_year)
filiere_source = ColumnDataSource(filiere_data)

# Bar plot for Sum of Valeur by Filière
bar_plot = figure(x_range=filiere_data['Filière'], title="Sum of Valeur by Filière", x_axis_label='Filière', y_axis_label='Sum Valeur')
bar_plot.vbar(x=dodge('Filière', -0.25, range=bar_plot.x_range), top='Valeur', width=0.5, source=filiere_source, color="firebrick")
bar_plot.xaxis.major_label_orientation = 1.0  # Rotate x-axis labels 90 degrees

# Callback function to update the plots based on selected year range
def update_plots(attr, old, new):
    start_year = start_year_select.value
    end_year = end_year_select.value

    # Update line plot
    filtered_sum_valeur = sum_valeur[(sum_valeur['Occurrence'] >= start_year) & (sum_valeur['Occurrence'] <= end_year)]
    filtered_median_valeur = median_valeur[(median_valeur['Occurrence'] >= start_year) & (median_valeur['Occurrence'] <= end_year)]
    sum_median_source.data = dict(ColumnDataSource(filtered_sum_valeur).data)
    median_source.data = dict(ColumnDataSource(filtered_median_valeur).data)

    # Update bar plot
    updated_filiere_data = get_filiere_data(start_year, end_year)
    filiere_source.data = dict(ColumnDataSource(updated_filiere_data).data)
    bar_plot.x_range.factors = list(updated_filiere_data['Filière'])

# Attach the callback to the year selection widgets
start_year_select.on_change('value', update_plots)
end_year_select.on_change('value', update_plots)

# Layout for Dashboard 1
dashboard1_layout = row(column(start_year_select, end_year_select), sum_median_plot, bar_plot)

# Add the layout to the current document
curdoc().add_root(dashboard1_layout)
