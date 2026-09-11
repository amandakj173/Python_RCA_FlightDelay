# Root Cause Analysis - Flight Delay

This project applied root cause analysis (RCA) and causal inference to U.S airline delay data to identify the primary drivers of delays in flight arrivals. The project combined directed acyclic graphs (DAGs) with DoWhy's backdoor adjustment framework to isolate true causal mechanisms from statistical correlation, quantifying how incoming aircraft delays compound across airline operations. 

## Description

Flight delays present a complex operational challenge where multiple factors interact simultaneously. Traditional explaratory analysis can identify which categories have the most total delay minutes, but fail to answer whether specific delay causes directly drive overall arrival delays or simply correlate with them.

This project implements a structured causal inference workflow:
1. Explaratory RCA: Aggregate delay metrics across major cause categories to identify the top delay contributor
2. Causal graph modelling: Construct a DAG to map structural dependencies & identify confounding paths among carrier, air traffic control (NAS), late-arriving aircraft, security, and weather.
3. Causal effect estimation: Apply Backdoor Adjustment using linear regression with Inverse Propensity Score (IPS) weighting to measure the marginal effect of late aircraft on total arrival delays
4. Model sensitivity: Validate results against random correlation using Placebo Treament refutation tests.

## Interpretation
### RCA
An initial breakdown of total delay minutes across the dataset revealed that delays due to late aircraft contributed the highest number of overall delay minutes.

### Causal Inference
Based on the structural DAG, controlling for backdoor paths, mathematically guarantees an unbiased and unconfounded estimate of the causal impact of delays due to late arriving aircraft on total delay minutes.

### Effect Estimation
Causal estimate: 1.300

Controlling for confounding variables, every 1 additional minute of previous aircraft delay causes current flight arrival delay to increase by approximately 1.300 minutes (78 seconds). As this multiplier exceeds 1.000, late aircraft delays exhibit a compounding knock-on-effect, wherein a late incoming aeroplane incurs additional operational bottlenecks that enhance overall delay.

### Model Sensitivity
Test type: Placebo Treatment Refutation
New estimate: .0009 (_p_>.84)

Replacing the true treatment variable with a randomly generated placebo dropped the estimated causal effect. The high _p_-value confirms that the placebo effect is statistically indistinguishable from zero, proving the causal model is robust and that the primary estimate reflects a true causal relationship rather than random noise or modelling artefacts.

## Next Steps
1. Advance causal estimates using random and causal forests to capture non-linear interactions between variables and identify specific sub-conditions where incoming aircraft delays are exacerbated.
