from pathlib import Path

import folium
import pandas as pd

from .map_data import map_data

__all__ = ["get_tz_map", "get_ug_map", "export_maps"]


def format_df(df: pd.DataFrame) -> pd.DataFrame:
    del_cols = [
        "record_id",
        "survey_identifier",
        "survey_timestamp",
        "complete?",
        "survey_timestamp.1",
        "complete?.1",
        "repeat_instrument",
        "repeat_instance",
    ]
    df = df.copy().rename(
        columns={col: col.replace(" ", "_").lower() for col in df.columns}
    )
    df = (
        df.drop(columns=[col for col in del_cols if col in df.columns])
        .rename(
            columns={
                "longitudes_at_the_community_venue": "comm_lon",
                "latitudes_at_the_community_venue": "comm_lat",
                "facility_latitudes": "lat",
                "facility_longitudes": "lon",
                "community_venue_name": "comm_name",
                "facility_name": "name",
                "comunity_groups": "groups",
            }
        )
        .fillna(pd.NA)
    )
    df.loc[df["name"].isna(), "name"] = df.loc[df["name"].isna(), "comm_name"]
    df.loc[df["lat"].isna(), "lat"] = df.loc[df["lat"].isna(), "comm_lat"]
    df.loc[df["lon"].isna(), "lon"] = df.loc[df["lon"].isna(), "comm_lon"]
    df["location_type"] = "facility"
    df.loc[df["comm_name"].notna(), "location_type"] = "community"
    return df


def get_tz_map() -> folium.Map:
    df_coordinates = pd.DataFrame(data=map_data)

    tz_map = folium.Map(location=[-6.7039, 39.0406], zoom_start=10)

    rows = list(
        df_coordinates.query(
            "location_type=='community' and country=='tanzania'"
        ).iterrows()
    )
    for index, row in rows:
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f'{row["name"]} [{row["facility"]}]',
            icon=folium.Icon(color="blue", icon="users-rectangle", prefix="fa"),
        ).add_to(tz_map)

    rows = list(
        df_coordinates.query(
            "location_type=='facility' and country=='tanzania'"
        ).iterrows()
    )
    for index, row in rows:
        location = [row["lat"], row["lon"]]
        folium.Marker(
            location=location,
            popup=row["name"],
            icon=folium.Icon(color="red", icon="square-h", prefix="fa"),
        ).add_to(tz_map)
        folium.Circle(
            location=location,
            radius=5000,  # 5 km in meters
            color="gray",
            fill=True,
            fill_opacity=0.1,
        ).add_to(tz_map)
    return tz_map


def get_ug_map() -> folium.Map:
    df_coordinates = pd.DataFrame(data=map_data)
    ug_map = folium.Map(location=[0.4044, 32.4594], zoom_start=11)

    rows = list(
        df_coordinates.query(
            "location_type=='community' and country=='uganda'"
        ).iterrows()
    )
    for index, row in rows:
        folium.Marker(
            radius=5,
            location=[row["lat"], row["lon"]],
            popup=f'{row["name"]} [{row["facility"]}]',
            icon=folium.Icon(color="blue", icon="square-plus", prefix="fa"),
        ).add_to(ug_map)

    rows = list(
        df_coordinates.query(
            "location_type=='facility' and country=='uganda'"
        ).iterrows()
    )
    for index, row in rows:
        location = [row["lat"], row["lon"]]
        folium.Circle(
            location=location,
            radius=5000,  # 5 km in meters
            color="gray",
            fill=True,
            fill_opacity=0.1,
        ).add_to(ug_map)
        folium.Marker(
            radius=8,
            location=location,
            popup=row["name"],
            icon=folium.Icon(color="red", icon="square-h", prefix="fa"),
        ).add_to(ug_map)
    return ug_map


def export_maps(folder: Path) -> None:
    get_tz_map().save(folder / "intecomm_tz_map.html")
    get_ug_map().save(folder / "intecomm_ug_map.html")
