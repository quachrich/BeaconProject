import pandas as pd
import plotly.graph_objs as go
import geopandas as gpd
from pathlib import Path

WORLD_SHP = Path("ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")

COUNTRY_FIXES = {
    "United States": "United States of America",
    "Viet Nam": "Vietnam",
    "Ivory Coast": "Côte d'Ivoire",
    "Czechia": "Czech Republic",
    "South Korea": "Korea, Republic of",
    "North Korea": "Korea, Democratic People's Republic of",
    "Eswatini": "Eswatini",
}

def _normalize_country_names(series: pd.Series) -> pd.Series:
    return series.map(lambda x: COUNTRY_FIXES.get(x, x))

def _country_centroids_from_shp(shp_path: Path) -> pd.DataFrame:
    world = gpd.read_file(shp_path).to_crs(4326)
    # pick robust column names present in NE data (fall back if needed)
    name_col = next(c for c in ["NAME_EN", "NAME", "ADMIN"] if c in world.columns)
    iso_col  = next(c for c in ["ADM0_A3", "ISO_A3", "ISO_A3_EH"] if c in world.columns)
    reps = world.representative_point()  # safer than centroid for multipolygons
    return pd.DataFrame({
        "name": world[name_col].astype(str),
        "iso_a3": world[iso_col].astype(str),
        "lat": reps.y,
        "lon": reps.x,
    })

def create_world_map(data: pd.DataFrame | None = None,
                     country_col: str = "Country",
                     text_col: str = "Description",
                     size_col: str | None = None):
    # Start with an empty geo figure; let Plotly draw the basemap/borders
    fig = go.Figure()
    fig.update_geos(
        projection_type="natural earth",
        showcountries=True,
        countrycolor="#9a9fa4",
        countrywidth=0.6,
        showcoastlines=True,
        coastlinecolor="#9a9fa4",
        showland=True,
        landcolor="#f8f9fa",
        lataxis_showgrid=True,
        lonaxis_showgrid=True,
    )

    if data is not None and not data.empty:
        centroids = _country_centroids_from_shp(WORLD_SHP)
        df = data.copy()
        df[country_col] = _normalize_country_names(df[country_col].astype(str))
        merged = df.merge(centroids, left_on=country_col, right_on="name", how="left")
        unmatched = merged[merged["lat"].isna()][country_col].unique().tolist()
        if unmatched:
            print("Unmatched country names (add to COUNTRY_FIXES):", unmatched)
        merged = merged.dropna(subset=["lat", "lon"])

        # Hover text
        hover_text = merged[text_col] if text_col in merged.columns else merged[country_col]

        # ---------- more visible markers ----------
        if size_col and size_col in merged.columns:
            max_count = max(merged[size_col].max(), 1)
            target_max_px = 20  # max bubble size on screen
            sizeref = (2.0 * max_count) / (target_max_px ** 2)

            marker = dict(
                size=merged[size_col],
                sizemode="area",
                sizeref=sizeref,
                sizemin=5,                            # keep small values visible
                line=dict(width=2, color="black"),     # bold outline for contrast
                color="#e74c3c",                       # vivid red
                opacity=0.95
            )
        else:
            marker = dict(
                size=5,                                # bigger constant dots
                line=dict(width=2, color="black"),
                color="#e74c3c",
                opacity=0.95
            )
        # ------------------------------------------
    
        fig.add_trace(go.Scattergeo(
            lon=merged["lon"],
            lat=merged["lat"],
            mode="markers",
            marker=marker,
            text=hover_text,
            hoverinfo="text",
            name="Events",
        ))

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
    return fig