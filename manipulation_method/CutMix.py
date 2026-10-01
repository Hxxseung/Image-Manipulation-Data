# 한 이미지의 rectangular region을 다른 이미지의 동일 위치 patch로 교체하는 CutMix 코드
'''
의미: 한 이미지의 직사각형 영역을 다른 이미지의 영역으로 교체
level 기준:- 전체 이미지 면적 대비 교체 영역 비율

ratio 의미:- level 1 -> 5%
- level 2 -> 10%
- level 3 -> 20%
- level 4 -> 30%
'''

from PIL import Image
import random
import math


def CutMix(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:
    """
    CutMix 변조

    한 이미지의 rectangular region을
    다른 이미지의 patch로 교체한다.

    partial copy를 모델링하기 위한 mixed-image augmentation이다.

    level 기준:
    - 전체 이미지 면적 대비 교체 영역 비율
      level 1 -> 5%
      level 2 -> 10%
      level 3 -> 20%
      level 4 -> 30%
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    if aux_image is None:
        raise ValueError("CutMix는 aux_image가 필요합니다.")

    rng = random.Random(seed)

    image = image.convert("RGB").copy()
    aux_image = aux_image.convert("RGB").resize(image.size)

    width, height = image.size

    area_ratio = {
        1: 0.05,
        2: 0.10,
        3: 0.20,
        4: 0.30,
    }[level]

    target_area = width * height * area_ratio

    aspect_ratio = rng.uniform(0.5, 2.0)

    patch_w = int(math.sqrt(target_area * aspect_ratio))
    patch_h = int(target_area / max(1, patch_w))

    patch_w = min(width, max(1, patch_w))
    patch_h = min(height, max(1, patch_h))

    x = rng.randint(0, max(0, width - patch_w))
    y = rng.randint(0, max(0, height - patch_h))

    patch = aux_image.crop((x, y, x + patch_w, y + patch_h))
    image.paste(patch, (x, y))

    return image