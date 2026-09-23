# 두 이미지를 width 또는 height 방향으로 나누어 무작위로 stacking하는 코드
# 이것도 다양한 이미지를 바탕으로 stack. 지금 비율이 좋음

from PIL import Image
import random


def StackImage(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    if aux_image is None:
        raise ValueError("StackImage는 aux_image가 필요합니다.")

    rng = random.Random(seed)

    image = image.convert("RGB")
    aux_image = aux_image.convert("RGB").resize(image.size)

    width, height = image.size

    # 최종 이미지에서 aux_image가 차지하는 비율
    aux_ratio = {
        1: 0.20,
        2: 0.30,
        3: 0.40,
        4: 0.50,
    }[level]

    direction = rng.choice(["width", "height"])

    if direction == "width":

        split = int(width * (1 - aux_ratio))

        result = Image.new("RGB", image.size)

        result.paste(
            image.crop((0, 0, split, height)),
            (0, 0)
        )

        result.paste(
            aux_image.crop((split, 0, width, height)),
            (split, 0)
        )

    else:

        split = int(height * (1 - aux_ratio))

        result = Image.new("RGB", image.size)

        result.paste(
            image.crop((0, 0, width, split)),
            (0, 0)
        )

        result.paste(
            aux_image.crop((0, split, width, height)),
            (0, split)
        )

    return result