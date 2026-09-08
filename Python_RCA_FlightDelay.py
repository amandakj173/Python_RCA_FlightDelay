# DATA WRANGLING

# Import Packages
import dowhy
import pandas as pd
import numpy as np

# Set Parameters
pd.set_option("display.precision",3)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width',2000)

# Import Data
ds = pd.read_csv('Airline_Delay_Cause.csv')

# Initial Data Exploration
print(ds.head())

# ROOT CAUSE ANALYSIS

delay_min_col = ["carrier_delay", "weather_delay", "nas_delay", "security_delay", "late_aircraft_delay"]
total_delay_min = ds[delay_min_col].sum()

print("Delay type with most minutes:")
print(total_delay_min.sort_values(ascending=False))
