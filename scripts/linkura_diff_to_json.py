import os
import yaml
import json
from typing import List
from yaml.reader import Reader


primary_key_rules = {
    "AdvDatas": [["Id"], ["Name"]],
    "AdvSeries": [["Id"], ["Name", "Description"]],
    "AdvStoryDigestMovies": [["Id"], ["Title"]],
    "BeginnerMissionBannerRewards": [[], []],
    "BeginnerMissionsHint": [["Id"], ["Name", "Description"]],
    # "BeginnerMissionsHintImages": [[], []],
    # "BirthdayRareBonuses": [["Id"], ["SkillName"]],
    "Campaign": [["Id"], ["Name", "Description"]],
    # "CampaignAddRewards": [[], []],
    # "CampaignAddRewardSeries": [[], []],
    # "CardCoordinates": [[], []],
    "CardDatas": [["Id"], ["Name", "Description"]],
    # "CardDuetVoice": [[], []],
    # "CardEvolutionMaterials": [[], []],
    # "CardGetMovieSettings": [[], []],
    # "CardLevels": [[], []],
    # "CardLimitBreakMaterials": [[], []],
    # "CardRarities": [[], []],
    # "CardSeries": [[], []],
    # "CardSkillEffectDetailParams": [[], []],
    # "CardSkillEffectDetails": [[], []],
    # "CardSkillEffects": [[], []],
    # "CardSkillLevelUpMaterials": [[], []],
    "CardSkills": [["Id"], ["Description"]],
    "CardSkillSeries": [["Id"], ["Name"]],
    # "CenterAttributeEffects": [[], []],
    "CenterAttributes": [["Id"], ["CenterAttributeName", "Description"]],
    # "CenterSkillConditions": [[], []],
    # "CenterSkillEffects": [[], []],
    "CenterSkills": [["Id"], ["CenterSkillName", "Description"]],
    # "ChallengeModeEffectDetails": [[], []],
    # "ChallengeModeEffects": [[], []],
    # "ChallengeModeReleaseCondition": [[], []],
    # "ChallengeModeStages": [[], []],
    # "CharacterFavoriteGifts": [[], []],
    "Characters": [["Id"], ["NameLast", "NameFirst", "CharacterVoice", "Introduction", "DisplayFullName"]],
    "Comics": [["Id"], ["Name"]],
    # "CommonMissions": [[], []],
    # "ContentGuidances": [[], []],
    # "ContentsReleaseConditions": [[], []],
    # "CostumeModels": [["Id"], ["Label"]], # 似乎不能汉化
    # "Costumes": [["Id"], ["Label"]], # 似乎不能汉化
    # "CustomComplementMaterials": [["Id"], ["Name"]], # 似乎不能汉化
    # "DailyLiveReleaseConditions": [[], []],
    "DailyQuestSeries": [["Id"], ["Name", "Description"]],
    "DailyQuestStages": [["Id"], ["Name", "Description", "Hint"]],
    # "DeckMemberPositions": [[], []],
    # "DifficultyBgImages": [[], []],
    "DownloadImages": [["Id"], ["Title"]],
    # "DreamLiveReleaseConditions": [[], []],
    # "DreamLiveSeriesList": [[], []],
    "DreamQuestSeries": [["Id"], ["Name"]],
    "DreamQuestStages": [["Id"], ["Name", "Description"]],
    "EmojiCategory": [["Id"], ["Name"]],
    # "Emojis": [["Id"], ["Name"]], # 似乎不能汉化
    "EventLoginBonuses": [["Id"], ["Name"]],
    # "EventMissionAchieveRewards": [[], []],
    # "EventMissionRewards": [[], []],
    "EventMissions": [["Id"], ["Name", "Description"]],
    "EventMissionSeries": [["Id"], ["Name", "Description"]],
    # "ExchangePointConvert": [[], []],
    # "ExchangePointRate": [[], []],
    "FlowerStandColors": [["Id"], ["Name"]],
    "FlowerStandIdolPictures": [["Id"], ["Name"]],
    "FlowerStandTypes": [["Id"], ["Name"]],
    "GachaCampaigns": [["Id"], ["CampaignName"]],
    # "GachaSeries": [["Id"], ["NoticeText", "Description"]], # 不汉化
    # "Generations": [["Id"], ["Name"]],
    # "GiftBonusGachas": [[], []],
    # "GiftlessGachas": [[], []],
    # "GpPrizeExchanges": [[], []],
    "Grade": [["Id"], ["Name"]],
    # "GradeAddSkillEffectDetails": [[], []],
    # "GradeAddSkillEffects": [[], []],
    "GradeAddSkills": [["Id"], ["Name", "Description"]],
    # "GradeChalQuestStageRewardDatas": [[], []],
    "GradeChalQuestStages": [["Id"], ["Name"]],
    # "GradeChalQuestStagesRewards": [[], []],
    # "GradeChalSeason": [["Id"], ["Name"]],
    # "GradeChalTotalScoreRewardDatas": [[], []],
    # "GradeChalTotalScoreRewards": [[], []],
    # "GradeDatas": [[], []],
    "GradeQuestLivePointBonus": [["Id"], ["Description"]],
    "GradeQuestRewards": [["Id"], ["ConditionsDescription"]],
    # "GradeQuestRewardsDatas": [[], []],
    "GradeQuestSeason": [["Id"], ["Name"]],
    "GradeQuestSeasonReleaseCond": [["Id"], ["ConditionsDescription"]],
    "GradeQuestSeries": [["Id"], ["Name"]],
    # "GradeQuestSeriesReleaseCond": [[], []],
    # "GradeQuestSquare": [[], []],
    # "GradeQuestSquareDatas": [[], []],
    "GradeQuestStages": [["Id"], ["Name", "Description"]],
    # "GradeRewardDatas": [[], []],
    # "GradeRewards": [[], []],
    "GrandPrix": [["Id"], ["Name", "Description"]],
    # "GrandPrixDailyPoints": [[], []],
    # "GrandPrixPointBonuses": [[], []],
    # "GrandPrixQuestSeries": [["Id"], ["Name", "Description"]],
    # "GrandPrixQuestStages": [["Id"], ["Name", "Description"]],
    # "GrandPrixReleaseCondition": [[], []],
    # "GrandPrixRewardDatas": [[], []],
    # "GrandPrixRewards": [[], []],
    "HelpImages": [["Id"], ["Name"]],
    # "HomeBgms": [[], []],
    # "ItemExchanges": [[], []],
    "Items": [["Id"], ["Name", "NameFurigana", "Description"]],
    # "ItemSources": [[], []],
    # "LauncherBanners": [[], []],
    # "LearningLiveReleaseConditions": [[], []],
    # "LimitBreakMaterialConvertRate": [[], []],
    # "LimitBreakMaterialRate": [[], []],
    "LiveChannels": [["Id"], ["Name", "Description"]],
    "LiveCharacters": [["Id"], ["Label"]],
    # "LiveEventsEvol": [[], []],
    # "LiveItems": [[], []],
    # "LiveLocations": [["Id"], ["Label"]], # 似乎不用汉化
    # "LiveMovies": [[], []],
    # "LiveMusic": [["Id"], ["Label"]], # 不确定是否需要汉化
    # "LivePoses": [["Id"], ["Label"]], # 似乎不用汉化
    # "LiveProps": [["Id"], ["Label"]], # 似乎不用汉化
    "LiveStages": [["Id"], ["Name", "Description", "StageSkillDescription"]],
    # "LiveTimelinesEvol": [["Id"], ["Label"]],  # 不确定是否需要汉化
    "LoginBonuses": [["Id"], ["Name"]],
    # "LoginBonusRewardDatas": [[], []],
    # "MemberFanLevels": [[], []],
    "MemberMovies": [["Id"], ["Name"]],
    "MemberVoices": [["Id"], ["Name"]],
    # "MissionAchieveRewards": [[], []],
    # "MissionRewards": [[], []],
    "Missions": [["Id"], ["Name", "Description"]],
    # "MusicDropRewardDetails": [[], []],
    # "MusicDropRewards": [[], []],
    "MusicLearningQuestSeries": [["Id"], ["Name"]],
    "MusicLearningQuestStages": [["Id"], ["Name", "Description"]],
    # "MusicLevels": [[], []],
    # "MusicMasteryHeartBonuses": [[], []],
    # "MusicMasteryLevels": [[], []],
    # "MusicMasteryLoveBonuses": [[], []],
    # "MusicMasteryMentalBonuses": [[], []],
    "MusicMasterySkill": [["Id"], ["MusicMasterySkillsName"]],
    # "MusicMasteryVoltageBonuses": [[], []],
    "Musics": [["Id"], ["Title", "TitleFurigana", "Description", "ReleaseConditionText"]],
    # "MusicScoreRewardDatas": [[], []],
    # "MusicScoreRewards": [[], []],
    # "MusicScores": [[], []],
    # "PetalCoinExchangeRate": [[], []],
    # "PetalExchangeRates": [[], []],
    "PresentTexts": [["Id"], ["Description"]],
    # "QuestAreaReleaseConditions": [[], []],
    "QuestLiveDownloads": [["Id"], ["Title"]],
    "QuestLiveLoadings": [["Id"], ["Title"]],
    # "QuestLiveReleaseConditions": [[], []],
    # "QuestSections": [[], []],
    # "RaidEvents": [["Id"], ["Name", "Description"]], # 不确定是否需要汉化
    "RaidQuestDropRateUp": [["Id"], ["Name"]],
    # "RaidQuestReleaseCondition": [[], []],
    "RaidQuestSeries": [["Id"], ["Name", "Description"]],
    "RaidQuestStages": [["Id"], ["Name", "Description"]],
    # "RaidResource": [[], []],
    # "RaidResourceAddDate": [[], []],
    # "RaidResourceRecoveryDatas": [[], []],
    # "RaidRewardDatas": [[], []],
    # "RaidRewards": [[], []],
    # "RaidTopProgressImage": [[], []],
    # "RentalCardDatas": [[], []],
    # "RentalDeckCards": [[], []],
    "RentalDecks": [["Id"], ["DeckName"]],
    # "RhythmGameClassDatas": [[], []],
    # "RhythmGameClassMissionRewards": [[], []],
    # "RhythmGameClasses": [[], []],
    "RhythmGameHelpImages": [["Id"], ["Name"]],
    # "RhythmGameSkillConditions": [[], []],
    # "RhythmGameSkillEffects": [[], []],
    # "RhythmGameSkillLvUpItemDetails": [[], []],
    # "RhythmGameSkillLvUpItems": [[], []],
    "RhythmGameSkills": [["Id"], ["RhythmGameSkillName", "Description"]],
    # "RhythmGameTotalMissionRewards": [[], []],
    "RhythmGameTotalMissions": [["Id"], ["Description"]],
    # "SeasonFanLevels": [[], []],
    "SeasonGrade": [["Id"], ["Description", "TermTitle"]],
    # "SeasonGradeRewardDatas": [[], []],
    # "SeasonGradeRewards": [[], []],
    "Seasons": [["Id"], ["Name"]],
    # "SectionSkillEffectDetails": [[], []],
    # "SectionSkillEffects": [[], []],
    "SectionSkills": [["Id"], ["Description"]],
    # "SelectTicketExchangeRate": [[], []],
    "SelectTicketSeries": [["Id"], ["ExchangeTicketName", "Description"]],
    # "ShopItems": [[], []],
    "Shops": [["Id"], ["Name"]],
    # "SideStyleSettings": [[], []],
    # "SimulationGraphLimit": [[], []],
    # "StageSkillConditionDetails": [[], []],
    # "StageSkillConditions": [[], []],
    # "StageSkillEffectDetails": [[], []],
    # "StageSkillEffects": [[], []],
    # "StageSkillSets": [[], []],
    "Stamps": [["Id"], ["Name"]],
    # "StandardQuestAreas": [["Id"], ["Name", "Description"]], # 不确定是否需要汉化
    # "StandardQuestStages": [["Id"], ["Description"]], # 不确定是否需要汉化
    # "StickerExchanges": [[], []],
    "Stickers": [["Id"], ["Name", "Text", "RequirementText"]],
    "StyleMovies": [["Id"], ["Name"]],
    "StyleVoices": [["Id"], ["Name"]],
    # "SubCharacters": [["Id"], ["Label"]], # 似乎不用汉化
    "TabList": [["Id"], ["TabListName"]],
    # "Targets": [[], []],
    "TextsPlaceHolder": [["Id"], ["Description"]],
    # "TicketOnlyGachas": [[], []],
    # "TutorialDeckCards": [[], []],
    # "TutorialDeckDatas": [[], []],
    # "TutorialQuestAreas": [[], []],
    # "TutorialQuestStages": [[], []],
    # "TutorialRewardDatas": [[], []],
    "TutorialSchoolIdolStageMovies": [["Id"], ["Title"]],
    "Tutorials": [["Id"], ["Description"]],
    # "UnitCharacters": [[], []],
    "Units": [["Id"], ["UnitName"]]
}

