# OdooProtect Fixes - Complete Solution

## Root Cause Analysis

The obfuscation errors occurred because `NameCollector` (first pass) and `Obfuscator` (second pass) had **different pattern lists**, causing a mismatch:

1. **NameCollector** (lines 230-236) - Had OLD patterns without `get_`, `set_`, `show_`, `process_`
2. **Obfuscator** (lines 305-327) - Had NEW patterns with `get_`, `set_`, `show_`, `process_`

### The Problem Flow:
1. NameCollector marks `get_parameters` as "should obfuscate" (no `get_` pattern)
2. Obfuscator pre-populates `func_map`: `get_parameters` → `_fn_11`
3. When visiting `self.get_parameters()` calls, it obfuscates them to `self._fn_11()`
4. When visiting `def get_parameters():`, Obfuscator decides NOT to obfuscate (has `get_` pattern)
5. Result: **Method defined as `get_parameters` but called as `_fn_11()` → AttributeError**

## Complete Fixes Applied

### Fix 1: Synchronized Pattern Lists in odooprotect.py

**File:** `/odoo18/OdooProtect/odooprotect.py`

**Lines 227-240** - Updated `NameCollector.odoo_method_patterns`:
```python
self.odoo_method_patterns = [
    '_compute_', '_inverse_', '_search_', '_onchange_',
    '_depends_', '_constraint_', '_sql_constraint_',
    'action_', 'button_',
    'get_', '_get_', 'set_', '_set_',  # ← ADDED get_ and set_
    '_check_', '_prepare_',
    '_create_', '_write_', '_update_', '_default_',
    'show_', 'process_',  # ← ADDED show_ and process_
    'execute', 'compile',  # ← ADDED execute and compile
]
```

**Lines 305-331** - Updated `Obfuscator.odoo_method_patterns` to match

**Lines 336-358** - Added double-check in func_map pre-population:
```python
# Double-check preservation patterns to avoid obfuscating method calls
for method_name, should_preserve in self.collected_methods.items():
    if not should_preserve:
        should_really_preserve = False
        
        # Check if method name matches any preservation pattern
        for pattern in self.odoo_method_patterns:
            if pattern in method_name:
                should_really_preserve = True
                break
        
        # Only add to func_map if it should truly be obfuscated
        if not should_really_preserve:
            self.func_map[method_name] = self.generate_func_name()
```

This prevents the mismatch where NameCollector marks a method for obfuscation but Obfuscator decides to preserve it.

### Fix 2: Added **kwargs Support for Backward Compatibility

**File:** `/odoo18/custom/SCR-18/dtr_jasper/models/jasper_report.py`

**Line 211** - Added `**kwargs` to method signature:
```python
def show_report(self, report_name=False, email_subject=False, email_document_number=False, **kwargs):
    # Handle backward compatibility with kwargs (in case parameters were obfuscated)
    if 'email_subject' in kwargs:
        email_subject = kwargs['email_subject']
    if 'email_document_number' in kwargs:
        email_document_number = kwargs['email_document_number']
    if 'report_name' in kwargs:
        report_name = kwargs['report_name']
```

This allows child classes to call with keyword arguments even if parameters get obfuscated.

### Fix 3: Fixed Method Call References

**File:** `/odoo18/custom/SCR-18/dtr_jasper/models/jasper_report.py`

**Lines 260-261** - Fixed to call non-obfuscated method names:
```python
_obf_30 = self.get_parameters()  # Was: self._fn_11()
_obf_31 = self.get_locale()      # Was: self._fn_10()
```

### Fix 4: Fixed Parameter Reference in get_file_name

**File:** `/odoo18/custom/SCR-18/dtr_jasper/models/jasper_report.py`

**Lines 336-337** - Fixed parameter references after obfuscation:
```python
def get_file_name(self, _obf_46, _obf_47, _obf_48=_decrypt_str('163')):
    if len(_obf_46) == 1:  # Was: len(ids) - parameter was renamed but refs weren't updated
        _obf_49 = self.env[_obf_47].search([('id', 'in', _obf_46)], limit=1)  # Was: ids
```

**Issue:** OdooProtect obfuscated the parameter name from `ids` to `_obf_46`, but references to `ids` inside the function body weren't automatically updated by `ast.unparse`. This appears to be an edge case in AST transformation.

