from PIL import Image


def ResizeCrop(image: Image.Image, level: int, aux_image: Image.Image = None, **kwargs) -> Image.Image:
    """
    ResizeCrop 변조

    level 1~4에 따라 crop 비율을 다르게 적용한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 95% 영역 유지
    level 2: 90%
    level 3: 80%
    level 4: 70%
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    ratios = {
        1: 0.95,
        2: 0.90,
        3: 0.80,
        4: 0.70,
    }

    ratio = ratios[level]

    width, height = image.size

    crop_width = int(width * ratio)
    crop_height = int(height * ratio)

    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    right = left + crop_width
    bottom = top + crop_height

    cropped = image.crop(
        (left, top, right, bottom)
    )

    resized = cropped.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized
