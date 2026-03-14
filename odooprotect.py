#!/usr/bin/env python3
"""
Simple Python Obfuscator with Machine ID Binding - Proof of Concept
==================================================================

This demonstrates Python code obfuscation with hardware binding.
NOT suitable for production use - just educational.

Features:
- Variable name obfuscation
- String encryption
- Machine ID binding
- License key verification
- Hardware fingerprinting
- Anti-tampering measures
"""

import ast
import base64
import hashlib
import os
import sys
import platform
import uuid
import subprocess
import time
import shutil
from pathlib import Path

def get_default_output_path():
    """Get the default output path in OdooProtect/dist directory"""
    # Resolve symlinks to get the actual script path
    actual_script_path = Path(__file__).resolve()
    script_dir = actual_script_path.parent.absolute()
    return script_dir / "dist"

def create_backup(output_path):
    """Create a backup of existing output before overwriting"""
    if output_path.exists():
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_name = f"{output_path.name}_backup_{timestamp}"

        if output_path.is_dir():
            backup_path = output_path.parent / backup_name
            try:
                shutil.copytree(str(output_path), str(backup_path))
                print(f"📦 Created backup: {backup_path}")
            except Exception as e:
                print(f"⚠️  Warning: Could not create directory backup: {e}")
        else:
            backup_path = output_path.parent / backup_name
            try:
                shutil.copy2(str(output_path), str(backup_path))
                print(f"📦 Created backup: {backup_path}")
            except Exception as e:
                print(f"⚠️  Warning: Could not create file backup: {e}")

def get_machine_id():
    """Generate a unique machine identifier based on hardware"""
    components = []

    try:
        # CPU info
        cpu_info = platform.processor()
        if cpu_info:
            components.append(f"cpu:{cpu_info}")
    except:
        pass

    try:
        # Machine name
        machine = platform.machine()
        if machine:
            components.append(f"arch:{machine}")
    except:
        pass

    try:
        # MAC address
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                       for elements in range(0, 2*6, 2)][::-1])
        components.append(f"mac:{mac}")
    except:
        pass

    try:
        # Disk serial (Linux)
        result = subprocess.run(['lsblk', '-o', 'SERIAL', '-n', '-d'],
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            disk_serial = result.stdout.strip().split('\n')[0]
            if disk_serial:
                components.append(f"disk:{disk_serial}")
    except:
        pass

    # Combine all components
    combined = '|'.join(components)

    # Generate consistent hash
    machine_id = hashlib.sha256(combined.encode()).hexdigest()[:32]

    return machine_id

def check_license_status(directory):
    """Check license status in the specified directory"""
    print("🔍 Checking License Status:")
    print("="*50)

    license_dir = Path(directory)

    if not license_dir.exists():
        print(f"❌ Directory not found: {directory}")
        return

    # Look for license files
    license_files = []
    license_files.extend(license_dir.glob("*.license"))
    license_files.extend(license_dir.glob("project.license"))

    if not license_files:
        print(f"❌ No license files found in: {directory}")
        print("Looked for: *.license, project.license")
        return

    print(f"Found {len(license_files)} license file(s):")
    current_machine_id = get_machine_id()

    for license_file in license_files:
        print(f"\n📄 License File: {license_file.name}")
        print("-" * 30)

        try:
            with open(license_file, 'r') as f:
                content = f.read().strip()

            lines = content.split('\n')
            license_info = {}

            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    license_info[key.strip()] = value.strip()

            # Extract license data
            machine_id = license_info.get('Machine ID', 'Unknown')
            license_key = license_info.get('License Key', 'Unknown')
            expires_str = license_info.get('Expires', 'Unknown')
            protected_date = license_info.get('Protected', 'Unknown')

            print(f"Machine ID: {machine_id}")
            print(f"License Key: {license_key}")
            print(f"Expires: {expires_str}")
            print(f"Protected: {protected_date}")

            # Validate license
            if license_key and license_key != 'Unknown':
                is_valid, message = verify_license_key(license_key)
                status = "✅ VALID" if is_valid else "❌ INVALID"
                print(f"Status: {status} - {message}")

                # Additional checks
                if machine_id == current_machine_id:
                    print("✅ Machine ID matches current machine")
                else:
                    print("⚠️  Machine ID does not match current machine")
                    print(f"   License Machine: {machine_id}")
                    print(f"   Current Machine: {current_machine_id}")

            else:
                print("❌ Invalid license key format")

        except Exception as e:
            print(f"❌ Error reading license file: {e}")

    print("\n" + "="*50)
    print("💡 Tip: Use 'python3 odooprotect.py -m' to see your current machine ID")

def generate_license_key(machine_id, expiration_days=365):
    """Generate a license key for the machine"""
    expiration = int(time.time()) + (expiration_days * 24 * 60 * 60)

    # Create license data
    license_data = f"{machine_id}:{expiration}"

    # Sign with a simple hash
    signature = hashlib.sha256(f"secret_salt:{license_data}".encode()).hexdigest()[:16]

    license_key = f"{license_data}:{signature}"

    return license_key, expiration

def verify_license_key(license_key):
    """Verify if license is valid for current machine"""
    try:
        parts = license_key.split(':')
        if len(parts) != 3:
            return False, "Invalid license format"

        machine_id = parts[0]
        expiration = int(parts[1])
        signature = parts[2]

        # Check expiration
        current_time = int(time.time())
        if current_time > expiration:
            return False, "License expired"

        # Verify signature
        expected_signature = hashlib.sha256(f"secret_salt:{machine_id}:{expiration}".encode()).hexdigest()[:16]
        if signature != expected_signature:
            return False, "Invalid license signature"

        # Check machine ID
        current_machine_id = get_machine_id()
        if machine_id != current_machine_id:
            return False, "License not valid for this machine"

        return True, "License valid"

    except Exception as e:
        return False, f"License verification error: {e}"

class NameCollector(ast.NodeVisitor):
    """Collect all Odoo field names and method names before obfuscation"""
    
    def __init__(self):
        self.field_names = set()
        self.method_names = {}  # Map method names to whether they should be obfuscated
        # IMPORTANT: Keep this list synchronized with Obfuscator.odoo_method_patterns
        self.odoo_method_patterns = [
            '_compute_', '_inverse_', '_search_', '_onchange_',
            '_depends_', '_constraint_', '_sql_constraint_',
            'action_', 'button_',
            'get_', '_get_', 'set_', '_set_',
            '_check_', '_prepare_',
            '_create_', '_write_', '_update_', '_default_',
            'show_', 'process_',
            'execute', 'compile',  # Added execute and compile
        ]
    
    def visit_Assign(self, node):
        """Detect Odoo field assignments"""
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Attribute):
                if isinstance(node.value.func.value, ast.Name):
                    if node.value.func.value.id == 'fields':
                        # This is an Odoo field assignment
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                self.field_names.add(target.id)
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        """Collect all function/method names"""
        # Check if this method matches Odoo patterns that should be preserved
        should_preserve = False
        for pattern in self.odoo_method_patterns:
            if pattern in node.name:
                should_preserve = True
                break
        
        self.method_names[node.name] = should_preserve
        self.generic_visit(node)


class Obfuscator(ast.NodeTransformer):
    """AST-based obfuscator with advanced complexity"""

    def __init__(self, odoo_field_names=None, collected_methods=None, preserve_public_api=True):
        self.var_count = 0
        self.func_count = 0
        self.class_count = 0
        self.var_map = {}
        self.func_map = {}
        self.class_map = {}
        self.strings = []
        self.preserve_public_api = preserve_public_api  # New flag to preserve public APIs
        self.module_level_depth = 0  # Track if we're at module level
        self.public_names = set()  # Track public function/class names
        self.in_public_class = False  # Track if we're inside a public class
        self.in_controller_class = False  # Track if we're inside a Controller class
        self.in_fstring = False  # Track if we're inside an f-string
        self.collected_methods = collected_methods or {}  # Pre-collected method names
        
        # Odoo-specific reserved attributes that must not be obfuscated
        self.odoo_reserved = {
            # Model definition attributes
            '_name', '_description', '_inherit', '_inherits', '_rec_name',
            '_order', '_sql_constraints', '_constraints', '_auto', '_table',
            '_table_query', '_sequence', '_parent_name', '_parent_store',
            '_date_name', '_fold_name', '_abstract', '_transient', '_log_access',
            '_check_company_auto',
            # Model lifecycle methods
            '_register_hook', '_setup_complete', '_constraint_methods',
            # Field-related attributes
            '_columns', '_defaults', '_rec_name', '_order',
            # Technical attributes
            'env', 'id', 'ids', '_context', '_cr', '_uid',
            # Common methods that shouldn't be obfuscated
            'create', 'write', 'unlink', 'search', 'browse', 'read',
            'search_read', 'name_get', 'name_search', 'name_create',
            'default_get', 'fields_get', 'fields_view_get',
            # API decorators - these are method names typically
            'api', 'models', 'fields', 'tools', '_',
        }
        
        # Odoo method name patterns that must be preserved
        # These are called from other modules or referenced by string
        self.odoo_method_patterns = [
            '_compute_',  # compute='_compute_field_name'
            '_inverse_',  # inverse='_inverse_field_name'
            '_search_',   # search='_search_field_name'
            '_onchange_', # onchange methods
            '_depends_',  # depends methods
            '_constraint_', # constraint methods
            '_sql_constraint_', # SQL constraints
            'action_',    # action methods (often called from XML)
            'button_',    # button methods (called from XML)
            'get_',       # getter methods (public API, can be overridden)
            '_get_',      # private getter methods (often part of public API)
            'set_',       # setter methods (public API, can be overridden)
            '_set_',      # private setter methods (often part of public API)
            '_check_',    # validation methods
            '_prepare_',  # preparation methods
            '_create_',   # creation helper methods
            '_write_',    # write helper methods
            '_update_',   # update helper methods
            '_default_',  # default value methods
            'show_',      # show methods (often used in wizards/transient models)
            'process_',   # process methods (common in business logic)
            'execute',    # execute methods (common for command execution)
            'compile',    # compile methods
        ]
        
        # Odoo field names collected from first pass
        self.odoo_field_names = odoo_field_names or set()
        
        # Pre-populate func_map with methods that will be obfuscated
        # This handles forward references (method A calls method B defined later)
        # IMPORTANT: Double-check preservation patterns to avoid obfuscating method calls
        for method_name, should_preserve in self.collected_methods.items():
            if not should_preserve:
                # Double-check against Obfuscator's patterns (may differ from NameCollector's old state)
                should_really_preserve = False
                
                # Check if method name matches any preservation pattern
                for pattern in self.odoo_method_patterns:
                    if pattern in method_name:
                        should_really_preserve = True
                        break
                
                # Check if it's in odoo_reserved
                if method_name in self.odoo_reserved:
                    should_really_preserve = True
                
                # Only add to func_map if it should truly be obfuscated
                if not should_really_preserve:
                    # This method will be obfuscated, pre-assign it an obfuscated name
                    self.func_map[method_name] = self.generate_func_name()

    def generate_var_name(self):
        """Generate obfuscated variable name"""
        name = f"_obf_{self.var_count}"
        self.var_count += 1
        return name

    def generate_func_name(self):
        """Generate obfuscated function name"""
        name = f"_fn_{self.func_count}"
        self.func_count += 1
        return name

    def generate_class_name(self):
        """Generate obfuscated class name"""
        name = f"_cls_{self.class_count}"
        self.class_count += 1
        return name

    def visit_Name(self, node):
        """Obfuscate variable names"""
        # Skip Odoo reserved attributes
        if node.id in self.odoo_reserved:
            return node
        
        # Skip Odoo field names
        if node.id in self.odoo_field_names:
            return node
        
        # Skip UPPERCASE_CONSTANTS (Python convention for public module-level constants)
        # These are often imported by other modules
        if node.id.isupper() and '_' in node.id:
            return node
            
        if isinstance(node.ctx, ast.Store):
            if node.id not in self.var_map:
                self.var_map[node.id] = self.generate_var_name()
            node.id = self.var_map[node.id]
        elif isinstance(node.ctx, ast.Load):
            if node.id in self.var_map:
                node.id = self.var_map[node.id]
            elif node.id in self.func_map:
                node.id = self.func_map[node.id]
            elif node.id in self.class_map:
                node.id = self.class_map[node.id]
        return node

    def visit_Attribute(self, node):
        """Obfuscate attribute access (including method calls)"""
        # Obfuscate attribute names if they are methods or known attributes
        if hasattr(node, 'attr'):
            # Check if this attribute is accessed via super()
            # super() calls should NEVER be obfuscated because they reference parent class methods
            is_super_call = False
            if isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Name) and node.value.func.id == 'super':
                    is_super_call = True
            
            if is_super_call:
                # Don't obfuscate super().method_name() calls
                pass
            # Skip Odoo reserved attributes
            elif node.attr in self.odoo_reserved:
                pass
            elif node.attr in self.func_map:
                node.attr = self.func_map[node.attr]
            # Don't obfuscate 'self' or other common attributes
            elif node.attr not in ['self', '__name__', '__file__', '__init__']:
                # For other attributes, we could obfuscate them too, but for now skip
                pass

        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        """Obfuscate function names (skip special methods and public API)"""
        should_obfuscate = True
        
        # Skip special methods like __init__, __str__, etc.
        if node.name.startswith('__') and node.name.endswith('__'):
            should_obfuscate = False
        
        # Skip Odoo reserved methods
        if node.name in self.odoo_reserved:
            should_obfuscate = False
        
        # NEW: Skip Odoo method patterns (compute, inverse, search, onchange, etc.)
        # These are referenced by string in field definitions and must keep their names
        for pattern in self.odoo_method_patterns:
            if pattern in node.name:
                should_obfuscate = False
                break
        
        # NEW: Skip public API functions at module level (don't start with _)
        # This preserves functions that can be imported: from module import function_name
        if self.preserve_public_api and self.module_level_depth == 0:
            if not node.name.startswith('_'):
                should_obfuscate = False
                self.public_names.add(node.name)
        
        # NEW: Also preserve public methods inside public classes
        # This allows code to call methods on imported classes
        if self.preserve_public_api and self.in_public_class:
            if not node.name.startswith('_'):
                should_obfuscate = False
        
        # Obfuscate the function name if needed
        if should_obfuscate:
            if node.name not in self.func_map:
                self.func_map[node.name] = self.generate_func_name()
            node.name = self.func_map[node.name]
        else:
            # If we decide NOT to obfuscate, remove from func_map if it was pre-populated
            # This prevents calls to this function from being obfuscated
            if node.name in self.func_map:
                del self.func_map[node.name]

        # Obfuscate argument names (skip 'self' and controller route params)
        # Controller route parameters must match the URL pattern and should not be obfuscated
        for arg in node.args.args:
            # Skip 'self'
            if arg.arg == 'self':
                continue
            
            # Skip parameters in controller methods (they're matched by URL routes)
            if self.in_controller_class:
                # Don't obfuscate parameters in controller methods
                continue
            
            # Obfuscate other parameters
            if arg.arg not in self.var_map:
                self.var_map[arg.arg] = self.generate_var_name()
            arg.arg = self.var_map.get(arg.arg, arg.arg)

        # Increase depth before visiting function body
        self.module_level_depth += 1
        # Recursively visit the function body
        self.generic_visit(node)
        # Decrease depth after visiting
        self.module_level_depth -= 1
        
        return node

    def visit_ClassDef(self, node):
        """Obfuscate class names (preserve public API classes)"""
        should_obfuscate = True
        is_public_class = False
        is_controller_class = False
        
        # Check if this is a Controller class (Odoo HTTP controllers)
        # Controllers need special handling - their route parameter names must not be obfuscated
        for base in node.bases:
            if isinstance(base, ast.Attribute):
                if base.attr == 'Controller':
                    is_controller_class = True
            elif isinstance(base, ast.Name):
                if 'Controller' in base.id:
                    is_controller_class = True
        
        # NEW: Skip public API classes at module level (don't start with _)
        # This preserves classes that can be imported: from module import ClassName
        if self.preserve_public_api and self.module_level_depth == 0:
            if not node.name.startswith('_'):
                should_obfuscate = False
                is_public_class = True
                self.public_names.add(node.name)
        
        # Obfuscate the class name if needed
        if should_obfuscate:
            if node.name not in self.class_map:
                self.class_map[node.name] = self.generate_class_name()
            node.name = self.class_map[node.name]

        # Track if we're in a public class or controller class
        old_in_public_class = self.in_public_class
        old_in_controller_class = self.in_controller_class
        if is_public_class:
            self.in_public_class = True
        if is_controller_class:
            self.in_controller_class = True
        
        # Increase depth before visiting class body
        self.module_level_depth += 1
        # Recursively visit the class body
        self.generic_visit(node)
        # Decrease depth after visiting
        self.module_level_depth -= 1
        
        # Restore the previous state
        self.in_public_class = old_in_public_class
        self.in_controller_class = old_in_controller_class
        
        return node

    def visit_Constant(self, node):
        """Encrypt string literals (skip if inside f-string)"""
        # Don't encrypt strings inside f-strings as it creates invalid AST
        if self.in_fstring:
            return node
            
        if isinstance(node.value, str) and len(node.value) > 3:  # Only encrypt longer strings
            # Skip encryption for strings that contain Python code or suspicious patterns
            # as these might be used with ast.literal_eval or cause parsing issues
            skip_keywords = ['import', 'def ', 'class ', 'if ', 'for ', 'while ', 'try ', 'with ', 'from ', 'lambda ', 'return ', 'yield ', 'raise ', 'break', 'continue', 'pass', 'assert ', 'global ', 'nonlocal ', 'except ', 'finally ', 'elif ', 'else:', ' and ', ' or ', ' not ', ' is ', ' in ', 'True', 'False', 'None']
            # Also skip strings that look like code (newlines, brackets, operators)
            suspicious_patterns = ['\n', '\t', '\r', '(', ')', '[', ']', '{', '}', '=', '+', '-', '*', '/', '//', '%', '==', '!=', '<', '>', '<=', '>=', '+=', '-=', '*=', '/=', '//=', '%=', '&', '|', '^', '~', '<<', '>>', '->', ':', ';', ',', '.']
            # Count suspicious characters
            suspicious_count = sum(1 for pattern in suspicious_patterns if pattern in node.value)
            has_keywords = any(keyword in node.value for keyword in skip_keywords)
            has_many_suspicious = suspicious_count > 5  # More than 5 suspicious chars
            has_newlines = '\n' in node.value or '\r' in node.value or '\t' in node.value
            is_very_long = len(node.value) > 200  # Very long strings might be code

            if has_keywords or has_many_suspicious or has_newlines or is_very_long:
                return node  # Don't encrypt, keep original string

            # Use a format that clearly indicates this is encrypted data
            encrypted = f"__ENCRYPTED__{base64.b64encode(node.value.encode()).decode()}__ENCRYPTED__"
            self.strings.append(encrypted)
            # Replace with decryption call
            return ast.Call(
                func=ast.Name(id='_decrypt_str', ctx=ast.Load()),
                args=[ast.Constant(value=str(len(self.strings)-1))],
                keywords=[]
            )
        return node

    def visit_BinOp(self, node):
        """Obfuscate binary operations by making them more complex"""
        # For simple additions, make them more complex
        if isinstance(node.op, ast.Add) and isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
            if isinstance(node.left.value, (int, float)) and isinstance(node.right.value, (int, float)):
                # Convert x + y to (x * 2 + y * 2) // 2 or similar
                new_left = ast.BinOp(
                    left=ast.BinOp(left=node.left, op=ast.Mult(), right=ast.Constant(value=2)),
                    op=ast.Add(),
                    right=ast.BinOp(left=node.right, op=ast.Mult(), right=ast.Constant(value=2))
                )
                new_node = ast.BinOp(
                    left=new_left,
                    op=ast.FloorDiv(),
                    right=ast.Constant(value=2)
                )
                return new_node

        self.generic_visit(node)
        return node


    def visit_JoinedStr(self, node):
        """Handle f-strings - obfuscate variable names but don't encrypt literals"""
        # Mark that we're inside an f-string to prevent string encryption
        old_in_fstring = self.in_fstring
        self.in_fstring = True
        
        # Visit the expressions inside the f-string to obfuscate variable names
        # This ensures that f'{variable}' uses the obfuscated variable name
        self.generic_visit(node)
        
        # Restore the previous state
        self.in_fstring = old_in_fstring
        return node
    
    def visit_ListComp(self, node):
        """Handle list comprehensions - obfuscate loop variables"""
        return self._visit_comprehension(node)
    
    def visit_DictComp(self, node):
        """Handle dict comprehensions - obfuscate loop variables"""
        return self._visit_comprehension(node)
    
    def visit_SetComp(self, node):
        """Handle set comprehensions - obfuscate loop variables"""
        return self._visit_comprehension(node)
    
    def visit_GeneratorExp(self, node):
        """Handle generator expressions - obfuscate loop variables"""
        return self._visit_comprehension(node)
    
    def _visit_comprehension(self, node):
        """Common logic for all comprehension types"""
        # Save current var_map state
        saved_var_map = self.var_map.copy()
        
        # First, process the generators to establish loop variable mappings
        for generator in node.generators:
            # Visit the target (loop variable) - this adds it to var_map
            if isinstance(generator.target, ast.Name):
                if generator.target.id not in self.var_map:
                    self.var_map[generator.target.id] = self.generate_var_name()
                generator.target.id = self.var_map[generator.target.id]
            else:
                # Handle tuple unpacking in comprehensions: for (a, b) in items
                self.visit(generator.target)
            
            # Visit the iterator (what we're looping over)
            generator.iter = self.visit(generator.iter)
            
            # Visit any filter conditions
            generator.ifs = [self.visit(condition) for condition in generator.ifs]
        
        # Now visit the element/key/value expressions with the loop variables in var_map
        if isinstance(node, ast.DictComp):
            node.key = self.visit(node.key)
            node.value = self.visit(node.value)
        elif isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
            node.elt = self.visit(node.elt)
        
        # Restore var_map (comprehension variables are local to the comprehension)
        # But keep the changes for any outer-scope variables that were referenced
        self.var_map = saved_var_map
        
        return node

