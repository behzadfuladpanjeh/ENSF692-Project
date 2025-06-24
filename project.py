"""
ENSF 692 Group Project

@Authors: Behzad, Matin
@Group: Group #5

This program so far imports global datasets (CO2 emissions, GDP per capita, population and continents), merges, cleans, reshapes, and visualizes the data.
"""

#references
#[1] pandas.DataFrame.melt - pandas 2.2.2 documentation. [Online]. Available: https://pandas.pydata.org/docs/reference/api/pandas.melt.html. [Accessed: June 15, 2025].
#[2] pandas.to_numeric - pandas 2.2.2 documentation. [Online]. Available: https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html. [Accessed: June 15, 2025].
#[3] Matplotlib documentation, "Set alpha values (transparency)," Matplotlib 3.8.4 Documentation, 2025. [Online]. Available: https://matplotlib.org/stable/gallery/color/set_alpha.html. [Accessed: June 21, 2025].
#[4] pandas documentation, "pandas.DataFrame.xs," pandas 2.2.2 documentation. [Online]. Available: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.xs.html. [Accessed: June 21, 2025].
#[5] Matplotlib documentation, "matplotlib.pylot.tight_layout," Matplotlib 3.8.4 documentation. [Online]. Available: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.tight_layout.html. [Accessed: June 21, 2025].
#[6] Matplotlib documentation, "matplotlib.pyplot.savefig," Matplotlib 3.8.4 documentation. [Online]. Available: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html. [Accessed: June 21, 2025].
#[7] Matplotlib documentation, "matplotlib.axes.Axes.set_xscale," Matplotlib 3.8.4 documentation. [Online]. Available: https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_xscale.html. [Accessed: June 21, 2025].
#[8] Matplotlib documentation, "matplotlib.axes.Axes.set_yscale," Matplotlib 3.8.4 documentation. [Online]. Available: https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_yscale.html. [Accessed: June 21, 2025].
#[9] pandas documentation, "pandas.DataFrame.reset_index," pandas 2.2.2 documentation. [Online]. Available: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reset_index.html. [Accessed: June 21, 2025]
#[10] pandas documentation, "pandas.pivot_table," pandas 2.2.2 documentation. [Online]. Available: https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html. [Accessed: June 21, 2025].
#[11] Matplotlib documentation, "matplotlib.pyplot.imshow," Matplotlib 3.8.4 documentation. [Online]. Available: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html. [Accessed: June 21, 2025].
#[12] Matplotlib documentation, "Chooseing Colormaps in Matplotlib," Matplotlib 3.8.4 documentation. [Online]. Available: https://matplotlib.org/stable/users/explain/colors/colormaps.html. [Accessed: June 21, 2025].
#[13] Matplotlib documentation, "matplotlib.pyplot.xticks," Matplotlib 3.8.4 documentation. [Online]. Available: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.xticks.html. [Accessed: June 21, 2025].
#[14] Matplotlib documentation, "matplotlib.pyplot.yticks," Matplotlib 3.8.4 documentation. [Online]. Available: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.yticks.html. [Accessed: June 21, 2025].


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import seaborn as sns

sys.path.append(os.path.dirname(__file__))

from modules.data_loader import DataLoader

#Study 1 plots, graphs
def scatter_gdp_vs_co2(data, year_filter):
    """create a scatter plot of GDP vs CO2 per capita for a specified year

    Parameters
    ----------
    data : dataframe
        cleaned data that contains continent, country, years and other useful information
    year : a value
        year that the user has inputted
    
    Returns
        no return values
    """
    scatter_data = data[data["year"] == year_filter]
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=scatter_data, x="gdp", y="co2", hue="Continent", alpha=0.7)
    plt.xscale("log")
    plt.yscale("log")
    plt.title(f"GDP vs CO₂ per Capita ({year_filter})")
    plt.xlabel(f"GDP per Capita (USD, log scale)")
    plt.ylabel(f"CO₂ per Capita (tons, log scale)")
    plt.legend()
    plt.tight_layout()
    filename = f"study1_scatter_gdp_co2_{year_filter}.png"
    plt.savefig(filename)
    plt.show()
    print(f"Saved scatter plot as {filename}")

