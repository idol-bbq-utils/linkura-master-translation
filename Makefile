update:
	cd link-like-diff/orig && git fetch && git checkout origin/main
	python3 scripts/linkura_diff_to_json.py

gen-todo:
	python3 main.py gentodo -i link-like-diff/json/

merge:
	python3 scripts/pretranslate_process.py --merge
