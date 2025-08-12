# gakumas-master-translation


[简体中文](README.md) | English



# Updating with Scripts

- Use `make update` to update the MasterDB (`orig` and `json`) file.
- Use `make gen-todo` to generate files to be translated into the `pretranslate_todo/todo` folder.
  - Manually copy the files from `pretranslate_todo/todo` into `gakumas-generic-strings-translation/working/todo`. Then, run `make pretranslate` in the `gakumas-generic-strings-translation`.
  - After translation is complete, copy the files from `gakumas-generic-strings-translation/working/new` into `pretranslate_todo/todo/new`. If the `new` folder does not exist, create it manually.
- Use `make merge` to merge the files from `pretranslate_todo/todo/new` into `data`.
- Once all processes are completed, please manually clear the `pretranslate_todo` folder.



# Manual Execution

## Full Translation Workflow

1. First, run `gakumasu_diff_to_json.py` to convert the YAML files from the `gakumasu-diff` repository into JSON files readable by the plugin. At this stage, the JSON contains the original Japanese text.
2. Run `export_db_json.py` to convert the generated JSON into the `key: original Japanese text` format.
3. Execute `pretranslate_process.py` and select option `1` to convert `key: original Japanese text` into `Japanese: ""` format for pre-translation.
4. Perform pre-translation manually to obtain a `Japanese: Chinese` file.
5. Once completed, run `pretranslate_process.py` again and select option `3` to convert the pre-translated `Japanese: Chinese` file into the `key: Chinese` format.
6. Finally, execute `import_db_json.py` to convert the `key: Chinese` file into a JSON file readable by the plugin.

## Updating Based on Old Files

1. Generate the `todo` files by running `pretranslate_process.py` and selecting option `2`. The old translation data is located in the `data` directory, and new files are generated using `gakumasu_diff_to_json`.
2. After pre-translation is complete, place the new files into `todo/new` and run `pretranslate_process.py`, selecting option `4`.
