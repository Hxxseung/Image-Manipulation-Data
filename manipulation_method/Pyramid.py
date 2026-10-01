# 원본 이미지를 배경으로 두고 여러 이미지를 pyramid 형태로 쌓아 배치하는 코드
'''예시처럼 원본 이미지를 배경으로 깔고, 위쪽에 작은 이미지들을 pyramid 형태로 쌓는 방식으로 바꿨습니다.
예전에 드린 “행 전체 채우기” 방식보다 예시와 훨씬 가깝습니다.
- level 기준:
  - overlay tile 개수 증가
  - level이 올라갈수록 피라미드가 조금 더 커짐'''

from PIL import Image
import random


def Pyramid(
    image: Image.Image,
    level: int,
    aux_images: list[Image.Image] | None = None,
    seed: int | None = None
) -> Image.Image:
    """
    Pyramid 변조

    원본 이미지를 배경으로 두고,
    작은 이미지들을 위쪽 중앙에 pyramid 형태로 배치한다.

    level 기준:
    - pyramid에 올리는 작은 tile 수
      level 1 -> 3개
      level 2 -> 4개
      level 3 -> 5개
      level 4 -> 6개
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    rng = random.Random(seed)

    image = image.convert("RGB")
    width, height = image.size

    result = image.copy()

    if aux_images is None:
        image_pool = [image.copy()]
    else:
        image_pool = [image.copy()] + [img.convert("RGB").resize(image.size) for img in aux_images]

    tile_count = {
        1: 3,
        2: 4,
        3: 5,
        4: 6,
    }[level]

    # pyramid row 구성 예: [1, 2, 3]
    rows = []
    remaining = tile_count
    current = 1
    while remaining > 0:
        n = min(current, remaining)
        rows.append(n)
        remaining -= n
        current += 1

    overlay_top = int(height * 0.05)
    row_h = int(height * 0.12)

    for r, n_tiles in enumerate(rows):
        tile_w = int(width * (0.18 - 0.02 * r))
        tile_h = int(height * (0.12 - 0.01 * r))

        tile_w = max(30, tile_w)
        tile_h = max(25, tile_h)

        total_w = n_tiles * tile_w
        start_x = (width - total_w) // 2
        y = overlay_top + r * row_h

        for i in range(n_tiles):
            selected = rng.choice(image_pool)
            patch = selected.resize((tile_w, tile_h))
            x = start_x + i * tile_w
            result.paste(patch, (x, y))

    return result