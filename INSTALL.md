# Installation Guide for DeepWiki CLI

This guide covers installing and configuring `deepwiki` across different environments and shells.

## Quick Install with Windows PowerShell (Recommended)

```powershell
.\install.ps1
```

This script:
- Configures `PYTHONIOENCODING=utf-8` at the user level (persistent across sessions)
- Sets it for the current session (works immediately)
- Installs deepwiki via `uv tool`
- Verifies the installation

---

## Quick Install with `uv` (Alternative)

```bash
uv tool install git+https://github.com/davidw-philips/deepwiki
```

### Updating DeepWiki

To update to the latest version (which overwrites any previous installation):

```bash
uv tool install git+https://github.com/davidw-philips/deepwiki --force
```

The `--force` flag ensures the tool is reinstalled even if already present, guaranteeing you have the latest fixes, features, and improvements.

### After Installation

#### For End Users
After installation completes, you have two options:

**Option 1: Update Shell Profile (Recommended)**
```bash
uv tool update-shell
```
Then restart your terminal or editor for the changes to take effect.

**Option 2: Manual PATH Update**
Add `~/.local/bin` (or the equivalent for your OS) to your system PATH environment variable.

#### For Agents (Copilot, Claude, etc.)
If you're installing deepwiki as an agent within an editor, the tool is immediately available for the current session by running:

```powershell
# Windows PowerShell
$env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"
```

```bash
# macOS/Linux bash/zsh
export PATH="$HOME/.local/bin:$PATH"
```

This temporary PATH addition allows the agent to use `deepwiki` commands immediately without waiting for shell restart. The user can then run `uv tool update-shell` for permanent installation, which takes effect after terminal restart.

## Alternative Installation Methods

### `uvx` (No Installation)
Use without installing—the tool runs in a temporary environment:
```bash
uvx --from git+https://github.com/davidw-philips/deepwiki deepwiki --help
```

### `pipx` or `pip`
```bash
pipx install git+https://github.com/davidw-philips/deepwiki.git
pip install git+https://github.com/davidw-philips/deepwiki.git
```

After installation with `pipx` or `pip`, the command should be available immediately. If not, ensure the installation directory (typically `~/.local/bin` on Linux/macOS or `%APPDATA%\Python\Scripts` on Windows) is on your PATH.

### Local Clone
```bash
git clone https://github.com/davidw-philips/deepwiki.git
cd deepwiki
pip install -e .
```

## Troubleshooting

### Command Not Found After Installation
1. Verify the installation location:
   ```bash
   uv tool list
   ```
   Look for `deepwiki` in the output.

2. Check your PATH:
   ```bash
   # Windows
   $env:PATH -split ';'
   
   # macOS/Linux
   echo $PATH | tr ':' '\n'
   ```

3. Add the directory to PATH:
   - **Windows:** Update System Environment Variables → PATH
   - **macOS/Linux:** Add to `~/.bashrc`, `~/.zshrc`, or `~/.profile` (depending on your shell)

4. Restart your terminal or editor.

### PATH Issues on Windows
Windows uses `;` as a PATH separator, while Unix uses `:`. The installation directory is typically:
```
C:\Users\{username}\.local\bin
```

To add this to PATH in Windows:
1. Press `Win + X` and select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", click "New"
5. Variable name: `PATH`
6. Variable value: `C:\Users\{username}\.local\bin`
7. Click OK and restart your terminal

Or from PowerShell (run as Administrator):
```powershell
[Environment]::SetEnvironmentVariable(
    "PATH",
    "$([Environment]::GetEnvironmentVariable('PATH', 'User'));$env:USERPROFILE\.local\bin",
    "User"
)
```

## Verifying Installation

Test that `deepwiki` is working:

```bash
deepwiki --help
```

You should see output listing available DeepWiki tools.

## Updating DeepWiki (Important)

To update deepwiki to the latest version with bug fixes and improvements:

```bash
# Update with --force to override existing installation
uv tool install git+https://github.com/davidw-philips/deepwiki --force
```

**Always use `--force`** when updating to ensure:
- ✅ Latest bug fixes are applied
- ✅ New features are installed
- ✅ Previous version is completely replaced
- ✅ No conflicts from partial updates

## Using DeepWiki with Agents

If deepwiki is installed in an editor-integrated agent context (Copilot, Claude, etc.), agents can immediately use the tool by temporarily adding it to PATH as shown above. After the user runs `uv tool update-shell`, subsequent terminal sessions will have permanent access to the command without any additional setup.