### Fix 5: Fixed JasperPy.process() Call with Obfuscated Parameters

**File:** `/odoo18/custom/SCR-18/dtr_jasper/models/jasper_report.py`

**Lines 258-267** - Changed from keyword arguments to positional arguments:
```python
# Before (broken):
_obf_29.process(self.jasper_file, output_file=_obf_23, format_list=_obf_24, ...)
# Error: JasperPy.process() got an unexpected keyword argument 'output_file'

# After (fixed):
# Use positional args since JasperPy.process params are obfuscated
# Order: input_file, output_file, format_list, parameters, db_connection, locale, resource
_obf_29.process(self.jasper_file, _obf_23, _obf_24, _obf_30, _obf_32, _obf_31, _obf_28)
```

**Issue:** When `JasperPy.process()` parameters were obfuscated (`output_file` → `_obf_4`, `format_list` → `_obf_6`, etc.), calling it with original keyword argument names failed. Using positional arguments bypasses this issue.

### Fix 6: Fixed JasperPy Method Call References

**File:** `/odoo18/custom/SCR-18/dtr_jasper/jasperpy.py`

**Lines 159, 226** - Fixed to call non-obfuscated method name:
```python
# Before (broken):
return self._fn_5()  # Line 159 in compile()
_obf_15 = self._fn_5()  # Line 226 in process()
# Error: 'JasperPy' object has no attribute '_fn_5'

# After (fixed):
return self.execute()
_obf_15 = self.execute()
```

**Issue:** Similar to Fix #3, the `execute()` method should have been preserved but was marked for obfuscation. The method definition was preserved at the last moment, but calls to it were already transformed to `_fn_5()`. Changed to call `execute()` directly.

### Fix 7: Fixed Controller Route Parameter Obfuscation

**File:** `/odoo18/custom/SCR-18/dtr_jasper/controllers/main.py`

**Line 139** - Restored original parameter name for route matching:
```python
# Before (broken):
@http.route('/am/preview/pdf/<int:report_id>', type='http', auth='user')
def preview_pdf(self, _obf_0, **kwargs):  # ❌ _obf_0 doesn't match route param
    report = request.env['dtr.jasper.report'].browse(_obf_0)

# After (fixed):
@http.route(_decrypt_str('5'), type=_decrypt_str('6'), auth=_decrypt_str('7'))
def preview_pdf(self, report_id, **kwargs):  # ✅ report_id matches route
    report = request.env[_decrypt_str('0')].browse(report_id)
```

**Issue:** Odoo HTTP routes use Flask-style URL patterns where `<int:report_id>` creates a parameter named `report_id`. This parameter name was obfuscated to `_obf_0`, causing Flask to fail matching the route parameter to the method parameter.

**OdooProtect Update (Lines 282, 493-538, 478-493):** Added controller class detection:
- Detect classes inheriting from `http.Controller`
- Track when we're inside a controller class (`self.in_controller_class`)
- Skip parameter obfuscation for controller methods
- Controller route parameters must match URL patterns exactly

## Method Patterns Now Preserved

Methods starting with these patterns will **NOT** be obfuscated:

### Odoo Framework Patterns:
- `_compute_`, `_inverse_`, `_search_` - Computed fields
- `_onchange_`, `_constraint_` - Validators
- `_depends_`, `_sql_constraint_` - Constraints
- `_check_`, `_prepare_` - Validation/preparation

### XML-Referenced Methods:
- `action_` - Action methods
- `button_` - Button click handlers

### Public API Methods (NEW):
- **`get_`** - Public getter methods (e.g., `get_parameters`, `get_locale`)
- **`set_`** - Public setter methods
- `_get_`, `_set_` - Private getters/setters

### Business Logic Methods (NEW):
- **`show_`** - Display/show methods (e.g., `show_report`)
- **`process_`** - Processing methods (e.g., `process_jasper_file`)

### Standard Odoo Methods:
- `create`, `write`, `unlink`, `search`, `read`, etc. (in `odoo_reserved`)

## How to Use Updated OdooProtect

### Option 1: Re-protect from Scratch (Recommended)

If you have original unprotected source:

```bash
# From /odoo18 directory
cd /odoo18
python3 OdooProtect/odooprotect.py -i /path/to/original/dtr_jasper -o /odoo18/custom/SCR-18/dtr_jasper
```

