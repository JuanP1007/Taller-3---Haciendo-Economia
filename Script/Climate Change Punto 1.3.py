import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

os.makedirs("../Figures", exist_ok=True)
os.makedirs("../RawData", exist_ok=True)

# -----------------------------------------------
# CARGA DE DATOS DE TEMPERATURA (NASA GISS)
# -----------------------------------------------
url_temp = "https://data.giss.nasa.gov/gistemp/tabledata_v4/NH.Ts+dSST.csv"
temp_data = pd.read_csv(url_temp, skiprows=1, na_values=["*", "**", "***", "****", ""])
temp_data.columns = temp_data.columns.str.strip()
for col in temp_data.columns:
    temp_data[col] = pd.to_numeric(temp_data[col], errors="coerce")
temp_data = temp_data.dropna(subset=["Year"])
temp_data["Year"] = temp_data["Year"].astype(int)

# -----------------------------------------------
# CARGA DE DATOS DE CO₂ (NOAA - Mauna Loa)
# El archivo tiene líneas de comentario con # y luego
# una fila de encabezado real con los nombres de columnas
# -----------------------------------------------
url_co2 = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.csv"
co2_data = pd.read_csv(url_co2, comment="#")

# Limpiar nombres de columnas por si tienen espacios
co2_data.columns = co2_data.columns.str.strip()

print("Columnas detectadas:", co2_data.columns.tolist())
print(co2_data.head())

# Reemplazar valores faltantes (-9.99 y -1) por NaN
co2_data.replace(-9.99, np.nan, inplace=True)
co2_data.replace(-1, np.nan, inplace=True)

# Renombrar columnas al formato del taller
# 'average' -> interpolated, 'deseasonalized' -> trend
co2_data.rename(columns={
    "average":        "interpolated",
    "deseasonalized": "trend"
}, inplace=True)

# Asegurar tipos numéricos en year y month
co2_data["year"]  = pd.to_numeric(co2_data["year"],  errors="coerce")
co2_data["month"] = pd.to_numeric(co2_data["month"], errors="coerce")
co2_data = co2_data.dropna(subset=["year", "month"])
co2_data["year"]  = co2_data["year"].astype(int)
co2_data["month"] = co2_data["month"].astype(int)

co2_data.to_csv("../RawData/co2_mauna_loa.csv", index=False)

# -----------------------------------------------
# PREGUNTA 1.3.3 - GRÁFICO CO₂ (interpolated y trend)
# -----------------------------------------------
co2_data["Date"] = pd.to_datetime(
    dict(year=co2_data["year"], month=co2_data["month"], day=1)
)

co2_1960 = co2_data[co2_data["Date"] >= "1960-01-01"].copy()

plt.figure(figsize=(12, 5))
plt.plot(co2_1960["Date"], co2_1960["interpolated"], color="steelblue",
         label="Interpolado", linewidth=1)
plt.plot(co2_1960["Date"], co2_1960["trend"], color="tomato",
         label="Tendencia", linewidth=1.5)
plt.title("Concentración de CO₂ en la atmósfera – Mauna Loa (1960–Presente)")
plt.xlabel("Año")
plt.ylabel("CO₂ (ppm)")
plt.legend()
plt.tight_layout()
plt.savefig("../Figures/co2_trend.png", dpi=300)
plt.show()

# -----------------------------------------------
# PREGUNTA 1.3.4 - DISPERSIÓN CO₂ vs ANOMALÍA (JULIO)
# -----------------------------------------------
temp_july = temp_data[["Year", "Jul"]].dropna()
temp_july = temp_july.rename(columns={"Jul": "temp_anomaly"})

co2_july = co2_data[co2_data["month"] == 7][["year", "trend"]].dropna()
co2_july = co2_july.rename(columns={"year": "Year", "trend": "co2_trend"})

merged = pd.merge(temp_july, co2_july, on="Year")

plt.figure(figsize=(8, 6))
plt.scatter(merged["temp_anomaly"], merged["co2_trend"],
            color="darkorange", edgecolors="white", alpha=0.8, s=50)
plt.xlabel("Anomalía de temperatura en Julio (°C)")
plt.ylabel("Tendencia de CO₂ (ppm)")
plt.title("CO₂ vs Anomalía de temperatura – Julio")
plt.tight_layout()
plt.savefig("../Figures/co2_vs_temp_scatter.png", dpi=300)
plt.show()

r, p_value = stats.pearsonr(merged["temp_anomaly"], merged["co2_trend"])
print(f"\n===== PREGUNTA 1.3.4 =====")
print(f"Coeficiente de correlación de Pearson (r): {r:.4f}")
print(f"Valor p: {p_value:.4e}")
