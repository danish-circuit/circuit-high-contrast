#!/usr/bin/env python3
"""Generate the Circuit High Contrast dark and light theme JSON files from a single source of truth."""

import json
import os

# ---------------------------------------------------------------------------
# Color palettes
#
# Values come from the Circuit Design System tokens
# (frontend/packages/circuit-ui/src/styles/generated/tokens.css).
# ---------------------------------------------------------------------------

DARK = {
    "ui_theme":         "vs-dark",
    "fg":               "#FFFFFF",
    "bg":               "#000000",
    "transparent":      "#00000000",
    # Accent: text uses `accent`, borders/fills use `line` + alpha
    "accent":           "#1ce370",  # green-9
    "line":             "#1ce370",  # green-9
    "inactive_fg":      "#1ce37075",
    "hint":             "#7ce2fe",  # sky-9
    # Syntax
    "comment":          "#7d7d7d",  # gray-10
    "string":           "#fbb81b",  # amber-9
    "keyword":          "#eb605c",  # red-10
    "type":             "#7ce2fe",  # sky-9
    "number":           "#d398ff",  # purple-11
    "param":            "#ffa057",  # orange-11
    "function":         "#1ce370",  # green-9
    "json_string":      "#ededed",  # gray-12
    "diff_header":      "#a1a1a1",  # gray-11
    "muted":            "#7d7d7d",  # gray-10
    "invalid_fg":       "#FFFFFF",
    "invalid_bg":       "#e1292f",  # red-9
    "deprecated_bg":    "#a953f5",  # purple-9
    # Editor surfaces
    "caret":            "#FFFFFF",
    "invisibles":       "#3d3d3d",  # gray-7
    "line_highlight":   "#1d2520",  # green-2
    "selection":        "#11572e",  # green-6
    "selection_inactive": "#11572eA4",
    "selection_border": "#183826",  # green-4
    "find_highlight":   "#ffe29e",  # amber-11
    "indent_guide":     "#4f4f4f",  # gray-8
    "bracket":          "#ededed",  # gray-12
    "active_guide":     "#a66b0c",  # amber-7
    "link":             "#7eb8f1",  # blue-11
    "marker_bg":        "#1c1c1c",  # gray-2
    "marker_error":     "#72212c",  # red-6
    "marker_warning":   "#885903",  # amber-6
    "hover_surface":    "#1c1c1c",  # gray-2
    "debug":            "#7ce2fe",  # sky-9
    "diff_added":       "#18c15f55",  # green-8
    "diff_removed":     "#d1012370",  # red-8
    # Status
    "error":            "#eb605c",  # red-10
    "warning":          "#ffa057",  # orange-11
    "added":            "#1ce370",  # green-9
    "modified":         "#fbb81b",  # amber-9
    "renamed":          "#7ce2fe",  # sky-9
    "submodule":        "#d398ff",  # purple-11
    "conflict":         "#ffa057",  # orange-11
    "ignored":          "#7d7d7d",  # gray-10
    # Terminal
    "ansi_black":           "#7d7d7d",  # gray-10
    "ansi_bright_black":    "#a1a1a1",  # gray-11
    "ansi_red":             "#eb605c",  # red-10
    "ansi_bright_red":      "#fa9b94",  # red-11
    "ansi_green":           "#1ce370",  # green-9
    "ansi_bright_green":    "#9ff9c5",  # green-11
    "ansi_yellow":          "#fbb81b",  # amber-9
    "ansi_bright_yellow":   "#ffe29e",  # amber-11
    "ansi_blue":            "#489ff5",  # blue-10
    "ansi_bright_blue":     "#7eb8f1",  # blue-11
    "ansi_magenta":         "#b466fd",  # purple-10
    "ansi_bright_magenta":  "#d398ff",  # purple-11
    "ansi_cyan":            "#7ce2fe",  # sky-9
    "ansi_bright_cyan":     "#c2f3ff",  # sky-12
    "ansi_white":           "#ededed",  # gray-12
    "ansi_bright_white":    "#FFFFFF",
    # Alpha levels (0–255) applied to `line`
    "find_match_alpha":     200,
    "list_active_alpha":    156,
    "list_inactive_alpha":  96,
}

