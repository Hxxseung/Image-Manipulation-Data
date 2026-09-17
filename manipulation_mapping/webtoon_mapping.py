from pathlib import Path
import re

import pandas as pd


# ============================================================
# 1. 사용자 설정
# ============================================================

# 여기에 웹툰 97개 폴더가 들어있는 경로를 넣으세요.
ROOT_DIR = Path(__file__).resolve().parent

# 결과 Excel 파일
OUTPUT_XLSX = ROOT_DIR / "webtoon_mapping.csv"

# 웹툰 이미지로 인정할 확장자
IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp"
}


# ============================================================
# 2. 폴더명 파싱
# ============================================================

def parse_folder_name(folder_name):
    """
    예시
    ----------------------------------------------------------
    [연재] 스페이스 차이나드레스 2화 - 원현재
        ↓
    title       = 스페이스 차이나드레스
    episode_num = 2
    author      = 원현재

    [웹툰판] 계약 남친이 원하는 것 1화 - 미야마 ...
        ↓
    title       = 계약 남친이 원하는 것
    episode_num = 1
    author      = 미야마 ...
    """

    name = folder_name.strip()

    # --------------------------------------------------------
    # 맨 앞의 [연재], [웹툰], [웹툰판] 등 제거
    # --------------------------------------------------------
    name_without_tag = re.sub(
        r"^\[[^\]]+\]\s*",
        "",
        name
    )

    title = name_without_tag
    episode_num = None
    author = ""

    # --------------------------------------------------------
    # "작품명 2화 - 작가명"
    # 형태를 찾음
    #
    # (.*?)    → 작품명
    # (\d+)화  → 화수
    # (.*)     → 작가명
    # --------------------------------------------------------
    pattern = r"^(.*?)\s*(\d+)화(?:\s*-\s*(.*))?$"

    match = re.match(pattern, name_without_tag)

    if match:
        title = match.group(1).strip()
        episode_num = int(match.group(2))

        if match.group(3):
            author = match.group(3).strip()

    return {
        "original_folder_name": folder_name,
        "title": title,
        "episode_num": episode_num,
        "author": author
    }


# ============================================================
# 3. 파일명 자연 정렬 함수
# ============================================================

def natural_sort_key(text):
    """
    일반 문자열 정렬:
        1.png
        10.png
        2.png

    자연 정렬:
        1.png
        2.png
        10.png

    컷 순서를 올바르게 부여하기 위해 사용
    """

    return [
        int(token) if token.isdigit() else token.lower()
        for token in re.split(r"(\d+)", text)
    ]


# ============================================================
# 4. 폴더 스캔
# ============================================================

def scan_webtoon_folders(root_dir):
    """
    ROOT_DIR 바로 아래에 존재하는 폴더만 웹툰 episode 폴더로 간주
    """

    folder_infos = []

    folders = sorted(
        [
            p for p in root_dir.iterdir()
            if p.is_dir()
        ],
        key=lambda x: natural_sort_key(x.name)
    )

    print(f"발견된 웹툰 폴더 수: {len(folders)}")

    for folder in folders:

        parsed = parse_folder_name(folder.name)

        parsed["folder_path"] = str(folder.resolve())

        # 폴더 안 이미지 개수도 확인
        images = [
            p
            for p in folder.iterdir()
            if p.is_file()
            and p.suffix.lower() in IMAGE_EXTENSIONS
        ]

        parsed["image_count"] = len(images)

        folder_infos.append(parsed)

    return folder_infos


# ============================================================
# 5. WT ID 부여
# ============================================================

def assign_webtoon_ids(folder_infos):
    """
    동일한 title은 동일한 WT ID를 가짐.

    예:
    스페이스 차이나드레스 2화
    스페이스 차이나드레스 3화

        ↓

    둘 다 WT001
    """

    # 작품명 목록
    unique_titles = sorted(
        set(info["title"] for info in folder_infos)
    )

    title_to_wt = {}

    for idx, title in enumerate(unique_titles, start=1):
        title_to_wt[title] = f"WT{idx:03d}"

    # 각 폴더에 ID 적용
    for info in folder_infos:

        info["WT_ID"] = title_to_wt[info["title"]]

        episode_num = info["episode_num"]

        if episode_num is not None:
            info["EP_ID"] = f"EP{episode_num:03d}"
        else:
            # 화수를 자동 인식하지 못한 경우
            info["EP_ID"] = "EP_UNKNOWN"

    return folder_infos


# ============================================================
# 6. 컷 Mapping 생성
# ============================================================

