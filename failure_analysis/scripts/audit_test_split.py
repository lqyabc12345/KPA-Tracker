import os
import json
from collections import Counter, defaultdict


# ========= 1. 根据你本地的数据位置修改这里 =========
DATA_ROOT = "dataset1"
CATEGORY = "laptop"

# 当前 KPA-Tracker laptop 的 test URDF IDs
TEST_URDF_IDS = [10040, 10885, 11242, 11030, 11156]


def main():
    category_root = os.path.join(DATA_ROOT, CATEGORY)

    # 原代码虽然 evaluation 是 val/test 语义，
    # 但实际 annotation 是从 laptop/train/ 下读取
    annotation_root = os.path.join(category_root, "train")

    test_txt_path = os.path.join(category_root, "test.txt")

    print("=== Split Audit ===")
    print("category_root :", category_root)
    print("annotation_root:", annotation_root)
    print("test.txt      :", test_txt_path)
    print()

    # ========= 2. 读取 test.txt =========
    with open(test_txt_path, "r") as f:
        test_entries = [line.strip() for line in f if line.strip()]

    test_entry_set = set(test_entries)

    print("Number of entries in test.txt:", len(test_entries))
    print("Unique entries in test.txt   :", len(test_entry_set))
    print()

    # ========= 3. 统计结果 =========
    total_by_urdf = Counter()
    matched_by_urdf = Counter()

    # filename -> [(video_name, urdf_id), ...]
    filename_locations = defaultdict(list)

    matched_samples = []

    # ========= 4. 遍历每个 video =========
    for video_name in sorted(os.listdir(annotation_root)):
        video_dir = os.path.join(annotation_root, video_name)

        if not os.path.isdir(video_dir):
            continue

        annotations_dir = os.path.join(video_dir, "annotations")

        if not os.path.isdir(annotations_dir):
            continue

        for filename in sorted(os.listdir(annotations_dir)):
            if not filename.endswith(".json"):
                continue

            annotation_path = os.path.join(annotations_dir, filename)

            try:
                with open(annotation_path, "r") as f:
                    annotation = json.load(f)
            except Exception as e:
                print("Failed to read:", annotation_path)
                print("Reason:", e)
                continue

            # ========= 5. 获取 urdf_id =========
            #
            # 不同 annotation 格式字段可能略有不同。
            # 先尝试最常见的写法。
            #
            instances = annotation.get("instances", [])

            if len(instances) != 1:
                print(
                    "WARNING: unexpected number of instances:",
                    annotation_path,
                    "count =", len(instances)
                )
                continue

            urdf_id = int(instances[0]["urdf_id"])

            total_by_urdf[urdf_id] += 1
            filename_locations[filename].append(
                (video_name, urdf_id)
            )

            # ========= 6. 模拟 loader 的 test.txt filtering =========
            if filename in test_entry_set:
                matched_by_urdf[urdf_id] += 1

                matched_samples.append(
                    {
                        "video": video_name,
                        "filename": filename,
                        "urdf_id": urdf_id,
                    }
                )

    # ========= 7. 打印五个 test URDF 的结果 =========
    print("=" * 60)
    print("TEST URDF SUMMARY")
    print("=" * 60)

    for urdf_id in TEST_URDF_IDS:
        print(
            f"URDF {urdf_id}: "
            f"total annotations = {total_by_urdf[urdf_id]}, "
            f"matched by test.txt = {matched_by_urdf[urdf_id]}"
        )

    print()

    # ========= 8. 所有 test.txt matched annotations =========
    print("=" * 60)
    print("ALL MATCHED URDF COUNTS")
    print("=" * 60)

    for urdf_id, count in matched_by_urdf.most_common():
        print(f"URDF {urdf_id}: {count}")

    print()
    print("Total matched samples:", len(matched_samples))

    # ========= 9. 检查 basename 是否跨 video 重复 =========
    duplicated_filenames = {
        filename: locations
        for filename, locations in filename_locations.items()
        if len(locations) > 1
    }

    print()
    print("=" * 60)
    print("FILENAME DUPLICATION CHECK")
    print("=" * 60)

    print(
        "Number of annotation filenames appearing in multiple videos:",
        len(duplicated_filenames),
    )

    # 只展示前 20 个，避免刷屏
    for i, (filename, locations) in enumerate(
        sorted(duplicated_filenames.items())
    ):
        if i >= 20:
            print("... more duplicated filenames omitted")
            break

        print()
        print(filename)

        for video_name, urdf_id in locations:
            print(
                "   ",
                "video =", video_name,
                "urdf_id =", urdf_id,
            )

    # ========= 10. 检查 test.txt 中每个 entry 命中了多少 annotation =========
    print()
    print("=" * 60)
    print("TEST.TXT MATCH MULTIPLICITY")
    print("=" * 60)

    match_multiplicity = Counter()

    for filename in test_entries:
        match_multiplicity[len(filename_locations.get(filename, []))] += 1

    for number_of_matches, number_of_entries in sorted(
        match_multiplicity.items()
    ):
        print(
            f"{number_of_entries} test.txt entries "
            f"matched {number_of_matches} annotation(s)"
        )

    # 找出异常项
    strange_entries = []

    for filename in test_entries:
        locations = filename_locations.get(filename, [])

        if len(locations) != 1:
            strange_entries.append(
                (filename, locations)
            )

    print()
    print(
        "Number of test.txt entries that do NOT map to exactly one annotation:",
        len(strange_entries),
    )

    for filename, locations in strange_entries[:20]:
        print()
        print("entry:", filename)
        print("matches:", locations)


if __name__ == "__main__":
    main()