def top_co2_with_gdp(data, year):
    """bar chart that has top 15 countries for c02 and gdp
    Parameters
    ----------
    data : dataframe
        cleaned data that contains continent, country, years and other useful information
    year : a value
        year that the user has inputted
    
    Returns
        no return values
    """
    #drop missing values
    df_year = data[data['year'] == year].dropna(subset=['total_co2','total_gdp']) 
    
    #get top 15 countries by total co2
    top_15 = df_year.sort_values('total_co2',ascending=False).head(15)
    
    #extract values
    countries = top_15['Country']
    co2_values = top_15['total_co2']
    gdp_values = top_15['total_gdp']
    
    #bar settings
    x = np.arange(len(countries)) #label locations
    width=0.4 #width of the bars

    #create plot
    fig, ax1 = plt.subplots(figsize=(14,7))

    #bar for co2 on primary y-axis
    bars1 = ax1.bar(x - width/2, co2_values, width, label='Total CO₂', color='skyblue')
    ax1.set_xlabel('Country')
    ax1.set_ylabel('Total CO2 emissions (tons)', color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')

    #create secondary y-axis for gdp
    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width/2, gdp_values, width, label='Total GDP (USD)', color='orange')
    ax2.set_ylabel('Total GDP (Scaled)', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    #Title and x-ticks
    ax1.set_title(f'Top 15 Countries by Total CO2 Emissions with Total GDP ({year})')
    ax1.set_xticks(x)
    ax1.set_xticklabels(countries, rotation=45, ha='right')

    #legends
    #combine legends from both axes
    bars = [bars1, bars2]
    labels = [bar.get_label() for bar in bars]
    ax1.legend(bars, labels, loc='upper right')

    plt.tight_layout(); 
    filename = f"study1_top15_co2_gdp_{year}.png"
    plt.savefig(filename)
    plt.show()
    print(f"Saved bar chart as {filename}")

def trend_for_selected_countries(data, selected_countries):
    """plot of time series of gdp and co2 for selected countries 

    Parameters
    ----------
    data : dataframe
        cleaned data that contains continent, country, years and other useful information
    selected_countries : a string 
        a list of country names
    
    Returns
        no return values
    """
    for country in selected_countries:
        cData = data[data["Country"] == country].sort_values("year")
        fig, ax1 = plt.subplots(figsize=(10, 5))
        ax1.set_title(f"{country}: GDP and CO2 per Capita Over Time")
        ax1.plot(cData["year"], cData["gdp"], color="blue", label="GDP per Capita")
        ax1.set_ylabel("GDP per Capita (USD)", color="blue")
        ax1.tick_params(axis='y', labelcolor="blue")

        ax2 = ax1.twinx()
        ax2.plot(cData["year"], cData["co2"], color="red", label="CO2 per Capita")
        ax2.set_ylabel("CO2 per Capita (tons)", color="red")
        ax2.tick_params(axis='y', labelcolor="red")

        plt.tight_layout()
        filename = f"study1_time_series_{country}.png"
        plt.savefig(filename)
        plt.show()
        print(f"Saved time-series plot as {filename}")

def correlation_trend(data):
    """calculate and plot pearson correlation between gdp and co2 per capita

    Parameters
    ----------
    data : dataframe
        cleaned data that contains continent, country, years and other useful information
    
    Returns
        no return values
    """
    #makes the infinity as na so the correlation ignores/skips the infinity entries
    with pd.option_context('mode.use_inf_as_na', True):
        # Calculate Pearson correlation between GDP and CO₂ per capita for each year
        correlation_by_year = data.groupby("year").apply(lambda group: group["gdp"].corr(group["co2"])).reset_index(name="pearson_correlation")

    # Plot the correlation trend over time
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=correlation_by_year, x="year", y="pearson_correlation", marker="o")
    plt.title(f"Pearson Correlation Between GDP and CO2 per Capita Over Time")
    plt.xlabel("Year")
    plt.ylabel("Pearson Correlation Coefficient")
    plt.grid(True)
    plt.tight_layout()
    filename = 'study1_gdp_co2_correlation.png'
    plt.savefig(filename)
    plt.show()
    print(f"Saved correlation plot as {filename}")

#study 2 plots, graphs
def scatter_pop_vs_co2(data, year_filter):
    """scatter plot of population vs co2 per capita for a year

    Parameters
    ----------
    data : dataframe
        cleaned data that contains continent, country, years and other useful information
    year_filter : a value
        year that the user has inputted
    
    Returns
        no return values
    """
    scatter_data = data[data["year"] == year_filter]

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=scatter_data, x="population", y="co2", hue="Continent", alpha=0.7)
    plt.xscale("log")
    plt.yscale("log")
    plt.title(f"Population vs CO2 per Capita ({year_filter})")
    plt.xlabel("Population (log scale)")
    plt.ylabel("CO2 per Capita (tons, log scale)")
    plt.legend()
    plt.tight_layout()
    filename = f"study2_scatter_pop_co2_{year_filter}.png"
    plt.savefig(filename)
    plt.show()
    print(f"Saved scatter plot as {filename}")

