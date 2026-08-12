# Token Counter Pro

A modern, user-friendly desktop application for analyzing token usage in your codebase. Built with Python and CustomTkinter, featuring a sleek interface with multiple theme options.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## Features

- **Fast Analysis** - Recursively scans your project folders in seconds
- **Multiple Themes** - Switch between beautiful color schemes on the fly
- **Smart Statistics** - Get detailed token counts, file counts, and extension analysis
- **Drag & Drop** - Simply drag your project folder into the app
- **Persistent Settings** - Remembers your theme preferences
- **Local Processing** - All analysis happens locally, no data leaves your machine
- **Smart Filtering** - Automatically skips unnecessary directories (node_modules, .git, etc.)

## Supported Models

The app supports multiple OpenAI tokenizer models:

| Model | Tokenizer | Description |
|-------|-----------|-------------|
| GPT-4o | o200k_base | Latest OpenAI model |
| GPT-4 | cl100k_base | GPT-4 series |
| GPT-3.5 | cl100k_base | GPT-3.5 Turbo |
| Codex | p50k_base | Code-focused model |

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/token-counter-pro.git
cd token-counter-pro