def generate_runtime(machine_id=None, license_key=None):
    """Generate runtime decryption and license verification functions"""
    license_check = ""
    if license_key:
        license_check = f'''
# License verification
_LICENSE_KEY = "{license_key}"

def _get_machine_id():
    """Generate machine identifier"""
    import hashlib
    import platform
    import uuid
    import subprocess

    components = []
    try:
        cpu_info = platform.processor()
        if cpu_info:
            components.append(f"cpu:{{cpu_info}}")
    except:
        pass

    try:
        machine = platform.machine()
        if machine:
            components.append(f"arch:{{machine}}")
    except:
        pass

    try:
        mac = ':'.join(['{{:02x}}'.format((uuid.getnode() >> elements) & 0xff)
                       for elements in range(0, 2*6, 2)][::-1])
        components.append(f"mac:{{mac}}")
    except:
        pass

    try:
        result = subprocess.run(['lsblk', '-o', 'SERIAL', '-n', '-d'],
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            disk_serial = result.stdout.strip().split('\\n')[0]
            if disk_serial:
                components.append(f"disk:{{disk_serial}}")
    except:
        pass

    combined = '|'.join(components)
    machine_id = hashlib.sha256(combined.encode()).hexdigest()[:32]
    return machine_id

def _verify_license_key(license_key):
    """Verify license validity"""
    import hashlib
    import time

    try:
        parts = license_key.split(':')
        if len(parts) != 3:
            return False

        machine_id = parts[0]
        expiration = int(parts[1])
        signature = parts[2]

        current_time = int(time.time())
        if current_time > expiration:
            return False

        expected_signature = hashlib.sha256(f"secret_salt:{{machine_id}}:{{expiration}}".encode()).hexdigest()[:16]
        if signature != expected_signature:
            return False

        current_machine_id = _get_machine_id()
        if machine_id != current_machine_id:
            return False

        return True
    except:
        return False

def _check_license():
    """Verify license on startup"""
    if not _verify_license_key(_LICENSE_KEY):
        print("ERROR: Invalid or expired license!")
        print("This software is licensed to run on a different machine.")
        import sys
        sys.exit(1)

# Check license immediately
_check_license()
'''

    runtime_code = f'''
import ast

# Override ast.literal_eval IMMEDIATELY to handle encrypted strings gracefully
_original_literal_eval = ast.literal_eval

def _safe_literal_eval(node_or_string):
    """Safe version of ast.literal_eval that handles encrypted strings"""
    try:
        return _original_literal_eval(node_or_string)
    except (ValueError, SyntaxError) as e:
        # If literal_eval fails, check if it's due to encrypted strings
        if isinstance(node_or_string, str):
            # Try to detect if this might be a decrypted string that contains code
            if any(keyword in node_or_string for keyword in ['import ', 'def ', 'class ', 'if ', 'for ']):
                # This looks like Python code, not a literal. Return a safe default.
                # You might want to adjust this based on your use case.
                return None
        # Re-raise the original exception for other cases
        raise e

# Replace the original function immediately
ast.literal_eval = _safe_literal_eval

import base64
import sys

_STRINGS = []  # Will be populated by obfuscator

def _decrypt_str(index):
    """Decrypt string at given index"""
    encrypted = _STRINGS[int(index)]
    # Handle the new encrypted format
    if encrypted.startswith('__ENCRYPTED__') and encrypted.endswith('__ENCRYPTED__'):
        encrypted = encrypted[13:-13]  # Remove the markers
    try:
        return base64.b64decode(encrypted).decode()
    except Exception:
        # If decryption fails, return empty string to prevent crashes
        return ""

{license_check}
# Obfuscated code will be inserted here
'''

    return runtime_code