LIGHT = {
    "ui_theme":         "vs",
    "fg":               "#171717",  # gray-12
    "bg":               "#FFFFFF",
    "transparent":      "#FFFFFF00",
    "accent":           "#0f763a",  # green-10
    "line":             "#18c15f",  # green-8
    "inactive_fg":      "#0f763aA0",
    "hint":             "#00749e",  # sky-11
    "comment":          "#707070",  # gray-11
    "string":           "#a35c00",  # amber-11, darkened for 4.5:1 contrast on white
    "keyword":          "#a60d11",  # red-11
    "type":             "#00749e",  # sky-11
    "number":           "#711fb7",  # purple-11
    "param":            "#cc4e00",  # orange-11
    "function":         "#0f763a",  # green-10
    "json_string":      "#171717",  # gray-12
    "diff_header":      "#707070",  # gray-11
    "muted":            "#858585",  # gray-10
    "invalid_fg":       "#FFFFFF",
    "invalid_bg":       "#e1292f",  # red-9
    "deprecated_bg":    "#a953f5",  # purple-9
    "caret":            "#171717",  # gray-12
    "invisibles":       "#dbdbdb",  # gray-7
    "line_highlight":   "#effaf4",  # green-2
    "selection":        "#adebc7",  # green-6
    "selection_inactive": "#def7e8",  # green-4
    "selection_border": "#adebc7",  # green-6
    "find_highlight":   "#fbe579",  # amber-5
    "indent_guide":     "#c7c7c7",  # gray-8
    "bracket":          "#171717",  # gray-12
    "active_guide":     "#fece5c",  # amber-7
    "link":             "#0a599e",  # blue-11
    "marker_bg":        "#f7f7f7",  # gray-2
    "marker_error":     "#ffdbdc",  # red-4
    "marker_warning":   "#ffef9e",  # amber-4
    "hover_surface":    "#f2f2f2",  # gray-3
    "debug":            "#00749e",  # sky-11
    "diff_added":       "#18c15f40",  # green-8
    "diff_removed":     "#e1292f33",  # red-9
    "error":            "#c72a2e",  # red-10
    "warning":          "#cc4e00",  # orange-11
    "added":            "#0f763a",  # green-10
    "modified":         "#a35c00",  # amber-11 (darkened)
    "renamed":          "#00749e",  # sky-11
    "submodule":        "#711fb7",  # purple-11
    "conflict":         "#cc4e00",  # orange-11
    "ignored":          "#858585",  # gray-10
    "ansi_black":           "#171717",  # gray-12
    "ansi_bright_black":    "#707070",  # gray-11
    "ansi_red":             "#c72a2e",  # red-10
    "ansi_bright_red":      "#a60d11",  # red-11
    "ansi_green":           "#0f763a",  # green-10
    "ansi_bright_green":    "#139a4c",  # green-9
    "ansi_yellow":          "#a35c00",  # amber-11 (darkened)
    "ansi_bright_yellow":   "#c56f00",  # amber-11
    "ansi_blue":            "#0a599e",  # blue-11
    "ansi_bright_blue":     "#047ad7",  # blue-10
    "ansi_magenta":         "#711fb7",  # purple-11
    "ansi_bright_magenta":  "#9343db",  # purple-10
    "ansi_cyan":            "#00749e",  # sky-11
    "ansi_bright_cyan":     "#10a27b",  # teal-11
    "ansi_white":           "#a6a6a6",  # gray-9
    "ansi_bright_white":    "#c7c7c7",  # gray-8
    "find_match_alpha":     160,
    "list_active_alpha":    110,
    "list_inactive_alpha":  60,
}

MODES = {"dark": DARK, "light": LIGHT}


def resolver(p):
    """Return ``c(expr)`` resolving ``"name"`` or ``"name/alpha"`` (alpha 0–255) against palette ``p``."""
    def c(expr):
        if "/" in expr:
            name, alpha_str = expr.split("/", 1)
            return f"{p[name]}{int(alpha_str):02X}"
        return p[expr]
    return c


# ---------------------------------------------------------------------------
# Token colors
# ---------------------------------------------------------------------------

