from pathlib import Path
import random

from PIL import Image

from config import (
    OUTPUT_ROOT,
    NUM_VARIANTS
)

# from manipulation_method.ResizeCrop import ResizeCrop
# from manipulation_method.Skew import Skew
# from manipulation_method.Swirl import Swirl

# ============================================================
# 변조 함수 Registry
# ============================================================

MANIPULATION_REGISTRY = {
    
    # Example:
    # "ResizeCrop": {
    #     "func": ResizeCrop,
    #     "requires_aux": False,
    # },
    # "Skew": {
    #     "func": Skew,
    #     "requires_aux": False,
    # },
    # "Swirl": {
    #     "func": Swirl,
    #     "requires_aux": True
    # }
    
    # You need to change the MAANIPULATIONS list in config.py to include the names of the manipulations you want to run.
    # If you want to add more manipulations, you can add them to this registry in the same format as above.
    
}


# ============================================================
# 보조 이미지 선택
# ============================================================

def select_aux_image_path(
    mapping_df,
    current_image_path,
    rng
):
    """
    현재 이미지가 아닌 다른 이미지 중 하나를
    aux image로 선택한다.
    """

    candidates = []

    for row in mapping_df.itertuples(index=False):

        candidate_path = Path(
            row.Source_Path
        )

        if (
            candidate_path != current_image_path
            and candidate_path.exists()
        ):
            candidates.append(
                candidate_path
            )

    if not candidates:
        raise RuntimeError(
            "사용 가능한 aux image가 없습니다."
        )

    return rng.choice(
        candidates
    )


# ============================================================
# 하나의 기법 실행
# ============================================================

def run_single_manipulation(
    manipulation_name,
    manipulation_config,
    mapping_df
):

    manipulation_func = (
        manipulation_config["func"]
    )

    requires_aux = (
        manipulation_config["requires_aux"]
    )

    output_dir = (
        OUTPUT_ROOT
        / manipulation_name
    )

    # 기본 Output 루트 디렉토리 생성
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------
    # 레벨별 / origin 디렉토리 사전 생성
    # --------------------------------------------
    origin_dir = output_dir / "origin"
    origin_dir.mkdir(parents=True, exist_ok=True)

    level_dirs = {}
    for level in range(1, NUM_VARIANTS + 1):
        lv_dir = output_dir / f"lv{level}"
        lv_dir.mkdir(parents=True, exist_ok=True)
        level_dirs[level] = lv_dir

    print()
    print("=" * 60)
    print(
        f"Manipulation: "
        f"{manipulation_name}"
    )
    print("=" * 60)

    total_images = len(
        mapping_df
    )

    # --------------------------------------------
    # 재현 가능한 랜덤 선택
    # --------------------------------------------

    rng = random.Random(42)

    for index, row in enumerate(
        mapping_df.itertuples(index=False),
        start=1
    ):

        image_path = Path(
            row.Source_Path
        )

        base_name = str(
            row.Final_Base_Name
        )

        try:

            # --------------------------------------------
            # 파일 존재 확인
            # --------------------------------------------

            if not image_path.exists():

                raise FileNotFoundError(
                    f"원본 이미지가 없습니다: "
                    f"{image_path}"
                )

            # --------------------------------------------
            # 이미지 읽기
            # --------------------------------------------

            with Image.open(
                image_path
            ) as image:

                image = image.convert(
                    "RGB"
                )

                # ----------------------------------------
                # 원본 저장 (origin 폴더 하위)
                # ----------------------------------------

                origin_path = (
                    origin_dir
                    / f"{base_name}_origin.png"
                )

                image.save(
                    origin_path
                )

                # ----------------------------------------
                # aux image 준비
                # ----------------------------------------

                aux_image = None

                if requires_aux:

                    aux_path = (
                        select_aux_image_path(
                            mapping_df,
                            image_path,
                            rng
                        )
                    )

                    with Image.open(
                        aux_path
                    ) as aux:

                        aux_image = (
                            aux.convert("RGB")
                            .copy()
                        )

                # ----------------------------------------
                # 변조본 생성 및 레벨별 폴더 저장
                # ----------------------------------------

                for level in range(
                    1,
                    NUM_VARIANTS + 1
                ):

                    transformed = (
                        manipulation_func(
                            image,
                            level,
                            aux_image=aux_image
                        )
                    )

                    # 각 level별 폴더 내부로 저장 경로 변경
                    output_path = (
                        level_dirs[level]
                        / (
                            f"{base_name}_"
                            f"lv{level}.png"
                        )
                    )

                    transformed.save(
                        output_path
                    )

        except Exception as e:

            print(
                f"[ERROR] "
                f"{base_name}"
            )

            print(
                f"Source: "
                f"{image_path}"
            )

            print(
                f"Reason: {e}"
            )

        # --------------------------------------------
        # 진행 상황 출력
        # --------------------------------------------

        if (
            index % 100 == 0
            or index == total_images
        ):

            print(
                f"{index}/"
                f"{total_images} "
                f"처리 완료"
            )


# ============================================================
# 여러 기법 순차 실행
# ============================================================

def run_manipulations(
    mapping_df,
    manipulation_names
):

    OUTPUT_ROOT.mkdir(
        parents=True,
        exist_ok=True
    )

    for manipulation_name in (
        manipulation_names
    ):

        if (
            manipulation_name
            not in MANIPULATION_REGISTRY
        ):

            print(
                "[WARNING] "
                "등록되지 않은 기법: "
                f"{manipulation_name}"
            )

            continue

        manipulation_config = (
            MANIPULATION_REGISTRY[
                manipulation_name
            ]
        )

        run_single_manipulation(
            manipulation_name,
            manipulation_config,
            mapping_df
        )

    print()
    print("=" * 60)
    print("모든 변조 생성 완료")
    print("=" * 60)

    print(
        f"Output: "
        f"{OUTPUT_ROOT}"
    )