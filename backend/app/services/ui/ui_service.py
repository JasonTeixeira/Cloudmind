"""
Advanced UI Service
Professional UI system with theme, layout, and settings management
"""

import asyncio
import logging
import os
import json
import hashlib
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional, Any, Tuple, Union
from uuid import UUID, uuid4
from pathlib import Path
import tempfile
import shutil

from app.core.config import settings
from app.schemas.ui import (
    Theme, Layout, Panel, View, Split, Shortcut, FontSettings, EditorSettings,
    AnimationSettings, UISettings, ColorPalette, IconTheme, AccessibilitySettings,
    ThemeType, ColorScheme, LayoutType, PanelPosition, ViewType, ShortcutCategory,
    FontFamily, FontWeight, FontStyle, CursorStyle, AnimationType
)

logger = logging.getLogger(__name__)


class UIService:
    """Manages UI themes, layouts, and settings"""
    
    def __init__(self):
        self.themes: Dict[str, Theme] = {}
        self.layouts: Dict[str, Layout] = {}
        self.user_settings: Dict[str, UISettings] = {}
        self.color_palettes: Dict[str, ColorPalette] = {}
        self.icon_themes: Dict[str, IconTheme] = {}
        self.previews: Dict[str, Dict[str, Any]] = {}
        
        # Initialize default themes and layouts
        self._initialize_default_themes()
        self._initialize_default_layouts()
        self._initialize_default_shortcuts()
    
    def _initialize_default_themes(self):
        """Initialize default themes"""
        default_themes = [
            Theme(
                id="dark-default",
                name="dark-default",
                display_name="Dark Default",
                description="Default dark theme with modern colors",
                type=ThemeType.DARK,
                color_scheme=ColorScheme.VSCODE,
                author="CloudMind Team",
                version="1.0.0",
                is_default=True,
                colors={
                    "background": "#1e1e1e",
                    "foreground": "#d4d4d4",
                    "editor.background": "#1e1e1e",
                    "editor.foreground": "#d4d4d4",
                    "editor.lineHighlightBackground": "#2a2a2a",
                    "editor.selectionBackground": "#264f78",
                    "editor.inactiveSelectionBackground": "#3a3d41",
                    "editor.wordHighlightBackground": "#575757",
                    "editor.findMatchBackground": "#515c6a",
                    "editor.findMatchHighlightBackground": "#3a3d41",
                    "editor.hoverHighlightBackground": "#2a2d2e",
                    "editor.lineHighlightBorder": "#454545",
                    "editorCursor.foreground": "#aeafad",
                    "editorWhitespace.foreground": "#3b3a32",
                    "editorIndentGuide.background": "#3b3a32",
                    "editorIndentGuide.activeBackground": "#939393",
                    "sideBar.background": "#252526",
                    "sideBar.foreground": "#cccccc",
                    "sideBarTitle.foreground": "#cccccc",
                    "titleBar.activeBackground": "#3c3c3c",
                    "titleBar.activeForeground": "#cccccc",
                    "activityBar.background": "#333333",
                    "activityBar.foreground": "#cccccc",
                    "statusBar.background": "#007acc",
                    "statusBar.foreground": "#ffffff",
                    "tab.activeBackground": "#1e1e1e",
                    "tab.inactiveBackground": "#2d2d30",
                    "tab.activeForeground": "#ffffff",
                    "tab.inactiveForeground": "#cccccc"
                },
                token_colors=[
                    {"name": "Comment", "scope": ["comment"], "settings": {"foreground": "#6a9955"}},
                    {"name": "String", "scope": ["string"], "settings": {"foreground": "#ce9178"}},
                    {"name": "Keyword", "scope": ["keyword"], "settings": {"foreground": "#569cd6"}},
                    {"name": "Function", "scope": ["entity.name.function"], "settings": {"foreground": "#dcdcaa"}},
                    {"name": "Variable", "scope": ["variable"], "settings": {"foreground": "#9cdcfe"}},
                    {"name": "Number", "scope": ["constant.numeric"], "settings": {"foreground": "#b5cea8"}},
                    {"name": "Type", "scope": ["entity.name.type"], "settings": {"foreground": "#4ec9b0"}}
                ],
                semantic_token_colors={
                    "variable": {"foreground": "#9cdcfe"},
                    "function": {"foreground": "#dcdcaa"},
                    "class": {"foreground": "#4ec9b0"},
                    "interface": {"foreground": "#4ec9b0"},
                    "enum": {"foreground": "#4ec9b0"},
                    "keyword": {"foreground": "#569cd6"},
                    "string": {"foreground": "#ce9178"},
                    "number": {"foreground": "#b5cea8"},
                    "comment": {"foreground": "#6a9955"}
                },
                ui_colors={
                    "button.background": "#0e639c",
                    "button.foreground": "#ffffff",
                    "button.hoverBackground": "#1177bb",
                    "input.background": "#3c3c3c",
                    "input.foreground": "#cccccc",
                    "input.border": "#3c3c3c",
                    "dropdown.background": "#3c3c3c",
                    "dropdown.foreground": "#cccccc",
                    "dropdown.border": "#3c3c3c"
                },
                created_at=datetime.now(timezone.utc)
            ),
            Theme(
                id="light-default",
                name="light-default",
                display_name="Light Default",
                description="Default light theme with clean colors",
                type=ThemeType.LIGHT,
                color_scheme=ColorScheme.VSCODE,
                author="CloudMind Team",
                version="1.0.0",
                is_default=False,
                colors={
                    "background": "#ffffff",
                    "foreground": "#1e1e1e",
                    "editor.background": "#ffffff",
                    "editor.foreground": "#1e1e1e",
                    "editor.lineHighlightBackground": "#f7f7f7",
                    "editor.selectionBackground": "#add6ff",
                    "editor.inactiveSelectionBackground": "#e5ebf1",
                    "editor.wordHighlightBackground": "#575757",
                    "editor.findMatchBackground": "#a8ac94",
                    "editor.findMatchHighlightBackground": "#ea5c0055",
                    "editor.hoverHighlightBackground": "#add6ff26",
                    "editor.lineHighlightBorder": "#eeeeee",
                    "editorCursor.foreground": "#000000",
                    "editorWhitespace.foreground": "#333333",
                    "editorIndentGuide.background": "#d3d3d3",
                    "editorIndentGuide.activeBackground": "#939393",
                    "sideBar.background": "#f3f3f3",
                    "sideBar.foreground": "#616161",
                    "sideBarTitle.foreground": "#424242",
                    "titleBar.activeBackground": "#dddddd",
                    "titleBar.activeForeground": "#424242",
                    "activityBar.background": "#f3f3f3",
                    "activityBar.foreground": "#424242",
                    "statusBar.background": "#007acc",
                    "statusBar.foreground": "#ffffff",
                    "tab.activeBackground": "#ffffff",
                    "tab.inactiveBackground": "#ececec",
                    "tab.activeForeground": "#424242",
                    "tab.inactiveForeground": "#616161"
                },
                token_colors=[
                    {"name": "Comment", "scope": ["comment"], "settings": {"foreground": "#008000"}},
                    {"name": "String", "scope": ["string"], "settings": {"foreground": "#a31515"}},
                    {"name": "Keyword", "scope": ["keyword"], "settings": {"foreground": "#0000ff"}},
                    {"name": "Function", "scope": ["entity.name.function"], "settings": {"foreground": "#795e26"}},
                    {"name": "Variable", "scope": ["variable"], "settings": {"foreground": "#001080"}},
                    {"name": "Number", "scope": ["constant.numeric"], "settings": {"foreground": "#098658"}},
                    {"name": "Type", "scope": ["entity.name.type"], "settings": {"foreground": "#267f99"}}
                ],
                semantic_token_colors={
                    "variable": {"foreground": "#001080"},
                    "function": {"foreground": "#795e26"},
                    "class": {"foreground": "#267f99"},
                    "interface": {"foreground": "#267f99"},
                    "enum": {"foreground": "#267f99"},
                    "keyword": {"foreground": "#0000ff"},
                    "string": {"foreground": "#a31515"},
                    "number": {"foreground": "#098658"},
                    "comment": {"foreground": "#008000"}
                },
                ui_colors={
                    "button.background": "#0e639c",
                    "button.foreground": "#ffffff",
                    "button.hoverBackground": "#1177bb",
                    "input.background": "#ffffff",
                    "input.foreground": "#616161",
                    "input.border": "#cccccc",
                    "dropdown.background": "#ffffff",
                    "dropdown.foreground": "#616161",
                    "dropdown.border": "#cccccc"
                },
                created_at=datetime.now(timezone.utc)
            ),
            Theme(
                id="high-contrast",
                name="high-contrast",
                display_name="High Contrast",
                description="High contrast theme for accessibility",
                type=ThemeType.HIGH_CONTRAST,
                color_scheme=ColorScheme.CUSTOM,
                author="CloudMind Team",
                version="1.0.0",
                is_default=False,
                colors={
                    "background": "#000000",
                    "foreground": "#ffffff",
                    "editor.background": "#000000",
                    "editor.foreground": "#ffffff",
                    "editor.lineHighlightBackground": "#1a1a1a",
                    "editor.selectionBackground": "#ffff00",
                    "editor.inactiveSelectionBackground": "#404040",
                    "editor.wordHighlightBackground": "#575757",
                    "editor.findMatchBackground": "#ffff00",
                    "editor.findMatchHighlightBackground": "#ffff00",
                    "editor.hoverHighlightBackground": "#404040",
                    "editor.lineHighlightBorder": "#404040",
                    "editorCursor.foreground": "#ffffff",
                    "editorWhitespace.foreground": "#404040",
                    "editorIndentGuide.background": "#404040",
                    "editorIndentGuide.activeBackground": "#ffffff",
                    "sideBar.background": "#000000",
                    "sideBar.foreground": "#ffffff",
                    "sideBarTitle.foreground": "#ffffff",
                    "titleBar.activeBackground": "#000000",
                    "titleBar.activeForeground": "#ffffff",
                    "activityBar.background": "#000000",
                    "activityBar.foreground": "#ffffff",
                    "statusBar.background": "#ffff00",
                    "statusBar.foreground": "#000000",
                    "tab.activeBackground": "#000000",
                    "tab.inactiveBackground": "#404040",
                    "tab.activeForeground": "#ffffff",
                    "tab.inactiveForeground": "#ffffff"
                },
                token_colors=[
                    {"name": "Comment", "scope": ["comment"], "settings": {"foreground": "#00ff00"}},
                    {"name": "String", "scope": ["string"], "settings": {"foreground": "#ffff00"}},
                    {"name": "Keyword", "scope": ["keyword"], "settings": {"foreground": "#00ffff"}},
                    {"name": "Function", "scope": ["entity.name.function"], "settings": {"foreground": "#ff00ff"}},
                    {"name": "Variable", "scope": ["variable"], "settings": {"foreground": "#ffffff"}},
                    {"name": "Number", "scope": ["constant.numeric"], "settings": {"foreground": "#00ff00"}},
                    {"name": "Type", "scope": ["entity.name.type"], "settings": {"foreground": "#ff00ff"}}
                ],
                semantic_token_colors={
                    "variable": {"foreground": "#ffffff"},
                    "function": {"foreground": "#ff00ff"},
                    "class": {"foreground": "#ff00ff"},
                    "interface": {"foreground": "#ff00ff"},
                    "enum": {"foreground": "#ff00ff"},
                    "keyword": {"foreground": "#00ffff"},
                    "string": {"foreground": "#ffff00"},
                    "number": {"foreground": "#00ff00"},
                    "comment": {"foreground": "#00ff00"}
                },
                ui_colors={
                    "button.background": "#ffff00",
                    "button.foreground": "#000000",
                    "button.hoverBackground": "#ffffff",
                    "input.background": "#000000",
                    "input.foreground": "#ffffff",
                    "input.border": "#ffffff",
                    "dropdown.background": "#000000",
                    "dropdown.foreground": "#ffffff",
                    "dropdown.border": "#ffffff"
                },
                created_at=datetime.now(timezone.utc)
            )
        ]
        
        for theme in default_themes:
            self.themes[theme.id] = theme
    
    def _initialize_default_layouts(self):
        """Initialize default layouts"""
        default_layouts = [
            Layout(
                id="default-layout",
                name="default-layout",
                display_name="Default Layout",
                description="Default layout with standard panels",
                type=LayoutType.DEFAULT,
                is_default=True,
                panels=[
                    {
                        "id": "explorer-panel",
                        "name": "Explorer",
                        "type": "explorer",
                        "position": "left",
                        "size": 250,
                        "is_visible": True,
                        "is_resizable": True,
                        "is_draggable": True,
                        "is_collapsible": True,
                        "is_pinned": False,
                        "order": 0
                    },
                    {
                        "id": "editor-panel",
                        "name": "Editor",
                        "type": "editor",
                        "position": "center",
                        "size": 800,
                        "is_visible": True,
                        "is_resizable": True,
                        "is_draggable": False,
                        "is_collapsible": False,
                        "is_pinned": True,
                        "order": 1
                    },
                    {
                        "id": "terminal-panel",
                        "name": "Terminal",
                        "type": "terminal",
                        "position": "bottom",
                        "size": 300,
                        "is_visible": True,
                        "is_resizable": True,
                        "is_draggable": True,
                        "is_collapsible": True,
                        "is_pinned": False,
                        "order": 2
                    },
                    {
                        "id": "problems-panel",
                        "name": "Problems",
                        "type": "problems",
                        "position": "bottom",
                        "size": 200,
                        "is_visible": False,
                        "is_resizable": True,
                        "is_draggable": True,
                        "is_collapsible": True,
                        "is_pinned": False,
                        "order": 3
                    }
                ],
                views=[
                    {
                        "id": "file-explorer",
                        "name": "File Explorer",
                        "type": "explorer",
                        "panel_id": "explorer-panel",
                        "is_active": True,
                        "is_visible": True,
                        "is_pinned": True,
                        "order": 0
                    },
                    {
                        "id": "main-editor",
                        "name": "Main Editor",
                        "type": "editor",
                        "panel_id": "editor-panel",
                        "is_active": True,
                        "is_visible": True,
                        "is_pinned": True,
                        "order": 0
                    },
                    {
                        "id": "integrated-terminal",
                        "name": "Integrated Terminal",
                        "type": "terminal",
                        "panel_id": "terminal-panel",
                        "is_active": False,
                        "is_visible": True,
                        "is_pinned": False,
                        "order": 0
                    },
                    {
                        "id": "problems-view",
                        "name": "Problems",
                        "type": "problems",
                        "panel_id": "problems-panel",
                        "is_active": False,
                        "is_visible": False,
                        "is_pinned": False,
                        "order": 0
                    }
                ],
                splits=[
                    {
                        "id": "main-split",
                        "name": "Main Split",
                        "direction": "horizontal",
                        "size": 0.7,
                        "is_resizable": True,
                        "children": ["explorer-panel", "editor-panel"],
                        "parent_id": None
                    },
                    {
                        "id": "bottom-split",
                        "name": "Bottom Split",
                        "direction": "vertical",
                        "size": 0.6,
                        "is_resizable": True,
                        "children": ["terminal-panel", "problems-panel"],
                        "parent_id": None
                    }
                ],
                created_at=datetime.now(timezone.utc)
            ),
            Layout(
                id="compact-layout",
                name="compact-layout",
                display_name="Compact Layout",
                description="Compact layout for small screens",
                type=LayoutType.COMPACT,
                is_default=False,
                panels=[
                    {
                        "id": "explorer-panel-compact",
                        "name": "Explorer",
                        "type": "explorer",
                        "position": "left",
                        "size": 200,
                        "is_visible": True,
                        "is_resizable": True,
                        "is_draggable": True,
                        "is_collapsible": True,
                        "is_pinned": False,
                        "order": 0
                    },
                    {
                        "id": "editor-panel-compact",
                        "name": "Editor",
                        "type": "editor",
                        "position": "center",
                        "size": 600,
                        "is_visible": True,
                        "is_resizable": True,
                        "is_draggable": False,
                        "is_collapsible": False,
                        "is_pinned": True,
                        "order": 1
                    },
                    {
                        "id": "terminal-panel-compact",
                        "name": "Terminal",
                        "type": "terminal",
                        "position": "bottom",
                        "size": 200,
                        "is_visible": False,
                        "is_resizable": True,
                        "is_draggable": True,
                        "is_collapsible": True,
                        "is_pinned": False,
                        "order": 2
                    }
                ],
                views=[
                    {
                        "id": "file-explorer-compact",
                        "name": "File Explorer",
                        "type": "explorer",
                        "panel_id": "explorer-panel-compact",
                        "is_active": True,
                        "is_visible": True,
                        "is_pinned": True,
                        "order": 0
                    },
                    {
                        "id": "main-editor-compact",
                        "name": "Main Editor",
                        "type": "editor",
                        "panel_id": "editor-panel-compact",
                        "is_active": True,
                        "is_visible": True,
                        "is_pinned": True,
                        "order": 0
                    },
                    {
                        "id": "integrated-terminal-compact",
                        "name": "Integrated Terminal",
                        "type": "terminal",
                        "panel_id": "terminal-panel-compact",
                        "is_active": False,
                        "is_visible": False,
                        "is_pinned": False,
                        "order": 0
                    }
                ],
                splits=[
                    {
                        "id": "main-split-compact",
                        "name": "Main Split",
                        "direction": "horizontal",
                        "size": 0.75,
                        "is_resizable": True,
                        "children": ["explorer-panel-compact", "editor-panel-compact"],
                        "parent_id": None
                    }
                ],
                created_at=datetime.now(timezone.utc)
            ),
            Layout(
                id="minimal-layout",
                name="minimal-layout",
                display_name="Minimal Layout",
                description="Minimal layout with focus on editor",
                type=LayoutType.MINIMAL,
                is_default=False,
                panels=[
                    {
                        "id": "editor-panel-minimal",
                        "name": "Editor",
                        "type": "editor",
                        "position": "center",
                        "size": 1000,
                        "is_visible": True,
                        "is_resizable": False,
                        "is_draggable": False,
                        "is_collapsible": False,
                        "is_pinned": True,
                        "order": 0
                    }
                ],
                views=[
                    {
                        "id": "main-editor-minimal",
                        "name": "Main Editor",
                        "type": "editor",
                        "panel_id": "editor-panel-minimal",
                        "is_active": True,
                        "is_visible": True,
                        "is_pinned": True,
                        "order": 0
                    }
                ],
                splits=[],
                created_at=datetime.now(timezone.utc)
            )
        ]
        
        for layout in default_layouts:
            self.layouts[layout.id] = layout
    
    def _initialize_default_shortcuts(self):
        """Initialize default keyboard shortcuts"""
        self.default_shortcuts = [
            Shortcut(
                id="file-new",
                name="New File",
                description="Create a new file",
                category=ShortcutCategory.FILE,
                key="Ctrl+N",
                command="file.new",
                context="editor",
                is_enabled=True,
                is_global=False,
                is_custom=False,
                order=0,
                created_at=datetime.now(timezone.utc)
            ),
            Shortcut(
                id="file-open",
                name="Open File",
                description="Open a file",
                category=ShortcutCategory.FILE,
                key="Ctrl+O",
                command="file.open",
                context="editor",
                is_enabled=True,
                is_global=False,
                is_custom=False,
                order=1,
                created_at=datetime.now(timezone.utc)
            ),
            Shortcut(
                id="file-save",
                name="Save",
                description="Save the current file",
                category=ShortcutCategory.FILE,
                key="Ctrl+S",
                command="file.save",
                context="editor",
                is_enabled=True,
                is_global=False,
                is_custom=False,
                order=2,
                created_at=datetime.now(timezone.utc)
            ),
            Shortcut(
                id="edit-undo",
                name="Undo",
                description="Undo the last action",
                category=ShortcutCategory.EDIT,
                key="Ctrl+Z",
                command="edit.undo",
                context="editor",
                is_enabled=True,
                is_global=False,
                is_custom=False,
                order=0,
                created_at=datetime.now(timezone.utc)
            ),
            Shortcut(
                id="edit-redo",
                name="Redo",
                description="Redo the last undone action",
                category=ShortcutCategory.EDIT,
                key="Ctrl+Y",
                command="edit.redo",
                context="editor",
                is_enabled=True,
                is_global=False,
                is_custom=False,
                order=1,
                created_at=datetime.now(timezone.utc)
            ),
            Shortcut(
                id="edit-copy",
                name="Copy",
                description="Copy selected text",
                category=ShortcutCategory.EDIT,
                key="Ctrl+C",
                command="edit.copy",
                context="editor",
                is_enabled=True,
                is_global=False,
                is_custom=False,
                order=2,
                created_at=datetime.utcnow()
            ),
            Shortcut(
                id="edit-paste",
                name="Paste",
                description="Paste text from clipboard",
                category=ShortcutCategory.EDIT,
                key="Ctrl+V",
                command="edit.paste",
                context="editor",
                is_enabled=True,
                is_global=False,
                is_custom=False,
                order=3,
                created_at=datetime.utcnow()
            ),
            Shortcut(
                id="search-find",
                name="Find",
                description="Find text in current file",
                category=ShortcutCategory.SEARCH,
                key="Ctrl+F",
                command="search.find",
                context="editor",
                is_enabled=True,
                is_global=False,
                is_custom=False,
                order=0,
                created_at=datetime.utcnow()
            ),
            Shortcut(
                id="search-replace",
                name="Replace",
                description="Find and replace text",
                category=ShortcutCategory.SEARCH,
                key="Ctrl+H",
                command="search.replace",
                context="editor",
                is_enabled=True,
                is_global=False,
                is_custom=False,
                order=1,
                created_at=datetime.utcnow()
            ),
            Shortcut(
                id="terminal-toggle",
                name="Toggle Terminal",
                description="Show/hide integrated terminal",
                category=ShortcutCategory.TERMINAL,
                key="Ctrl+`",
                command="terminal.toggle",
                context="editor",
                is_enabled=True,
                is_global=False,
                is_custom=False,
                order=0,
                created_at=datetime.utcnow()
            ),
            Shortcut(
                id="debug-start",
                name="Start Debugging",
                description="Start debugging session",
                category=ShortcutCategory.DEBUG,
                key="F5",
                command="debug.start",
                context="editor",
                is_enabled=True,
                is_global=False,
                is_custom=False,
                order=0,
                created_at=datetime.utcnow()
            ),
            Shortcut(
                id="debug-step-over",
                name="Step Over",
                description="Step over current line",
                category=ShortcutCategory.DEBUG,
                key="F10",
                command="debug.stepOver",
                context="debug",
                is_enabled=True,
                is_global=False,
                is_custom=False,
                order=1,
                created_at=datetime.utcnow()
            ),
            Shortcut(
                id="debug-step-into",
                name="Step Into",
                description="Step into function call",
                category=ShortcutCategory.DEBUG,
                key="F11",
                command="debug.stepInto",
                context="debug",
                is_enabled=True,
                is_global=False,
                is_custom=False,
                order=2,
                created_at=datetime.utcnow()
            ),
            Shortcut(
                id="debug-step-out",
                name="Step Out",
                description="Step out of current function",
                category=ShortcutCategory.DEBUG,
                key="Shift+F11",
                command="debug.stepOut",
                context="debug",
                is_enabled=True,
                is_global=False,
                is_custom=False,
                order=3,
                created_at=datetime.utcnow()
            )
        ]
    
    async def get_user_settings(self, user_id: UUID) -> UISettings:
        """Get user UI settings"""
        try:
            if str(user_id) not in self.user_settings:
                # Create default settings for user
                default_theme = next((t for t in self.themes.values() if t.is_default), None)
                default_layout = next((l for l in self.layouts.values() if l.is_default), None)
                
                if not default_theme or not default_layout:
                    raise ValueError("Default theme or layout not found")
                
                settings = UISettings(
                    id=str(uuid4()),
                    user_id=user_id,
                    theme_id=default_theme.id,
                    layout_id=default_layout.id,
                    font_settings=FontSettings(
                        family=FontFamily.JETBRAINS_MONO,
                        size=14,
                        weight=FontWeight.NORMAL,
                        style=FontStyle.NORMAL,
                        line_height=1.4,
                        letter_spacing=0.0,
                        ligatures=True,
                        created_at=datetime.utcnow()
                    ),
                    editor_settings=EditorSettings(
                        tab_size=4,
                        insert_spaces=True,
                        word_wrap=False,
                        line_numbers=True,
                        minimap=True,
                        scroll_beyond_last_line=False,
                        smooth_scrolling=True,
                        cursor_style=CursorStyle.LINE,
                        cursor_blinking=True,
                        cursor_width=2,
                        bracket_pair_colorization=True,
                        guides={"bracketPairs": True, "indentation": True, "guides": True},
                        rulers=[],
                        created_at=datetime.utcnow()
                    ),
                    animation_settings=AnimationSettings(
                        type=AnimationType.SMOOTH,
                        duration=0.3,
                        easing="ease-in-out",
                        enabled=True,
                        reduced_motion=False,
                        created_at=datetime.utcnow()
                    ),
                    panels=[],
                    views=[],
                    splits=[],
                    shortcuts=self.default_shortcuts.copy(),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                self.user_settings[str(user_id)] = settings
            
            return self.user_settings[str(user_id)]
            
        except Exception as e:
            logger.error(f"Failed to get user settings for {user_id}: {e}")
            raise
    
    async def update_user_settings(
        self, 
        user_id: UUID, 
        updates: Dict[str, Any]
    ) -> UISettings:
        """Update user UI settings"""
        try:
            settings = await self.get_user_settings(user_id)
            
            # Update theme if provided
            if "theme_id" in updates and updates["theme_id"] in self.themes:
                settings.theme_id = updates["theme_id"]
            
            # Update layout if provided
            if "layout_id" in updates and updates["layout_id"] in self.layouts:
                settings.layout_id = updates["layout_id"]
            
            # Update font settings if provided
            if "font_settings" in updates:
                font_data = updates["font_settings"]
                settings.font_settings.family = font_data.get("family", settings.font_settings.family)
                settings.font_settings.size = font_data.get("size", settings.font_settings.size)
                settings.font_settings.weight = font_data.get("weight", settings.font_settings.weight)
                settings.font_settings.style = font_data.get("style", settings.font_settings.style)
                settings.font_settings.line_height = font_data.get("line_height", settings.font_settings.line_height)
                settings.font_settings.letter_spacing = font_data.get("letter_spacing", settings.font_settings.letter_spacing)
                settings.font_settings.ligatures = font_data.get("ligatures", settings.font_settings.ligatures)
                settings.font_settings.updated_at = datetime.utcnow()
            
            # Update editor settings if provided
            if "editor_settings" in updates:
                editor_data = updates["editor_settings"]
                settings.editor_settings.tab_size = editor_data.get("tab_size", settings.editor_settings.tab_size)
                settings.editor_settings.insert_spaces = editor_data.get("insert_spaces", settings.editor_settings.insert_spaces)
                settings.editor_settings.word_wrap = editor_data.get("word_wrap", settings.editor_settings.word_wrap)
                settings.editor_settings.line_numbers = editor_data.get("line_numbers", settings.editor_settings.line_numbers)
                settings.editor_settings.minimap = editor_data.get("minimap", settings.editor_settings.minimap)
                settings.editor_settings.scroll_beyond_last_line = editor_data.get("scroll_beyond_last_line", settings.editor_settings.scroll_beyond_last_line)
                settings.editor_settings.smooth_scrolling = editor_data.get("smooth_scrolling", settings.editor_settings.smooth_scrolling)
                settings.editor_settings.cursor_style = editor_data.get("cursor_style", settings.editor_settings.cursor_style)
                settings.editor_settings.cursor_blinking = editor_data.get("cursor_blinking", settings.editor_settings.cursor_blinking)
                settings.editor_settings.cursor_width = editor_data.get("cursor_width", settings.editor_settings.cursor_width)
                settings.editor_settings.bracket_pair_colorization = editor_data.get("bracket_pair_colorization", settings.editor_settings.bracket_pair_colorization)
                settings.editor_settings.guides = editor_data.get("guides", settings.editor_settings.guides)
                settings.editor_settings.rulers = editor_data.get("rulers", settings.editor_settings.rulers)
                settings.editor_settings.updated_at = datetime.utcnow()
            
            # Update animation settings if provided
            if "animation_settings" in updates:
                animation_data = updates["animation_settings"]
                settings.animation_settings.type = animation_data.get("type", settings.animation_settings.type)
                settings.animation_settings.duration = animation_data.get("duration", settings.animation_settings.duration)
                settings.animation_settings.easing = animation_data.get("easing", settings.animation_settings.easing)
                settings.animation_settings.enabled = animation_data.get("enabled", settings.animation_settings.enabled)
                settings.animation_settings.reduced_motion = animation_data.get("reduced_motion", settings.animation_settings.reduced_motion)
                settings.animation_settings.updated_at = datetime.utcnow()
            
            # Update custom CSS/JS if provided
            if "custom_css" in updates:
                settings.custom_css = updates["custom_css"]
            
            if "custom_js" in updates:
                settings.custom_js = updates["custom_js"]
            
            # Update timestamp
            settings.updated_at = datetime.utcnow()
            
            # Save updated settings
            self.user_settings[str(user_id)] = settings
            
            logger.info(f"Updated UI settings for user {user_id}")
            return settings
            
        except Exception as e:
            logger.error(f"Failed to update user settings for {user_id}: {e}")
            raise
    
    async def apply_theme(self, user_id: UUID, theme_id: str, preview: bool = False) -> Theme:
        """Apply theme to user"""
        try:
            if theme_id not in self.themes:
                raise ValueError(f"Theme {theme_id} not found")
            
            theme = self.themes[theme_id]
            
            if not preview:
                # Update user settings
                await self.update_user_settings(user_id, {"theme_id": theme_id})
            
            logger.info(f"Applied theme {theme_id} to user {user_id}")
            return theme
            
        except Exception as e:
            logger.error(f"Failed to apply theme {theme_id} to user {user_id}: {e}")
            raise
    
    async def apply_layout(self, user_id: UUID, layout_id: str, preview: bool = False) -> Layout:
        """Apply layout to user"""
        try:
            if layout_id not in self.layouts:
                raise ValueError(f"Layout {layout_id} not found")
            
            layout = self.layouts[layout_id]
            
            if not preview:
                # Update user settings
                await self.update_user_settings(user_id, {"layout_id": layout_id})
            
            logger.info(f"Applied layout {layout_id} to user {user_id}")
            return layout
            
        except Exception as e:
            logger.error(f"Failed to apply layout {layout_id} to user {user_id}: {e}")
            raise
    
    async def create_theme(self, user_id: UUID, theme_data: Dict[str, Any]) -> Theme:
        """Create custom theme"""
        try:
            theme_id = f"custom-{user_id}-{hashlib.md5(theme_data['name'].encode()).hexdigest()[:8]}"
            
            theme = Theme(
                id=theme_id,
                name=theme_data["name"],
                display_name=theme_data["display_name"],
                description=theme_data["description"],
                type=theme_data["type"],
                color_scheme=theme_data["color_scheme"],
                author=f"User {user_id}",
                version="1.0.0",
                is_default=False,
                is_custom=True,
                colors=theme_data.get("colors", {}),
                token_colors=theme_data.get("token_colors", []),
                semantic_token_colors=theme_data.get("semantic_token_colors", {}),
                ui_colors=theme_data.get("ui_colors", {}),
                created_at=datetime.utcnow()
            )
            
            self.themes[theme_id] = theme
            
            logger.info(f"Created custom theme {theme_id} for user {user_id}")
            return theme
            
        except Exception as e:
            logger.error(f"Failed to create theme for user {user_id}: {e}")
            raise
    
    async def create_layout(self, user_id: UUID, layout_data: Dict[str, Any]) -> Layout:
        """Create custom layout"""
        try:
            layout_id = f"custom-{user_id}-{hashlib.md5(layout_data['name'].encode()).hexdigest()[:8]}"
            
            layout = Layout(
                id=layout_id,
                name=layout_data["name"],
                display_name=layout_data["display_name"],
                description=layout_data["description"],
                type=layout_data["type"],
                is_default=False,
                is_custom=True,
                panels=layout_data.get("panels", []),
                views=layout_data.get("views", []),
                splits=layout_data.get("splits", []),
                created_at=datetime.utcnow()
            )
            
            self.layouts[layout_id] = layout
            
            logger.info(f"Created custom layout {layout_id} for user {user_id}")
            return layout
            
        except Exception as e:
            logger.error(f"Failed to create layout for user {user_id}: {e}")
            raise
    
    async def add_shortcut(self, user_id: UUID, shortcut_data: Dict[str, Any]) -> Shortcut:
        """Add custom shortcut"""
        try:
            settings = await self.get_user_settings(user_id)
            
            shortcut = Shortcut(
                id=str(uuid4()),
                name=shortcut_data["name"],
                description=shortcut_data["description"],
                category=shortcut_data["category"],
                key=shortcut_data["key"],
                command=shortcut_data["command"],
                context=shortcut_data.get("context"),
                is_enabled=True,
                is_global=shortcut_data.get("is_global", False),
                is_custom=True,
                order=len(settings.shortcuts),
                created_at=datetime.utcnow()
            )
            
            settings.shortcuts.append(shortcut)
            settings.updated_at = datetime.utcnow()
            
            self.user_settings[str(user_id)] = settings
            
            logger.info(f"Added custom shortcut {shortcut.id} for user {user_id}")
            return shortcut
            
        except Exception as e:
            logger.error(f"Failed to add shortcut for user {user_id}: {e}")
            raise
    
    async def get_themes(self) -> List[Theme]:
        """Get all available themes"""
        try:
            return list(self.themes.values())
            
        except Exception as e:
            logger.error(f"Failed to get themes: {e}")
            return []
    
    async def get_layouts(self) -> List[Layout]:
        """Get all available layouts"""
        try:
            return list(self.layouts.values())
            
        except Exception as e:
            logger.error(f"Failed to get layouts: {e}")
            return []
    
    async def get_shortcuts(self, user_id: UUID) -> List[Shortcut]:
        """Get user shortcuts"""
        try:
            settings = await self.get_user_settings(user_id)
            return settings.shortcuts
            
        except Exception as e:
            logger.error(f"Failed to get shortcuts for user {user_id}: {e}")
            return []
    
    async def create_preview(self, user_id: UUID, preview_data: Dict[str, Any]) -> str:
        """Create UI preview"""
        try:
            preview_id = str(uuid4())
            
            # Store preview data
            self.previews[preview_id] = {
                "user_id": user_id,
                "data": preview_data,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=1)  # Preview expires in 1 hour
            }
            
            logger.info(f"Created UI preview {preview_id} for user {user_id}")
            return preview_id
            
        except Exception as e:
            logger.error(f"Failed to create preview for user {user_id}: {e}")
            raise
    
    async def get_preview(self, preview_id: str) -> Optional[Dict[str, Any]]:
        """Get preview data"""
        try:
            if preview_id not in self.previews:
                return None
            
            preview = self.previews[preview_id]
            
            # Check if preview has expired
            if datetime.utcnow() > preview["expires_at"]:
                del self.previews[preview_id]
                return None
            
            return preview["data"]
            
        except Exception as e:
            logger.error(f"Failed to get preview {preview_id}: {e}")
            return None
    
    async def get_ui_statistics(self, user_id: UUID) -> Dict[str, Any]:
        """Get UI statistics"""
        try:
            settings = await self.get_user_settings(user_id)
            
            custom_themes = len([t for t in self.themes.values() if t.is_custom])
            custom_layouts = len([l for l in self.layouts.values() if l.is_custom])
            custom_shortcuts = len([s for s in settings.shortcuts if s.is_custom])
            
            return {
                "total_themes": len(self.themes),
                "total_layouts": len(self.layouts),
                "total_shortcuts": len(settings.shortcuts),
                "active_theme": self.themes[settings.theme_id].display_name,
                "active_layout": self.layouts[settings.layout_id].display_name,
                "custom_themes": custom_themes,
                "custom_layouts": custom_layouts,
                "custom_shortcuts": custom_shortcuts,
                "created_at": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Failed to get UI statistics for user {user_id}: {e}")
            return {}


# Global instance
ui_service = UIService()
