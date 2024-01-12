import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Load the dataset
data = pd.read_csv('ItvaccinationMergedMap.csv')

# Replace NaN values in the 'gdp_tot' column with 0
data['gdp_tot'].fillna(0, inplace=True)

# Set the page width to a wider layout
st.set_page_config(layout="wide")

# Title of the dashboard
st.title('Vaccination Dashboard')

# Sidebar for navigation
page = st.sidebar.selectbox("Select a Page", ["Dashboard", "Age Range Investigation", "GDP and Population", "Regions in Details","Overtime Investigation"])

if page == "Dashboard":
    # Line chart for dailytotal over time
    daily_chart = px.line(data, x='administration_date', y='dailytotal', title='Daily Vaccination Over Time')
    daily_chart.update_layout(height=400)  # Set the height to your desired value

    st.plotly_chart(daily_chart, use_container_width=True)  # Use container width for responsive plot size
  

    # Create a layout with two columns (col1 and col2)
    col1, col2 = st.columns(2)

    # Bar plot for Total Number of Doses by Dose Type (placed in the first column)
    with col1:
    #   st.subheader('Total Number of Doses by Dose Type')
        dose_sums = data[['first_dose', 'second_dose', 'previous_infection', 'additional_booster_dose', 'second_booster', 'db3']].sum()
        df_plot = pd.DataFrame({'Dose Type': dose_sums.index, 'Count': dose_sums.values})
        fig_doses = px.bar(df_plot, x='Dose Type', y='Count', title= 'Total Number of Doses by Dose Type',
                           labels={'Count': 'Total Number of Doses'},
                           )
        st.plotly_chart(fig_doses, use_container_width=True)

    # Pie chart for suppliers (placed in the second column)
    with col2:
      #  st.subheader('Vaccination Suppliers Distribution')
        suppliers_pie = px.pie(data,title = 'Vaccination Suppliers Distribution', names='supplier')
        st.plotly_chart(suppliers_pie, use_container_width=True)  # Use container width for responsive plot size


    # Assuming you have loaded your data into a DataFrame called data
    region_dailytotal = data.groupby('region_name')['dailytotal'].sum().reset_index()

    # Drop rows with missing values
    region_dailytotal = region_dailytotal.dropna()

    # Convert 'dailytotal' to numeric if needed
    region_dailytotal['dailytotal'] = pd.to_numeric(region_dailytotal['dailytotal'], errors='coerce')
    region_dailytotal = region_dailytotal.dropna()

    # Create a treemap plot
    fig_dailytotal_treemap = px.treemap(region_dailytotal, path=['region_name'], values='dailytotal',
                                        labels={'dailytotal': 'Total Daily Vaccinations'},
                                        title='Daily Total Vaccinations for Each Region (Treemap Plot)')

    st.plotly_chart(fig_dailytotal_treemap, use_container_width=True)


   





elif page == "Age Range Investigation":
    # New bar plot for Distribution of Age Range by Region (placed below col1 and col2)
    #st.subheader('Distribution of Age Range by Region')
    region_age_distribution = data.groupby(['region_name', 'age_range'])['dailytotal'].sum().reset_index()
    fig_age_distribution = px.bar(region_age_distribution, title='Distribution of Age Range by Region', x='region_name', y='dailytotal', color='age_range',
                                  labels={'dailytotal': 'Count', 'region_name': 'Region', 'age_range': 'Age Range'},
                                  width=1000, height=700)
    st.plotly_chart(fig_age_distribution, use_container_width=True)  # Use container width for responsive plot size

    # Sum the doses for each age range
    df_summed = data.groupby('age_range').agg({
        'first_dose': 'sum',
        'second_dose': 'sum',
        'previous_infection': 'sum',
        'additional_booster_dose': 'sum',
        'second_booster': 'sum',
        'db3': 'sum'
    }).reset_index()

    # Melt the DataFrame to create a long-format for Plotly Express
    df_melted = pd.melt(df_summed, id_vars=['age_range'], value_vars=['first_dose', 'second_dose', 'previous_infection', 'additional_booster_dose', 'second_booster', 'db3'],
                        var_name='Dose Type', value_name='Count')

    # Create a bar plot
    fig_age_investigation = px.bar(df_melted, x='Dose Type', y='Count', color='age_range',
                                   labels={'Count': 'Count', 'age_range': 'Age Range', 'Dose Type': 'Dose Type'},
                                   title='Distribution of Doses by Age Range',
                                   width=1000, height=600)

    # Show the plot
    st.plotly_chart(fig_age_investigation, use_container_width=True)  # Use container width for responsive plot size

elif page == "GDP and Population":

       # st.subheader('Comparison of Daily Total with Population Residual for Each Region')
        region_stats_daily_total = data.groupby('region_name').agg({'dailytotal': 'sum', 'pop_resid': 'first'}).reset_index()
        scatter_plot_daily_total = px.scatter(region_stats_daily_total, title='Comparison of Daily Total with Population Residual for Each Region', x='dailytotal', y='pop_resid', color='region_name',
                                              labels={'dailytotal': 'Daily Total', 'pop_resid': 'Population Residual'},
                                              width=800, height=400)
        st.plotly_chart(scatter_plot_daily_total, use_container_width=True)  # Use container width for responsive plot size

    # Scatter plot for Comparison of dailytotal with GDP and Population for Each Region (placed in the fourth column)
       # st.subheader('Comparison of dailytotal with GDP and Population for Each Region')
        region_stats_previous_infection = data.groupby('region_name').agg({'dailytotal': 'sum', 'gdp_tot': 'first', 'pop_resid': 'first'}).reset_index()
        region_stats_previous_infection['gdp_tot'] *= 1000000
        region_stats_previous_infection['pop_resid'].fillna(0, inplace=True)
        scatter_plot_previous_infection = px.scatter(region_stats_previous_infection,title='Comparison of dailytotal with GDP and Population for Each Region',x='dailytotal', y='gdp_tot', size='pop_resid', color='region_name',
                                                     labels={'dailytotal': 'Sum of dailytotal', 'gdp_tot': 'GDP Total', 'pop_resid': 'Population'},
                                                     width=800, height=400)
        st.plotly_chart(scatter_plot_previous_infection, use_container_width=True)  # Use container width for responsive plot size
         # Population Residual, GDP, and Daily Total for Each Region (3D Scatter Plot)
       # st.subheader('Population Residual, GDP, and Daily Total for Each Region (3D Scatter Plot)')
        region_stats_3d = data.groupby('region_name').agg({
            'pop_resid': 'first',
            'gdp_tot': 'first',
            'dailytotal': 'sum'
        }).reset_index()

        region_stats_3d = region_stats_3d.dropna(subset=['pop_resid', 'gdp_tot'])  # Remove rows with NaN values

        # Create a 3D scatter plot
        fig_3d_scatter = px.scatter_3d(region_stats_3d, x='pop_resid', y='gdp_tot', z='dailytotal',
                                    color='region_name', size='dailytotal',
                                    labels={'pop_resid': 'Population Residual', 'gdp_tot': 'GDP Total (Billion Euros)', 'dailytotal': 'Total Daily Vaccinations'},
                                    title='Population Residual, GDP, and Daily Total for Each Region (3D Scatter Plot)',
                                    size_max=30)  # Adjust size_max as needed

        st.plotly_chart(fig_3d_scatter, use_container_width=True)
# ... (previous code)

