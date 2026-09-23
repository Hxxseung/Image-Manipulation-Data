# 단일 이미지 기법, 고정 2-이미지 기법, level별 랜덤 2-이미지 기법을 함께 처리하는 runner 코드

from pathlib import Path
import random

from PIL import Image

from config import (
    OUTPUT_ROOT,
    NUM_VARIANTS
)

from manipulation_method.ResizeCrop import ResizeCrop
from manipulation_method.CopyMove import CopyMove
from manipulation_method.BGChange import BGChange
from manipulation_method.Splicing import Splicing

from manipulation_method.CutPaste import CutPaste
from manipulation_method.Superpixel import Superpixel
from manipulation_method.Voronoi import Voronoi
from manipulation_method.Erasing import Erasing
from manipulation_method.FGRemove import FGRemove
from manipulation_method.Removal import Removal
# from manipulation_method.Inpainting import Inpainting
from manipulation_method.Inpainting_LaMaModel import Inpainting

from manipulation_method.Blend import Blend
from manipulation_method.StackImage import StackImage
from manipulation_method.ShufPixels import ShufPixels
from manipulation_method.Repeat import Repeat


# ============================================================
# 변조 함수 Registry
# ============================================================

MANIPULATION_REGISTRY = {
    "Blend": {
        "func": Blend,
        "requires_aux": True,
    },

    "StackImage": {
        "func": StackImage,
        "requires_aux": True,
    },

    "ShufPixels": {
        "func": ShufPixels,
        "requires_aux": False,
    },

    "Repeat": {
        "func": Repeat,
        "requires_aux": False,
    },
}


# ============================================================
# level마다 다른 aux image를 랜덤하게 뽑을 기법!!!!!!!!!!!!!! runner2에서 이 부분이 추가 됨!!!!!!!!!!!!!!!!!!!!!!!
# ============================================================

RANDOM_AUX_METHODS = {
    "Blend",
    "StackImage",
}

# ------------------------------------------------------------
# 필요 시 아래처럼 추가 가능
#
# RANDOM_AUX_METHODS = {
#     "Blend",
#     "StackImage",
#     "PatchInter",
# }
# ------------------------------------------------------------


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


def load_aux_image(aux_path: Path):
    """
    aux image를 RGB로 읽어 copy하여 반환한다.
    """
    with Image.open(aux_path) as aux:
        return aux.convert("RGB").copy()


# ============================================================
# 하나의 기법 실행
# ============================================================

def run_single_manipulation(
    manipulation_name,
    manipulation_config,
    mapping_df,
    base_seed=42
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

    # --------------------------------------------------------
    # 이미지 단위 재현성용 rng
    # --------------------------------------------------------
    global_rng = random.Random(base_seed)

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
            with Image.open(image_path) as image:

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
                # aux image 준비
                # 일반 2-image 기법은
                # 한 번만 뽑아서 lv1~lv4에 공통 사용
                # ----------------------------------------
                fixed_aux_image = None

                if (
                    requires_aux
                    and manipulation_name
                    not in RANDOM_AUX_METHODS
                ):
                    fixed_aux_path = (
                        select_aux_image_path(
                            mapping_df,
                            image_path,
                            random.Random(
                                base_seed + index
                            )
                        )
                    )

                    fixed_aux_image = load_aux_image(
                        fixed_aux_path
                    )

                # ----------------------------------------
                # 변조본 생성
                # ----------------------------------------
                for level in range(
                    1,
                    NUM_VARIANTS + 1
                ):

                    current_seed = (
                        base_seed
                        + index * 100
                        + level
                    )

                    aux_image = None

                    if requires_aux:

                        # --------------------------------
                        # Blend, StackImage 등:
                        # level마다 다른 aux image 사용
                        # --------------------------------
                        if (
                            manipulation_name
                            in RANDOM_AUX_METHODS
                        ):
                            aux_path = (
                                select_aux_image_path(
                                    mapping_df,
                                    image_path,
                                    random.Random(
                                        current_seed
                                    )
                                )
                            )

                            aux_image = load_aux_image(
                                aux_path
                            )

                        # --------------------------------
                        # 일반 2-image 기법:
                        # 같은 aux image를 유지
                        # --------------------------------
                        else:
                            aux_image = (
                                fixed_aux_image.copy()
                                if fixed_aux_image
                                is not None
                                else None
                            )

                    transformed = (
                        manipulation_func(
                            image=image.copy(),
                            level=level,
                            aux_image=aux_image,
                            seed=current_seed
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
    manipulation_names,
    seed=42
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
            mapping_df,
            base_seed=seed
        )

    print()
    print("=" * 60)
    print("모든 변조 생성 완료")
    print("=" * 60)

    print(
        f"Output: "
        f"{OUTPUT_ROOT}"
    )