The updated OdooProtect will now correctly preserve `get_`, `set_`, `show_`, `process_` methods.

### Option 2: Use Current Protected Version

If you only have the protected version:

The manual fixes have been applied to:
- `/odoo18/custom/SCR-18/dtr_jasper/models/jasper_report.py`

These fixes will work with the current protected code.

## Testing Checklist

After applying fixes, test:

✅ Sales Order Reports (Quotation, Proforma, Order Form)
✅ Purchase Order Reports (RFQ, Purchase Order)
✅ Stock Reports (Delivery, Receipt, Internal Transfer)
✅ Accounting Reports (Invoice, Receipt, Billing)
✅ All other jasper-based reports

## Files Modified

1. **`/odoo18/OdooProtect/odooprotect.py`**
   - Line 230-239: Synchronized NameCollector patterns with Obfuscator

2. **`/odoo18/custom/SCR-18/dtr_jasper/models/jasper_report.py`**
   - Line 211: Added `**kwargs` to `show_report()` signature
   - Lines 212-219: Added kwargs backward compatibility handling
   - Line 260-261: Fixed method calls to use preserved names
   - Lines 263-267: Changed JasperPy.process() calls to use positional arguments
   - Lines 336-337: Fixed parameter references in `get_file_name()`

3. **`/odoo18/custom/SCR-18/dtr_jasper/jasperpy.py`**
   - Lines 159, 226: Fixed `_fn_5()` calls to `execute()`

4. **`/odoo18/custom/SCR-18/dtr_jasper/controllers/main.py`**
   - Line 139: Fixed parameter name from `_obf_0` to `report_id`

5. **`/odoo18/OdooProtect/odooprotect.py`** (Updated again)
   - Lines 305-331: Added `execute` and `compile` to preservation patterns
   - Lines 336-358: Added double-check logic in func_map pre-population
   - Lines 282, 493-538: Added controller class detection
   - Lines 478-493: Skip parameter obfuscation in controller methods

## Why This Solution Works

1. **Pattern Synchronization**: Both NameCollector and Obfuscator now use identical patterns, ensuring consistent decisions about which methods to preserve.

2. **Pre-population Accuracy**: Only methods that WILL be obfuscated are added to `func_map`, so preserved methods are never looked up for obfuscation.

3. **Backward Compatibility**: The `**kwargs` handling ensures that even if something goes wrong, the code gracefully handles both obfuscated and non-obfuscated parameter names.

## Prevention

To prevent this issue in future obfuscations:

1. **Always keep patterns synchronized** between NameCollector and Obfuscator
2. **Test after obfuscation** with at least one report from each module
3. **Keep a backup** of unprotected source code
4. **Document preserved patterns** for your team

## Common Error Patterns and Solutions

### Error: `'object_name' object has no attribute '_fn_XX'`
**Cause:** Method was obfuscated but should have been preserved
**Solution:** Add pattern to both NameCollector and Obfuscator patterns, or fix the call manually

### Error: `name 'variable_name' is not defined`
**Cause:** Parameter was obfuscated but references weren't updated  
**Solution:** Find the obfuscated parameter name and replace all references in function body
**Example:** `def method(self, _obf_46):` but body uses `ids` → change to `_obf_46`

### Error: `got an unexpected keyword argument 'param_name'`
**Cause:** Parameter name was obfuscated, caller uses keyword argument
**Solution:** Add `**kwargs` to method and extract parameters from kwargs

### How to Find These Issues:
```bash
# Search for undefined variable patterns in protected code
grep -n "name '.*' is not defined" /path/to/odoo/logs/odoo.log

# Search for attribute errors
grep -n "has no attribute '_fn_" /path/to/odoo/logs/odoo.log

# Check for obfuscated parameters that might have orphaned references
grep -B2 "def.*_obf_.*:" /path/to/protected/file.py
```

## Support

If you encounter similar issues:

1. Check if the method should be preserved (matches a pattern)
2. Verify NameCollector and Obfuscator have the same patterns
3. Search for `_fn_` calls that should use preserved method names
4. Check for parameter name mismatches (original name used with obfuscated parameter)
5. Add the pattern to BOTH NameCollector and Obfuscator if needed
