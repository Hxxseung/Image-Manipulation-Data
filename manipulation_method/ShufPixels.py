# 전체 이미지의 일정 비율에 해당하는 pixel 위치를 무작위로 shuffle하는 코드

from PIL import Image
import numpy as np


def ShufPixels(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    rng = np.random.default_rng(seed)

    image = image.convert("RGB")
    arr = np.array(image)

    h, w, c = arr.shape

    # 전체 pixel 중 shuffle할 pixel 비율
    shuffle_ratio = {
        1: 0.05,
        2: 0.10,
        3: 0.20,
        4: 0.30,
    }

    flat = arr.reshape(-1, c).copy()

    n_pixels = len(flat)
    n_shuffle = int(n_pixels * shuffle_ratio[level])

    indices = rng.choice(
        n_pixels,
        size=n_shuffle,
        replace=False
    )

    shuffled = flat[indices].copy()
    rng.shuffle(shuffled)

    flat[indices] = shuffled

    return Image.fromarray(flat.reshape(h, w, c))