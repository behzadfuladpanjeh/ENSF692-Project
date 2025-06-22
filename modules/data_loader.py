import pandas as pd
import numpy as np

class DataLoader:
    @staticmethod
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
                return float(value[:-1])*1_000_000 #mutliply a million
            elif value.endswith('B'): #checks if string has B
                return float(value[:-1])*1_000_000_000 #mutliply by a billion
            else:
                return float(value) #return float
        except:
            return np.nan #no value give nan

    def load_and_prepare_data(self):
        #load csv files
        co2 = pd.read_csv("data/co2_pcap_cons.csv")
        gdp = pd.read_csv("data/gdp_pcap.csv")
        pop = pd.read_csv("data/pop.csv")
        cont = pd.read_csv("data/countries_continents.csv")

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
        gdp["gdp"] = gdp["gdp"].apply(self.conversion) #convert string to float
        pop["population"] = pop["population"].apply(self.conversion) #convert string to float

        #merge all datasetse
        data = pd.merge(co2, gdp, on=["Country", "year"], how="inner") #merge the co2 and gdp datasets on country and year, only keeps rows where both data are available
        data = pd.merge(data, pop, on=["Country", "year"], how="inner") #merge data with population data based on country and year
        data = pd.merge(data, cont, on="Country") #merge data with continent and using country as a key

              
        #sort data
        data.set_index(["Continent", "Country", "year"], inplace=True)#indexing by the Continent, Country and year
        data.sort_index(inplace=True) #sort data by index
        data["total_co2"] = data["co2"]*data["population"]
        data["total_gdp"] = data["gdp"]*data["population"]
        data.reset_index(inplace=True)

        return data