def build_cut_mapping(folder_infos):
    """
    각 episode 폴더 안의 이미지에 CUT ID 부여

    WT001_EP002_CUT001
    WT001_EP002_CUT002
    ...
    """

    cut_rows = []

    for info in folder_infos:

        folder_path = Path(info["folder_path"])

        image_files = [
            p
            for p in folder_path.iterdir()
            if p.is_file()
            and p.suffix.lower() in IMAGE_EXTENSIONS
        ]

        # 자연 정렬
        image_files = sorted(
            image_files,
            key=lambda x: natural_sort_key(x.name)
        )

        for cut_index, image_path in enumerate(
            image_files,
            start=1
        ):

            cut_id = f"CUT{cut_index:03d}"

            final_base_name = (
                f"{info['WT_ID']}_"
                f"{info['EP_ID']}_"
                f"{cut_id}"
            )

            cut_rows.append({
                "WT_ID": info["WT_ID"],
                "EP_ID": info["EP_ID"],
                "CUT_ID": cut_id,

                "Original_Title": info["title"],
                "Episode_Num": info["episode_num"],
                "Author": info["author"],

                "Original_Folder": info["original_folder_name"],
                "Original_File": image_path.name,

                "Source_Path": str(image_path.resolve()),

                "Final_Base_Name": final_base_name
            })

    return cut_rows


# ============================================================
# 7. Excel 생성
# ============================================================

def save_excel(folder_infos, cut_rows, output_path):

    # --------------------------------------------------------
    # Sheet 1: 작품 / 화 매핑
    # --------------------------------------------------------

    webtoon_rows = []

    for info in folder_infos:

        webtoon_rows.append({
            "WT_ID": info["WT_ID"],
            "Original_Title": info["title"],
            "Author": info["author"],

            "Episode_Num": info["episode_num"],
            "EP_ID": info["EP_ID"],

            "Original_Folder": info["original_folder_name"],
            "Image_Count": info["image_count"],

            "Folder_Path": info["folder_path"]
        })

    webtoon_df = pd.DataFrame(webtoon_rows)

    # 보기 쉽게 WT / EP 기준 정렬
    webtoon_df = webtoon_df.sort_values(
        by=[
            "WT_ID",
            "Episode_Num"
        ],
        na_position="last"
    )

    # --------------------------------------------------------
    # Sheet 2: Cut Mapping
    # --------------------------------------------------------

    cut_df = pd.DataFrame(cut_rows)

    cut_df = cut_df.sort_values(
        by=[
            "WT_ID",
            "Episode_Num",
            "CUT_ID"
        ],
        na_position="last"
    )

    # --------------------------------------------------------
    # Excel 저장
    # --------------------------------------------------------

    with pd.ExcelWriter(
        output_path,
        engine="openpyxl"
    ) as writer:

        webtoon_df.to_excel(
            writer,
            sheet_name="Webtoon_Mapping",
            index=False
        )

        cut_df.to_excel(
            writer,
            sheet_name="Cut_Mapping",
            index=False
        )

        # ====================================================
        # Excel 기본 서식
        # ====================================================

        workbook = writer.book

        for sheet_name in [
            "Webtoon_Mapping",
            "Cut_Mapping"
        ]:

            worksheet = workbook[sheet_name]

            # 첫 행 고정
            worksheet.freeze_panes = "A2"

            # 자동 필터
            worksheet.auto_filter.ref = worksheet.dimensions

            # 열 너비 설정
            for column_cells in worksheet.columns:

                max_length = 0

                column_letter = (
                    column_cells[0].column_letter
                )

                for cell in column_cells:

                    if cell.value is not None:

                        cell_length = len(
                            str(cell.value)
                        )

                        if cell_length > max_length:
                            max_length = cell_length

                # 지나치게 넓어지지 않도록 제한
                adjusted_width = min(
                    max_length + 2,
                    45
                )

                worksheet.column_dimensions[
                    column_letter
                ].width = adjusted_width


# ============================================================
# 8. Main
# ============================================================

def main():

    print("=" * 60)
    print("Webtoon Mapping 생성 시작")
    print("=" * 60)

    # ROOT_DIR 존재 확인
    if not ROOT_DIR.exists():
        raise FileNotFoundError(
            f"경로가 존재하지 않습니다:\n{ROOT_DIR}"
        )

    # --------------------------------------------------------
    # Step 1
    # 폴더 스캔
    # --------------------------------------------------------

    folder_infos = scan_webtoon_folders(
        ROOT_DIR
    )

    # --------------------------------------------------------
    # Step 2
    # WT / EP ID 부여
    # --------------------------------------------------------

    folder_infos = assign_webtoon_ids(
        folder_infos
    )

    # --------------------------------------------------------
    # Step 3
    # CUT Mapping 생성
    # --------------------------------------------------------

    cut_rows = build_cut_mapping(
        folder_infos
    )

    # --------------------------------------------------------
    # Step 4
    # Excel 저장
    # --------------------------------------------------------

    save_excel(
        folder_infos,
        cut_rows,
        OUTPUT_XLSX
    )

    # --------------------------------------------------------
    # 결과 출력
    # --------------------------------------------------------

    unique_webtoons = len(
        set(
            info["WT_ID"]
            for info in folder_infos
        )
    )

    total_folders = len(folder_infos)
    total_cuts = len(cut_rows)

    print()
    print("=" * 60)
    print("완료")
    print("=" * 60)

    print(
        f"웹툰 작품 수 : {unique_webtoons}"
    )

    print(
        f"Episode 폴더 수 : {total_folders}"
    )

    print(
        f"전체 Cut 수 : {total_cuts}"
    )

    print(
        f"Excel 저장 위치 : {OUTPUT_XLSX}"
    )


if __name__ == "__main__":
    main()
