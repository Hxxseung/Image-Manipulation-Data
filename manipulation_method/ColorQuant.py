import random
from PIL import Image


def ColorQuant(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    ColorQuant 변조

    이미지에서 사용하는 distinct color(고유 색상)의 수를 무작위로 감소시킨 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세한 색상 제한 (colors = 64 ~ 128)
    level 2: 약한 색상 제한 (colors = 32 ~ 64)
    level 3: 중간 색상 제한 (colors = 16 ~ 32)
    level 4: 강한 색상 제한 (colors = 4 ~ 16)
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # ========================================================
    # Level별 표현 가능한 색상 수(Max Colors) 범위 설정
    # ========================================================

    color_ranges = {
        1: (64, 128),
        2: (32, 64),
        3: (16, 32),
        4: (4, 16),
    }

    c_min, c_max = color_ranges[level]
    target_colors = random.randint(c_min, c_max)
    width, height = image.size

    target = image.convert("RGB")

    # ========================================================
    # Color Quantization (Palette 기반 양자화)
    # ========================================================

    # PIL quantize를 사용하여 지정된 개수의 팔레트로 색상 감소
    quantized = target.quantize(
        colors=target_colors,
        method=Image.Quantize.MEDIANCUT
    )

    # RGB 모드로 복원
    quantized_rgb = quantized.convert("RGB")

    # ========================================================
    # Resize 처리
    # ========================================================

    resized = quantized_rgb.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized