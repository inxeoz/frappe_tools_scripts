Nice catch 👍 — let’s add **password management** to the cheatsheet. Here’s the **updated full cheatsheet** for your `digipass.site`:

---

# 🚀 Bench Developer Cheatsheet (`digipass.site`)

## 🔑 API Keys / Secrets

```bash
# Set Administrator API Key + Secret
bench --site digipass.site execute frappe.db.set_value --kwargs \
'{"doctype":"User","name":"Administrator","values":{"api_key":"myapikey","api_secret":"myapisecret"}}'

# Commit changes (required after set_value)
bench --site digipass.site execute frappe.db.commit

# Verify inside Python console
bench --site digipass.site console
>>> frappe.db.get_value("User", "Administrator", ["api_key", "api_secret"])
```

---

## 👤 Password Management

```bash
# Set Administrator password
bench --site digipass.site set-admin-password 'newpassword'

# Set any user’s password
bench --site digipass.site execute frappe.utils.password.set_user_password --args '["user@example.com", "newpassword"]'

# (Alternative way) Update password directly in console
bench --site digipass.site console
>>> from frappe.utils.password import set_user_password
>>> set_user_password("user@example.com", "newpassword")
```

---

## 🧑‍💻 Developer Mode

```bash
# Enable developer mode
bench --site digipass.site set-config developer_mode 1

# Disable developer mode
bench --site digipass.site set-config developer_mode 0
```

---

## 📜 Server Scripts

```bash
# Enable server scripts
bench --site digipass.site set-config server_script_enabled true

# Disable server scripts
bench --site digipass.site set-config server_script_enabled false
```

---

## 🌍 CORS

```bash
# Allow all origins
bench --site digipass.site set-config allow_cors '*'

# Allow specific domains
bench --site digipass.site set-config allow_cors '["https://example.com","https://app.example.com"]'

# Disable CORS (remove key)
bench --site digipass.site set-config -r allow_cors
```

---

## ⚡ Scheduler

```bash
bench --site digipass.site set-config enable_scheduler 1   # enable
bench --site digipass.site set-config enable_scheduler 0   # disable
```

---

## 📧 Email Queue

```bash
bench --site digipass.site set-config email_queue_enabled 1   # enable
bench --site digipass.site set-config email_queue_enabled 0   # disable
```

---

## 🛠 Site Config / Maintenance

```bash
# Show site config
bench --site digipass.site show-config

# Enter/exit maintenance mode
bench --site digipass.site set-maintenance-mode on
bench --site digipass.site set-maintenance-mode off
```

---

## 📊 Debugging / Dev Work

```bash
bench --site digipass.site list-apps         # list installed apps
bench --site digipass.site migrate           # run migrations/patches
bench --site digipass.site clear-cache       # clear cache
bench --site digipass.site clear-website-cache
bench --site digipass.site reload-doc myapp doctype MyDocType
bench --site digipass.site build             # build assets (css/js)
bench --site digipass.site console           # open python console with frappe context
bench --site digipass.site execute myapp.module.method --kwargs '{"param":"value"}'
```

---

## 🔄 Scheduler & Jobs

```bash
bench --site digipass.site trigger-scheduler   # run all scheduled jobs now
bench --site digipass.site enable-scheduler
bench --site digipass.site disable-scheduler
bench --site digipass.site purge-jobs          # clear stuck jobs
```

---

## 🧪 Testing

```bash
bench --site digipass.site run-tests                   # run all tests
bench --site digipass.site run-tests --app myapp       # app tests only
bench --site digipass.site run-tests --doctype "My DocType"
```

---

## 🗄 Backup & Restore

```bash
bench --site digipass.site backup
bench --site digipass.site restore path/to/backup.sql.gz
```

---

✅ **Rule of Thumb:**

* Use `set-config` for site toggles.
* Use `execute frappe.db.set_value` for DB fields.
* Use `set-admin-password` or `frappe.utils.password.set_user_password` for credentials.
* Always `clear-cache` or restart after config changes.

---

👉 Do you want me to create a **single `dev_setup.sh` script** that applies:

* `developer_mode=1`
* `server_script_enabled=true`
* `allow_cors='*'`
* set admin API key/secret
* set admin password

all in **one run**?