def obfuscate_directory(input_dir, output_dir, bind_machine=False, expiration_days=365, preserve_api=True):
    """Obfuscate all Python files in a directory recursively"""
    print(f"🔍 Scanning directory: {input_dir}")
    print(f"📁 Output directory: {output_dir}")
    print()

    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        print(f"❌ Input directory not found: {input_dir}")
        return False

    if not input_path.is_dir():
        print(f"❌ Input path is not a directory: {input_dir}")
        return False

    # Create backup if output already exists
    create_backup(output_path)

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all files (not just Python files)
    all_files = []
    for root, dirs, files in os.walk(input_path):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if not d.startswith('__pycache__')]
        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(input_path)
            all_files.append((file_path, rel_path))

    if not all_files:
        print("❌ No files found in the directory")
        return False

    # Separate Python and non-Python files
    python_files = [(fp, rp) for fp, rp in all_files if fp.suffix == '.py']
    non_python_files = [(fp, rp) for fp, rp in all_files if fp.suffix != '.py']

    print(f"📋 Found {len(all_files)} total files:")
    print(f"   • {len(python_files)} Python files to obfuscate")
    print(f"   • {len(non_python_files)} other files to copy")
    if python_files:
        print("   📝 Python files:")
        for _, rel_path in python_files:
            print(f"      • {rel_path}")
    if non_python_files:
        print("   📄 Other files:")
        for _, rel_path in non_python_files:
            print(f"      • {rel_path}")
    print()

    # Generate machine ID and license once for the whole project
    machine_id = None
    license_key = None

    if bind_machine:
        print("🔒 Generating machine binding license for project...")
        machine_id = get_machine_id()
        license_key, expiration = generate_license_key(machine_id, expiration_days)

        print(f"📋 Machine ID: {machine_id}")
        print(f"🔑 License Key: {license_key}")
        print(f"⏰ Expires: {time.ctime(expiration)}")
        print()

        # Save license info
        license_file = output_path / "project.license"
        with open(license_file, 'w') as f:
            f.write(f"Machine ID: {machine_id}\n")
            f.write(f"License Key: {license_key}\n")
            f.write(f"Expires: {time.ctime(expiration)}\n")
            f.write(f"Protected: {time.ctime(time.time())}\n")
        print(f"💾 Project license saved to: {license_file}")
        print()

    # Process all files
    processed_files = []
    copied_files = []

    # Process Python files (obfuscate)
    for file_path, rel_path in python_files:
        output_file = output_path / rel_path

        # Create output subdirectory if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)

        print(f"🔧 Obfuscating: {rel_path}")

        try:
            # Use the same machine_id and license_key for all files in the project
            success = obfuscate_file_single(file_path, output_file, machine_id, license_key, preserve_api)
            if success:
                processed_files.append(rel_path)
                print(f"   ✅ {rel_path}")
            else:
                print(f"   ❌ Failed: {rel_path}")
        except Exception as e:
            print(f"   ❌ Error: {rel_path} - {e}")

    # Process non-Python files (copy as-is)
    for file_path, rel_path in non_python_files:
        output_file = output_path / rel_path

        # Create output subdirectory if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)

        print(f"📄 Copying: {rel_path}")

        try:
            shutil.copy2(file_path, output_file)
            copied_files.append(rel_path)
            print(f"   ✅ {rel_path}")
        except Exception as e:
            print(f"   ❌ Error: {rel_path} - {e}")

    print()
    print(f"🎉 Directory processing complete!")
    print(f"   📊 Python files obfuscated: {len(processed_files)}/{len(python_files)}")
    print(f"   📄 Other files copied: {len(copied_files)}/{len(non_python_files)}")
    print(f"   📦 Total files processed: {len(processed_files) + len(copied_files)}/{len(all_files)}")

    if bind_machine:
        print(f"   🔒 Machine binding: ENABLED (ID: {machine_id[:16]}...)")
        print(f"   ⏰ License expires: {time.ctime(expiration)}")
    else:
        print(f"   🔓 Machine binding: DISABLED")

    return True