def bar_highpop_lowemissions(data, year):
    """bar graph of the top 10 countries with the highest population but lowest co2 emissions

    Parameters
    ----------
    data : dataframe
        cleaned data that contains continent, country, years and other useful information
    year_filter : a value
        year that the user has inputted

    Returns
        no return values
    """
    scatter_data = data[data['year']==year]
    # Get top 10 countries by population
    top_pop = scatter_data.sort_values(by='population', ascending=False).head(10)

    # Filter for low per capita CO2 emissions (< median)
    low_emissions = top_pop[top_pop['co2'] < top_pop['co2'].median()]
    low_emissions.head(10)
    # Display results
    low_emissions_sorted = low_emissions.sort_values(by='population', ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(low_emissions_sorted['Country'], low_emissions_sorted['co2'], color='green')
    ax.set_ylabel('CO₂ per Capita (tons)')
    ax.set_title(f'High Population Countries with Low CO₂ Emissions per Capita ({year})')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    filename = f"study2_bar_highpop_lowemissions_{year}.png"
    plt.savefig(filename)
    plt.show()
    print(f"Saved bar graph as {filename}")

def bubble_pop_vs_co2(data, year):
    """bubble chart of the population vs co2, bubbles are sized for gdp size

    Parameters
    ----------
    data : dataframe
        cleaned data that contains continent, country, years and other useful information
    year_filter : a value
        year that the user has inputted
    
    Returns
        no return values
    """
    scatter_data = data[data['year']==year]
    # Get top 10 countries by population
    top_pop = scatter_data.sort_values(by='population', ascending=False).head(10)

    # Filter for low per capita CO2 emissions (< median)
    low_emissions = top_pop[top_pop['co2'] < top_pop['co2'].median()]
    low_emissions.head(10)
    # Display results
    low_emissions_sorted = low_emissions.sort_values(by='population', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(
    data=low_emissions_sorted,
    x='co2',
    y='population',
    size='total_gdp',
    hue='Country',
    legend=False,
    sizes=(100, 2000)
    )

    # Add country names to each point
    for i in range(len(low_emissions_sorted)):
        row = low_emissions_sorted.iloc[i]
        plt.text(
            row['co2'],
            row['population'],
            row['Country'],
            fontsize=9,
            ha='center',
            va='center'
        )

    plt.title('Population vs. CO2 per Capita (Bubble Size = Total GDP)')
    plt.xlabel('CO2 per Capita (tons)')
    plt.ylabel('Population')
    plt.grid(True)
    plt.tight_layout()
    filename = f"study2_bubble_pop_vs_co2_{year}.png"
    plt.savefig(filename)
    plt.show()
    print(f"Saved bubble plot as {filename}")

def corr_pop_co2(data):
    """pearson correlation between popoulation and co2, per capita for each year

    Parameters
    ----------
    data : dataframe
        cleaned data that contains continent, country, years and other useful information
    
    Returns
        no return values
    """
    correlation_by_year = data.groupby("year").apply(
        lambda group: group["population"].corr(group["co2"])
    ).reset_index(name="pearson_correlation")

    # Plot the correlation trend over time
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=correlation_by_year, x="year", y="pearson_correlation", marker="o")
    plt.title("Pearson Correlation Between population and CO2 per Capita Over Time")
    plt.xlabel("Year")
    plt.ylabel("Pearson Correlation Coefficient")
    plt.grid(True)
    plt.tight_layout()
    filename = f"study2_corr_pop_co2.png"
    plt.savefig(filename)
    plt.show()
    print(f"Saved Pearson correlation graph saved as {filename}")

#study 3 plots, graphs
def scatter_cont_pop_vs_co2(data, year_filter, top_n):
    """scatter plot between continents, population and co2

    Parameters
    ----------
    data : dataframe 
        cleaned data that contains continent, country, years and other useful information
    year_filter : int
        user input for year
    top_n : int
        number of continents they want to include

    Returns
        None
    """
    # Filter and prepare the data
    scatter_data = data[data["year"] == year_filter].copy()

    # Drop missing or invalid values
    scatter_data = scatter_data.dropna(subset=["co2", "gdp"])
    scatter_data = scatter_data.replace([np.inf, -np.inf], np.nan)
    scatter_data = scatter_data.dropna(subset=["co2", "gdp"])

    # Calculate carbon intensity: CO2 per unit of GDP
    scatter_data["co2_per_gdp"] = scatter_data["co2"] / scatter_data["gdp"]

    # Sort and select top N
    top_countries = scatter_data.sort_values(by="co2_per_gdp", ascending=False).head(top_n)

    # Plotting
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(top_countries["Country"], top_countries["co2_per_gdp"], color="crimson")

    # Annotate values on bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}', 
                xy=(bar.get_x() + bar.get_width() / 2, height), 
                xytext=(0, 5),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=8)

    # Axis labeling
    ax.set_title(f"Top {top_n} Countries by CO₂ per GDP (Carbon Intensity) - {year_filter}")
    ax.set_ylabel("CO₂ per unit GDP (tons/USD)")
    ax.set_xlabel("Country")
    ax.set_xticklabels(top_countries["Country"], rotation=45, ha="right")

    plt.tight_layout()
    filename = f"study3_scatter_cont_pop_vs_co2.png"
    plt.savefig(filename)
    plt.show()
    print(f"Saved scatter plot as {filename}")