def build_token_colors(p):
    c = resolver(p)
    FG = c("fg")
    return [
        {
            "settings": {
                "foreground": FG,
                "background": c("bg"),
                "caret": c("caret"),
                "invisibles": c("invisibles"),
                "lineHighlight": c("line_highlight"),
                "selection": c("selection"),
                "findHighlight": c("find_highlight"),
                "findHighlightForeground": c("fg"),
                "selectionBorder": c("selection_border"),
                "activeGuide": c("active_guide/176"),
                "bracketsForeground": c("bracket/165"),
                "bracketsOptions": "underline",
                "bracketContentsForeground": c("bracket/165"),
                "bracketContentsOptions": "underline",
                "tagsOptions": "stippled_underline",
            }
        },
        {
            "name": "Comment",
            "scope": ["comment"],
            "settings": {"foreground": c("comment")},
        },
        {
            "name": "String",
            "scope": "string",
            "settings": {"foreground": c("string")},
        },
        {
            "name": "Number",
            "scope": "constant.numeric",
            "settings": {"foreground": c("number")},
        },
        {
            "name": "Built-in constant",
            "scope": "constant.language",
            "settings": {"foreground": c("number")},
        },
        {
            "name": "User-defined constant",
            "scope": ["constant.character", "constant.other"],
            "settings": {"foreground": c("number")},
        },
        {
            "name": "Variable",
            "scope": "variable",
            "settings": {"fontStyle": ""},
        },
        {
            "name": "Keyword",
            "scope": "keyword",
            "settings": {"fontStyle": "bold", "foreground": c("keyword")},
        },
        {
            "name": "Storage",
            "scope": "storage",
            "settings": {"fontStyle": "bold", "foreground": c("keyword")},
        },
        {
            "name": "Storage type",
            "scope": "storage.type",
            "settings": {"fontStyle": "italic", "foreground": c("type")},
        },
        {
            "name": "Class name",
            "scope": "entity.name.class",
            "settings": {"fontStyle": "underline", "foreground": c("function")},
        },
        {
            "name": "Inherited class",
            "scope": "entity.other.inherited-class",
            "settings": {"fontStyle": "italic underline", "foreground": c("function")},
        },
        {
            "name": "Function name",
            "scope": "entity.name.function",
            "settings": {"fontStyle": "", "foreground": c("function")},
        },
        {
            "name": "Function argument",
            "scope": "variable.parameter",
            "settings": {"fontStyle": "italic", "foreground": c("param")},
        },
        {
            "name": "Tag name",
            "scope": "entity.name.tag",
            "settings": {"fontStyle": "bold", "foreground": c("keyword")},
        },
        {
            "name": "Tag attribute",
            "scope": "entity.other.attribute-name",
            "settings": {"fontStyle": "", "foreground": c("function")},
        },
        {
            "name": "Library function",
            "scope": "support.function",
            "settings": {"fontStyle": "", "foreground": c("type")},
        },
        {
            "name": "Library constant",
            "scope": "support.constant",
            "settings": {"fontStyle": "", "foreground": c("type")},
        },
        {
            "name": "Library class/type",
            "scope": ["support.type", "support.class"],
            "settings": {"fontStyle": "italic", "foreground": c("type")},
        },
        {
            "name": "Library variable",
            "scope": "support.other.variable",
            "settings": {"fontStyle": ""},
        },
        {
            "name": "Invalid",
            "scope": "invalid",
            "settings": {
                "background": c("invalid_bg"),
                "fontStyle": "bold",
                "foreground": c("invalid_fg"),
            },
        },
        {
            "name": "Invalid deprecated",
            "scope": "invalid.deprecated",
            "settings": {"background": c("deprecated_bg"), "foreground": c("invalid_fg")},
        },
        {
            "name": "JSON String",
            "scope": ["meta.structure.dictionary.json", "string.quoted.double.json"],
            "settings": {"foreground": c("json_string")},
        },
        {
            "name": "diff.header",
            "scope": "meta.diff, meta.diff.header",
            "settings": {"foreground": c("diff_header")},
        },
        {
            "name": "diff.deleted",
            "scope": "markup.deleted",
            "settings": {"foreground": c("error")},
        },
        {
            "name": "diff.inserted",
            "scope": "markup.inserted",
            "settings": {"foreground": c("added")},
        },
        {
            "name": "diff.changed",
            "scope": "markup.changed",
            "settings": {"foreground": c("modified")},
        },
        {
            "scope": "constant.numeric.line-number.find-in-files - match",
            "settings": {"foreground": c("number/160")},
        },
        {
            "scope": "entity.name.filename.find-in-files",
            "settings": {"foreground": c("string")},
        },
        {
            "name": "Language methods",
            "scope": ["variable.language"],
            "settings": {"foreground": c("function")},
        },
        {
            "scope": "heading.1.markdown",
            "settings": {"foreground": c("function"), "fontStyle": "bold"},
        },
        {
            "scope": "punctuation.definition.heading.markdown",
            "settings": {"foreground": c("function")},
        },
        {
            "scope": "entity.name.section.markdown",
            "settings": {"foreground": c("function")},
        },
        {
            "scope": "punctuation.definition.list.begin.markdown",
            "settings": {"foreground": c("number")},
        },
        {
            "scope": "meta.image.inline.markdown",
            "settings": {"foreground": c("string")},
        },
        {
            "scope": "markup.bold.markdown",
            "settings": {"foreground": FG, "fontStyle": "bold"},
        },
        {
            "scope": "markup.italic.markdown",
            "settings": {"foreground": FG, "fontStyle": "italic"},
        },
        {
            "scope": "markup.inline.raw.string.markdown",
            "settings": {"foreground": c("type")},
        },
        {
            "scope": "meta.separator.markdown",
            "settings": {"foreground": c("muted")},
        },
        {
            "scope": [
                "punctuation.definition.template-expression.begin",
                "punctuation.definition.template-expression.end",
            ],
            "settings": {"foreground": c("number")},
        },
        {
            "scope": [
                "variable.other.object",
                "punctuation.accessor",
                "meta.brace.round",
                "variable.other.readwrite",
                "punctuation.separator.comma",
            ],
            "settings": {"foreground": FG},
        },
    ]