def obfuscate_file_single(input_file, output_file, machine_id=None, license_key=None, preserve_api=True):
    """Obfuscate a single file with pre-computed license info"""
    try:
        # Read source
        with open(input_file, 'r', encoding='utf-8') as f:
            source = f.read()

        # Check if this is a manifest file (Odoo loads these with ast.literal_eval)
        input_path = Path(input_file)
        is_manifest = input_path.name == '__manifest__.py' or input_path.name == '__openerp__.py'

        # For manifest files, skip obfuscation entirely as Odoo uses ast.literal_eval to load them
        if is_manifest:
            # Copy manifest files as-is without obfuscation
            output_code = source
        else:
            # Parse AST
            tree = ast.parse(source, filename=str(input_file))

            # First pass: collect Odoo field names and method names
            collector = NameCollector()
            collector.visit(tree)
            
            # Second pass: apply obfuscation with collected names
            # preserve_public_api ensures public functions/classes can be imported
            obfuscator = Obfuscator(
                odoo_field_names=collector.field_names,
                collected_methods=collector.method_names,
                preserve_public_api=preserve_api
            )
            obfuscated_tree = obfuscator.visit(tree)
            # Generate runtime code with strings and license
            strings_repr = repr(obfuscator.strings)
            runtime_code = generate_runtime(machine_id, license_key)

            # Replace the placeholder in runtime code
            runtime_code = runtime_code.replace('_STRINGS = []', f'_STRINGS = {strings_repr}')

            # Convert AST back to source
            try:
                # Use ast.unparse if available (Python 3.9+)
                obfuscated_source = ast.unparse(obfuscated_tree)
                output_code = runtime_code.replace('# Obfuscated code will be inserted here', obfuscated_source)
            except AttributeError:
                # Fallback for older Python versions
                output_code = runtime_code.replace('# Obfuscated code will be inserted here',
                                                 "# Obfuscated AST (requires Python 3.9+ for ast.unparse)\n" + source)

        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_code)

        return True

    except Exception as e:
        print(f"   Error obfuscating {input_file}: {e}")
        return False

