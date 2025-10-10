import os
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for rendering plots
from scipy.spatial import cKDTree
from datetime import datetime
from scipy.stats import norm

station = 'AN15'

# File paths
tide_gauge_file = f"/work/cmcc/re35220/AdriaClimPlus/analysis/EvalRun/TSL/insitu/TS_SLEV_{station}.nc"
mask_file = "/work/cmcc/resm-dev/vladimir/FLAME/EXPS/EvalRUN_03s/bathy_mask_03s/mesh_mask_03s.nc"

# Load tide gauge data
tide_gauge = xr.open_dataset(tide_gauge_file)
lon_tide_gauge = tide_gauge.longitude.values
lat_tide_gauge = tide_gauge.latitude.values
sea_level = tide_gauge.SLEV.values

# Time in seconds since 1970-01-01
time_tide_gauge = tide_gauge.time.values
tide_gauge_time = pd.to_datetime(time_tide_gauge)

# Convert to DataFrame for processing
tide_gauge_df = pd.DataFrame({"datetime": tide_gauge_time, "sea_level": sea_level}).set_index("datetime")

# Remove invalid values (-999) and outliers
tide_gauge_df["sea_level"] = tide_gauge_df["sea_level"].replace(-999, np.nan)
tide_gauge_df = tide_gauge_df[np.abs(tide_gauge_df["sea_level"] - tide_gauge_df["sea_level"].mean()) <= 3 * tide_gauge_df["sea_level"].std()]
tide_gauge_df = tide_gauge_df.interpolate().dropna()  # Interpolate missing values and drop NaNs

# Load the steric and SSH data
Ssteric_file = "files/Ssteric_NEMO_EvalRun_daily_1990_2019.npz"
Tsteric_file = "files/Tsteric_NEMO_EvalRun_daily_1990_2019.npz"
SSHmodel_file = "files/SSHmodel_NEMO_EvalRun_daily_1990_2019.npz"

Ssteric_data = np.load(Ssteric_file)
Tsteric_data = np.load(Tsteric_file)
SSHmodel_data = np.load(SSHmodel_file)

Ssteric = Ssteric_data["Ssteric"]
Tsteric = Tsteric_data["Tsteric"]
SSHmodel = SSHmodel_data["SSHmodel"]

# Load model grid and mask
mask_data = xr.open_dataset(mask_file)
tmask = mask_data.tmask[0, 0, :, :].values  # Surface mask
lon_model = mask_data.nav_lon.values
lat_model = mask_data.nav_lat.values

# Flatten model grid and mask
model_points = np.column_stack((lon_model.ravel(), lat_model.ravel()))
tmask_flat = tmask.ravel()

# Create KDTree
tree = cKDTree(model_points)
tide_gauge_point = np.array([lon_tide_gauge, lat_tide_gauge]).flatten()

# Find nearest sea index
def find_nearest_sea_point(tide_gauge_point, tree, tmask_flat):
    _, idx = tree.query(tide_gauge_point)
    if tmask_flat[idx] == 1:
        return np.unravel_index(idx, lon_model.shape)
    for k in range(2, len(tmask_flat)):
        _, neighbors = tree.query(tide_gauge_point, k=k)
        sea_points = neighbors[tmask_flat[neighbors] == 1]
        if len(sea_points) > 0:
            return np.unravel_index(sea_points[0], lon_model.shape)
    return None

nearest_sea_idx = find_nearest_sea_point(tide_gauge_point, tree, tmask_flat)

# Function to extract model data
def load_model_data_for_day(date):
    day_index = (date - np.datetime64('1990-01-01')).days
    if 0 <= day_index < len(SSHmodel):
        ssh_day = SSHmodel[day_index]
        steric_day = Ssteric[day_index] + Tsteric[day_index]
        if nearest_sea_idx is not None:
            return ssh_day[nearest_sea_idx] + steric_day[nearest_sea_idx]
    return None

# Align time series
start_date = pd.Timestamp("1990-01-01")
end_date = pd.Timestamp("2019-12-31")
model_dates = pd.date_range(start_date, end_date, freq="D")

model_zos = [load_model_data_for_day(date) for date in model_dates]
model_zos = np.array(model_zos)

# Convert to DataFrame
model_df = pd.DataFrame({"datetime": model_dates, "zos": model_zos}).set_index("datetime")
print("model date=",model_df)

# Process tide gauge data to daily means
tide_gauge_daily = tide_gauge_df.resample("D").mean()

# Handle missing values
tide_gauge_daily = tide_gauge_daily.ffill().bfill()
model_df = model_df.ffill().bfill()

# Ensure both datasets have the same time range
common_dates = model_df.index.intersection(tide_gauge_daily.index)
model_df = model_df.loc[common_dates]
tide_gauge_daily = tide_gauge_daily.loc[common_dates]
print("new model date=",model_df)

# Check lengths before merging
#print("Model data points:", len(model_df))
#print("Tide gauge data points:", len(tide_gauge_daily))

# Calculate anomalies
model_anomaly = model_df - model_df.mean()
tide_gauge_anomaly = tide_gauge_daily - tide_gauge_daily.mean()

# Merge datasets
valid_data = tide_gauge_anomaly.join(model_anomaly, how='inner').dropna()

# Check details after merging
#print("Final dataset points:", len(valid_data))
#print("Overlapping period:", valid_data.index.min(), "to", valid_data.index.max())
#print("Missing values:", valid_data.isna().sum())
#print("size model:", np.size(valid_data["zos"]))
#print("size tide gauge:", np.size(valid_data["sea_level"]))

# Fit normal distributions
mu_model, std_model = norm.fit(valid_data["zos"])
mu_tide_gauge, std_tide_gauge = norm.fit(valid_data["sea_level"])

# Bin edges for both histograms
bins = np.linspace(valid_data["sea_level"].min(), valid_data["sea_level"].max(), 100)

# Plotting histograms
plt.figure(figsize=(12, 6))

plt.hist(valid_data["sea_level"], bins=bins, density=True, alpha=0.6, color='firebrick', label='Tide Gauge')
plt.hist(valid_data["zos"], bins=bins, density=True, alpha=0.6, color='steelblue', label='Model')

# Plot normal distribution fits
x = np.linspace(min(valid_data.min()), max(valid_data.max()), 1000)
plt.plot(x, norm.pdf(x, mu_tide_gauge, std_tide_gauge), 'r--', label=rf'Tide Gauge Fit ($\mu$={mu_tide_gauge:.3f}, $\sigma$={std_tide_gauge:.3f})')
plt.plot(x, norm.pdf(x, mu_model, std_model), 'b--', label=rf'Model Fit ($\mu$={mu_model:.3f}, $\sigma$={std_model:.3f})')

plt.ylim(0,5)
plt.xlim(-0.8, 0.8)
plt.xlabel("Sea Level Anomaly (m)")
plt.ylabel("Probability Density")
plt.legend(loc="upper right")
plt.grid()
plt.tight_layout()
plt.savefig(f'sea_level_pdf_{station}.png', dpi=300)

