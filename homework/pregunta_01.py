# pylint: disable=line-too-long
"""Genera un dashboard estático con gráficas y un archivo HTML en la carpeta docs."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def _find_data_file() -> Path:
    """Busca el archivo CSV en las rutas más comunes del proyecto."""
    base_dir = Path(__file__).resolve().parents[1]
    candidates = [
        base_dir / "files" / "input" / "shipping-data.csv",
        base_dir / "data" / "shipping-data.csv",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No se encontró el archivo shipping-data.csv")


def _save_plot(path: Path, plotter) -> None:
    """Guarda una figura en disco y la cierra."""
    plotter()
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()


def pregunta_01():
    """Crea el dashboard estático en la carpeta docs."""
    project_dir = Path(__file__).resolve().parents[1]
    docs_dir = project_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    data_file = _find_data_file()
    df = pd.read_csv(data_file)

    def plot_shipping_per_warehouse():
        plt.figure(figsize=(6, 4))
        counts = df["Warehouse_block"].value_counts()
        counts.plot.bar(color="tab:blue")
        plt.title("Shipping per Warehouse")
        plt.xlabel("Warehouse block")
        plt.ylabel("Record count")

    def plot_mode_of_shipment():
        plt.figure(figsize=(6, 4))
        counts = df["Mode_of_Shipment"].value_counts()
        counts.plot.pie(autopct="%1.1f%%", startangle=90)
        plt.title("Mode of Shipment")
        plt.ylabel("")

    def plot_average_customer_rating():
        plt.figure(figsize=(6, 4))
        summary = (
            df.groupby("Mode_of_Shipment")["Customer_rating"]
            .mean()
            .sort_values()
        )
        summary.plot.barh(color="tab:green")
        plt.title("Average Customer Rating")
        plt.xlabel("Average rating")
        plt.ylabel("Mode of Shipment")

    def plot_weight_distribution():
        plt.figure(figsize=(6, 4))
        df["Weight_in_gms"].plot.hist(bins=20, color="tab:orange", edgecolor="black")
        plt.title("Weight Distribution")
        plt.xlabel("Weight (g)")
        plt.ylabel("Frequency")

    _save_plot(docs_dir / "shipping_per_warehouse.png", plot_shipping_per_warehouse)
    _save_plot(docs_dir / "mode_of_shipment.png", plot_mode_of_shipment)
    _save_plot(docs_dir / "average_customer_rating.png", plot_average_customer_rating)
    _save_plot(docs_dir / "weight_distribution.png", plot_weight_distribution)

    html_content = f"""<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"utf-8\">
    <title>Shipping Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }}
        .card {{ border: 1px solid #ddd; padding: 12px; border-radius: 8px; }}
        img {{ width: 100%; height: auto; }}
    </style>
</head>
<body>
    <h1>Shipping Dashboard</h1>
    <div class=\"grid\">
        <div class=\"card\"><h2>Shipping per Warehouse</h2><img src=\"shipping_per_warehouse.png\" alt=\"Shipping per Warehouse\"></div>
        <div class=\"card\"><h2>Mode of Shipment</h2><img src=\"mode_of_shipment.png\" alt=\"Mode of Shipment\"></div>
        <div class=\"card\"><h2>Average Customer Rating</h2><img src=\"average_customer_rating.png\" alt=\"Average Customer Rating\"></div>
        <div class=\"card\"><h2>Weight Distribution</h2><img src=\"weight_distribution.png\" alt=\"Weight Distribution\"></div>
    </div>
</body>
</html>
"""
    (docs_dir / "index.html").write_text(html_content, encoding="utf-8")
