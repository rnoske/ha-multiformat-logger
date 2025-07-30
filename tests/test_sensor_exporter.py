from pathlib import Path

import pandas as pd

from multiformat_logger.src import sensor_exporter
from multiformat_logger.src.sensor_exporter import export


def test_export_creates_csv(tmp_path: Path, monkeypatch):
    def fake_get_states(base_url: str, token: str):
        return [
            {"entity_id": "sensor.temperature"},
            {"entity_id": "sensor.humidity"},
            {"entity_id": "light.kitchen"},
        ]

    def fake_get_history(base_url: str, token: str, entity_id: str):
        if entity_id == "sensor.temperature":
            return [
                {"timestamp": "2023-01-01T00:00:00Z", "value": 20},
                {"timestamp": "2023-01-01T01:00:00Z", "value": 21},
            ]
        elif entity_id == "sensor.humidity":
            return [
                {"timestamp": "2023-01-01T00:30:00Z", "value": 50},
                {"timestamp": "2023-01-01T01:00:00Z", "value": 55},
            ]
        return []

    monkeypatch.setattr(sensor_exporter, "get_states", fake_get_states)
    monkeypatch.setattr(sensor_exporter, "get_history", fake_get_history)

    output_csv = tmp_path / "out.csv"
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        f"ha_url: http://localhost\napi_token: token\noutput_csv: {output_csv}\n"
    )

    df = export(config_path=config_file)

    assert output_csv.exists()
    csv_df = pd.read_csv(output_csv)
    # DataFrame should have same rows as returned df
    assert len(csv_df) == len(df)
    assert "sensor.temperature" in csv_df.columns
    assert "sensor.humidity" in csv_df.columns