TestMode = False

class CustomLoader(yaml.SafeLoader):
    def __init__(self, stream):
        # 重写初始化以支持特定的控制字符
        super().__init__(stream)

    def check_printable(self, data):
        """
        重写检查函数以允许不可打印字符（如 #x000b）
        """
        for char in data:
            if char == "\x0b":  # 允许垂直制表符
                continue
            if not super().check_printable(char):
                return False
        return True


def save_json(data: list, name: str):
    """
    主流程:
      1. 从 primary_key_rules[name] 中取出主键列表 (primary_keys) 和 非主键列表 (other_keys)。
      2. 仅保留这些字段（拆分 '.' 处理嵌套/数组）。
      3. 如果 TestMode = True，则对「非主键列表」中的字符串或字符串数组，追加 "TEST"。
    """
    if not data:
        return

    # 取出该 name 对应的规则
    rule = primary_key_rules.get(name)
    if not rule or len(rule) < 2:
        return

    primary_keys = rule[0]  # 第一列表 (主键)
    other_keys = rule[1]    # 第二列表 (可能追加 TEST)

    # 合并所有需要保留的字段（第一项 + 第二项）
    all_keys = primary_keys + other_keys

    processed_data = []
    for record in data:
        # 为当前 record 构造一个新对象，只包含需要的字段
        filtered_record = filter_record_fields(
            record,
            all_keys,
            primary_keys,
            other_keys
        )
        processed_data.append(filtered_record)

    # Make first data has all key
    # This can be removed when app can parse all key(also key type) properly.
    # Currently there is a bug on finding type and find local key from data
    # We must make first data has all key
    if not sort_records_fields(processed_data, all_keys):
        print(f"Failed to find super key object from {name}")

    # 生成最终的 JSON 结构
    result = {
        "rules": {
            "primaryKeys": primary_keys
        },
        "data": processed_data
    }

    # 写入 JSON 文件
    os.makedirs('./link-like-diff/json', exist_ok=True)
    with open(f'link-like-diff/json/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    return f'link-like-diff/json/{name}.json'

def sort_records_fields(records: List[dict], field_paths: list):
    def hasPaths(record:dict, path:list):
        if not path:
            return False
        key = path[0]
        if not isinstance(record, dict) or key not in record:
            return False
        record_value = record[key]
        # No more sub object, we find all object from record by path 
        if len(path) == 1:
            return True
        
        # If there is obj use treversal to find value 
        if isinstance(record_value, dict):
            return hasPaths(record_value, path[1:])

        # When obj is list, check all element 
        if isinstance(record_value, list):
            for item in record_value:
                if isinstance(item, dict):
                    if hasPaths(item, path[1:]):
                        # it has all subkey
                        return True
        # Failed to find value by key
        return False
    for idx in range(len(records)):
        hasAllField = True
        for paths in field_paths:
            path = paths.split(".") 
            if not hasPaths(records[idx], path):
                hasAllField = False
                break
        if hasAllField:
            records.insert(0, records.pop(idx))
            return True
    return False

def filter_record_fields(record: dict, field_paths: list,
                         primary_keys: list, other_keys: list) -> dict:
    """
    给定一条原始记录 record，以及需要保留的字段路径列表 field_paths，
    返回一个只包含这些字段（及其嵌套结构）的新字典。
    若路径在 other_keys 且 TestMode = True，则对字符串或字符串列表添加 "TEST"。
    """
    new_record = {}
    for path_str in field_paths:
        path = path_str.split(".")  # "descriptions.type" -> ["descriptions", "type"]
        value = get_nested_value(record, path)
        if value is not None:
            # 若属于非主键列表 & TestMode = True，对字符串/字符串列表值追加 "TEST"
            if TestMode and (path_str in other_keys):
                value = transform_value_for_test_mode(value)
            # 将获取到的 value 合并到 new_record 中，保持相同嵌套结构
            merge_nested_value(new_record, path, value)
    return new_record


def get_nested_value(obj, path: list):
    """
    从 obj 中按照 path 依次深入，获取对应的 value。
    如果中间任何一步不存在，则返回 None。
    若遇到列表，则对列表中每个对象做同样的处理，并返回一个同样长度的列表。
    """
    if not path:
        return obj

    key = path[0]
    if not isinstance(obj, dict) or key not in obj:
        return None

    sub_obj = obj[key]
    # 如果仅剩最后一层路径，直接返回
    if len(path) == 1:
        return sub_obj

    # 如果是字典，继续深入
    if isinstance(sub_obj, dict):
        return get_nested_value(sub_obj, path[1:])

    # 如果是列表，则对每个元素做同样的处理，并返回一个列表
    if isinstance(sub_obj, list):
        results = []
        for item in sub_obj:
            if isinstance(item, dict):
                val = get_nested_value(item, path[1:])
                results.append(val)
            else:
                # 如果列表里不是 dict，就无法再深入，只能返回 None
                results.append(None)
        return results

    # 其他情况（数字、字符串等）无法继续深入
    return None


def merge_nested_value(target_dict: dict, path: list, value):
    """
    将 value 根据 path 的层级结构，合并到 target_dict 中。
    若某级是列表，则需要在 target_dict 中也构造出相同长度的列表，再逐项合并。
    """
    if not path:
        return

    key = path[0]

    # 如果只剩最后一级 key，则直接写入
    if len(path) == 1:
        target_dict[key] = value
        return

    # 如果 value 是个列表，说明当前层是列表，需要特殊处理
    if isinstance(value, list):
        # 如果 target_dict[key] 不存在或不是列表，则先初始化为空列表
        if key not in target_dict or not isinstance(target_dict[key], list):
            target_dict[key] = [None] * len(value)

        # 遍历 value 中的每一项，递归合并
        for i, v in enumerate(value):
            if v is None:
                continue  # 跳过 None
            # 如果 target_dict[key][i] 还没创建，就初始化为 dict
            if target_dict[key][i] is None:
                target_dict[key][i] = {}
            # 继续深入合并
            merge_nested_value(target_dict[key][i], path[1:], v)
        return

    # 否则，如果 target_dict[key] 不存在或不是字典，则初始化为字典
    if key not in target_dict or not isinstance(target_dict[key], dict):
        target_dict[key] = {}

    # 递归处理剩余路径
    merge_nested_value(target_dict[key], path[1:], value)


def transform_value_for_test_mode(value):
    """
    如果是字符串，追加 "TEST"。
    如果是字符串列表，为列表中的每项追加 "TEST"。
    其他类型不变。
    """
    if isinstance(value, str):
        return value + "TEST"
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        return [v + "TEST" for v in value]
    return value


# process_list = ["ProduceStepLesson", "SupportCardFlavor"]
process_list = None

def convert_yaml_types(folder_path="./link-like-diff/orig"):
    """
    遍历指定文件夹中的所有 YAML 文件，加载它们的内容，并打印每个文件的类型。
    自动替换 YAML 文件中的制表符为空格。
    """
    if not os.path.isdir(folder_path):
        print(f"路径 '{folder_path}' 不是一个有效的文件夹。")
        return

    for root, _, files in os.walk(folder_path):
        total = len(files)
        for n, file in enumerate(files):
            if file.endswith('.yaml'):
                if process_list:
                    if file[:-5] not in process_list:
                        continue

                file_path = os.path.join(root, file)
                # print(f"\"{file[:-5]}\": [[], []],")
                # continue

                print("Generating", file_path, f"to json. ({n}/{total})")
                try:
                    # 预处理文件：替换制表符为 4 个空格
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # content = content.replace('\t', '    ')  # 替换制表符
                    content = content.replace(": \t", ": \"\t\"")  # 替换制表符
                    content = content.replace("|\n", "|+\n") # Fix literal strings newline chomping

                    # 解析 YAML 内容
                    # data = yaml.safe_load(content)
                    data = yaml.load(content, CustomLoader)
                    save_json(data, file[:-5])

                    # print(f"文件: {file_path}")
                    # print(f"类型: {type(data)}\n")
                except Exception as e:
                    print(f"加载文件 {file_path} 时出错: {e}")


if __name__ == '__main__':
    convert_yaml_types()
