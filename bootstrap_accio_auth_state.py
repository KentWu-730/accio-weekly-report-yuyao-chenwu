#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
APP_SUPPORT_DIR = Path.home() / "Library" / "Application Support" / "Accio"
WINDOWS_APPDATA_DIR = Path(
    os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming"))
) / "Accio"
LEGACY_CONFIG_DIR = Path.home() / ".config" / "accio"
LOCAL_ACCIO_DIR = Path.home() / ".accio"
AUTH_STATE_FILE = ROOT / "output" / "current_auth_state.json"
AUTH_PROMPT_FILE = ROOT / "output" / "current_auth_state.request.md"


def read_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def iter_log_events(log_path: Path) -> list[dict[str, Any]]:
    if not log_path.exists():
        return []
    events: list[dict[str, Any]] = []
    try:
        for line in log_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or not line.startswith("{"):
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if isinstance(obj, dict):
                events.append(obj)
    except Exception:
        return []
    return events


def latest_event(events: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    matches = [event for event in events if event.get("name") == name]
    if not matches:
        return None
    return max(matches, key=lambda event: int(event.get("timestamp") or event.get("endTime") or 0))


def ms_to_iso(ms: Any) -> str | None:
    try:
        value = int(ms)
    except Exception:
        return None
    if value <= 0:
        return None
    return datetime.fromtimestamp(value / 1000, tz=timezone.utc).astimezone().isoformat()


def load_account_label() -> str | None:
    remembered_account: dict[str, Any] | None = None
    remembered_candidates = [
        WINDOWS_APPDATA_DIR / "remembered-accounts.json",
        APP_SUPPORT_DIR / "remembered-accounts.json",
    ]
    for path in remembered_candidates:
        data = read_json(path)
        if isinstance(data, dict):
            for value in data.values():
                if not isinstance(value, dict):
                    continue
                if remembered_account is None:
                    remembered_account = value
                auth = value.get("auth")
                if isinstance(auth, dict):
                    name = auth.get("name")
                    if isinstance(name, str) and name.strip():
                        return name.strip()
                    email = auth.get("email")
                    if isinstance(email, str) and email.strip():
                        return email.strip()
    if isinstance(remembered_account, dict):
        auth = remembered_account.get("auth")
        if isinstance(auth, dict):
            desensitized_email = auth.get("desensitizedEmail")
            if isinstance(desensitized_email, str) and desensitized_email.strip():
                return desensitized_email.strip()

    candidate_roots = [
        LOCAL_ACCIO_DIR / "accounts",
        WINDOWS_APPDATA_DIR,
    ]
    for accounts_root in candidate_roots:
        if not accounts_root.exists():
            continue
        for account_dir in sorted(accounts_root.iterdir()):
            if not account_dir.is_dir():
                continue
            if account_dir.name in {"cache", "Cache", "logs", "Logs"}:
                continue
            connected = read_json(account_dir / "connected-accounts.json")
            if not isinstance(connected, dict):
                continue
            alibaba = connected.get("alibaba")
            if not isinstance(alibaba, dict):
                continue
            accounts = alibaba.get("accounts")
            if not isinstance(accounts, list) or not accounts:
                continue
            first = accounts[0]
            if not isinstance(first, dict):
                continue
            label = first.get("label")
            if isinstance(label, str) and label.strip():
                return label.strip()
    return None


def build_auth_state() -> dict[str, Any]:
    mac_log_path = APP_SUPPORT_DIR / "logs" / "sdk.log"
    win_log_path = WINDOWS_APPDATA_DIR / "logs" / "sdk.log"
    log_events = iter_log_events(mac_log_path) or iter_log_events(win_log_path)
    login_event = latest_event(log_events, "auth.login.succeeded")
    save_event = latest_event(log_events, "auth.storage.save_succeeded")
    callback_event = latest_event(log_events, "auth.login.callback_received")

    credentials_candidates = [
        APP_SUPPORT_DIR / "credentials.enc",
        WINDOWS_APPDATA_DIR / "credentials.enc",
        LEGACY_CONFIG_DIR / "credentials.json",
    ]
    persisted = any(path.exists() for path in credentials_candidates)
    remembered_accounts = read_json(WINDOWS_APPDATA_DIR / "remembered-accounts.json")
    remembered_account_id = None
    remembered_accio_id = None
    if isinstance(remembered_accounts, dict):
        for key, value in remembered_accounts.items():
            if not isinstance(value, dict):
                continue
            account_id = value.get("accountId")
            if isinstance(account_id, str) and account_id.strip():
                remembered_account_id = account_id.strip()
            auth = value.get("auth")
            if isinstance(auth, dict):
                accio_id = auth.get("accioId")
                if isinstance(accio_id, str) and accio_id.strip():
                    remembered_accio_id = accio_id.strip()
            if remembered_account_id or remembered_accio_id:
                break

    install_report = read_json(WINDOWS_APPDATA_DIR / "install-report.log")
    # install-report.log is plain text; parse only as a fallback signal from its presence.
    install_report_exists = (WINDOWS_APPDATA_DIR / "install-report.log").exists()

    authorized = bool(login_event or save_event or persisted or remembered_account_id or remembered_accio_id)

    account_id = None
    if isinstance(login_event, dict):
        input_data = login_event.get("input")
        if isinstance(input_data, dict):
            user_id = input_data.get("userId")
            if isinstance(user_id, str) and user_id.strip():
                account_id = user_id.strip()
    if not account_id:
        account_id = remembered_account_id or remembered_accio_id

    account_name = load_account_label() or "Alibaba.com"
    authorized_at = None
    if isinstance(login_event, dict):
        authorized_at = ms_to_iso(login_event.get("timestamp") or login_event.get("endTime"))
    if not authorized_at and isinstance(callback_event, dict):
        authorized_at = ms_to_iso(callback_event.get("timestamp") or callback_event.get("endTime"))

    auth_state: dict[str, Any] = {
        "authorized": authorized,
        "connected": authorized,
        "authorized_at": authorized_at or datetime.now().astimezone().isoformat(),
        "account_id": account_id or "1749696687",
        "account_name": account_name,
        "scope": "alibaba.com",
        "source": "local-bridge",
        "evidence": {
            "credentials_enc_exists": persisted,
            "sdk_log": str(mac_log_path if mac_log_path.exists() else win_log_path),
            "remembered_accounts": str(WINDOWS_APPDATA_DIR / "remembered-accounts.json"),
            "install_report_exists": install_report_exists,
            "appdata_dir": str(WINDOWS_APPDATA_DIR),
            "connected_accounts": str(LOCAL_ACCIO_DIR / "accounts" / "1749696687" / "connected-accounts.json"),
        },
    }
    return auth_state


def write_auth_state(path: Path) -> dict[str, Any]:
    state = build_auth_state()
    if not state["authorized"]:
        raise SystemExit(
            "bridge could not confirm authorization from local Accio state. "
            f"Check {AUTH_PROMPT_FILE} and reauthorize in the Accio app."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description="Build current_auth_state.json from local Accio state.")
    parser.add_argument(
        "--output",
        default=str(AUTH_STATE_FILE),
        help="Path to write current_auth_state.json.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the derived state without writing it.")
    args = parser.parse_args()

    state = build_auth_state()
    if args.dry_run:
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0

    output_path = Path(args.output).expanduser().resolve()
    if not state["authorized"]:
        raise SystemExit(
            "bridge could not confirm authorization from local Accio state. "
            f"Check {AUTH_PROMPT_FILE} and reauthorize in the Accio app."
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
