"""
ENSF 692 Group Project

This program so far imports global datasets (CO2 emissions, GDP per capita, population and continents), merges, cleans, reshapes, and visualizes the data.
"""
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
    
    #sort data
    data.set_index(["Continent", "Country", "year"], inplace=True)#indexing by the Continent, Country and year
    data.sort_index(inplace=True)#sort data by index
    data.reset_index(inplace=True)#reset index for plotting
    
    #plot population trend of canada
    cName = 'Canada'

    cData = data[data["Country"] == cName].sort_values("year")

    plt.figure(figsize=(10,5))
    plt.plot(cData["year"], cData["population"]/1000000)
    plt.title("Population of Canada")
    plt.xlabel("Year")
    plt.ylabel("Population in millions")
    plt.show(block=False)

    #plot canadian gdp and co2 per capita over time
    cData = data[data["Country"] == 'Canada'].sort_values("year")
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_xlabel("Year")
    ax1.set_ylabel("GDP per Capita (USD)", color="tab:blue")
    ax1.plot(cData["year"], cData["gdp"], label="GDP per Capita", color="tab:blue")
    ax1.tick_params(axis='y', labelcolor="tab:blue")
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    ax2.set_ylabel("CO₂ per Capita (tons)", color="tab:red")
    ax2.plot(cData["year"], cData["co2"], label="CO₂ per Capita", color="tab:red")
    ax2.tick_params(axis='y', labelcolor="tab:red")
    plt.title("Canada: GDP and CO₂ per Capita Over Time (Dual Y-Axis)")
    fig.tight_layout()
    plt.savefig("canada_gdp_co2_dual_axis.png")
    plt.show(block=False)

    
    #plot global co2 per capita over time
    global_co2 = data.groupby("year")["co2"].mean()
    
    plt.figure(figsize=(10, 6))
    global_co2.plot(title="Average Global CO2 per Capita Over Time", ylabel="CO2 (tons)")
    plt.xlabel("Year")
    plt.ylabel("CO₂ (tons)")
    plt.tight_layout()
    plt.savefig("global_co2_trend.png")
    plt.tight_layout()
    plt.show(block=False)
 
    
    #plot gdp vs co2 per capita for the year 2020
    year_filter = 2020
    scatter_data = data[data["year"] == year_filter]
    plt.figure(figsize=(8, 6))
    plt.scatter(scatter_data["gdp"], scatter_data["co2"], alpha=0.7)
    plt.title(f"GDP vs CO₂ per Capita ({year_filter})")
    plt.xlabel("GDP per Capita (USD)")
    plt.ylabel("CO₂ per Capita (tons)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("gdp_vs_co2_2020.png")
    plt.show(block=False)
    
    scatter_data = data[data["year"] == year_filter][["Country", "population", "co2"]].dropna()
    
    #plot population vs c02 per capita for the year 2020
    plt.figure(figsize=(8, 6))
    plt.scatter(scatter_data["population"], scatter_data["co2"], alpha=0.7)
    plt.xscale("log")
    plt.yscale("log")
    plt.title(f"Population vs CO₂ per Capita ({year_filter}) ")
    plt.xlabel("Population")
    plt.ylabel("CO₂ per Capita (tons)")
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("pop_vs_co2_2023.png")
    plt.show()

    


if __name__ == "__main__":
    main()


#references
#[1] pandas.DataFrame.melt - pandas 2.2.2 documentation. [Online]. Available: https://pandas.pydata.org/docs/reference/api/pandas.melt.html. [Accessed: June 15, 2025].
#[2] pandas.to_numeric - pandas 2.2.2 documentation. [Online]. Available: https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html. [Accessed: June 15, 2025].