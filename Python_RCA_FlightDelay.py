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

# CAUSAL INFERENCE  # Driver set first
causal_graph = """digraph {
    late_aircraft_delay;
    carrier_delay;
    nas_delay;
    security_delay;
    weather_delay;
    arr_delay;
    
    late_aircraft_delay -> arr_delay;
    
    carrier_delay -> arr_delay;
    nas_delay -> arr_delay;
    security_delay -> arr_delay;
    weather_delay -> arr_delay;

    carrier_delay -> late_aircraft_delay;
    weather_delay -> late_aircraft_delay;
    weather_delay -> nas_delay;
}"""

import sys
import networkx as nx

# Fix the breaking change where DoWhy looks for the old function path
try:
    import networkx.algorithms.d_separation as ds_mod
    # Inject it directly into the expected module namespace
    sys.modules['networkx.algorithms'].d_separated = ds_mod.is_d_separator
except (ImportError, AttributeError):
    pass

# Create model object
from dowhy import CausalModel

treatment_col = "late_aircraft_delay"
outcome_col = "arr_delay"

model = CausalModel(
    data = ds,
    treatment =  treatment_col,
    outcome = outcome_col,
    graph= causal_graph,
)

identified_estimand = model.identify_effect(proceed_when_unidentifiable=True) # Estimate desired quantity
print(identified_estimand) # Explore proposed methods