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
    year = st.sidebar.selectbox('Year', sorted(data['year'].unique()))

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

def main():
    file = './new.csv'
    data = pd.read_csv(file)
    dashboard_1(data)
    visualize_temperature_threshold(data)

if __name__ == "__main__":
    main()