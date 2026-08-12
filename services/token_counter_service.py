import os
import tiktoken

# ================= GLOBAL CONFIGURATION =================
TOKENIZERS = {
    "gpt-4o": "o200k_base",
    "gpt-4": "cl100k_base",
    "gpt-3.5": "cl100k_base",
    "codex": "p50k_base"
}

# Only files matching these extensions will be read and counted
ALLOWED_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.txt', 
    '.md', '.json', '.html', '.css', '.yaml', '.yml'
}

# Directories completely skipped to save processing time
IGNORE_DIRS = {
    '.git', 'node_modules', '__pycache__', 'venv', '.idea', '.vscode'
}
# ========================================================

def count_project_tokens(path, model_name="gpt-4o"):
    """Recursively counts tokens strictly for allowed extensions."""
    if model_name not in TOKENIZERS:
        raise ValueError(f"Unknown model. Choose from: {list(TOKENIZERS.keys())}")
        
    encoding = tiktoken.get_encoding(TOKENIZERS[model_name])
    total_tokens = 0
    total_files = 0
    scanned_extensions = set()

    # Handle a single file path input
    if os.path.isfile(path):
        _, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext in ALLOWED_EXTENSIONS:
            scanned_extensions.add(ext)
            return count_file_tokens(path, encoding), scanned_extensions
        return 0, scanned_extensions

    # Handle directory tree traversal
    for root, dirs, files in os.walk(path):
        # Modify dirs in-place to prevent os.walk from even opening ignored folders
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            _, ext = os.path.splitext(file)
            ext = ext.lower()
            
            if ext in ALLOWED_EXTENSIONS:
                scanned_extensions.add(ext)
                file_path = os.path.join(root, file)
                total_tokens += count_file_tokens(file_path, encoding)
                total_files += 1
    return total_tokens, sorted(list(scanned_extensions)), total_files

def count_file_tokens(file_path, encoding):
    """Helper to safely read a file and return token count."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return len(encoding.encode(f.read()))
    except Exception as e:
        print(f"Skipping {file_path} due to error: {e}")
        return 0

# --- Example Usage ---
if __name__ == "__main__":
    project_path = "C:/Users/lubun/Downloads/carpets-lead/carpets-lead"
    chosen_model = "gpt-4o" 
    
    total, extensions = count_project_tokens(project_path, model_name=chosen_model)
    
    print(f"--- Analysis for '{project_path}' ---")
    print(f"Scanned extensions: {', '.join(extensions) if extensions else 'None'}")
    print(f"Total tokens: {total:,}")
