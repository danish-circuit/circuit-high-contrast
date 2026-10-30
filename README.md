# Circuit High Contrast theme for vscode

Dark and light high-contrast color themes for VS Code, built on the Circuit design system palette (`frontend/packages/circuit-ui/src/styles/generated/tokens.css`). Forked from [danielhdzzz/vscode-ember-high-contrast](https://github.com/danielhdzzz/vscode-ember-high-contrast), itself based on [74th/vscode-monokaicharcoal](https://github.com/74th/vscode-monokaicharcoal).

## Themes

- **Circuit High Contrast Dark**: pure black background, Circuit `green-9` accent, syntax colors from the Circuit dark scales.
- **Circuit High Contrast Light**: pure white background, Circuit `green-10` / `green-8` accents, syntax colors from the Circuit light scales.

## Install

Search for **Circuit High Contrast** in the VS Code Extensions Marketplace, or install from the command line:

```bash
code --install-extension danish-circuit.circuit-high-contrast
```

### Install from .vsix

You can also package and install the theme manually:

```bash
npm install -g @vscode/vsce
vsce package
code --install-extension circuit-high-contrast-<version>.vsix
```

For VSCodium:

```bash
codium --install-extension circuit-high-contrast-<version>.vsix
```

## Development

1. Open this folder in VS Code and press **F5** — a second window opens with the theme loaded live.
2. Edit `generate_themes.py` (the `DARK` and `LIGHT` palettes, token colors, color template) and regenerate:
   ```bash
   python3 generate_themes.py
   ```
3. The dev host picks up color changes automatically. If it doesn't, run **Developer: Reload Window** (`Cmd+Shift+P`).

No packaging or installing needed — just edit and see. Do not edit the theme JSON files by hand.
