import pandas as pd

from config import (
    MAPPING_FILE,
    NUM_IMAGES
)


def load_cut_mapping():
    """
    webtoon_mapping.xlsx의 Cut_Mapping 시트를 읽는다.

    Excel의 현재 행 순서를 그대로 유지하며,
    NUM_IMAGES 값에 따라 처리 개수를 제한한다.
    """

    if not MAPPING_FILE.exists():
        raise FileNotFoundError(
            f"Mapping 파일이 존재하지 않습니다:\n"
            f"{MAPPING_FILE}"
        )

    df = pd.read_excel(
        MAPPING_FILE,
        sheet_name="Cut_Mapping"
    )


    # ========================================================
    # 필수 컬럼 확인
    # ========================================================

    required_columns = {
        "Source_Path",
        "Final_Base_Name",
    }

    missing_columns = (
        required_columns
        - set(df.columns)
    )

    if missing_columns:

        raise ValueError(
            "Cut_Mapping 시트에 "
            f"필요한 컬럼이 없습니다: "
            f"{missing_columns}"
        )


    # ========================================================
    # 처리 개수 제한
    # ========================================================

    if NUM_IMAGES is not None:

        df = df.iloc[
            :NUM_IMAGES
        ].copy()


    print(
        f"처리 대상 이미지 수: "
        f"{len(df)}"
    )

    return df