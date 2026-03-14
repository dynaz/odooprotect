# Publishing odooprotect to PyPI

This project is published on [PyPI](https://pypi.org/manage/projects/) under the name **odooprotect**.

## Prerequisites

1. **PyPI account**  
   Create one at [pypi.org/account/register](https://pypi.org/account/register/) if needed.

2. **API token (recommended)**  
   - Go to [pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)  
   - Create a new API token (scope: entire account or only project `odooprotect`)  
   - Save the token; you will use it as the password when uploading.

## Build and upload

From the project root (`C:\PyProtect`):

### 1. Install build tools

```powershell
pip install build twine
```

### 2. Build distributions

```powershell
python -m build
```

This creates `dist/odooprotect-1.0.0.tar.gz` (sdist) and `dist/odooprotect-1.0.0-py3-none-any.whl` (wheel).

### 3. Upload to PyPI

**Production (real PyPI):**

```powershell
python -m twine upload dist/*
```

When prompted:
- **Username:** `__token__`
- **Password:** your PyPI API token (paste the whole token, including the `pypi-` prefix)

**Test PyPI (optional, for testing first):**

```powershell
python -m twine upload --repository testpypi dist/*
```

Use credentials from [test.pypi.org](https://test.pypi.org/).

### 4. Install from PyPI

After a successful upload, anyone can install with:

```powershell
pip install odooprotect
```

Then run:

- `odooprotect --help`
- or `python -m pyprotect --help`

## Bumping the version

Before each new release:

1. Update `version` in `setup.py` (e.g. `"1.0.1"`).
2. Re-run `python -m build` and `python -m twine upload dist/*`.

## Troubleshooting

- **Invalid or non-existent password:** Use an API token with scope that includes this project (or entire account).
- **File already exists:** PyPI does not allow re-uploading the same version; bump the version in `setup.py` and rebuild.
- **README/LICENSE not in sdist:** Ensure `MANIFEST.in` lists them and run `python -m build` again.
