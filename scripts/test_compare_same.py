import json
import os


def compare_json_folders(folder1, folder2):
    """
    比较两个文件夹中的 JSON 文件内容是否一致。

    Args:
        folder1 (str): 第一个文件夹路径。
        folder2 (str): 第二个文件夹路径。

    Returns:
        dict: 返回一个字典，包含比较结果：
            - "matched": 两个文件夹中内容一致的文件列表。
            - "mismatched": 内容不同的文件列表。
            - "missing_in_folder2": 在 folder1 中存在但在 folder2 中不存在的文件列表。
            - "missing_in_folder1": 在 folder2 中存在但在 folder1 中不存在的文件列表。
    """
    result = {
        "matched": [],
        "mismatched": [],
        "missing_in_folder2": [],
        "missing_in_folder1": []
    }

    # 获取两个文件夹中的 JSON 文件名
    files1 = {f for f in os.listdir(folder1) if f.endswith('.json')}
    files2 = {f for f in os.listdir(folder2) if f.endswith('.json')}

    # 找出仅存在于一个文件夹中的文件
    result["missing_in_folder2"] = list(files1 - files2)
    result["missing_in_folder1"] = list(files2 - files1)

    # 比较两个文件夹中共有文件的内容
    common_files = files1 & files2

    for file_name in common_files:
        path1 = os.path.join(folder1, file_name)
        path2 = os.path.join(folder2, file_name)

        try:
            with open(path1, 'r', encoding='utf-8') as f1, open(path2, 'r', encoding='utf-8') as f2:
                json1 = json.load(f1)
                json2 = json.load(f2)

            if json1 == json2:
                result["matched"].append(file_name)
            else:
                result["mismatched"].append(file_name)
        except Exception as e:
            print(f"Error comparing {file_name}: {e}")

    return result


folder1 = input("文件夹1: ")
folder2 = input("文件夹2: ")
comparison_result = compare_json_folders(folder1, folder2)

print("Matched files:", comparison_result["matched"])
print("Mismatched files:", comparison_result["mismatched"])
print("Missing in folder2:", comparison_result["missing_in_folder2"])
print("Missing in folder1:", comparison_result["missing_in_folder1"])
# Mismatched files: ['ProduceChallengeSlot.json', 'ProduceNavigation.json', 'ProduceCardCustomize.json']
