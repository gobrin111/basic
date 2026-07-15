# AV Operations Streamlit Demo

A small Streamlit application that combines two mock spreadsheet data sources in
one interface and applies role-based access control (RBAC).

## Included files

- `data/equipment.csv` — mock Spreadsheet A: AV Equipment Inventory
- `data/shifts.csv` — mock Spreadsheet B: Staff Shift Schedules
- `app.py` — Streamlit UI, login, RBAC, and JSON device-command simulation
- `test_app.py` — small tests for login roles and JSON payload generation

## Run the app

From this directory:

```bash
python -m venv .venv
```

Activate the environment on macOS/Linux:

```bash
source .venv/bin/activate
```

Or on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Then install and run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Test the roles

| Role | Username | Password | Access |
|---|---|---|---|
| Technician | `tech` | `tech123` | View both spreadsheets only |
| Manager | `manager` | `manager123` | View both spreadsheets and trigger commands |

These credentials are intentionally hard-coded for a prototype. A production app
should use an identity provider and store secrets outside source control.

## Trigger a device command

1. Sign in as `manager` / `manager123`.
2. In **Device Control**, select a device and command.
3. Click **Trigger Device Command**.
4. The valid JSON payload appears directly below the button. For example:

```json
{"command": "power_on", "device": "projector_1"}
```

The demo only displays the payload; it does not contact a real AV device. When
signed in as the technician, the entire command form is hidden and only a
view-only notice is shown.

## Optional checks

```bash
python -m pytest -q
```
