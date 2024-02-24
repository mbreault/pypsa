import pypsa
import numpy as np

# Define number of buses and lines
n_buses = 5
n_lines = 4

network = pypsa.Network()

# Add buses
for i in range(n_buses):
    network.add("Bus", f"bus{i}", v_nom=20)

# Add generators with varying parameters
for i in range(n_buses):
    network.add("Generator", f"gen{i}", bus=f"bus{i}", p_nom=100, marginal_cost=np.random.uniform(5, 25))

# Add loads with varying demands
for i in range(n_buses):
    network.add("Load", f"load{i}", bus=f"bus{i}", p_set=np.random.uniform(50, 150))

# Add lines with varying capacities and impedances
for i in range(n_lines):
    network.add("Line", f"line{i}", 
                bus0=f"bus{i}", 
                bus1=f"bus{(i+1)%n_buses}", 
                x=np.random.uniform(0.1, 0.3), 
                s_nom=np.random.uniform(90, 110))

# Define snapshots for time series data
snapshots = range(24)  # for one day hourly resolution
network.set_snapshots(snapshots)

# Add time-varying loads and generation (e.g., simulating a daily pattern)
load_p_set = np.random.uniform(60, 140, size=(24, n_buses))
gen_p_max_pu = np.random.uniform(0, 1, size=(24, n_buses))

for i in range(n_buses):
    network.loads_t.p_set[f"load{i}"] = load_p_set[:, i]
    network.generators_t.p_max_pu[f"gen{i}"] = gen_p_max_pu[:, i]

# Optimize the network over the snapshots
network.lopf(network.snapshots, solver_name="gurobi")

# Print the results
results = network.generators_t.p

print(results)

# Write the results to a file
network.export_to_csv_folder("results")
