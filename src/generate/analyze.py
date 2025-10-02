from typing import Set, Tuple
from pathlib import Path
import os
import json


def load_json_as_sets(file_path: Path, key = "raw") -> Set[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Invalid `data` / `raw` json format")
        res = set()
        for item in data:
            if isinstance(item, str):
                res.add(item)
            elif isinstance(item, dict):
                res.add(item[key])
        return res

def load_locale_count(file_path: Path, locale = "zh-CN") -> int:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Invalid locale json format")
        count = 0
        for item in data:
            if not isinstance(item, dict):
                continue
            if locale in item["translation"] and item["translation"][locale]["text"]:
                count += 1
        return count

def analyze_translation_progress(data_dir: Path, locale: str = "zh-CN")-> Tuple[int, int]: 
    """
    Analyze translation progress, recursively traverse directory structure
    
    Args:
        data_dir: Data directory path
        locale: Language code
        
    Returns:
        Tuple[int, int]: (total count, translated count)
    """
    raw_strings = set()
    translated_strings = 0
    
    # Recursively find all JSON files
    data_path = Path(data_dir)
    if not data_path.exists():
        return (0, 0)
    
    json_files = list(data_path.rglob("*.json"))
    
    for json_file in json_files:
        try:
            raw_strings.update(load_json_as_sets(json_file, "raw"))
            translated_strings += load_locale_count(json_file, locale)
        except Exception as e:
            print(f"Error processing file {json_file}: {e}")
            continue

    total = len(raw_strings)
    translated = translated_strings
    return (total, translated)

def write_translation_progress(readme_file: Path, total: int, translated: int, locale: str = "zh-CN"):
    """
    Update translation progress badge in README.md
    
    Args:
        total: Total string count
        translated: Translated string count
        locale: Language code
    """
    # Generate new badge URL
    sheilds_locale = locale.replace('-', '--')
    badge_url = f"![translation {locale}](https://img.shields.io/badge/translation_{sheilds_locale}-{translated/total*100:.1f}%25%7C{translated}%2F{total}-blue)"

    try:
        with open(readme_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        # If README.md doesn't exist, create a basic structure
        lines = [
            "# translation\n",
            "\n",
            "---\n",
            "\n", 
            "## translation progress\n",
            "\n",
            "---\n"
        ]
    
    # Find translation progress section
    start_idx = None
    end_idx = None
    
    for i, line in enumerate(lines):
        if "## translation progress" in line.lower():
            start_idx = i
        elif start_idx is not None and line.strip() == "---":
            end_idx = i
            break
    
    if start_idx is None:
        # If translation progress section is not found, add at the end of the file
        lines.extend([
            "\n",
            "## translation progress\n",
            "\n",
            f"{badge_url}\n",
            "\n",
            "---\n"
        ])
    else:
        # Search for existing badge in translation progress section
        locale_found = False
        badge_pattern = f"translation_{sheilds_locale}"
        
        # Search and replace existing locale badge
        for i in range(start_idx + 1, end_idx if end_idx else len(lines)):
            if badge_pattern in lines[i]:
                lines[i] = f"{badge_url}\n"
                locale_found = True
                break
        
        # If no existing locale badge found, add new one
        if not locale_found:
            if end_idx is not None:
                # Insert new badge before ---
                lines.insert(end_idx, f"{badge_url}\n")
            else:
                # If no end marker, add at the end of section
                lines.append(f"{badge_url}\n")
                lines.append("---\n")
    
    # Write back to file
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"Update {locale} translation progress: {translated}/{total} ({translated/total*100:.1f}%)")