# ---------------------------------------------------------------------------
# Workbench colors
# ---------------------------------------------------------------------------

def build_colors(p):
    """Build the ``colors`` dict for palette ``p``."""
    c = resolver(p)
    FG = c("fg")
    BG = c("bg")
    TRANSPARENT = c("transparent")
    a = c("accent")
    ln = c("line")

    def aa(alpha):
        return f"{ln}{alpha:02X}"

    return {
        "foreground": FG,
        "icon.foreground": FG,
        "contrastBorder": aa(117),
        "contrastActiveBorder": TRANSPARENT,
        "focusBorder": aa(117),
        "editor.foreground": FG,
        "editor.background": BG,
        "editor.inactiveSelectionBackground": c("selection_inactive"),
        "editor.findMatchBackground": aa(p["find_match_alpha"]),
        "editor.findMatchForeground": c("fg/204"),
        "editor.findMatchBorder": TRANSPARENT,
        "editor.selectionBackground": c("selection"),
        "editor.selectionForeground": FG,
        "editor.lineHighlightBorder": aa(117),
        "editorLineNumber.foreground": a,
        "editorLineNumber.activeForeground": a,
        "editorMarkerNavigation.background": c("marker_bg"),
        "editorMarkerNavigationError.background": c("marker_error"),
        "editorMarkerNavigationWarning.background": c("marker_warning"),
        "editorLink.activeForeground": c("link"),
        "editor.findMatchHighlightBackground": aa(102),
        "editor.findMatchHighlightForeground": FG,
        "terminal.ansiBlack": c("ansi_black"),
        "terminal.ansiBrightBlack": c("ansi_bright_black"),
        "terminal.ansiRed": c("ansi_red"),
        "terminal.ansiBrightRed": c("ansi_bright_red"),
        "terminal.ansiGreen": c("ansi_green"),
        "terminal.ansiBrightGreen": c("ansi_bright_green"),
        "terminal.ansiYellow": c("ansi_yellow"),
        "terminal.ansiBrightYellow": c("ansi_bright_yellow"),
        "terminal.ansiBlue": c("ansi_blue"),
        "terminal.ansiBrightBlue": c("ansi_bright_blue"),
        "terminal.ansiMagenta": c("ansi_magenta"),
        "terminal.ansiBrightMagenta": c("ansi_bright_magenta"),
        "terminal.ansiCyan": c("ansi_cyan"),
        "terminal.ansiBrightCyan": c("ansi_bright_cyan"),
        "terminal.ansiWhite": c("ansi_white"),
        "terminal.ansiBrightWhite": c("ansi_bright_white"),
        "titleBar.activeForeground": a,
        "editorSuggestWidget.background": BG,
        "editorSuggestWidget.foreground": FG,
        "editorSuggestWidget.border": ln,
        "editorSuggestWidget.highlightForeground": c("hint"),
        "editorSuggestWidget.selectedBackground": aa(117),
        "editorHoverWidget.background": BG,
        "editorHoverWidget.border": aa(117),
        "editorWidget.background": BG,
        "editorWidget.border": BG,
        "editorIndentGuide.activeBackground": c("indent_guide"),
        "breadcrumb.foreground": a,
        "menu.background": BG,
        "menu.border": aa(117),
        "panel.background": BG,
        "panel.dropBorder": ln,
        "panel.border": aa(117),
        "panelTitle.activeForeground": a,
        "panelTitle.inactiveForeground": c("inactive_fg"),
        "panelSection.border": aa(117),
        "sideBar.background": BG,
        "sideBarSectionHeader.border": aa(117),
        "sideBar.border": aa(117),
        "sideBarTitle.foreground": a,
        "sideBar.foreground": FG,
        "sideBarSectionHeader.background": BG,
        "sideBarSectionHeader.foreground": a,
        "badge.background": BG,
        "badge.foreground": a,
        "activityBar.background": BG,
        "activityBar.foreground": a,
        "activityBar.border": aa(117),
        "activityBar.inactiveForeground": c("inactive_fg"),
        "activityBarBadge.background": BG,
        "activityBarBadge.foreground": a,
        "titleBar.activeBackground": BG,
        "titleBar.border": aa(117),
        "titleBar.inactiveBackground": BG,
        "titleBar.inactiveForeground": a,
        "tab.activeForeground": FG,
        "tab.inactiveForeground": FG,
        "tab.unfocusedActiveForeground": FG,
        "tab.unfocusedInactiveForeground": FG,
        "tab.activeBackground": BG,
        "tab.inactiveBackground": BG,
        "tab.unfocusedActiveBackground": BG,
        "tab.unfocusedInactiveBackground": BG,
        "tab.hoverBackground": aa(37),
        "tab.unfocusedHoverBackground": aa(37),
        "tab.border": aa(117),
        "tab.activeBorder": FG,
        "tab.unfocusedActiveBorder": ln,
        "tab.activeModifiedBorder": aa(117),
        "tab.inactiveModifiedBorder": aa(117),
        "tab.hoverBorder": aa(117),
        "editorGroupHeader.tabsBackground": BG,
        "editorGroup.border": aa(117),
        "editorGroupHeader.tabsBorder": BG,
        "editorGroupHeader.border": BG,
        "editorGroupHeader.noTabsBackground": BG,
        "statusBar.background": BG,
        "statusBar.foreground": a,
        "statusBar.border": aa(117),
        "statusBar.noFolderBackground": BG,
        "statusBar.noFolderForeground": a,
        "statusBar.debuggingBackground": c("debug/21"),
        "statusBar.debuggingForeground": a,
        "statusBarItem.hoverBackground": c("hover_surface"),
        "notificationCenter.border": ln,
        "notifications.foreground": FG,
        "notifications.background": BG,
        "notifications.border": aa(117),
        "notificationCenterHeader.background": BG,
        "notificationCenterHeader.foreground": FG,
        "editorHint.foreground": c("hint"),
        "diffEditor.insertedTextBackground": c("diff_added"),
        "diffEditor.insertedTextBorder": c("diff_added"),
        "diffEditor.removedTextBackground": c("diff_removed"),
        "diffEditor.removedTextBorder": c("diff_removed"),
        "merge.border": aa(117),
        "peekView.border": aa(117),
        "peekViewTitle.background": BG,
        "peekViewTitleLabel.foreground": FG,
        "debugExceptionWidget.background": BG,
        "debugExceptionWidget.border": ln,
        "debugToolBar.background": BG,
        "debugToolBar.border": ln,
        "button.background": BG,
        "button.foreground": FG,
        "button.hoverBackground": BG,
        "dropdown.border": aa(117),
        "dropdown.background": BG,
        "dropdown.foreground": FG,
        "input.background": aa(20),
        "input.foreground": FG,
        "input.border": aa(117),
        "input.placeholderForeground": c("inactive_fg"),
        "checkbox.border": aa(117),
        "quickInput.background": BG,
        "list.activeSelectionBackground": aa(p["list_active_alpha"]),
        "list.activeSelectionForeground": FG,
        "list.inactiveSelectionBackground": aa(p["list_inactive_alpha"]),
        "list.inactiveSelectionForeground": FG,
        "list.hoverBackground": aa(117),
        "list.inactiveFocusOutline": ln,
        "gitlens.trailingLineBackgroundColor": BG,
        "gitlens.trailingLineForegroundColor": a,
        "terminal.border": aa(117),
        "editorWarning.foreground": c("warning"),
        "list.warningForeground": c("warning"),
        "editorOverviewRuler.warningForeground": c("warning"),
        "gitDecoration.modifiedResourceForeground": c("modified"),
        "gitDecoration.addedResourceForeground": c("added"),
        "gitDecoration.deletedResourceForeground": c("error"),
        "gitDecoration.untrackedResourceForeground": c("added"),
        "gitDecoration.ignoredResourceForeground": c("ignored"),
        "gitDecoration.conflictingResourceForeground": c("conflict"),
        "gitDecoration.renamedResourceForeground": c("renamed"),
        "gitDecoration.stageDeletedResourceForeground": c("error"),
        "gitDecoration.stageModifiedResourceForeground": c("modified"),
        "gitDecoration.submoduleResourceForeground": c("submodule"),
        "scrollbar.shadow": BG,
        "scrollbarSlider.background": aa(64),
        "scrollbarSlider.hoverBackground": aa(112),
        "scrollbarSlider.activeBackground": aa(204),
        # Chat UI
        "chat.requestBubbleHoverBackground": aa(50),
        "chat.requestCodeBorder": aa(80),
        "chat.slashCommandBackground": aa(37),
        "chat.slashCommandForeground": a,
        "chat.avatarBackground": BG,
        "chat.avatarForeground": a,
        "textPreformat.foreground": a,
        "chat.editedFileForeground": a,
        "chat.linesAddedForeground": c("added"),
        "chat.linesRemovedForeground": c("error"),
        "chat.checkpointSeparator": aa(117),
        "chat.thinkingShimmer": ln,
        # Inline Chat
        "inlineChat.background": BG,
        "inlineChat.foreground": FG,
        "inlineChat.border": aa(117),
        "inlineChatInput.border": aa(117),
        "inlineChatInput.focusBorder": ln,
        "inlineChatInput.background": BG,
        "inlineChatInput.placeholderForeground": c("inactive_fg"),
        "inlineChatDiff.inserted": c("diff_added"),
        "inlineChatDiff.removed": c("diff_removed"),
    }


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------

