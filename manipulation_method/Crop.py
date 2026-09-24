from PIL import Image


def Crop(image: Image.Image, level: int, aux_image: Image.Image = None, **kwargs) -> Image.Image:
    """
    Crop 변조

    level 1~4에 따라 crop 비율을 다르게 적용하여
    이미지의 일부 영역을 잘라내어 사용한다. (resize 미수행)

    level 1: 95% 영역 크롭
    level 2: 90% 영역 크롭
    level 3: 80% 영역 크롭
    level 4: 70% 영역 크롭
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

    return cropped