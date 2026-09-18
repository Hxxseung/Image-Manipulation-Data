from PIL import Image


def VertFLIP(image: Image.Image, level: int) -> Image.Image:
    """
    VertFLIP 변조

    level 1~4에 따라 상하 반전(Vertical Flip)을 적용한다.

    level 1: 상하 반전 적용
    level 2: 상하 반전 적용
    level 3: 상하 반전 적용
    level 4: 상하 반전 적용
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    flipped = image.transpose(Image.FLIP_TOP_BOTTOM)

    return flipped