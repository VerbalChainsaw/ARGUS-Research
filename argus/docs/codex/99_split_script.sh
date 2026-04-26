
## 10. Split script — desktop-side conversion to repo structure

When you're ready to convert this single Codex into the multi-file repo structure, save the script below as `split_codex.sh`, place it in the same directory as `ARGUS_CODEX.md`, run `bash split_codex.sh`, and commit the resulting `codex/` directory to GitHub.

```bash
#!/usr/bin/env bash
# split_codex.sh — extract ARGUS_CODEX.md into the multi-file repo structure
#
# Usage: bash split_codex.sh [path-to-ARGUS_CODEX.md]
#        Defaults to ./ARGUS_CODEX.md if no argument given.
#
# Produces a codex/ directory tree per the manifest in Section 1 of the Codex.
# Portable across Linux (gawk) and macOS (BSD awk) — uses pure bash + sed.

set -euo pipefail

CODEX="${1:-ARGUS_CODEX.md}"

if [[ ! -f "$CODEX" ]]; then
  echo "ERROR: $CODEX not found" >&2
  exit 1
fi

current_file=""
while IFS= read -r line; do
  if [[ "$line" =~ \<!--\ FILE:\ ([^[:space:]]+)\ --\> ]]; then
    current_file="${BASH_REMATCH[1]}"
    mkdir -p "$(dirname "$current_file")"
    : > "$current_file"   # truncate or create empty
    continue
  fi
  if [[ "$line" =~ \<!--\ END\ FILE\ --\> ]]; then
    current_file=""
    continue
  fi
  if [[ -n "$current_file" ]]; then
    printf '%s\n' "$line" >> "$current_file"
  fi
done < "$CODEX"

echo "Split complete. Generated tree:"
find codex -type f | sort
```

**To make the result a proper Git repo:**

```bash
cd codex
git init
git add .
git commit -m "Initial Codex import from ARGUS_CODEX.md v1.0"
# Then create the GitHub repo and push:
# git remote add origin git@github.com:VerbalChainsaw/argus-codex.git
# git branch -M main
# git push -u origin main
```

**Recommended .gitignore:**
```
.DS_Store
*.swp
__pycache__/
.venv/
node_modules/
build/
dist/
*.egg-info/
```

