from PIL import Image, ImageEnhance


def Grayscale(image: Image.Image, level: int, aux_image: Image.Image = None, **kwargs) -> Image.Image:
    """
    Grayscale 변조

    level 1~4에 따라 채도 감소 비율을 다르게 적용한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 25% 흑백화 (채도 75% 유지)
    level 2: 50% 흑백화 (채도 50% 유지)
    level 3: 75% 흑백화 (채도 25% 유지)
    level 4: 100% 완전 흑백화 (채도 0%)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 채도(Color) 계수 (1.0: 원본, 0.0: 완전 흑백)
    factors = {
        1: 0.75,
        2: 0.50,
        3: 0.25,
        4: 0.00,
    }

    factor = factors[level]
    width, height = image.size

    enhancer = ImageEnhance.Color(image)
    grayscale_image = enhancer.enhance(factor)

    resized = grayscale_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized