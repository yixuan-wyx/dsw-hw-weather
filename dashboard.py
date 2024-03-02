import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar


file = './new.csv'
data = pd.read_csv(file)


def dashboard_1(data):
    st.title("Weather Data Interactive Dashboard")
    st.write("Use the left Sidebar to select a year to display the monthly average temperature:")

    data = pd.read_csv(file)

    # Sidebar for year selection
    # year = st.sidebar.selectbox('Year', sorted(data['year'].unique()))
    year = st.slider('Select a year to view monthly extremes:', 
                     min_value=int(data['year'].min()), 
                     max_value=int(data['year'].max()), 
                     value=int(data['year'].max()),
                     key='dashboard_1_year_slider')

    # Filter data for the selected year
    filtered_data = data[data['year'] == year]

    # Group by month to get average temperature
    monthly_avg = filtered_data.groupby('month')['monthly_avg_Ftemp'].mean().reset_index()
    season_avg = filtered_data.groupby('month')['seasonal_avg_Ftemp'].mean().reset_index()

    # Plotting
    # fig, ax = plt.subplots()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))

    # Monthly average temperature plot
    ax1.plot(monthly_avg['month'], monthly_avg['monthly_avg_Ftemp'], marker='o')
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)])
    for i, txt in enumerate(monthly_avg['monthly_avg_Ftemp']):
        ax1.annotate(f"{txt:.2f}", (monthly_avg['month'][i], monthly_avg['monthly_avg_Ftemp'][i]))
    ax1.set_title(f"Monthly Average Temperature in {year}")
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Avg Temperature (°F)')
    ax1.grid(True)

    # Seasonal average temperature plot
    ax2.plot(season_avg['month'], season_avg['seasonal_avg_Ftemp'], marker='o', color='orange')
    ax2.set_xticks(range(1, 13))
    ax2.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)])
    for i, txt in enumerate(season_avg['seasonal_avg_Ftemp']):
        ax2.annotate(f"{txt:.2f}", (season_avg['month'][i], season_avg['seasonal_avg_Ftemp'][i]))
    ax2.set_title(f"Seasonal Average Temperature in {year}")
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Seasonal Avg Temperature (°F)')
    ax2.grid(True)

    st.pyplot(fig)


def visualize_temperature_threshold(data):
    st.subheader("Yearly Average Temperature Analysis")
    st.write("Visualization of the first year when the average temperature exceeds 55 degrees:")

    # Calculate yearly average temperature
    yearly_avg = data.groupby('year')['yearly_avg_Ftemp'].first().reset_index()

    # Find the first year where the average temperature exceeds 55 degrees
    warm_year = yearly_avg[yearly_avg['yearly_avg_Ftemp'] > 55].min()['year']

    # Plotting
    fig, ax = plt.subplots()
    ax.plot(yearly_avg['year'], yearly_avg['yearly_avg_Ftemp'], marker='o', linestyle='-', color='blue')
    ax.axhline(y=55, color='r', linestyle='--')
    ax.text(x=yearly_avg['year'].min(), y=55, s=' 55 °F', color='red', va='bottom')

    # Highlighting the year
    if not pd.isnull(warm_year):
        ax.axvline(x=warm_year, color='green', linestyle='--')
        ax.text(x=warm_year, y=yearly_avg['yearly_avg_Ftemp'].min(), s=f' {warm_year}', color='green', va='bottom', ha='right')

    ax.set_title("Yearly Average Temperature")
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Temperature (°F)')
    ax.grid(True)

    st.pyplot(fig)

    if not pd.isnull(warm_year):
        st.write(f"The first year where the average temperature exceeds 55 degrees is {int(warm_year)}.")


