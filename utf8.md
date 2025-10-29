# Python Subprocess UTF-8 Encoding Solutions

## Problem
The subprocess module in Python on Windows defaults to using code page 1252 (cp1252) instead of UTF-8, which can cause encoding issues when working with international characters or modern text.

## Root Cause
The `subprocess._text_encoding()` function (lines 367-384 in subprocess.py):
- Returns `"utf-8"` if `sys.flags.utf8_mode` is `True`
- Otherwise returns `locale.getencoding()` which gives "cp1252" on Windows

This encoding is used when `text=True` is specified but no explicit `encoding` parameter is provided.

## Solutions (Ranked from Best to Least Recommended)

### 1. Enable Python UTF-8 Mode (RECOMMENDED)
This is the cleanest solution - it makes Python use UTF-8 by default for all text operations.

#### Option A: Environment Variable (Persistent)
Set the environment variable system-wide:

**Windows Command Prompt:**
```cmd
setx PYTHONUTF8 1
```

**Windows PowerShell:**
```powershell
[System.Environment]::SetEnvironmentVariable('PYTHONUTF8', '1', 'User')
```

**Temporary (current session only):**
```cmd
set PYTHONUTF8=1  # CMD
```
```powershell
$env:PYTHONUTF8=1  # PowerShell
```

#### Option B: Python Command-Line Flag
```bash
python -X utf8 your_script.py
```

#### Option C: IDE Configuration
Configure your IDE (VS Code, PyCharm, etc.) to set the `PYTHONUTF8=1` environment variable for all Python runs.

### 2. Monkey-Patch locale.getencoding()
Override the locale module's encoding function early in your script:

```python
import locale
import functools

# Monkey-patch locale.getencoding to always return utf-8
locale.getencoding = functools.partial(lambda: 'utf-8')

# Now import and use subprocess
import subprocess
```

**Pros:**
- Simple one-time change
- Affects all subprocess calls automatically

**Cons:**
- Must be done before importing subprocess
- May affect other code that relies on locale.getencoding()

### 3. Monkey-Patch subprocess._text_encoding()
Override the subprocess module's internal encoding function:

```python
import subprocess

def _utf8_text_encoding():
    return 'utf-8'

subprocess._text_encoding = _utf8_text_encoding
```

**Pros:**
- Targeted to subprocess only
- Simple implementation

**Cons:**
- Relies on internal/private API (underscore prefix)
- May break in future Python versions

### 4. Wrapper Function for subprocess.run()
Create a wrapper that defaults to UTF-8:

```python
import subprocess
import functools

# Store original function
_original_run = subprocess.run

# Create wrapper with utf-8 default
def run_utf8(*args, **kwargs):
    if 'encoding' not in kwargs and 'text' not in kwargs:
        kwargs['encoding'] = 'utf-8'
    return _original_run(*args, **kwargs)

# Replace subprocess.run
subprocess.run = run_utf8
```

**Pros:**
- More control over behavior
- Can customize per use case

**Cons:**
- More complex
- Doesn't affect Popen directly
- Need separate wrappers for check_output, etc.

### 5. Create Custom Wrapper Functions
If you only have a few subprocess calls, create simple wrapper functions:

```python
import subprocess

def run_utf8(*args, **kwargs):
    kwargs.setdefault('encoding', 'utf-8')
    kwargs.setdefault('text', True)
    return subprocess.run(*args, **kwargs)

def check_output_utf8(*args, **kwargs):
    kwargs.setdefault('encoding', 'utf-8')
    kwargs.setdefault('text', True)
    return subprocess.check_output(*args, **kwargs)
```

**Pros:**
- Explicit and clear
- No monkey-patching

**Cons:**
- Must remember to use wrapper instead of original
- Need to update existing code

## Recommended Approach

**For most Windows development: Use Solution #1 (PYTHONUTF8=1 environment variable)**

This is the official, supported Python feature (PEP 540) and provides the most comprehensive solution:
- Affects all text I/O operations (not just subprocess)
- No code changes needed
- Works across all Python scripts
- Supported and documented by Python core team
- Prevents similar issues with file I/O, sys.stdout, etc.

**To set permanently on Windows:**
1. Open System Properties → Environment Variables
2. Add new User variable: `PYTHONUTF8` = `1`
3. Restart your terminal/IDE

**For quick testing:**
```cmd
set PYTHONUTF8=1
python your_script.py
```

## Verification

Test that UTF-8 is now the default:

```python
import subprocess
import sys

print(f"UTF-8 Mode: {sys.flags.utf8_mode}")
print(f"Default encoding: {subprocess._text_encoding()}")

# Test subprocess
result = subprocess.run(
    ['python', '-c', 'print("Hello UTF-8: 你好 🎉")'],
    capture_output=True,
    text=True  # Note: no encoding parameter needed!
)
print(result.stdout)
```

## References
- [PEP 540 - Add a new UTF-8 mode](https://www.python.org/dev/peps/pep-0540/)
- [Python subprocess documentation](https://docs.python.org/3/library/subprocess.html)
- subprocess.py location: `C:\Users\mike\miniconda3\Lib\subprocess.py:367-384`
