from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Any

import requests

import pandas as pd
import yaml


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yaml"


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """Load YAML configuration."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_states(base_url: str, token: str) -> List[Dict[str, Any]]:
    """Return all entity states from Home Assistant."""
    url = f"{base_url.rstrip('/')}/api/states"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_history(base_url: str, token: str, entity_id: str) -> List[Dict[str, Any]]:
    """Return history for a single entity."""
    url = f"{base_url.rstrip('/')}/api/history/period"
    params = {"filter_entity_id": entity_id}
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    result = resp.json()
    if not result:
        return []
    values = []
    for item in result[0]:
        value = item["state"]
        try:
            value = float(value)
        except ValueError:
            pass
        values.append({"timestamp": item["last_changed"], "value": value})
    return values


def load_sensor_data(base_url: str, token: str) -> Dict[str, List[Dict[str, Any]]]:
    """Retrieve data for all sensors from Home Assistant."""
    states = get_states(base_url, token)
    data: Dict[str, List[Dict[str, Any]]] = {}
    for state in states:
        entity_id = state.get("entity_id", "")
        if not entity_id.startswith("sensor."):
            continue
        history = get_history(base_url, token, entity_id)
        if history:
            data[entity_id] = history
    return data


def build_dataframe(data: Dict[str, List[Dict[str, Any]]]) -> pd.DataFrame:
    """Create dataframe with unified timestamp index from sensor data."""
    df: pd.DataFrame | None = None
    for name, entries in data.items():
        sensor_df = pd.DataFrame(entries)
        sensor_df["timestamp"] = pd.to_datetime(sensor_df["timestamp"], utc=True)
        sensor_df = sensor_df.rename(columns={"value": name})
        sensor_df = sensor_df[["timestamp", name]]
        if df is None:
            df = sensor_df
        else:
            df = pd.merge(df, sensor_df, on="timestamp", how="outer")
    assert df is not None
    df = df.sort_values("timestamp").set_index("timestamp")
    return df


def export(config_path: Path = DEFAULT_CONFIG_PATH) -> pd.DataFrame:
    """Export sensors defined in the configuration to CSV."""
    config = load_config(config_path)
    base_url = config["ha_url"]
    token = config["api_token"]
    output_path = Path(config["output_csv"])

    data = load_sensor_data(base_url, token)
    df = build_dataframe(data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path)
    return df


if __name__ == "__main__":
    export()
