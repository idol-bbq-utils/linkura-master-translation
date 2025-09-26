update:
	cd link-like-diff/orig && git fetch && git checkout origin/main
	python scripts/linkura_diff_to_json.py

gen-todo:
	python main.py gentodo -i link-like-diff/json/

merge:
	python scripts/pretranslate_process.py --merge
