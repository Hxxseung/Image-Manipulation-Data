from PIL import Image, ImageEnhance


def Contrast_enhancement(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    Contrast_enhancement 변조

    level 1~4에 따라 대비 계수(Factor)를 크게 적용하여 
    이미지의 대비(Contrast)를 강화한 뒤 원래 이미지 크기로 resize한다.

    level 1: 약한 대비 강화 (1.3배)
    level 2: 중간 대비 강화 (1.6배)
    level 3: 강한 대비 강화 (2.0배)
    level 4: 매우 강한 대비 강화 (2.5배)
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # ========================================================
    # Level별 대비 강화 계수(Factor) 설정
    # ========================================================

    factors = {
        1: 1.3,
        2: 1.6,
        3: 2.0,
        4: 2.5,
    }

    factor = factors[level]
    width, height = image.size

    # ========================================================
    # 대비(Contrast) 조절
    # ========================================================

    target_rgb = image.convert("RGB")
    enhancer = ImageEnhance.Contrast(target_rgb)
    enhanced_image = enhancer.enhance(factor)

    # ========================================================
    # Resize 처리
    # ========================================================

    resized = enhanced_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized