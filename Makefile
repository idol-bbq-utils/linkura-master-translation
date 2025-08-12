update:
	cd link-like-diff/orig && git fetch && git checkout origin/main
	python scripts/linkura_diff_to_json.py

gen-todo:
	python scripts/pretranslate_process.py --gen_todo

merge:
	python scripts/pretranslate_process.py --merge
