from pathlib import Path


# ============================================================
# 기본 경로
# ============================================================

BASE_DIR = Path(
    r"/home/juhyun/Desktop/web"
)

MAPPING_FILE = (
    BASE_DIR
    / "manipulation_mapping"
    / "webtoon_mapping.xlsx"
)

OUTPUT_ROOT = (
    BASE_DIR
    / "data_manipulation"
)


# ============================================================
# 실행 설정
# ============================================================

# 10   -> Excel 앞 10개
# 100  -> Excel 앞 100개
# None -> 전체 이미지
NUM_IMAGES = 15


# 이미지당 변조본 개수
NUM_VARIANTS = 4


# 실행할 변조 기법
MANIPULATIONS = [
    "ResizeCrop",
]