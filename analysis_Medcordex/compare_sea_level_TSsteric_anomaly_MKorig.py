import os
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for rendering plots
from scipy.spatial import cKDTree
from datetime import datetime
from sklearn.linear_model import LinearRegression
import pymannkendall as mk

station = 'OT15'
st_name = 'OTRANTO'
print("Station = ",station)

# File paths
tide_gauge_file = f"/work/cmcc/re35220/AdriaClimPlus/analysis/EvalRun/TSL/insitu/TS_SLEV_{station}.nc"
mask_file = "/work/cmcc/resm-dev/vladimir/FLAME/EXPS/EvalRUN_03s/bathy_mask_03s/mesh_mask_03s.nc"

# Load tide gauge data
tide_gauge = xr.open_dataset(tide_gauge_file)
lon_tide_gauge = tide_gauge.longitude.values
lat_tide_gauge = tide_gauge.latitude.values
sea_level = tide_gauge.SLEV.values

# Convert time to pandas datetime
time_tide_gauge = tide_gauge.time.values
tide_gauge_time = pd.to_datetime(time_tide_gauge)

# Convert to DataFrame for processing
tide_gauge_df = pd.DataFrame({"datetime": tide_gauge_time, "sea_level": sea_level}).set_index("datetime")

# Remove invalid values (-999) and outliers
tide_gauge_df["sea_level"] = tide_gauge_df["sea_level"].replace(-999, np.nan)
tide_gauge_df = tide_gauge_df[np.abs(tide_gauge_df["sea_level"] - tide_gauge_df["sea_level"].mean()) <= 3 * tide_gauge_df["sea_level"].std()]
tide_gauge_df = tide_gauge_df.interpolate().dropna()

# Convert to monthly means
tide_gauge_monthly1 = tide_gauge_df.resample("ME").mean()

# Load steric and SSH data
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
tmask = mask_data.tmask[0, 0, :, :].values
lon_model = mask_data.nav_lon.values
lat_model = mask_data.nav_lat.values

# Flatten model grid
model_points = np.column_stack((lon_model.ravel(), lat_model.ravel()))
tmask_flat = tmask.ravel()

# Create KDTree for nearest point search
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

# Extract model data for given day
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
model_df = pd.DataFrame({"datetime": model_dates, "zos": model_zos}).set_index("datetime")

# Convert model data to monthly means
model_monthly1 = model_df.resample("ME").mean()

# Handle missing values
tide_gauge_monthly1 = tide_gauge_monthly1.ffill().bfill()
model_monthly1 = model_monthly1.ffill().bfill()

# Ensure both datasets have the same time range
common_dates = model_monthly1.index.intersection(tide_gauge_monthly1.index)
model_monthly1 = model_monthly1.loc[common_dates]
tide_gauge_monthly1 = tide_gauge_monthly1.loc[common_dates]

# Calculate anomalies
model_monthly = model_monthly1 - model_monthly1.mean()
tide_gauge_monthly = tide_gauge_monthly1 - tide_gauge_monthly1.mean()

# Deseasonalization: Remove monthly means
tide_gauge_monthly["month"] = tide_gauge_monthly.index.month
model_monthly["month"] = model_monthly.index.month

# Compute monthly means
tide_gauge_monthly["monthly_mean"] = tide_gauge_monthly.groupby("month")["sea_level"].transform("mean")
model_monthly["monthly_mean"] = model_monthly.groupby("month")["zos"].transform("mean")

# Remove seasonal cycle
tide_gauge_monthly["deseasonalized"] = tide_gauge_monthly["sea_level"] - tide_gauge_monthly["monthly_mean"]
model_monthly["deseasonalized"] = model_monthly["zos"] - model_monthly["monthly_mean"]

#plt.figure()
#plt.plot(tide_gauge_monthly.index, tide_gauge_monthly["monthly_mean"])
#plt.savefig(f'monthly_mean_{station}.png', dpi=300)

#plt.figure()
#plt.plot(model_monthly.index, model_monthly["monthly_mean"])
#plt.savefig(f'monthly_mean_{station}_model.png', dpi=300)

# Drop unnecessary columns
tide_gauge_monthly = tide_gauge_monthly.drop(columns=["month", "monthly_mean"])
model_monthly = model_monthly.drop(columns=["month", "monthly_mean"])

# Mann-Kendall trend test using deseasonalized data
mk_model = mk.original_test(model_monthly["deseasonalized"])
mk_tide_gauge = mk.original_test(tide_gauge_monthly["deseasonalized"])

print("MK model (deseasonalized) =", mk_model)
print("MK tide_gauge (deseasonalized) =", mk_tide_gauge)

# Extract trend slopes
slope_model = mk_model.slope
slope_tide_gauge = mk_tide_gauge.slope

# Convert slopes to mm/year
slope_model_mm_yr = slope_model * 12 * 1000
slope_tide_gauge_mm_yr = slope_tide_gauge * 12 * 1000

# Compute linear trends starting from the mean value of each dataset
t = np.arange(len(tide_gauge_monthly))
mean_model = model_monthly["deseasonalized"].mean()
mean_tide_gauge = tide_gauge_monthly["deseasonalized"].mean()

trend_model = mean_model + slope_model * (t - t.mean())  # Centered trend
trend_tide_gauge = mean_tide_gauge + slope_tide_gauge * (t - t.mean())  # Centered trend

# Metrics
correlation = tide_gauge_monthly["deseasonalized"].corr(model_monthly["deseasonalized"])
rmse = (np.sqrt(np.mean((model_monthly["deseasonalized"] - tide_gauge_monthly["deseasonalized"])**2))) * 100
bias = (np.mean(model_monthly["deseasonalized"] - tide_gauge_monthly["deseasonalized"])) * 100
print("BIAS = ",bias)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(tide_gauge_monthly.index, tide_gauge_monthly["deseasonalized"], label="Tide Gauge", linewidth=2, color='firebrick')
plt.plot(model_monthly.index, model_monthly["deseasonalized"], label="Model", linewidth=2, color='steelblue')

# Add Mann-Kendall trend lines (centered)
plt.plot(tide_gauge_monthly.index, trend_tide_gauge, '--', label=f"Tide Gauge Trend ({slope_tide_gauge_mm_yr:.2f} mm/yr)", color='indianred', linewidth=2)
plt.plot(model_monthly.index, trend_model, '--', label=f"Model Trend ({slope_model_mm_yr:.2f} mm/yr)", color='skyblue', linewidth=2)

#plt.plot(tide_gauge_monthly.index,tide_gauge_monthly["monthly_mean"])

# Add metrics text
plt.text(0.02, 0.05, f"Correlation: {correlation:.2f}\nRMSE: {rmse:.3f} cm", 
         transform=plt.gca().transAxes, fontsize=14, bbox=dict(facecolor="white", alpha=0.8, edgecolor="black"))

plt.ylim(-0.4,0.4)
plt.ylabel("Sea Level Anomaly (m)",fontsize=14)
plt.legend(loc="upper left",fontsize=14)
plt.title(f'{st_name}',fontsize=14)
plt.grid()
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.tight_layout()
plt.savefig(f'sea_level_nonseason_{station}.png', dpi=300)