elif page == "Regions in Details":

    # Population Residual for Each Region (Horizontal Bar Plot)
   # st.subheader('Population Residual for Each Region')
    unique_pop_resid = data.groupby('region_name').agg({'pop_resid': 'first', 'dailytotal': 'sum'}).reset_index()
    unique_pop_resid = unique_pop_resid[unique_pop_resid['pop_resid'].notnull()]  # Remove empty columns

    # Create a horizontal bar plot
    fig_population_residual_bar = px.bar(unique_pop_resid, x='pop_resid', y='region_name',
                                        labels={'pop_resid': 'Population Residual', 'dailytotal': 'Total Daily Vaccinations'},
                                        title='Population Residual for Each Region (Horizontal Bar Plot)',
                                        orientation='h')

    # Update x-axis title
    fig_population_residual_bar.update_layout(xaxis_title='Population Residual')

    st.plotly_chart(fig_population_residual_bar, use_container_width=True)



    # Stacked bar plot for Distribution of Vaccination Doses by Region
  #  st.subheader('Distribution of Vaccination Doses by Region')
    df_summed = data.groupby('region_name').agg({
        'first_dose': 'sum',
        'second_dose': 'sum',
        'previous_infection': 'sum',
        'additional_booster_dose': 'sum',
        'second_booster': 'sum',
        'db3': 'sum'
    }).reset_index()
    df_melted = pd.melt(df_summed, id_vars=['region_name'], value_vars=['first_dose', 'second_dose', 'previous_infection', 'additional_booster_dose', 'second_booster', 'db3'],
                        var_name='Dose Type', value_name='Count')
    fig_vaccination_doses = px.bar(df_melted, x='Count', y='region_name', color='Dose Type',
                                   labels={'Count': 'Count', 'Dose Type': 'Dose Type'},
                                   title='Distribution of Vaccination Doses by Region',
                                   orientation='h', barmode='stack')
    st.plotly_chart(fig_vaccination_doses, use_container_width=True)

    # Bar plot for Distribution of Suppliers by Region (Weighted by dailytotal)
   # st.subheader('Distribution of Suppliers by Region (Weighted by dailytotal)')
    supplier_region_weighted_counts = data.groupby(['region_name', 'supplier'])['dailytotal'].sum().reset_index(name='Weighted_Count')
    fig_supplier_distribution = px.bar(supplier_region_weighted_counts, x='Weighted_Count', y='region_name', color='supplier',
                                       labels={'Weighted_Count': 'Weighted Occurrences'},
                                       title='Distribution of Suppliers by Region (Weighted by dailytotal)',
                                       orientation='h')
    st.plotly_chart(fig_supplier_distribution, use_container_width=True)

   # GDP for Each Region (Treemap Plot)
  #  st.subheader('GDP for Each Region (Treemap Plot)')
    region_gdp = data.groupby('region_name')['gdp_tot'].first().reset_index()
    region_gdp = region_gdp.dropna(subset=['gdp_tot'])  # Remove rows with NaN values

    # Create a treemap plot
    fig_gdp_treemap = px.treemap(region_gdp, path=['region_name'], values='gdp_tot',
                                labels={'gdp_tot': 'GDP Total'},
                                title='GDP for Each Region (Treemap Plot)')

    st.plotly_chart(fig_gdp_treemap, use_container_width=True)

 


elif page == "Overtime Investigation":
    # Line plot for Daily Vaccination Counts Over Time by Supplier
  #  st.subheader('Daily Vaccination Counts Over Time by Supplier')

    # Create an interactive line plot using Plotly Express
    fig_supplier_overtime = px.line(data, x='administration_date', y='dailytotal', color='supplier',
                                    labels={'dailytotal': 'Daily Vaccination Count'},
                                    title='Vaccination Counts Over Time by Supplier')

    # Add a range slider for date selection
    fig_supplier_overtime.update_layout(xaxis_rangeslider_visible=True)

    # Show the plot
    st.plotly_chart(fig_supplier_overtime, use_container_width=True)

    # Subplot for Number of Doses Administered Over Time
   # st.subheader('Number of Doses Administered Over Time')
    DosesOverTime_df = data[['administration_date', 'first_dose', 'second_dose', 'previous_infection', 'additional_booster_dose', 'second_booster', 'db3']].copy()
    DosesOverTime_df.set_index('administration_date', inplace=True)

    # Define a custom color palette with bold colors
    custom_palette = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6", "#34495e"]

    fig_doses_overtime = make_subplots(rows=1, cols=1)

    # Iterate over the columns and add traces
    for column in DosesOverTime_df.columns:
        fig_doses_overtime.add_trace(go.Scatter(x=DosesOverTime_df.index, y=DosesOverTime_df[column], mode='lines', name=column, line=dict(width=2.5)))

    # Add a range slider for date selection
    fig_doses_overtime.update_layout(xaxis_rangeslider_visible=True)

    # Update layout for better presentation
    fig_doses_overtime.update_layout(title_text='Number of Doses Administered Over Time',
                                    xaxis_title='Administration Date',
                                    yaxis_title='Cumulative Count',
                                    legend_title='Dose Type')

    # Show the plot
    st.plotly_chart(fig_doses_overtime, use_container_width=True)
