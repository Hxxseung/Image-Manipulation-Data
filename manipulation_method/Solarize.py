import random
from PIL import Image, ImageOps


def Solarize(image: Image.Image, level: int, aux_image: Image.Image = None, **kwargs) -> Image.Image:
    """
    Solarize 변조

    level 1~4에 따라 무작위 임계값(random threshold) 이상 pixel 값을 invert하여 강한 contrast 효과를 생성하고,
    원래 이미지 크기로 resize한다.

    level 1: 높은 임계값 범위 (약한 효과, threshold 192~240)
    level 2: 중간 임계값 범위 (약한-중간 효과, threshold 128~192)
    level 3: 낮은 임계값 범위 (중간-강한 효과, threshold 64~128)
    level 4: 매우 낮은 임계값 범위 (매우 강한 효과, threshold 1~64)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    threshold_ranges = {
        1: (192, 240),
        2: (128, 192),
        3: (64, 128),
        4: (1, 64)
    }

    min_t, max_t = threshold_ranges[level]
    threshold = random.randint(min_t, max_t)

    solarized = ImageOps.solarize(image, threshold=threshold)

    resized = solarized.resize(
        image.size,
        Image.Resampling.LANCZOS
    )

    return resized