def serialize_theme(theme_dict):
    """Serialize the theme dict to JSON with consistent formatting."""
    return _serialize_compact(theme_dict)


def _serialize_compact(theme_dict):
    """Serialize a theme dict to JSON with compact single-line settings."""
    lines = []
    lines.append("{")
    lines.append(f'    "$schema": "vscode://schemas/color-theme",')
    lines.append(f'    "name": {json.dumps(theme_dict["name"])},')
    lines.append(f'    "tokenColors": [')

    token_colors = theme_dict["tokenColors"]
    for i, entry in enumerate(token_colors):
        comma = "," if i < len(token_colors) - 1 else ""
        _emit_token_entry_compact(lines, entry, comma)

    lines.append("    ],")
    lines.append('    "colors": {')

    colors = theme_dict["colors"]
    color_keys = list(colors.keys())
    for i, key in enumerate(color_keys):
        comma = "," if i < len(color_keys) - 1 else ""
        lines.append(f'        {json.dumps(key)}: {json.dumps(colors[key])}{comma}')

    lines.append("    }")
    lines.append("}")
    return "\n".join(lines) + "\n"


def _emit_token_entry_compact(lines, entry, comma):
    """Emit a single tokenColors entry in compact format."""
    settings = entry.get("settings", {})
    scope = entry.get("scope")
    name = entry.get("name")

    # First entry (base settings, no scope/name) gets special treatment
    if scope is None and name is None:
        lines.append("        {")
        lines.append('            "settings": {')
        settings_keys = list(settings.keys())
        for j, sk in enumerate(settings_keys):
            sc = "," if j < len(settings_keys) - 1 else ""
            lines.append(f'                {json.dumps(sk)}: {json.dumps(settings[sk])}{sc}')
        lines.append("            }")
        lines.append(f"        }}{comma}")
        return

    # Inherited class entry has multi-line settings
    if name == "Inherited class":
        lines.append("        {")
        lines.append(f'            "name": {json.dumps(name)},')
        lines.append(f'            "scope": {json.dumps(scope)},')
        lines.append('            "settings": {')
        skeys = list(settings.keys())
        for j, sk in enumerate(skeys):
            sc = "," if j < len(skeys) - 1 else ""
            lines.append(f'                {json.dumps(sk)}: {json.dumps(settings[sk])}{sc}')
        lines.append("            }")
        lines.append(f"        }}{comma}")
        return

    # Invalid entry has multi-line settings (3 keys: background, fontStyle, foreground)
    if name == "Invalid" and scope == "invalid":
        lines.append("        {")
        lines.append(f'            "name": {json.dumps(name)},')
        lines.append(f'            "scope": {json.dumps(scope)},')
        lines.append('            "settings": {')
        skeys = list(settings.keys())
        for j, sk in enumerate(skeys):
            sc = "," if j < len(skeys) - 1 else ""
            lines.append(f'                {json.dumps(sk)}: {json.dumps(settings[sk])}{sc}')
        lines.append("            }")
        lines.append(f"        }}{comma}")
        return

    # All other entries: compact single-line settings
    settings_str = _inline_obj(settings)
    lines.append("        {")

    if name is not None:
        lines.append(f'            "name": {json.dumps(name)},')

    if scope is not None:
        if _should_expand_scope(scope):
            _emit_scope_array(lines, scope, has_next=True)
        else:
            lines.append(f'            "scope": {json.dumps(scope)},')

    lines.append(f'            "settings": {settings_str}')
    lines.append(f"        }}{comma}")


