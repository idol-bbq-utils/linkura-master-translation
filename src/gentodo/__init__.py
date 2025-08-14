import json
import re
from pathlib import Path

def extract_japanese_texts(data):
    """
    Extract Japanese text from JSON data
    Converts Unicode escape sequences to UTF-8 and filters for Japanese characters
    """
    import re
    
    japanese_texts = []
    
    def decode_unicode_escapes(text):
        """Safely decode Unicode escape sequences in text"""
        def replace_unicode(match):
            try:
                code = int(match.group(1), 16)
                return chr(code)
            except (ValueError, OverflowError):
                return match.group(0)  # Return original if can't decode
        
        # Handle \uXXXX patterns
        unicode_pattern = re.compile(r'\\u([0-9a-fA-F]{4})')
        return unicode_pattern.sub(replace_unicode, text)
    
    def process_item(item):
        if isinstance(item, dict):
            # Look for 'value' field in dictionary items
            if 'value' in item:
                text = item['value']
                if isinstance(text, str) and text.strip():
                    # Convert Unicode escape sequences to actual characters
                    decoded_text = decode_unicode_escapes(text)
                    # Check if text contains Japanese characters
                    if is_japanese_text(decoded_text):
                        japanese_texts.append(decoded_text)
            # Recursively process other values
            for value in item.values():
                process_item(value)
        elif isinstance(item, list):
            for element in item:
                process_item(element)
        elif isinstance(item, str) and item.strip():
            # Process string directly
            decoded_text = decode_unicode_escapes(item)
            if is_japanese_text(decoded_text):
                japanese_texts.append(decoded_text)
    
    process_item(data)
    return japanese_texts


def is_japanese_text(text):
    """
    Check if text contains Japanese characters (Hiragana, Katakana, Kanji)
    """
    if not text:
        return False
    
    # Japanese Unicode ranges:
    # Hiragana: U+3040-U+309F
    # Katakana: U+30A0-U+30FF
    # CJK Unified Ideographs (Kanji): U+4E00-U+9FAF
    # Full-width characters: U+FF00-U+FFEF
    japanese_ranges = [
        (0x3040, 0x309F),  # Hiragana
        (0x30A0, 0x30FF),  # Katakana
        (0x4E00, 0x9FAF),  # CJK Unified Ideographs (Kanji)
        (0xFF00, 0xFFEF),  # Full-width forms
    ]
    
    for char in text:
        char_code = ord(char)
        for start, end in japanese_ranges:
            if start <= char_code <= end:
                return True
    return False

def basic_gen_file(input_file: Path, output_file: Path):
    """
    Process a single JSON file, extract Japanese text and generate TranslatedItem list with incremental updates
    """
    from ..model.localization import TranslatedItem, I18nLanguage
    
    try:
        # Read JSON file
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract Japanese text
        japanese_texts = extract_japanese_texts(data)
        
        # Remove duplicates and sort Japanese texts
        unique_texts = sorted(list(set(japanese_texts)))
        
        # Load existing output file if it exists
        existing_items = {}
        existing_raw_set = set()
        
        if output_file.exists():
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    for item_data in existing_data:
                        raw_text = item_data.get("raw", "")
                        existing_raw_set.add(raw_text)
                        existing_items[raw_text] = item_data
            except Exception as e:
                print(f"Warning: Could not read existing output file {output_file}: {e}")
        
        # Get all available I18nLanguage values for consistency
        all_languages = set(I18nLanguage)
        
        # Create or update TranslatedItems
        updated_items = {}
        new_items_count = 0
        updated_items_count = 0
        
        # Process new Japanese texts
        for text in unique_texts:
            if text in existing_items:
                # Update existing item with any missing language keys
                existing_item = existing_items[text]
                translation = existing_item.get("translation", {})
                
                # Check if we need to add missing language keys
                needs_update = False
                for lang in all_languages:
                    lang_key = lang.value
                    if lang_key not in translation:
                        translation[lang_key] = {"text": "", "author": ""}
                        needs_update = True
                
                if needs_update:
                    updated_items_count += 1
                    existing_item["translation"] = translation
                
                updated_items[text] = existing_item
            else:
                # Create new item
                new_items_count += 1
                new_item = {
                    "raw": text,
                    "translation": {
                        lang.value: {"text": "", "author": ""}
                        for lang in all_languages
                    }
                }
                updated_items[text] = new_item
        
        # Add existing items that weren't in the new extraction (preserve existing translations)
        for raw_text, item_data in existing_items.items():
            if raw_text not in updated_items:
                # Still need to check for missing language keys in preserved items
                translation = item_data.get("translation", {})
                needs_update = False
                
                for lang in all_languages:
                    lang_key = lang.value
                    if lang_key not in translation:
                        translation[lang_key] = {"text": "", "author": ""}
                        needs_update = True
                
                if needs_update:
                    updated_items_count += 1
                    item_data["translation"] = translation
                
                updated_items[raw_text] = item_data
        
        # Sort all items by raw text for consistent output
        sorted_items = [updated_items[key] for key in sorted(updated_items.keys())]
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write results to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sorted_items, f, ensure_ascii=False, indent=2)
        
        # Log incremental update statistics
        total_items = len(sorted_items)
        print(f"  Incremental update stats:")
        print(f"    - New items added: {new_items_count}")
        print(f"    - Existing items updated: {updated_items_count}")
        print(f"    - Total items in file: {total_items}")
        
        return new_items_count
        
    except Exception as e:
        print(f"Error processing file {input_file}: {e}")
        return 0


def basic_gen(input_dir: Path, output_dir: Path):
    """
    Recursively process all JSON files in input directory, maintaining file structure
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    
    # Check that input and output directories are not the same
    if input_dir.resolve() == output_dir.resolve():
        raise ValueError("Input and output directories cannot be the same")
    
    # Check if input directory exists
    if not input_dir.exists():
        raise ValueError(f"Input directory does not exist: {input_dir}")
    
    # Statistics for processed files and extracted Japanese items
    processed_files = 0
    total_japanese_items = 0
    
    # Recursively find all JSON files
    json_files = list(input_dir.rglob("*.json"))
    
    if not json_files:
        print(f"No JSON files found in directory {input_dir}")
        return
    
    print(f"Found {len(json_files)} JSON files")
    
    for json_file in json_files:
        try:
            # Calculate relative path
            relative_path = json_file.relative_to(input_dir)
            
            # Construct output file path, maintaining the same file structure and filename
            output_file = output_dir / relative_path
            
            print(f"Processing file: {json_file} -> {output_file}")
            
            # Process single file
            item_count = basic_gen_file(json_file, output_file)
            
            if item_count > 0:
                processed_files += 1
                total_japanese_items += item_count
                print(f"  Extracted {item_count} Japanese items")
            else:
                print(f"  No Japanese content found")
                
        except Exception as e:
            print(f"Error processing file {json_file}: {e}")
            continue
    
    print(f"\nProcessing completed:")
    print(f"- Successfully processed files: {processed_files}")
    print(f"- Total Japanese items extracted: {total_japanese_items}")
    print(f"- Output directory: {output_dir}")
