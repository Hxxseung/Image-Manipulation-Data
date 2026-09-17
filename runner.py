from pathlib import Path

from PIL import Image

from config import (
    OUTPUT_ROOT,
    NUM_VARIANTS
)

from manipulation_method.ResizeCrop import ResizeCrop


# ============================================================
# 변조 함수 Registry
# ============================================================

MANIPULATION_REGISTRY = {
    "ResizeCrop": ResizeCrop,
}


# ============================================================
# 하나의 기법 실행
# ============================================================

def run_single_manipulation(
    manipulation_name,
    manipulation_func,
    mapping_df
):

    output_dir = (
        OUTPUT_ROOT
        / manipulation_name
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

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
                # 원본 저장
                # ----------------------------------------

                origin_path = (
                    output_dir
                    / f"{base_name}_origin.png"
                )

                image.save(
                    origin_path
                )


                # ----------------------------------------
                # 변조본 4개
                # ----------------------------------------

                for level in range(
                    1,
                    NUM_VARIANTS + 1
                ):

                    transformed = (
                        manipulation_func(
                            image,
                            level
                        )
                    )

                    output_path = (
                        output_dir
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


        manipulation_func = (
            MANIPULATION_REGISTRY[
                manipulation_name
            ]
        )


        run_single_manipulation(
            manipulation_name,
            manipulation_func,
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