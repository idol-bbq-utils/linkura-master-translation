import argparse
import sys
from pathlib import Path
from src.generate import analyze
from src.model.localization import I18nLanguage
from src.translate import translate_file, claude
import os

i18n = [lang.value for lang in I18nLanguage]
i18n_map = {lang.value: lang for lang in I18nLanguage}
OUTPUT_DIR = Path("data")
RAW_DIR = Path("raw")
README_FILE = Path("README.md")


def command_gentodo(args):
    """From raw file to translation todo file"""
    from src.gentodo import basic_gen
    
    input_dir = args.input if hasattr(args, 'input') and args.input else RAW_DIR
    output_dir = args.output if hasattr(args, 'output') and args.output else OUTPUT_DIR
    
    print(f"Extracting Japanese content from {input_dir} to {output_dir}")
    
    try:
        basic_gen(Path(input_dir), Path(output_dir))
        print("gentodo command completed successfully!")
        return 0
    except Exception as e:
        print(f"Error executing gentodo: {e}")
        return 1

def command_translate(args):
    """
    Translation tool, providing basic large model API translation interface

    And user also can translated by handmade
    """
    if args.file:
        client = claude.setup_client(os.environ["ANTHROPIC_API_KEY"], os.environ["ANTHROPIC_BASE_URL"])
        limit = args.limit if hasattr(args, 'limit') and args.limit else None
        translate_file(client, Path(args.file), i18n_map.get(args.locale, I18nLanguage.ZH_CN), limit=limit)
    return 0

def command_generate(args):
    """Generate translated files and progress reports"""
    (total, translated) = analyze.analyze_translation_progress(OUTPUT_DIR, locale=args.locale)
    analyze.write_translation_progress(README_FILE, total, translated, locale=args.locale)
    # print(f"Progress report updated in {README_FILE}")
    return 0

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Linkura Translation Tool Template",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--locale', '-l',
        default='zh-CN',
        choices=i18n,
        help='Translation locale'
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        metavar='COMMAND'
    )
    # gentodo
    parser_gentodo = subparsers.add_parser(
        'gentodo',
        help='From raw file to translation todo file',
    )
    parser_gentodo.add_argument(
        '--input', '-i',
        default='raw',
        help='Input directory containing JSON files (default: raw)'
    )
    parser_gentodo.add_argument(
        '--output', '-o', 
        default='data',
        help='Output directory for translation files (default: data)'
    )
    parser_gentodo.set_defaults(func=command_gentodo)
    
    # translate
    parser_translate = subparsers.add_parser(
        'translate',
        help='Translation tool, providing basic large model API translation interface',
    )
    parser_translate.add_argument(
        '--file', '-f',
        help='Path to the input file containing text to translate'
    )
    parser_translate.add_argument(
        '--limit',
        type=int,
        help='Maximum number of items to translate (default: translate all untranslated items)'
    )
    parser_translate.set_defaults(func=command_translate)
    
    # generate
    parser_generate = subparsers.add_parser(
        'generate',
        help='Generate translated files and progress reports',
    )
    parser_generate.add_argument(
        '--about', '-a',
        help='Example for sub args'
    )
    parser_generate.set_defaults(func=command_generate)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        return args.func(args)
    except Exception as e:
        print(f"Error occurred while executing command: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())