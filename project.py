import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def conversion(value):
    try:
        value = value.replace(",", "").strip()
        if value.endswith('k'):
            return float(value[:-1])*1000
        elif value.endswith('M'):
            return float(value[:-1])*1000000
        else:
            return float(value)
    except:
        return np.nan
    
def main():
    co2 = pd.read_csv("co2_pcap_cons.csv")
    gdp = pd.read_csv("gdp_pcap.csv")
    pop = pd.read_csv("pop.csv")
    country = pd.read_csv("countries_continents.csv")

    co2 = co2.melt(id_vars=["country"], var_name="year", value_name="co2")
    gdp = gdp.melt(id_vars=["country"], var_name="year", value_name="gdp")
    pop = pop.melt(id_vars=["country"], var_name="year", value_name="population")

    co2["year"] = co2["year"].astype(int)
    gdp["year"] = gdp["year"].astype(int)
    pop["year"] = pop["year"].astype(int)

    co2["co2"] = pd.to_numeric(co2["co2"], errors='coerce')
    gdp["gdp"] = pd.to_numeric(gdp["gdp"], errors='coerce')
    pop["population"] = pop["population"].apply(conversion)

    data = pd.merge(co2, gdp, on=["country", "year"], how="inner")
    data = pd.merge(data, pop, on=["country", "year"], how="inner")
    data = pd.merge(data, country, left_on="country", right_on="Country")

    data.set_index(["Continent", "country", "year"], inplace=True)
    data.sort_index(inplace=True)

    data.reset_index(inplace=True)

    cName = 'Canada'

    cData = data[data["Country"] == cName].sort_values("year")

    plt.figure(figsize=(10,5))
    plt.plot(cData["year"], cData["population"]/1000000)
    plt.title("Population of Canada")
    plt.xlabel("Year")
    plt.ylabel("Population in millions")
    plt.show()


if __name__ == "__main__":
    main()
