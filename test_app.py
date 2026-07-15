import json

from app import authenticate, build_control_payload


def test_authenticate_known_users():
    assert authenticate("tech", "tech123") == "Technician"
    assert authenticate("manager", "manager123") == "Manager"


def test_authenticate_rejects_bad_credentials():
    assert authenticate("manager", "wrong") is None
    assert authenticate("unknown", "tech123") is None


def test_control_payload_is_valid_json():
    payload = build_control_payload("power_on", "projector_1")
    assert payload == {"command": "power_on", "device": "projector_1"}
    assert json.loads(json.dumps(payload)) == payload
