# 원본 이미지의 flipped/rotated 버전을 2x2 collage로 조합하는 FlipCollage 코드
'''
예시처럼 2×2 형태로 크고 굵게 배치되도록 바꿨습니다.
이전 코드처럼 너무 잘게 grid로 나누지 않습니다.
- level 기준:
  - 강도보다는 다른 random arrangement를 만드는 용도
  - 항상 2×2 구성 유지'''
from PIL import Image, ImageOps
import random


def _transform_patch(img: Image.Image, mode: str) -> Image.Image:
    if mode == "original":
        return img.copy()
    elif mode == "mirror":
        return ImageOps.mirror(img)
    elif mode == "flip":
        return ImageOps.flip(img)
    elif mode == "rot90":
        return img.rotate(90, expand=True)
    elif mode == "rot180":
        return img.rotate(180, expand=True)
    elif mode == "rot270":
        return img.rotate(270, expand=True)
    elif mode == "mirror_rot90":
        return ImageOps.mirror(img).rotate(90, expand=True)
    elif mode == "flip_rot90":
        return ImageOps.flip(img).rotate(90, expand=True)
    else:
        return img.copy()


def FlipCollage(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:
    """
    FlipCollage 변조

    원본 이미지의 flipped/rotated 버전을
    2x2 collage 형태로 조합한다.

    level 기준:
    - 배치 강도보다 random arrangement 차이
    - 4개 variant가 서로 다른 조합이 되도록 seed에 반영
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    rng = random.Random(seed)

    image = image.convert("RGB")
    width, height = image.size

    rows, cols = 2, 2
    cell_w = width // cols
    cell_h = height // rows

    transform_pool = [
        "original",
        "mirror",
        "flip",
        "rot90",
        "rot180",
        "rot270",
        "mirror_rot90",
        "flip_rot90",
    ]

    result = Image.new("RGB", (width, height))

    for row in range(rows):
        for col in range(cols):
            mode = rng.choice(transform_pool)
            patch = _transform_patch(image, mode)
            patch = patch.resize((cell_w, cell_h))
            result.paste(patch, (col * cell_w, row * cell_h))

    return result