# Home Assistant Multiformat Logger Add-on

Dieses Repository enthält ein Beispiel für ein pythonbasiertes Add-on für Home Assistant OS. Es stellt einen einfachen Logger bereit, der Meldungen in unterschiedlichen Log-Leveln ausgeben kann.

## Ordnerstruktur

- `multiformat_logger/` – Add-on Quelle
  - `config.json` – Metadaten für Home Assistant
  - `Dockerfile` – Docker Build Datei
  - `requirements.txt` – Python Abhängigkeiten
  - `run.sh` – Einstiegspunkt für den Container
  - `src/` – Python Source Code des Add-ons
- `tests/` – pytest-basierte Tests

## Tests

Die Tests basieren auf `pytest`. Beispielhafte Tests befinden sich im Verzeichnis `tests/` und können mit folgendem Befehl ausgeführt werden:

```bash
pytest
```

Für eine vollautomatische Ausführung kann eine CI‑Umgebung (z. B. GitHub Actions) verwendet werden.
