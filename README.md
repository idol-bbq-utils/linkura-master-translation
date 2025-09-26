# gakumas-master-translation


简体中文 | [English](README_EN.md)



# 使用脚本更新

 - `make update` 更新 MasterDB 的 `orig` 和 `json` 文件
 - `make gen-todo` 生成待翻译文件到 `data` 文件夹内
   - 可以使用 `python main.py --locale zh-CN translate --limit 100 -f data/Stickers.json` 执行大模型翻译
   - 如 `ANTHROPIC_API_KEY=key ANTHROPIC_BASE_URL=https://api_url/ python main.py --locale zh-CN translate --limit 9600 -f data/Stickers.json`
 - 翻译完成后可使用 `python main.py --locale zh-CN generate` 来生成汉化进度统计



# 手动运行

## 全新翻译流程

 - 首先执行 `gakumasu_diff_to_json.py` 将 gakumasu-diff 这个仓库的 yaml 转为插件能识别的 json，这时候 json 内容是日文原文
 - 然后执行 `export_db_json.py` 将第一步生成的 json 转为 `key: 日文原文` 形式
 - 运行 `pretranslate_process.py`，选 `1`，将 `key: 日文原文` 转为 `日文: ""` 用于 pretranslate
 - 然后自行 pretranslate，得到 `日文: 中文` 文件
 - 完成后再次运行 `pretranslate_process.py`，选 `3`，将 pretranslate 后的 `日文: 中文` 转为 `key: 中文` 文件
 - 最后运行 `import_db_json.py` 将 `key: 中文` 文件转为插件能识别的 json 文件

## 基于旧文件更新

1. 生成 todo 文件: 运行 `pretranslate_process.py` 选 2。旧的翻译数据在 `data` 内，新的文件使用 `gakumasu_diff_to_json` 生成
2. 预翻译完成后，将新文件放入 `todo/new` 内，运行 `pretranslate_process.py` 选 4

## translation progress

![translation zh-CN](https://img.shields.io/badge/translation_zh--CN-28909%2F29413-blue)

---
