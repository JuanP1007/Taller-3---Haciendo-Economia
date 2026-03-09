
import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------------------------
# CARGA DE DATOS DESDE URL (NASA GISS)
# -----------------------------------------------
url_temp = "https://data.giss.nasa.gov/gistemp/tabledata_v4/NH.Ts+dSST.csv"
data = pd.read_csv(url_temp, skiprows=1, na_values=["*", "**", "***", "****", ""])
data.columns = data.columns.str.strip()
for col in data.columns:
    data[col] = pd.to_numeric(data[col], errors="coerce")
data = data.dropna(subset=["Year"])
data["Year"] = data["Year"].astype(int)

os.makedirs("../RawData", exist_ok=True)
os.makedirs("../Figures", exist_ok=True)

# Guardar CSV en RawData con nombre adecuado
data.to_csv("../RawData/nh_temperature_anomalies_giss.csv", index=False)

# -----------------------------------------------
# GRÁFICO MENSUAL - ENERO
# -----------------------------------------------
month = "Jan"
plt.figure(figsize=(10, 5))
plt.plot(data["Year"], data[month], color="blue", label="Enero")
plt.axhline(0, linestyle="--", color="gray", label="Promedio de 1951 a 1980")
plt.title("Anomalía de temperatura en Enero (1880–Presente)")
plt.xlabel("Año")
plt.ylabel("Anomalía de temperatura (°C)")
plt.legend()
plt.savefig("../Figures/monthly_plot.png", dpi=300)
plt.show()

# -----------------------------------------------
# GRÁFICO ESTACIONAL
# -----------------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(data["Year"], data["DJF"], label="Invierno (DJF)")
plt.plot(data["Year"], data["MAM"], label="Primavera (MAM)")
plt.plot(data["Year"], data["JJA"], label="Verano (JJA)")
plt.plot(data["Year"], data["SON"], label="Otoño (SON)")
plt.axhline(0, linestyle="--", color="gray", label="Promedio de 1951 a 1980")
plt.title("Anomalías de temperatura por estación (1880–Presente)")
plt.xlabel("Año")
plt.ylabel("Anomalía de temperatura (°C)")
plt.legend()
plt.savefig("../Figures/seasonal_plot.png", dpi=300)
plt.show()

# -----------------------------------------------
# GRÁFICO ANUAL
# -----------------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(data["Year"], data["J-D"], color="black", label="Promedio anual")
plt.axhline(0, linestyle="--", color="gray", label="Promedio de 1951 a 1980")
plt.title("Anomalía anual de temperatura del hemisferio norte")
plt.xlabel("Año")
plt.ylabel("Anomalía de temperatura (°C)")
plt.legend()
plt.savefig("../Figures/annual_plot.png", dpi=300)
plt.show()