def obfuscate_file(input_file, output_file, bind_machine=False, expiration_days=365, preserve_api=True):
    """Obfuscate a single Python file with optional machine binding"""
    output_path = Path(output_file)

    # Create backup if output already exists
    create_backup(output_path)

    print(f"Obfuscating {input_file} -> {output_file}")

    # Generate license if binding is requested
    machine_id = None
    license_key = None

    if bind_machine:
        print("🔒 Generating machine binding license...")
        machine_id = get_machine_id()
        license_key, expiration = generate_license_key(machine_id, expiration_days)

        print(f"📋 Machine ID: {machine_id}")
        print(f"🔑 License Key: {license_key}")
        print(f"⏰ Expires: {time.ctime(expiration)}")

        # Save license info
        license_file = output_file + '.license'
        with open(license_file, 'w') as f:
            f.write(f"Machine ID: {machine_id}\n")
            f.write(f"License Key: {license_key}\n")
            f.write(f"Expires: {time.ctime(expiration)}\n")
        print(f"💾 License saved to: {license_file}")

    # Check if this is a manifest file (Odoo loads these with ast.literal_eval)
    input_path = Path(input_file)
    is_manifest = input_path.name == '__manifest__.py' or input_path.name == '__openerp__.py'

    # Read source
    with open(input_file, 'r') as f:
        source = f.read()

    # For manifest files, skip obfuscation entirely as Odoo uses ast.literal_eval to load them
    if is_manifest:
        # Copy manifest files as-is without obfuscation
        output_code = source
    else:
        # Parse AST
        tree = ast.parse(source, filename=input_file)

        # First pass: collect Odoo field names and method names
        collector = NameCollector()
        collector.visit(tree)
        
        # Second pass: apply obfuscation with collected names
        # preserve_public_api ensures public functions/classes can be imported
        obfuscator = Obfuscator(
            odoo_field_names=collector.field_names,
            collected_methods=collector.method_names,
            preserve_public_api=preserve_api
        )
        obfuscated_tree = obfuscator.visit(tree)
        # Generate runtime code with strings and license
        strings_repr = repr(obfuscator.strings)
        runtime_code = generate_runtime(machine_id, license_key)

        # Replace the placeholder in runtime code
        runtime_code = runtime_code.replace('_STRINGS = []', f'_STRINGS = {strings_repr}')

        # Convert AST back to source using built-in ast.unparse (Python 3.9+)
        try:
            # Use ast.unparse if available (Python 3.9+)
            obfuscated_source = ast.unparse(obfuscated_tree)
            output_code = runtime_code.replace('# Obfuscated code will be inserted here', obfuscated_source)
        except Exception as e:
            # Fallback for any unparsing errors
            print(f"⚠️  AST unparsing failed ({e}), using fallback")
            output_code = runtime_code.replace('# Obfuscated code will be inserted here',
                                             "# Obfuscated AST (unparsing failed)\n" + source)

    # Ensure output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_code)

    # Print summary (handle manifest files which don't have obfuscator)
    if is_manifest:
        print(f"✅ Manifest file copied without obfuscation (Odoo compatibility)")
    else:
        print(f"✅ Obfuscated {len(obfuscator.var_map)} variables")
        print(f"✅ Encrypted {len(obfuscator.strings)} strings")
        if obfuscator.public_names:
            print(f"✅ Preserved {len(obfuscator.public_names)} public API names (importable)")
        if bind_machine:
            print(f"✅ Machine binding enabled (ID: {machine_id[:16]}...)")