def _inline_obj(obj):
    """Serialize a small dict as ``{ "key": "value", ... }`` with spaces."""
    items = []
    for k, v in obj.items():
        items.append(f"{json.dumps(k)}: {json.dumps(v)}")
    return "{ " + ", ".join(items) + " }"


def _should_expand_scope(scope):
    """Return True if a scope array should be expanded across multiple lines."""
    if not isinstance(scope, list) or len(scope) <= 1:
        return False
    # Expand when the inline representation would be long (matches original formatting)
    inline = json.dumps(scope)
    return len(inline) > 50


def _emit_scope_array(lines, scope_list, has_next=True):
    """Emit a multi-element scope array expanded across lines."""
    comma_after = "," if has_next else ""
    lines.append('            "scope": [')
    for j, s in enumerate(scope_list):
        sc = "," if j < len(scope_list) - 1 else ""
        lines.append(f"                {json.dumps(s)}{sc}")
    lines.append(f"            ]{comma_after}")



# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    themes_dir = os.path.join(script_dir, "themes")
    os.makedirs(themes_dir, exist_ok=True)

    for mode, palette in MODES.items():
        theme = {
            "$schema": "vscode://schemas/color-theme",
            "name": f"Circuit High Contrast {mode.capitalize()}",
            "tokenColors": build_token_colors(palette),
            "colors": build_colors(palette),
        }
        output = serialize_theme(theme)
        path = os.path.join(themes_dir, f"circuit-high-contrast-{mode}.json")
        with open(path, "w", newline="\n") as f:
            f.write(output)
        print(f"  wrote {path}")

    print("Done.")


if __name__ == "__main__":
    main()