def plot_cornell_movein(data):
    st.subheader("Cornell Tech Construction and Nearby Temperature Analysis")
    
    years_1 = [1970, 1980, 1990, 2000, 2010, 2013, 2014]
    years_2 = [1970, 1980, 1990, 2000, 2010, 2013, 2017, 2018]
    years_3 = [1970, 1980, 1990, 2000, 2010, 2013, 2021]

    colors = {1970: 'grey', 1980:'grey', 1990: 'grey', 2000: 'grey', 2010: 'grey',
              2013: 'green', 
              2014: 'blue', 2017: 'blue', 2018: 'blue', 2021: 'blue'}

    fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(20,8))

    for year in years_1:
        filtered_data = data[data['year'] == year]
        monthly_avg = filtered_data.groupby('month')['monthly_avg_Ftemp'].mean().reset_index()

        ax1.plot(monthly_avg['month'], monthly_avg['monthly_avg_Ftemp'], marker='o', linestyle='-', label=str(year), color=colors[year])

    ax1.set_title("Monthly Average Temperature with Construction & Move-in")
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)])
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Average Temperature (°F)')
    ax1.legend(title='Year')
    ax1.grid(True)

    for year in years_2:
        filtered_data = data[data['year'] == year]
        monthly_avg = filtered_data.groupby('month')['monthly_avg_Ftemp'].mean().reset_index()

        ax2.plot(monthly_avg['month'], monthly_avg['monthly_avg_Ftemp'], marker='o', linestyle='-', label=str(year), color=colors[year])

    # ax2.set_title("Monthly Average Temperature with Construction & Move-in")
    ax2.set_xticks(range(1, 13))
    ax2.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)])
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Average Temperature (°F)')
    ax2.legend(title='Year')
    ax2.grid(True)

    for year in years_3:
        filtered_data = data[data['year'] == year]
        monthly_avg = filtered_data.groupby('month')['monthly_avg_Ftemp'].mean().reset_index()

        ax3.plot(monthly_avg['month'], monthly_avg['monthly_avg_Ftemp'], marker='o', linestyle='-', label=str(year), color=colors[year])

    # ax3.set_title("Monthly Average Temperature with Construction & Move-in")
    ax3.set_xticks(range(1, 13))
    ax3.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)])
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Average Temperature (°F)')
    ax3.legend(title='Year')
    ax3.grid(True)

    st.pyplot(fig)


def plot_average_temperature_comparison(data):
    st.subheader("Average Monthly Temperature Comparison: 1950-2013 vs. 2014-2021")

    # Calculate average monthly temperatures for 1950-2013
    data_pre2014 = data[data['year'] < 2014]
    monthly_avg_pre2014 = data_pre2014.groupby('month')['monthly_avg_Ftemp'].mean().reset_index()

    # Calculate average monthly temperatures for 2014-2021
    data_post2013 = data[(data['year'] >= 2014) & (data['year'] <= 2021)]
    monthly_avg_post2013 = data_post2013.groupby('month')['monthly_avg_Ftemp'].mean().reset_index()

    # Plotting
    fig, ax = plt.subplots()

    # Plot for 1950-2013
    ax.plot(monthly_avg_pre2014['month'], monthly_avg_pre2014['monthly_avg_Ftemp'], marker='o', linestyle='-', color='blue', label='1950–2013')
    for i, txt in enumerate(monthly_avg_pre2014['monthly_avg_Ftemp']):
        ax.annotate(f"{txt:.2f}", (monthly_avg_pre2014['month'][i], monthly_avg_pre2014['monthly_avg_Ftemp'][i] +3))

    # Plot for 2014-2021
    ax.plot(monthly_avg_post2013['month'], monthly_avg_post2013['monthly_avg_Ftemp'], marker='o', linestyle='-', color='red', label='2014–2021')
    for i, txt in enumerate(monthly_avg_post2013['monthly_avg_Ftemp']):
        ax.annotate(f"{txt:.2f}", (monthly_avg_post2013['month'][i], monthly_avg_post2013['monthly_avg_Ftemp'][i]-3))

    ax.set_title("Average Monthly Temperature Comparison")
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)])
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Temperature (°F)')
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)



def plot_temperature_extremes(data):
    st.subheader("Monthly Temperature Extremes Analysis")

    # Slider for year selection
    year_to_filter = st.slider('Select a year to view monthly extremes:', 
                               min_value=int(data['year'].min()), 
                               max_value=int(data['year'].max()), 
                               value=int(data['year'].max()),
                               key='plot_temperature_extremes_year_slider')

    # Filter the data for the selected year
    filtered_data = data[data['year'] == year_to_filter]

    # Calculate highest and lowest temperatures for each month
    monthly_highs = filtered_data.groupby('month')['Ftemp'].max().reset_index()
    monthly_lows = filtered_data.groupby('month')['Ftemp'].min().reset_index()
    monthly_avg = filtered_data.groupby('month')['Ftemp'].mean().reset_index()

    # Plotting
    fig, ax = plt.subplots()

    # Plot the highest temperatures
    ax.plot(monthly_highs['month'], monthly_highs['Ftemp'], marker='o', linestyle='-', color='red', label='Monthly Highs')
    
    # Plot the lowest temperatures
    ax.plot(monthly_lows['month'], monthly_lows['Ftemp'], marker='o', linestyle='-', color='blue', label='Monthly Lows')

    ax.plot(monthly_avg['month'], monthly_avg['Ftemp'], marker='*', linestyle='-', color='green', label='Monthly average')

    ax.set_title(f"Monthly Temperature Extremes in {year_to_filter}")
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)])
    ax.set_xlabel('Month')
    ax.set_ylabel('Temperature (°F)')
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)



def main():
    file = './new.csv'
    data = pd.read_csv(file)
    dashboard_1(data)
    visualize_temperature_threshold(data)
    plot_cornell_movein(data)
    plot_average_temperature_comparison(data)
    plot_temperature_extremes(data)

if __name__ == "__main__":
    main()