def main():
    """CLI entry point for OdooProtect (odooprotect on PyPI)."""
    import argparse

    parser = argparse.ArgumentParser(description="OdooProtect - Python Obfuscator with Machine ID Binding")
    parser.add_argument("-i", "--input",
                       help="Input Python file or directory (not needed with -m)")
    parser.add_argument("-o", "--output", default=str(get_default_output_path()),
                       help="Output obfuscated file or directory (default: OdooProtect/dist/filename or OdooProtect/dist/inputname/)")
    parser.add_argument("-m", "--machine-id", action="store_true",
                       help="Display current machine ID and exit")
    parser.add_argument("-c", "--check-license", nargs='?', const=".",
                       help="Check license validity in directory (default: current dir)")
    parser.add_argument("-b", "--bind-machine", action="store_true",
                       help="Bind obfuscated code to current machine")
    parser.add_argument("-e", "--expiration", type=int, default=365,
                       help="License expiration in days (default: 365)")
    parser.add_argument("--no-preserve-api", action="store_true",
                       help="Obfuscate all names including public API (may break imports)")

    args = parser.parse_args()

    # Handle machine ID display
    if args.machine_id:
        machine_id = get_machine_id()
        print("🔍 Current Machine ID:")
        print("="*50)
        print(f"Machine ID: {machine_id}")
        print(f"Length: {len(machine_id)} characters")
        print()
        print("This ID will be used for machine binding.")
        print("Copy this ID if you need to manually configure licensing.")
        sys.exit(0)

    # Handle license checking
    if args.check_license:
        check_license_status(args.check_license)
        sys.exit(0)

    # Validate input is provided when not using machine-id flag
    if not args.input:
        print("❌ Error: Input file or directory is required (use -i flag)")
        print("Run 'python3 odooprotect.py --help' for usage information")
        sys.exit(1)

    input_path = Path(args.input)

    if not input_path.exists():
        print(f"❌ Input path not found: {args.input}")
        sys.exit(1)

    # Determine output path
    default_dist_path = get_default_output_path()
    resolved_output = Path(args.output).absolute()

    if input_path.is_dir():
        # Directory input -> always create input_dirname subdirectory
        output_path = resolved_output / input_path.name
    else:
        # File input -> create filename in output directory
        output_path = resolved_output / input_path.name

    try:
        # Determine if we should preserve public API (default: True, unless --no-preserve-api)
        preserve_api = not args.no_preserve_api
        
        if input_path.is_dir():
            # Directory mode
            print("🏗️  Directory obfuscation mode")
            print("="*50)
            if preserve_api:
                print("🔓 Public API preservation: ENABLED (Odoo/Framework compatible)")
            else:
                print("🔒 Public API preservation: DISABLED (Full obfuscation)")
            print()
            success = obfuscate_directory(
                str(input_path), str(output_path),
                bind_machine=args.bind_machine,
                expiration_days=args.expiration,
                preserve_api=preserve_api
            )

            if success:
                print("\n✅ Directory obfuscation complete!")
                if args.bind_machine:
                    print("\n⚠️  WARNING: All code is now bound to the current machine!")
                    print(f"   Only machines with Machine ID '{get_machine_id()[:16]}...' can run it.")
                    print(f"   License expires in {args.expiration} days.")
            else:
                print("\n❌ Directory obfuscation failed!")
                sys.exit(1)

        else:
            # Single file mode
            print("📄 Single file obfuscation mode")
            print("="*50)
            if preserve_api:
                print("🔓 Public API preservation: ENABLED (Odoo/Framework compatible)")
            else:
                print("🔒 Public API preservation: DISABLED (Full obfuscation)")
            print()
            obfuscate_file(str(input_path), str(output_path),
                          bind_machine=args.bind_machine,
                          expiration_days=args.expiration,
                          preserve_api=preserve_api)
            print(f"\n✅ File obfuscation complete: {output_path}")

            if args.bind_machine:
                print("\n⚠️  WARNING: This code is now bound to the current machine!")
                print(f"   Only machines with Machine ID '{get_machine_id()[:16]}...' can run it.")
                print(f"   License expires in {args.expiration} days.")

    except Exception as e:
        print(f"❌ Obfuscation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

