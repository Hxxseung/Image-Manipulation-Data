import random
from PIL import Image, ImageOps


def Posterize(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    Posterize 변조

    각 pixel의 color component를 표현하는 bit 수를 무작위로 감소시킨 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세한 비트 감소 (bits = 6~7)
    level 2: 약한 비트 감소 (bits = 4~5)
    level 3: 중간 비트 감소 (bits = 2~3)
    level 4: 강한 비트 감소 (bits = 1)
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # ========================================================
    # Level별 유지할 비트 수(bits) 범위 설정
    # ========================================================

    bit_ranges = {
        1: [6, 7],
        2: [4, 5],
        3: [2, 3],
        4: [1],
    }

    bits = random.choice(bit_ranges[level])
    width, height = image.size

    # Target 이미지 변환
    target = image.convert("RGB")

    # ========================================================
    # PIL ImageOps.posterize를 이용한 비트 감소
    # ========================================================

    posterized = ImageOps.posterize(target, bits)

    # ========================================================
    # Resize 처리
    # ========================================================

    resized = posterized.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized