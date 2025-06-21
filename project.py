"""
ENSF 692 Group Project

@Authors: Behzad, Matin

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

def conversion(value):
    """
    Converts the population and gdp strings to float values 

    Parameters
    ----------
    value is a string or float 

    Returns
    -------
    float converted value from string 
    """
    if isinstance(value, (int, float)):  # Already numeric
        return float(value)
    try:
        value = value.replace(",", "").strip() #removes the commas
        if value.endswith('k'): #checks if string has k
            return float(value[:-1])*1000 #multiply with 1000
        elif value.endswith('M'): #checks if string has M
            return float(value[:-1])*1000000 #mutliply a million
        elif value.endswith('B'): #checks if string has B
            return float(value[:-1])*1000000000 #mutliply by a billion
        else:
            return float(value) #return float
    except:
        return np.nan #no value give nan
    
def stat_country(df, country, year):
    idx = pd.IndexSlice
    try: 
        stat = df.loc[idx[:, country, year], ['gdp', 'co2', 'population']]
    except KeyError:
        print(f"No data for {country} in {year}.")
        return
    
    print(f"\n-----Summary for {country}, Year {year}-----")
    print(stat)
    print("\nStats:\n", stat.describe())

    cont = df.index.get_level_values('Continent')[0]
    cont_gdp = df.loc[idx[cont, :, year], 'gdp']
    print(f"\nAverage GDP per Capita for {cont} in {year} : {cont_gdp.mean():,.2f}")

def plot_data(df, country):
    
    plt.figure(figsize=(10,6))
    plt.plot(df['year'], df['gdp'], marker = 'o', label = 'GDP per Capita')
    plt.plot(df['year'], df['co2'], marker = 'o', label = 'CO2 per Capita')
    plt.title(f"{country}: GDP vs CO2 per capita")
    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout() #used reference [5]
    plt.savefig(f"{country}Trend.png") #used reference [6]
    plt.show()

    df_gc = df.groupby('Country').agg({'gdp' : 'sum', 'co2' : 'sum', 'population' : 'mean'}).dropna()
    pop_million = df_gc['population']/1000000
    plt.figure(figsize=(10,6))
    plt.scatter(df_gc['gdp'], df_gc['co2'], pop_million, alpha=0.5)
    plt.title("Total GDP vs Total CO2 per Country")
    plt.xlabel("Total GDP")
    plt.ylabel("Total CO2")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("bubblePlot.png")
    plt.show()

    last_year = df['year'].max()
    recent = df[df['year']==last_year].dropna()
    plt.figure(figsize=(10,6))
    plt.scatter(recent['population'], recent['co2'], alpha=0.5)
    plt.xscale('log') #used reference [7]
    plt.yscale('log') #used reference [8]
    plt.title(f"Population vs CO2 ({last_year})")
    plt.xlabel("Population (log scaled)")
    plt.ylabel("CO2 (log scaled)")
    plt.grid(True, which="both", linestyle='--')
    plt.tight_layout()
    plt.savefig("popvsco2.png")
    plt.show()

def menu(df):
    idx = pd.IndexSlice
    while True:
        print("\n-----Welcome to our program!-----")
        print("1. GDP vs CO2 per capita")
        print("2. Total GDP vs CO2")
        print("3. Population vs CO2")
        print("4. Average CO2 per Continent and Year")
        print("5. Exit")

        choice = input("Choose one of the options 1-5: ").strip()
        
        if choice == '5': 
            break

        if choice in {'1', '2', '3', '4'}:
            try:
                year = int(input("Enter a year: "))
            except ValueError:
                print("Invalid year, try again.")
                continue
        
            print()
            plt.figure()

        if choice == '1':
            #used xs reference [4]
            df_year = df.xs(year, level='year')
            plt.scatter(df_year['gdp'], df_year['co2'], alpha=0.5)
            plt.title(f"GDP vs CO2 per capita for {year}")
            plt.xlabel("GDP per capita")
            plt.ylabel("CO2 per capita")
        
        elif choice == '2':
            df_year = df.xs(year, level='year')
            pop_million = df_year['population']/1000000
            total_GDP = df_year['gdp']*df_year['population']
            total_CO2 = df_year['co2']*df_year['population']
            plt.scatter(total_GDP, total_CO2, pop_million, alpha=0.5)
            plt.title(f"Total GDP vs CO2 for {year}")
            plt.xlabel("Total GDP")
            plt.ylabel("Total CO2")

        elif choice == '3':
            df_year = df.xs(year, level='year')
            total_CO2 = df_year['co2']*df_year['population']
            plt.scatter(df_year['population'], total_CO2, alpha=0.5)
            plt.xscale('log')
            plt.yscale('log')
            plt.title(f"Population vs CO2 for {year}")
            plt.xlabel("Population")
            plt.ylabel("Total CO2")

        elif choice == '4':
            #used reset_index reference and pivot_table reference [9] [10]
            pivot = df.reset_index().pivot_table(index = 'Continent', columns = 'year', values = 'co2', aggfunc='mean')
            print(pivot)
            plt.title("Average CO2 per capita")
            #used imshow reference, cmap reference [11] [12]
            plt.imshow(pivot, cmap='YlOrRd', aspect='auto')
            plt.colorbar(label="Avg CO2 per capita")
            #used xticks reference [13]
            plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=45)
            #used ysticks reference [14]
            plt.yticks(range(len(pivot.index)), pivot.index)
            
        else:
            print("Invalid choice, please enter one number from 1-5")
            continue
        
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def main():
    #load csv files
    co2 = pd.read_csv("co2_pcap_cons.csv")
    gdp = pd.read_csv("gdp_pcap.csv")
    pop = pd.read_csv("pop.csv")
    cont = pd.read_csv("countries_continents.csv")

    #make sure that the columns are the same for merging
    co2.rename(columns={"country": "Country"}, inplace=True)
    gdp.rename(columns={"country": "Country"}, inplace=True)
    pop.rename(columns={"country": "Country"}, inplace=True)    

    #convert wide format to long format
    #used reference [1]
    co2 = co2.melt(id_vars=["Country"], var_name="year", value_name="co2")
    gdp = gdp.melt(id_vars=["Country"], var_name="year", value_name="gdp")
    pop = pop.melt(id_vars=["Country"], var_name="year", value_name="population")

    #convert year to integer
    co2["year"] = co2["year"].astype(int)
    gdp["year"] = gdp["year"].astype(int)
    pop["year"] = pop["year"].astype(int)

    #clean values 
    co2["co2"] = pd.to_numeric(co2["co2"], errors='coerce') #convert strings to actual values and then check if there is non-numeric values and it will be converted to Nan [2]
    gdp["gdp"] = gdp["gdp"].apply(conversion) #convert string to float
    pop["population"] = pop["population"].apply(conversion) #convert string to float

    #merge all datasetse
    data = pd.merge(co2, gdp, on=["Country", "year"], how="inner") #merge the co2 and gdp datasets on country and year, only keeps rows where both data are available
    data = pd.merge(data, pop, on=["Country", "year"], how="inner") #merge data with population data based on country and year
    data = pd.merge(data, cont, on="Country") #merge data with continent and using country as a key

    print(data.describe())
    
    #sort data
    data.set_index(["Continent", "Country", "year"], inplace=True)#indexing by the Continent, Country and year
    data.sort_index(inplace=True)#sort data by index
    
    data["total_co2"] = data["co2"]*data["population"]
    data["total_gdp"] = data["gdp"]*data["population"]

    data.reset_index().to_excel("processedData.xlsx", index=False)
    print("Data has been successfully been exported")

    while True:
        mode = input("Search by Continent or Country (type in Continent or Country): ").strip().title()
        if mode == "Continent":
            conts = data.index.get_level_values("Continent").unique().tolist()
            print("Available continents:", ", ".join(conts))
            cont_input = input("Enter continent: ").strip().title()
            if cont_input in conts:
                countries = data.xs(cont_input, level='Continent').index.get_level_values("Country").unique()
                print(f"Countries in {cont_input}: {', '.join(countries)}")
                country = input("Choose a country: ").strip().title()
                if country in countries:
                    break
        elif mode == "Country":
            country = input("Enter country: ").strip().title()
            if country in data.index.get_level_values("Country"):
                break
        print("Write the proper country name, or type continent.")
    
    yr = data.xs(country, level="Country").index.get_level_values("year").unique()
    while True:
        year_input = input(f"Enter a year {yr.min()}-{yr.max()}, or type 'all' for all the years: ").strip()
        if year_input.lower() == "all":
            idx = pd.IndexSlice
            data_year = data.loc[idx[:, country, :], :]
            break
        try:
            y = int(year_input)
            if y in yr:
                idx = pd.IndexSlice
                data_year = data.loc[idx[:, country, y], :]
                stat_country(data, country, y)
                break
            else:
                print("User input for year not available, please enter valid year or 'all' to choose all years.")
        except ValueError:
            print("User input for year not available, please enter valid year or 'all' to choose all years.")
    
    xp = data_year.reset_index()
    if 'year' not in xp.columns:
        xp['year'] = y
    
    print(f"\n-----Data for {country}-----")
    print(xp.head(10).to_string(index=False), "\n...")
    file_out = f"{country.lower().replace(' ', '_')}_export.xlsx"
    xp.to_excel(file_out, index=False)
    print(f"File was exported successfully.")

    if input("Do you want to view extra plots based on country? (y/n): ").strip().lower() == 'y':
        plot_data(xp, country)
    menu(data)

if __name__ == "__main__":
    main()


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

