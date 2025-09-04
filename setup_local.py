#!/usr/bin/env python3
import os
import subprocess
import sys

# ---- Defaults (override with environment variables if needed) ----
DEFAULT_BENCH_DIR = os.getenv("BENCH_DIR", os.getcwd())
DEFAULT_VENV_PATH = os.getenv("VENV_PATH", "~/.venv/cenv/bin/activate")
DEFAULT_SITE_NAME = os.getenv("SITE_NAME", "msite.local")

# Toggles: "1" to enable, anything else disables
ENABLE_DEVELOPER_MODE = os.getenv("ENABLE_DEVELOPER_MODE", "1")
ENABLE_SERVER_SCRIPTS = os.getenv("ENABLE_SERVER_SCRIPTS", "1")

# Admin credentials (use env vars in CI/secrets)
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "admin_key")
ADMIN_API_SECRET = os.getenv("ADMIN_API_SECRET", "admin_secret")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

# CORS: MODE one of: all | custom | disable
CORS_MODE = os.getenv("CORS_MODE", "all")
# Used only when CORS_MODE == "custom"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "https://example.com,https://app.example.com")

# ------------------------------------------------------------------

def run_command(command, cwd=None, env=None):
    """Run shell commands and stream output (non-interactive)."""
    process = subprocess.Popen(
        command,
        cwd=cwd,
        env=env,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        executable="/bin/bash"
    )
    for line in process.stdout:
        print(line, end="")
    process.wait()
    if process.returncode != 0:
        sys.exit(process.returncode)

def enable_developer_mode(activate_cmd, bench_dir):
    run_command(f"{activate_cmd} && bench set-config developer_mode 1", cwd=bench_dir)
    print("✅ Developer mode enabled")

def enable_server_scripts(activate_cmd, bench_dir):
    run_command(f"{activate_cmd} && bench set-config server_script_enabled true", cwd=bench_dir)
    print("✅ Server scripts enabled")

def set_admin_api_keys(activate_cmd, bench_dir, site_name, api_key, api_secret):
    api_cmd = f"""{activate_cmd} && bench --site {site_name} execute "exec(\\"import frappe; \
frappe.connect(); \
user=frappe.get_doc('User','Administrator'); \
user.api_key='{api_key}'; \
user.api_secret='{api_secret}'; \
user.save(ignore_permissions=True); \
frappe.db.commit(); \
print('✅ API credentials set for Administrator')\\")"
"""
    run_command(api_cmd, cwd=bench_dir)

def update_admin_password(activate_cmd, bench_dir, site_name, new_password):
    password_cmd = f"""{activate_cmd} && bench --site {site_name} execute "exec(\\"import frappe; \
frappe.connect(); \
from frappe.utils import password as _password; \
_password.update_password('Administrator', '{new_password}'); \
frappe.db.commit(); \
print('✅ Password updated for Administrator')\\")"
"""
    run_command(password_cmd, cwd=bench_dir)

def set_cors(activate_cmd, bench_dir, mode, origins):
    mode = (mode or "").lower().strip()
    if mode == "all":
        run_command(f"{activate_cmd} && bench set-config allow_cors '*'", cwd=bench_dir)
        print("✅ CORS set to allow all origins")
    elif mode == "custom":
        run_command(f"{activate_cmd} && bench set-config allow_cors '{origins}'", cwd=bench_dir)
        print(f"✅ CORS set to: {origins}")
    elif mode == "disable":
        run_command(f"{activate_cmd} && bench set-config -r allow_cors", cwd=bench_dir)
        print("✅ CORS disabled")
    else:
        print("⚠️ Unknown CORS_MODE; skipping CORS configuration")

def main():
    bench_dir = DEFAULT_BENCH_DIR
    venv_path = DEFAULT_VENV_PATH
    site_name = DEFAULT_SITE_NAME

    activate_cmd = f"source {os.path.expanduser(venv_path)}"

    if ENABLE_DEVELOPER_MODE == "1":
        enable_developer_mode(activate_cmd, bench_dir)

    if ENABLE_SERVER_SCRIPTS == "1":
        enable_server_scripts(activate_cmd, bench_dir)

    set_admin_api_keys(
        activate_cmd, bench_dir, site_name, ADMIN_API_KEY, ADMIN_API_SECRET
    )

    update_admin_password(
        activate_cmd, bench_dir, site_name, ADMIN_PASSWORD
    )

    set_cors(activate_cmd, bench_dir, CORS_MODE, CORS_ORIGINS)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted by user.")
        sys.exit(130)
