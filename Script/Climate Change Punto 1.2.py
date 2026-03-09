
import pandas as pd
import numpy as np
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

os.makedirs("../Figures", exist_ok=True)

# -----------------------------------------------
# PREPARAR ANOMALÍAS MENSUALES COMBINADAS
# -----------------------------------------------
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Extraer todas las anomalías mensuales por periodo
period1 = data[(data["Year"] >= 1951) & (data["Year"] <= 1980)][months].values.flatten()
period2 = data[(data["Year"] >= 1981) & (data["Year"] <= 2010)][months].values.flatten()

# Eliminar NaN
period1 = period1[~np.isnan(period1)]
period2 = period2[~np.isnan(period2)]

# -----------------------------------------------
# PREGUNTA 1.2.1 - TABLAS DE FRECUENCIAS
# -----------------------------------------------
bins = np.arange(-2.0, 2.25, 0.25)  # intervalos de 0.25°C

counts1, edges = np.histogram(period1, bins=bins)
counts2, _     = np.histogram(period2, bins=bins)

freq_table = pd.DataFrame({
    "Intervalo": [f"[{edges[i]:.2f}, {edges[i+1]:.2f})" for i in range(len(edges)-1)],
    "Frec. Absoluta 1951–1980": counts1,
    "Frec. Relativa 1951–1980 (%)": (counts1 / counts1.sum() * 100).round(2),
    "Frec. Absoluta 1981–2010": counts2,
    "Frec. Relativa 1981–2010 (%)": (counts2 / counts2.sum() * 100).round(2),
})

print("===== TABLA DE FRECUENCIAS =====")
print(freq_table.to_string(index=False))

# -----------------------------------------------
# PREGUNTA 1.2.2 - HISTOGRAMAS
# -----------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

axes[0].hist(period1, bins=bins, color="steelblue", edgecolor="white")
axes[0].set_title("Distribución de anomalías 1951–1980")
axes[0].set_xlabel("Anomalía de temperatura (°C)")
axes[0].set_ylabel("Frecuencia")
axes[0].axvline(0, linestyle="--", color="gray", label="Promedio de 1951 a 1980")
axes[0].legend()

axes[1].hist(period2, bins=bins, color="tomato", edgecolor="white")
axes[1].set_title("Distribución de anomalías 1981–2010")
axes[1].set_xlabel("Anomalía de temperatura (°C)")
axes[1].axvline(0, linestyle="--", color="gray", label="Promedio de 1951 a 1980")
axes[1].legend()

plt.suptitle("Comparación de distribuciones de anomalías de temperatura\n(Hemisferio Norte)", fontsize=13)
plt.tight_layout()
plt.savefig("../Figures/histograms_comparison.png", dpi=300)
plt.show()

# -----------------------------------------------
# PREGUNTA 1.2.3 - DECILES 3 Y 7 (1951–1980)
# -----------------------------------------------
decil3 = np.quantile(period1, 0.3)
decil7 = np.quantile(period1, 0.7)

print(f"\n===== PREGUNTA 1.2.3 =====")
print(f"Decil 3 (1951–1980): {decil3:.4f} °C")
print(f"Decil 7 (1951–1980): {decil7:.4f} °C")

# -----------------------------------------------
# PREGUNTA 1.2.4 - % DE ANOMALÍAS "CALIENTES" EN 1981–2010
# -----------------------------------------------
hot_count = np.sum(period2 > decil7)
hot_pct   = hot_count / len(period2) * 100

print(f"\n===== PREGUNTA 1.2.4 =====")
print(f"Anomalías 'calientes' en 1981–2010: {hot_count} de {len(period2)} ({hot_pct:.2f}%)")

# -----------------------------------------------
# PREGUNTA 1.2.5 - MEDIA Y VARIANZA POR ESTACIÓN Y PERIODO
# -----------------------------------------------
seasons = ["DJF", "MAM", "JJA", "SON"]
periods = {
    "1921–1950": (1921, 1950),
    "1951–1980": (1951, 1980),
    "1981–2010": (1981, 2010),
}

print(f"\n===== PREGUNTA 1.2.5 - MEDIA Y VARIANZA POR ESTACIÓN =====")
rows = []
for period_name, (y_start, y_end) in periods.items():
    subset = data[(data["Year"] >= y_start) & (data["Year"] <= y_end)]
    for season in seasons:
        values = subset[season].dropna()
        rows.append({
            "Periodo": period_name,
            "Estación": season,
            "Media (°C)": round(values.mean(), 4),
            "Varianza (°C²)": round(values.var(), 4),
        })

stats_table = pd.DataFrame(rows)
print(stats_table.to_string(index=False))

# Gráfico de varianzas por estación y periodo
fig, ax = plt.subplots(figsize=(10, 5))
bar_width = 0.25
x = np.arange(len(seasons))

for i, period_name in enumerate(periods.keys()):
    subset_stats = stats_table[stats_table["Periodo"] == period_name]
    ax.bar(x + i * bar_width, subset_stats["Varianza (°C²)"], width=bar_width, label=period_name)

ax.set_xticks(x + bar_width)
ax.set_xticklabels(seasons)
ax.set_xlabel("Estación")
ax.set_ylabel("Varianza (°C²)")
ax.set_title("Varianza de anomalías de temperatura por estación y periodo")
ax.legend()
plt.tight_layout()
plt.savefig("../Figures/variance_by_season.png", dpi=300)
plt.show()