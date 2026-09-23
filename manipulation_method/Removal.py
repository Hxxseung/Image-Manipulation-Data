# 전체 이미지 면적의 일정 비율에 해당하는 영역을 제거하는 Removal 변조 코드
# Erasing → 영역을 단순 색으로 지움.
# Removal → 선택된 영역을 삭제하고 주변 픽셀로 메꾸는 전통적 alteration.   ???????????????????????????
# 이미지의 특정 영역을 제거하고 해당 부분을 빈(흰색) 영역으로 남기는 Removal 코드
'''
from PIL import Image
import numpy as np
import cv2
import random
import math


def Removal(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:
    """
    Removal 변조

    이미지의 특정 region을 제거하고,
    해당 영역을 흰색으로 남긴다.

    level 기준:
    - 전체 이미지 면적 대비 제거 영역 비율
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    rng = random.Random(seed)

    image = image.convert("RGB")
    arr = np.array(image)

    height, width = arr.shape[:2]

    # 전체 이미지 면적 대비 제거 영역 비율
    area_ratio = {
        1: 0.05,
        2: 0.10,
        3: 0.15,
        4: 0.20,
    }

    target_area = width * height * area_ratio[level]

    # 원형 제거 영역의 반지름 계산
    radius = int(math.sqrt(target_area / math.pi))
    radius = max(2, radius)
    radius = min(radius, max(2, min(width, height) // 2 - 1))

    center_x = rng.randint(radius, max(radius, width - radius - 1))
    center_y = rng.randint(radius, max(radius, height - radius - 1))

    result = arr.copy()

    # 제거 영역 mask 생성
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(mask, (center_x, center_y), radius, 255, -1)

    # 제거된 부분을 흰색으로 처리
    result[mask == 255] = [255, 255, 255]

    return Image.fromarray(result)
'''

# 전체 이미지 면적의 일정 비율에 해당하는 영역을 제거하는 Removal 변조 코드

from PIL import Image
import numpy as np
import cv2
import random
import math


def Removal(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    rng = random.Random(seed)

    image = image.convert("RGB")
    arr = np.array(image)

    height, width = arr.shape[:2]

    # 전체 이미지 면적 대비 제거할 영역의 비율
    area_ratio = {
        1: 0.05,
        2: 0.10,
        3: 0.15,
        4: 0.20,
    }

    target_area = width * height * area_ratio[level]

    # 원본 이미지의 가로/세로 비율을 고려해 patch 크기 결정
    patch_w = int(
        math.sqrt(
            target_area * width / height
        )
    )

    patch_h = int(
        target_area / max(1, patch_w)
    )

    patch_w = min(width, max(1, patch_w))
    patch_h = min(height, max(1, patch_h))

    x = rng.randint(
        0,
        max(0, width - patch_w)
    )

    y = rng.randint(
        0,
        max(0, height - patch_h)
    )

    mask = np.zeros(
        (height, width),
        dtype=np.uint8
    )

    mask[
        y:y + patch_h,
        x:x + patch_w
    ] = 255

    bgr = cv2.cvtColor(
        arr,
        cv2.COLOR_RGB2BGR
    )

    result = cv2.inpaint(
        bgr,
        mask,
        3,
        cv2.INPAINT_TELEA
    )

    result = cv2.cvtColor(
        result,
        cv2.COLOR_BGR2RGB
    )

    return Image.fromarray(result)