#study 4 plots, graphs
def timeseries_count(data, countries, start_year):
    """plot of 3 different things for gdp per capita over time, co2 emissions per capita over time, and population over time

    Parameters
    ----------
    data : dataframe
        cleaned data that contains continent, country, years and other useful information
    countries : an array of string
        countires inputted by user
    start_year : int
        start year that the user wants the plot to start at

    REturns
        None
    """
    data_filtered = data.copy()
    if start_year:
        data_filtered = data_filtered[data_filtered['year'] >= start_year]

    #plot GDP per capita over time
    plt.figure(figsize=(10, 6))
    for country in countries:
        subset = data_filtered[data_filtered['Country'] == country]
        plt.plot(subset['year'], subset['gdp'], label=country)
    plt.title(f"GDP per Capita ({start_year or data_filtered['year'].min()}–{data_filtered['year'].max()})")
    plt.xlabel('Year')
    plt.ylabel('GDP per Capita (USD)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    gdp_filename = f"study4_gdp_overtime_{start_year or 'all'}.png"
    plt.savefig(gdp_filename)
    plt.show()
    print(f"Figures saved as {gdp_filename}")

    #plot co2 emissions per capita over time
    plt.figure(figsize=(10, 6))
    for country in countries:
        subset = data_filtered[data_filtered["Country"] == country]
        plt.plot(subset["year"], subset["co2"], label=country)
    plt.title(f"CO₂ Emissions per Capita ({start_year or data_filtered['year'].min()}–{data_filtered['year'].max()})")
    plt.xlabel("Year")
    plt.ylabel("CO₂ per Capita (tons)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    co2_filename = f"study4_emmissions_capita.png"
    plt.savefig(co2_filename)
    plt.show()
    print(f"Saved plot as {co2_filename}")

    #plot 3 population over time
    plt.figure(figsize=(10, 6))
    for country in countries:
        subset = data_filtered[data_filtered["Country"] == country]
        plt.plot(subset["year"], subset["population"] / 1e6, label=country)  # Convert to millions
    plt.title(f"Population in Millions ({start_year or data_filtered['year'].min()}–{data_filtered['year'].max()})")
    plt.xlabel("Year")
    plt.ylabel("Population (Millions)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    pop_filename = f"study4_population_overtime.png"
    plt.savefig(pop_filename)
    plt.show()
    print(f"Saved plot as {pop_filename}")

#study 5 plots, graphs
def emissions_continents(data, year):
    """plot co2 per capita, for specified countires and years

    Parameters
    ----------
    data : dataframe
        cleaned and merged csv files that contain continents, countries, years and other useful information
    year : int
        year that is specified by the user input
    
    Return
        None
    """
    #filter for selected coutnries and years
    data_year = data[data["year"] == year]

    # Drop rows with missing values
    data_year = data_year.dropna(subset=["co2", "gdp"])

    # Group by continent and calculate average CO₂ and GDP per capita
    continent_summary = data_year.groupby("Continent")[["co2", "gdp"]].mean().sort_values("co2", ascending=False)

    # Plotting
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot CO₂ per capita
    color1 = 'skyblue'
    ax1.bar(continent_summary.index, continent_summary["co2"], color=color1, width=0.4, label="CO₂ per Capita")
    ax1.set_ylabel("Average CO₂ per Capita (tons)", color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)

    # Add second Y-axis for GDP per capita
    ax2 = ax1.twinx()
    color2 = 'orange'
    ax2.plot(continent_summary.index, continent_summary["gdp"], color=color2, marker='o', label="GDP per Capita")
    ax2.set_ylabel("Average GDP per Capita (USD)", color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    # Title and layout
    plt.title(f"Average CO₂ and GDP per Capita by Continent ({year})")
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()
    filename = f"study5_emmissions_continents.png"
    plt.savefig(filename)
    plt.show()
    print(f"Saved plot as {filename}")

#study 6 plots, graphs
def co2_emissions_population(data, year):
    """creatinga a plot to visualize the correlation between co2 emissions and population for a specified year

    Parameters
    ----------
    data : dataframe
        cleaned and merged csv files that contain continents, countries, years and other useful information
    year : int
        a year inputted by the user

    Return
        None
    """
    data_year = data[data["year"] == year].copy()
    n = 15
    # Drop missing or invalid values
    data_year = data_year.dropna(subset=["co2", "gdp"])
    data_year = data_year.replace([np.inf, -np.inf], np.nan)
    data_year = data_year.dropna(subset=["co2", "gdp"])

    # Create scatter plot with log scales
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        data_year["population"],
        data_year["total_co2"],
        alpha=0.7,
        c='blue',
        edgecolors='k',
        s=50
    )

    # Annotate countries (optional: show only top emitters or sampled subset to avoid clutter)
    for i, row in data_year.nlargest(n, "total_co2").iterrows():
        plt.annotate(row["Country"], (row["population"], row["total_co2"]), fontsize=10)

    # Log scales
    plt.xscale("log")
    plt.yscale("log")

    # Labels and title
    plt.xlabel("Population (log scale)")
    plt.ylabel("Total CO₂ Emissions (log scale)")
    plt.title(f"CO₂ Emissions vs. Population (Log-Log Scale) - {year}")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)

    plt.tight_layout()
    filename = f"study6_co2_emissions_vs_pop.png"
    plt.savefig(filename)
    plt.show()
    print(f"Plot saved as {filename}")

#study 7 plots, graphs
def most_improved(data, start_year, end_year, n):
    """shows the countries that have the most reduced co2 emissions for a specified year

    Parameters
    ----------
    data : dataframe
        cleaned and merged csv files that contain continents, countries, years and other useful information
    start_year : int
        start year that the user inputs and wants to compare the data to end year
    end_year : int
        end year that the user inputs and wants the data to stop at
    n : int
        number of countries the user wants to see the results for
    
    REturn
        None
    """
    # Ensure country names are consistent
    data["Country"] = data["Country"].str.strip()

    # Filter data for the start and end years
    start_data = data[data["year"] == start_year][["Country", "co2"]].copy()
    end_data = data[data["year"] == end_year][["Country", "co2"]].copy()

    # Rename columns for clarity
    start_data.rename(columns={"co2": "start_co2"}, inplace=True)
    end_data.rename(columns={"co2": "end_co2"}, inplace=True)

    # Merge data on Country
    change_df = pd.merge(start_data, end_data, on="Country", how="inner")

    # Drop missing values
    change_df.dropna(inplace=True)

    # Calculate absolute and percent change
    change_df["change"] = change_df["end_co2"] - change_df["start_co2"]
    change_df["percent_change"] = 100 * (change_df["change"] / change_df["start_co2"].replace(0, float("nan")))

    # Filter out countries with very small initial emissions to avoid distortion
    change_df = change_df[change_df["start_co2"] > 1.0]

    # Get top 15 countries with the largest decrease in CO2 per capita
    most_improved = change_df.sort_values(by="change").head(n)

    # Plot the results
    plt.figure(figsize=(12, 6))
    bars = plt.barh(most_improved["Country"], most_improved["change"], color="seagreen")
    plt.xlabel("Reduction in CO₂ per Capita (%)")
    plt.title(f"Top {n} Most Improved Countries in CO₂ per Capita ({start_year} to {end_year})")
    plt.gca().invert_yaxis()  # Show largest improvements at the top
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    filename = f"study7_most_improved.png"
    plt.savefig(filename)
    plt.show()
    print(f"Graph saved as {filename}")

#study 8 figure
def trend_specific_country_year(data, country, year):
    """plots co2 per capita, gdp per capita for a population over a specified country and year

    Parameters
    ----------
    data : dataframe
        cleaned and merged csv files that contain continents, countries, years and other useful information
    country : array of strings
        user specfied array of strings of countries
    year : int
        user specifed int for the year
    
    Return
        None
    """
    filtered = data[(data['Country'] == country) & (data['year'].isin(year))].sort_values(by='year')

    if filtered.empty:
        print(f"No data found for {country} in years {year}.")
    
    # Plot setup
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # CO₂ per capita
    ax1.plot(filtered['year'], filtered['co2'], color='crimson', marker='o', label='CO₂ per capita (tons)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('CO₂ per capita (tons)', color='crimson')
    ax1.tick_params(axis='y', labelcolor='crimson')

    # Create a second y-axis for GDP
    ax2 = ax1.twinx()
    ax2.plot(filtered['year'], filtered['gdp'], color='navy', marker='s', label='GDP per capita ($)')
    ax2.set_ylabel('GDP per capita (USD)', color='navy')
    ax2.tick_params(axis='y', labelcolor='navy')

    # Add population on third axis using text annotations
    for i, row in filtered.iterrows():
        ax1.annotate(f"Pop: {int(row['population']):,}", 
                (row['year'], row['co2']),
                textcoords="offset points", xytext=(0,10),
                ha='center', fontsize=8, color='darkgreen')
    plt.title(f"{country} - CO₂, GDP, and Population Over Time")
    fig.tight_layout()
    plt.grid(True)
    filename = f"study8_country_trends.png"
    plt.savefig(filename)
    plt.show()
    print(f"Figure saved as {filename}")

#user inputs
def get_year(data):
    """gets the user input of the year
    Parameters
    ----------
    data : dataframe
        contains the cleaned and merged data from csv files
    
    Returns
        user input as int, if its a valid year
    """
    while True:
        user_input = input("Enter a year: ")
        if user_input.isdigit() and int(user_input) in data['year'].unique():
            return int(user_input)
        print("Please enter a valid year in a range from 1800-2022")

def get_countries(data):
    """gets a list of user input countries and returns it if its valid and unique from the dataframe

    Parameters
    ----------
    data : dataframe
        contains the cleaned and merged data from csv files

    Returns
    -------
    returns a list
        returns the user input as list if its valid
    """
    check = data['Country'].unique()
    while True:
        user_input = input("Enter countires seperated by commas: ")
        count = [inp.strip() for inp in user_input.split(',')]
        if all(inp in check for inp in count):
            return count
        print("Please enter valid country names")

def get_n():
    """gets an integer from the user and makes sure its above 0

    Returns
    -------
    int
        returns an integer that is greater than 0
    """
    while True:
        n = input("Enter a number of countries: ")
        if n.isdigit() and int(n) > 0:
            return int(n)
        print("Please enter a vaild number greater than 0")

#main menu for user
def main_menu(data):
    """outputs main menu to user in terminal and asks them to choose one of the studies

    Parameters
    ----------
    data : dataframe
        contains the cleaned and merged data from csv files
    Returns
        none
    """
    titles=["Economic Growth vs Emissions", "High Population, Low Emissions", "CO2 per GDP", "Time-Series", "Continental Emissiosn Comparison", "CO2 Emissions vs Population", "Most improved", "CO2 and GDP for Specified Country and Year"]
    while True:
        for i,t in enumerate(titles,1):
            print(f"{i}) {t}")
        print("0) Exit")
        user_input = input("Select study: ")
        if user_input == '1':
            study1_menu(data)
        elif user_input == '2':
            study2_menu(data)
        elif user_input == '3':
            study3_menu(data)
        elif user_input == '4':
            study4_menu(data)
        elif user_input == '5':
            study5_menu(data)
        elif user_input == '6':
            study6_menu(data)
        elif user_input == '7':
            study7_menu(data)
        elif user_input == '8':
            study8_menu(data)
        elif user_input == '0':
            break

#add sub menu for each study
def study1_menu(data):
    """study 1 menu that prompts user to input what plot/graph they want and it gives them a figure

    Parameters
    ----------
    data : dataframe 
        contains the cleaned and merged data from csv files

    Return
        None
    """
    while True:
        print("Study 1 Menu: a) Scatter b) Bar c) Trend d) Correlation e) exit")
        user_input = input("Please enter a letter from the menu: ").lower()
        if user_input == 'a':
            scatter_gdp_vs_co2(data, get_year(data))
        elif user_input == 'b':
            top_co2_with_gdp(data, get_year(data))
        elif user_input == 'c':
            trend_for_selected_countries(data, get_countries(data))
        elif user_input == 'd':
            correlation_trend(data)
        elif user_input == 'e':
            break
        else:
            print("Please enter a correct letter from the sub menu")  

def study2_menu(data):
    """study 2 menu that prompts user to input what plot/graph they want and it gives them a figure

    Parameters
    ----------
    data : dataframe 
        contains the cleaned and merged data from csv files

    Return
        None
    """
    while True:
        print("Study 2 Menu: a) Scatter b) Bar c) Bubble d) Correlation e) exit")
        user_input = input("Please enter a letter from the menu: ").lower()
        if user_input == 'a':
            scatter_pop_vs_co2(data, get_year(data))
        elif user_input == 'b':
            bar_highpop_lowemissions(data, get_year(data))
        elif user_input == 'c':
            bubble_pop_vs_co2(data, get_year(data))
        elif user_input == 'd':
            corr_pop_co2(data)
        elif user_input == 'e':
            break
        else:
            print("Please enter a correct letter from the sub menu")  

def study3_menu(data):
    """study 3 menu that prompts user to input what plot/graph they want and it gives them a figure

    Parameters
    ----------
    data : dataframe 
        contains the cleaned and merged data from csv files

    Return
        None
    """
    while True:
        print("Study 3 Menu: a) Scatter b) exit")
        user_input = input("Please enter a letter from the menu: ").lower()
        if user_input == 'a':
            scatter_cont_pop_vs_co2(data, get_year(data), get_n())
        elif user_input == 'b':
            break
        else:
            print("Please enter a correct letter from the sub menu")  

def study4_menu(data):
    """study 4 menu that prompts user to input if they want to start to get the figures or exit

    Parameters
    ----------
    data : dataframe 
        contains the cleaned and merged data from csv files

    Return
        None
    """
    while True:
        print("Study 4 Menu: a) Start b) exit")
        user_input = input("Please enter a letter from the menu: ").lower()
        if user_input == 'a':
            timeseries_count(data, get_countries(data), get_year(data))
        elif user_input == 'b':
            break
        else:
            print("Please enter a correct letter from the sub menu") 

def study5_menu(data):
    """study 5 menu that prompts user to input if they want to start to get the figures or exit

    Parameters
    ----------
    data : dataframe 
        contains the cleaned and merged data from csv files

    Return
        None
    """
    while True:
        print("Study 5 Menu: a) Start b) exit")
        user_input = input("Please enter a letter from the menu: ").lower()
        if user_input == 'a':
            emissions_continents(data, get_year(data))
        elif user_input == 'b':
            break
        else:
            print("Please enter a correct letter from the sub menu") 

def study6_menu(data):
    """study 6 menu that prompts user to input if they want to start to get the figures or exit

    Parameters
    ----------
    data : dataframe 
        contains the cleaned and merged data from csv files

    Return
        None
    """
    while True:
        print("Study 6 Menu: a) Start b) exit")
        user_input = input("Please enter a letter from the menu: ").lower()
        if user_input == 'a':
            co2_emissions_population(data, get_year(data))
        elif user_input == 'b':
            break
        else:
            print("Please enter a correct letter from the sub menu") 

def study7_menu(data):
    """study 7 menu that prompts user to input if they want to start to get the figures or exit

    Parameters
    ----------
    data : dataframe 
        contains the cleaned and merged data from csv files

    Return
        None
    """
    while True:
        print("Study 7 Menu: a) Start b) exit")
        user_input = input("Please enter a letter from the menu: ").lower()
        if user_input == 'a':
            most_improved(data, get_year(data), get_year(data), get_n())
        elif user_input == 'b':
            break
        else:
            print("Please enter a correct letter from the sub menu") 

def study8_menu(data):
    """study 8 menu that prompts user to input if they want to start to get the figures or exit

    Parameters
    ----------
    data : dataframe 
        contains the cleaned and merged data from csv files

    Return
        None
    """
    check_country = data['Country'].unique()
    check_year = data['year'].unique()

    while True:
        print("Study 8 Menu: a) Start b) exit")
        user_input = input("Please enter a letter from the menu: ").lower()
        if user_input == 'a':
            
            while True:
                country = input("Enter a single country: ").strip()
                if country in check_country:
                    break
                print(f"{country} not found, try again with a valid country. ex. Algeria")

            while True:
                years_input = input("Enter years seperated by commas (ex. 2000, 2001, 2002,...)")
                try:
                    years = [int(y.strip()) for y in years_input.split(',')]
                except ValueError:
                    print("Please enter only valid years, seperated by commas")
                    continue

                invalid_years = [y for y in years if y not in check_year]
                if invalid_years:
                    print(f"Years are not in dataset: {invalid_years}")
                    continue
                break
        
            trend_specific_country_year(data, country, years)

        elif user_input == 'b':
            break
        else:
            print("Please enter a correct letter from the sub menu") 

if __name__ == "__main__":
    #loads, cleans, and merges data
    loader = DataLoader()
    data = loader.load_and_prepare_data()

    #drop duplicate rows
    data.drop_duplicates(inplace=True)

    #prints the head of the dataset
    print("Describing the datasets of the first 5 rows from head()")
    print(data.head(5))

    #prints describe of the dataset
    print("Using the describe() function to show the dataset analysis")
    print(data.describe())

    #pivot table requirement
    pivot_table_co2 = data.pivot_table(values='co2', index='Continent', columns='year', aggfunc='mean')
    print("Printing pivot table of the CO2 per capita by continent and year")
    print(pivot_table_co2)

    #export cleaned and merged dataframe to excel
    data.to_excel('cleaned_merged_dataframe.xlsx', index=True)
    print(f"Exported excel file is named as cleaned_merged_dataframe.xlsx")

    #run program
    main_menu(data)


 #plots used for presentation
    #plot population trend of canada
    # cName = 'Canada'

    # cData = data[data["Country"] == cName].sort_values("year")

    # plt.figure(figsize=(10,5))
    # plt.plot(cData["year"], cData["population"]/1000000)
    # plt.title("Population of Canada")
    # plt.xlabel("Year")
    # plt.ylabel("Population in millions")
    # plt.show(block=False)

    # #plot canadian gdp and co2 per capita over time
    # cData = data[data["Country"] == 'Canada'].sort_values("year")
    # fig, ax1 = plt.subplots(figsize=(10, 6))
    # ax1.set_xlabel("Year")
    # ax1.set_ylabel("GDP per Capita (USD)", color="tab:blue")
    # ax1.plot(cData["year"], cData["gdp"], label="GDP per Capita", color="tab:blue")
    # ax1.tick_params(axis='y', labelcolor="tab:blue")
    # ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    # ax2.set_ylabel("CO₂ per Capita (tons)", color="tab:red")
    # ax2.plot(cData["year"], cData["co2"], label="CO₂ per Capita", color="tab:red")
    # ax2.tick_params(axis='y', labelcolor="tab:red")
    # plt.title("Canada: GDP and CO₂ per Capita Over Time (Dual Y-Axis)")
    # fig.tight_layout()
    # plt.savefig("canada_gdp_co2_dual_axis.png")
    # plt.show(block=False)

    
    # #plot global co2 per capita over time
    # global_co2 = data.groupby("year")["co2"].mean()
    
    # plt.figure(figsize=(10, 6))
    # global_co2.plot(title="Average Global CO2 per Capita Over Time", ylabel="CO2 (tons)")
    # plt.xlabel("Year")
    # plt.ylabel("CO₂ (tons)")
    # plt.tight_layout()
    # plt.savefig("global_co2_trend.png")
    # plt.tight_layout()
    # plt.show(block=False)
 
    
    # #plot gdp vs co2 per capita for the year 2020
    # year_filter = 2020
    # scatter_data = data[data["year"] == year_filter]
    # plt.figure(figsize=(8, 6))
    # plt.scatter(scatter_data["gdp"], scatter_data["co2"], alpha=0.7) #used reference [3]
    # plt.title(f"GDP vs CO₂ per Capita ({year_filter})")
    # plt.xlabel("GDP per Capita (USD)")
    # plt.ylabel("CO₂ per Capita (tons)")
    # plt.grid(True)
    # plt.tight_layout()
    # plt.savefig("gdp_vs_co2_2020.png")
    # plt.show(block=False)
    
    # scatter_data = data[data["year"] == year_filter][["Country", "population", "co2"]].dropna()
    
    # #plot population vs c02 per capita for the year 2020
    # plt.figure(figsize=(8, 6))
    # plt.scatter(scatter_data["population"], scatter_data["co2"], alpha=0.7)
    # plt.xscale("log")
    # plt.yscale("log")
    # plt.title(f"Population vs CO₂ per Capita ({year_filter}) ")
    # plt.xlabel("Population")
    # plt.ylabel("CO₂ per Capita (tons)")
    # plt.grid(True, which="both", linestyle='--', linewidth=0.5)
    # plt.tight_layout()
    # plt.savefig("pop_vs_co2_2023.png")
    # plt.show()

