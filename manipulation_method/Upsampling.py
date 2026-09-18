from PIL import Image


def UpSampling(image: Image.Image, level: int) -> Image.Image:
    """
    UpSampling 변조

    level 1~4에 따라 spatial resolution을 증가(Up-sampling)시키는 배율을 달리 적용한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 1.25배 해상도 증가 (약한 업샘플링 왜곡)
    level 2: 1.5배 해상도 증가 (중간 업샘플링 왜곡)
    level 3: 2.0배 해상도 증가 (강한 업샘플링 왜곡)
    level 4: 3.0배 해상도 증가 (매우 강한 업샘플링 왜곡)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    scales = {
        1: 1.25,
        2: 1.5,
        3: 2.0,
        4: 3.0,
    }

    scale = scales[level]
    width, height = image.size

    # 1. Spatial Resolution 증가 (Up-sampling)
    up_width = int(width * scale)
    up_height = int(height * scale)

    upsampled = image.resize(
        (up_width, up_height),
        Image.Resampling.BICUBIC
    )

    # 2. 원래 이미지 크기로 복원 (Down-sampling)
    resized = upsampled.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized