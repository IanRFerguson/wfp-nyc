import os

import folium
import geopandas as gpd
import pandas as pd
from logger import logger

##########

NYC_COORDS = [40.7128, -74.006]
ZOOM_START = 11


def main(
    data_directory: os.path,
    election_data: pd.DataFrame,
    nyc_shapefile: gpd.GeoDataFrame,
):
    logger.info("Building Folium map...")
    logger.debug("Aggregating election + shapefile data...")
    _agg_data = nyc_shapefile.merge(election_data, on="ElectDist")

    # Add percentage column to use for display
    _agg_data["clean_pct"] = _agg_data["wfp_pct"].apply(lambda x: f"{round(x, 2)}%")

    # Simplify geometry column in geo df
    _agg_data["geometry"] = gpd.GeoSeries.simplify(_agg_data["geometry"], tolerance=10)

    logger.debug(_agg_data.head())

    nyc_map = folium.Map(location=NYC_COORDS, zoom_start=ZOOM_START)

    # Choropleth component
    logger.debug("Adding Choropleth...")
    _choropleth = folium.Choropleth(
        geo_data=nyc_shapefile,
        data=election_data,
        columns=["ElectDist", "wfp_pct"],
        key_on="feature.properties.ElectDist",
        fill_color="RdYlGn",
        fill_opacity=0.9,
        line_opacity=0.15,
        highlights=True,
        legend_name="WFP Democratic Vote %",
        bins=[0, 2, 8, 14, 20, 26, 32, 38, 44, 50],
    )

    # Hacky way to hide the Choropleth legend
    for key in _choropleth._children:
        if key.startswith("color_map"):
            del _choropleth._children[key]

    _choropleth.add_to(nyc_map)

    # Tooltip component
    logger.debug("Adding tooltip...")
    style_function = lambda x: {
        "fillColor": "#ffffff",
        "color": "#000000",
        "fillOpacity": 0.1,
        "weight": 0.1,
    }

    _tooltip = folium.features.GeoJson(
        _agg_data,
        style_function=style_function,
        control=False,
        tooltip=folium.features.GeoJsonTooltip(
            fields=["ElectDist", "clean_pct", "vote_totals"],
            aliases=["Election District", "WFP Vote Share", "Total Harris Votes"],
            style=(
                "background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"
            ),
        ),
    )

    # Add elements to map
    nyc_map.add_child(_tooltip)
    nyc_map.keep_in_front(_tooltip)
    folium.LayerControl().add_to(nyc_map)

    # Save locally
    outfile = os.path.join(data_directory, "wfp_nyc.html")
    logger.debug(f"Writing to {outfile}...")

    nyc_map.save(outfile=outfile)
    logger.info("Successfully built map")


#####

if __name__ == "__main__":
    RAW_DIRECTORY = os.path.abspath("../raw")
    ELECTION_DATA_PATH = os.path.join(RAW_DIRECTORY, "analytics.csv")
    NYC_SHAPEFILE_PATH = os.path.join(RAW_DIRECTORY, "nyed_24d", "nyed.shp")

    FLASK_TEMPLATE_DIRECTORY = os.path.join("../static")

    ELECTION_DATA = pd.read_csv(ELECTION_DATA_PATH)
    NYC_SHAPEFILE = gpd.read_file(NYC_SHAPEFILE_PATH)

    main(
        data_directory=FLASK_TEMPLATE_DIRECTORY,
        election_data=ELECTION_DATA,
        nyc_shapefile=NYC_SHAPEFILE,
    )
