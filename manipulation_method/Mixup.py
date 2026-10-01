# 다른 이미지의 일부 영역을 원본의 대응 영역과 pixel-wise weighted average하여 partial mixed-image를 생성하는 코드

from PIL import Image
import numpy as np
import random
import math


def Mixup(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:
    """
    Partial Mixup 변조

    다른 이미지의 일부 rectangular region을 선택하고,
    해당 영역에서 두 이미지를 pixel-wise weighted average한다.

    원본의 나머지 영역은 그대로 유지한다.

    level 기준:
    - 전체 이미지 면적 대비 Mixup이 적용되는 영역 비율

      level 1 -> 10%
      level 2 -> 20%
      level 3 -> 30%
      level 4 -> 40%
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    if aux_image is None:
        raise ValueError("Mixup은 aux_image가 필요합니다.")

    rng = random.Random(seed)
    np_rng = np.random.default_rng(seed)

    image = image.convert("RGB")
    aux_image = aux_image.convert("RGB").resize(image.size)

    arr1 = np.array(
        image,
        dtype=np.float32
    )

    arr2 = np.array(
        aux_image,
        dtype=np.float32
    )

    height, width = arr1.shape[:2]

    # 전체 이미지 면적 대비
    # partial Mixup을 적용할 영역 비율
    area_ratio = {
        1: 0.10,
        2: 0.20,
        3: 0.30,
        4: 0.40,
    }[level]

    target_area = (
        width
        * height
        * area_ratio
    )

    # 직사각형의 가로/세로 비율을 랜덤하게 설정
    aspect_ratio = rng.uniform(
        0.5,
        2.0
    )

    patch_w = int(
        math.sqrt(
            target_area
            * aspect_ratio
        )
    )

    patch_h = int(
        target_area
        / max(1, patch_w)
    )

    patch_w = min(
        width,
        max(1, patch_w)
    )

    patch_h = min(
        height,
        max(1, patch_h)
    )

    # Mixup 영역 위치
    x = rng.randint(
        0,
        max(0, width - patch_w)
    )

    y = rng.randint(
        0,
        max(0, height - patch_h)
    )

    # Beta distribution 기반 mixing coefficient
    alpha = {
        1: 0.2,
        2: 0.4,
        3: 0.8,
        4: 1.0,
    }[level]

    lam = np_rng.beta(
        alpha,
        alpha
    )

    # 원본이 최소 50% 유지
    lam = max(
        lam,
        1.0 - lam
    )

    # aux가 최소 10% 이상 반영
    lam = min(
        lam,
        0.90
    )

    result = arr1.copy()

    # 선택된 영역에서만 Mixup
    result[
        y:y + patch_h,
        x:x + patch_w
    ] = (
        lam
        * arr1[
            y:y + patch_h,
            x:x + patch_w
        ]
        +
        (1.0 - lam)
        * arr2[
            y:y + patch_h,
            x:x + patch_w
        ]
    )

    result = np.clip(
        result,
        0,
        255
    ).astype(np.uint8)

    return Image.fromarray(result)