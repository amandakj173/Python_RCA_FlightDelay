# DATA WRANGLING

# Import Packages
import sys
import dowhy
import pandas as pd
import numpy as np
import networkx as nx

# Fix: Get Pandas 2.0+ positional indexing bug in DoWhy
_orig_getitem = pd.Series.__getitem__
def _patched_getitem(self, key):
    try:
        return _orig_getitem(self, key)
    except KeyError:
        if isinstance(key, int):
            return self.iloc[key]
        raise
pd.Series.__getitem__ = _patched_getitem

# Fix 2: NetworkX compatibility patch
try:
    import networkx.algorithms.d_separation as ds_mod
    sys.modules['networkx.algorithms'].d_separated = ds_mod.is_d_separator
except (ImportError, AttributeError):
    pass

# Set Parameters
pd.set_option("display.precision",3)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width',2000)

# Import Data
ds = pd.read_csv('Airline_Delay_Cause.csv')

# Initial Data Exploration
print(ds.head())

# Organise Data
ds = ds.dropna()

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

# EFFECT ESTIMATION
method = "backdoor.linear_regression"  # Use backdoor regression identified in causal model
desired_effect = "ate"  # Use average treatment effect to measure overall impact of change/variable across entire dataset

estimate = model.estimate_effect(
    identified_estimand,
    method_name = method,
    target_units = desired_effect,
    method_params = {"weighting_scheme":"ips_weight"}
)

print("Causal Estimate is " + str(estimate.value))

# REFUTATION
refute_placebo_delay = model.refute_estimate(
    identified_estimand,
    estimate,
    method_name = "placebo_treatment_refuter",
    placebo_type = "permute"
)

print(refute_placebo_delay)