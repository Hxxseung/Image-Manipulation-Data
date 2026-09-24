from PIL import Image, ImageOps


def Padding(image: Image.Image, level: int, aux_image: Image.Image = None, **kwargs) -> Image.Image:
    """
    Padding 변조

    level 1~4에 따라 이미지 외곽 패딩(여백) 비율을 다르게 적용한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 상하좌우 5% 패딩
    level 2: 상하좌우 10% 패딩
    level 3: 상하좌우 15% 패딩
    level 4: 상하좌우 20% 패딩
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 패딩 비율
    padding_ratios = {
        1: 0.05,
        2: 0.10,
        3: 0.15,
        4: 0.20,
    }

    ratio = padding_ratios[level]
    width, height = image.size

    # 패딩 픽셀 크기 계산
    pad_w = int(width * ratio)
    pad_h = int(height * ratio)

    # 외곽 여백 추가 (기본 검은색 여백)
    padded = ImageOps.expand(
        image,
        border=(pad_w, pad_h, pad_w, pad_h),
        fill="black"
    )

    # 원래 이미지 크기로 다시 리사이즈
    resized = padded.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized