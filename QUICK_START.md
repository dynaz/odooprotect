# PyProtect Quick Start Guide

## ✅ Fixed and Ready to Use!

PyProtect has been updated to correctly handle Odoo modules. The synchronization issue between NameCollector and Obfuscator has been resolved.

## Basic Usage

### Protect a Module

```bash
cd /odoo18
python3 PyProtect/pyprotect.py -i /path/to/your/module -o /path/to/output
```

### Example: Protect dtr_jasper

```bash
cd /odoo18
python3 PyProtect/pyprotect.py -i /odoo18/custom/SCR-18/dtr_jasper.backup -o /odoo18/custom/SCR-18/dtr_jasper
```

### With Machine Binding

```bash
python3 PyProtect/pyprotect.py -i /path/to/module -o /path/to/output -b -e 365
```

Options:
- `-b` or `--bind-machine`: Bind to current machine
- `-e 365` or `--expiration 365`: License expires in 365 days

## What Gets Preserved

PyProtect now preserves these method patterns (won't obfuscate):

| Pattern | Example | Why Preserved |
|---------|---------|---------------|
| `get_*` | `get_parameters()` | Public API, can be overridden |
| `set_*` | `set_value()` | Public API, can be overridden |
| `show_*` | `show_report()` | Wizard/UI methods |
| `process_*` | `process_jasper_file()` | Business logic |
| `action_*` | `action_confirm()` | Called from XML |
| `button_*` | `button_approve()` | Called from XML |
| `_compute_*` | `_compute_total()` | Computed fields |
| `_onchange_*` | `_onchange_partner()` | Onchange methods |

**Plus:** All Odoo reserved methods (`create`, `write`, `search`, etc.)

## Current Status

✅ **dtr_jasper** - Fixed and working
  - Methods `get_parameters()`, `get_locale()`, `show_report()` are preserved
  - Backward compatibility with **kwargs added
  - Method calls fixed to use non-obfuscated names

## Verify Protection Works

Test a report after protection:

```bash
# Start Odoo
cd /odoo18/odoo18-server
./odoo-bin -c /path/to/config

# In Odoo:
# 1. Create a sales order
# 2. Print the quotation
# 3. Should work without errors
```

## Check License Status

```bash
python3 PyProtect/pyprotect.py -c /path/to/protected/module
```

## Get Machine ID

```bash
python3 PyProtect/pyprotect.py -m
```

## Troubleshooting

### Error: "object has no attribute '_fn_XX'"

**Cause:** Method pattern not in preserved list

**Fix:** Check `/odoo18/PyProtect/FIXES.md` for details

### Error: "got an unexpected keyword argument"

**Cause:** Parameter names were obfuscated but caller uses keyword args

**Fix:** Already fixed in `dtr_jasper/models/jasper_report.py` with **kwargs

## Files You Can Safely Protect

✅ All Odoo addon modules
✅ Custom business logic
✅ Transient models (wizards)
✅ Reports and controllers

⚠️ **Do NOT obfuscate:**
- `__manifest__.py` (automatically skipped)
- `__openerp__.py` (automatically skipped)

## Need Help?

See `/odoo18/PyProtect/FIXES.md` for detailed technical information.

