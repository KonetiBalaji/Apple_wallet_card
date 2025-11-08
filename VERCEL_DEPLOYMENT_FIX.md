# Vercel Deployment Fix: FUNCTION_INVOCATION_FAILED

## 🔍 Root Cause Analysis

### What Was Happening vs. What Was Needed

**What the code was doing:**
- Using relative paths like `"output"` and `"assets/user"`
- Trying to write files to project root directories
- Assuming filesystem permissions like local development

**What it needed to do:**
- Use absolute paths that work in serverless
- Write to `/tmp` directory (only writable location in Vercel)
- Detect serverless environment and adapt accordingly

### Why This Error Occurred

**Vercel Serverless Environment Constraints:**
1. **Read-only filesystem**: Project root is read-only
2. **Ephemeral storage**: Files don't persist between invocations
3. **Limited write locations**: Only `/tmp` is writable
4. **Different working directory**: Current directory may not be project root

**The specific trigger:**
- Flask app tried to create `output/` directory in project root
- Vercel's filesystem is read-only → **Permission denied**
- Function crashed with `FUNCTION_INVOCATION_FAILED`

### The Misconception

**Wrong mental model:**
- "Serverless = same as local development"
- "Can write anywhere like on my machine"
- "Relative paths work the same way"

**Correct mental model:**
- Serverless = isolated, read-only environment
- Only `/tmp` is writable
- Must use absolute paths and environment detection
- Files are ephemeral (lost after function ends)

## 🛠️ The Fix

### Changes Made

1. **Environment Detection**
   ```python
   if os.environ.get("VERCEL"):
       # Use /tmp for writable files
       OUTPUT_FOLDER = Path("/tmp") / "output"
   else:
       # Local development
       OUTPUT_FOLDER = PROJECT_ROOT / "output"
   ```

2. **Absolute Paths Everywhere**
   - All file operations use absolute `Path` objects
   - No relative paths that depend on working directory

3. **Error Handling**
   - Added try/catch with detailed traceback
   - Shows actual error instead of generic 500

## 📚 Understanding Serverless Functions

### Why This Error Exists

**Security & Isolation:**
- Prevents functions from modifying codebase
- Ensures reproducible deployments
- Protects against malicious code

**Resource Management:**
- Limits disk usage
- Prevents storage bloat
- Enforces ephemeral storage model

### Correct Mental Model

**Serverless Function Lifecycle:**
1. Function starts → Fresh environment
2. Code executes → Can read project files, write to `/tmp`
3. Function ends → Environment destroyed
4. Next invocation → Fresh start again

**File Storage Strategy:**
- **Temporary files**: Use `/tmp` (ephemeral)
- **Persistent files**: Use external storage (S3, Vercel Blob, etc.)
- **Generated files**: Stream to client or external storage

## ⚠️ Warning Signs

### What to Look For

1. **Relative paths in serverless code**
   ```python
   # ❌ Bad
   Path("output/file.txt")
   
   # ✅ Good
   Path("/tmp/output/file.txt")  # Vercel
   Path(project_root / "output/file.txt")  # Local
   ```

2. **File writes outside `/tmp`**
   ```python
   # ❌ Bad
   with open("data.json", "w") as f:
       f.write(data)
   
   # ✅ Good
   with open("/tmp/data.json", "w") as f:
       f.write(data)
   ```

3. **No environment detection**
   ```python
   # ❌ Bad
   output_dir = "output"
   
   # ✅ Good
   output_dir = "/tmp/output" if os.environ.get("VERCEL") else "output"
   ```

### Code Smells

- Hardcoded relative paths
- No environment variable checks
- File operations without error handling
- Assuming filesystem permissions

## 🔄 Alternative Approaches

### Option 1: Use `/tmp` (Current Fix)
**Pros:**
- Simple and works immediately
- No external dependencies
- Good for temporary files

**Cons:**
- Files lost after function ends
- Not suitable for persistent storage
- Limited to 512MB on Vercel

### Option 2: Vercel Blob Storage
**Pros:**
- Persistent storage
- Integrated with Vercel
- Good for generated files

**Cons:**
- Requires additional setup
- API calls needed
- More complex

### Option 3: External Storage (S3, etc.)
**Pros:**
- Fully persistent
- Scalable
- Industry standard

**Cons:**
- Requires account setup
- Additional costs
- More complex integration

### Option 4: Stream Files Directly
**Pros:**
- No storage needed
- Immediate delivery
- Simple for downloads

**Cons:**
- Can't cache files
- Must regenerate each time
- Higher compute usage

## 🎯 Best Practices

1. **Always detect environment**
   ```python
   is_vercel = os.environ.get("VERCEL")
   ```

2. **Use absolute paths**
   ```python
   path = Path("/tmp/file.txt") if is_vercel else Path("file.txt")
   ```

3. **Handle errors gracefully**
   ```python
   try:
       # File operation
   except PermissionError:
       # Fallback or error message
   ```

4. **Document serverless constraints**
   - Note which features need external storage
   - Explain ephemeral nature of `/tmp`
   - Provide alternatives for persistence

## ✅ Current Solution

The fix uses `/tmp` for Vercel deployments, which:
- ✅ Works immediately
- ✅ No external dependencies
- ✅ Files available during function execution
- ⚠️ Files lost after function ends (expected for serverless)

For persistent storage, consider Vercel Blob Storage or S3.

