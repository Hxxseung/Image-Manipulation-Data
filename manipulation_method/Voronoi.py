
"""Superpixel
→ image content를 고려
→ 색상 + 공간적으로 비슷한 pixel끼리 grouping

Voronoi
→ image content를 고려하지 않고
→ seed와의 공간적 거리만으로 grouping
"""

# 각 픽셀을 가장 가까운 seed point에 할당하여 Voronoi 영역으로 분할하는 코드
# 이거 너무 심하게 뭉게짐..

from PIL import Image
import numpy as np


def Voronoi(
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

    height, width = arr.shape[:2]
    image_area = width * height

    # 하나의 Voronoi cell이 차지하는 목표 면적 비율
    cell_ratio = {
    1: 0.00010,
    2: 0.00020,
    3: 0.00030,
    4: 0.00040,
    }

    num_points = max(
        10,
        int(1.0 / cell_ratio[level])
    )

    xs = rng.integers(0, width, size=num_points)
    ys = rng.integers(0, height, size=num_points)

    # 각 seed point가 위치한 원본 이미지의 색을 representative color로 사용
    colors = arr[ys, xs]

    yy, xx = np.indices((height, width))

    result = np.empty_like(arr)

    for y in range(height):

        distances = (
            (xx[y, :, None] - xs[None, :]) ** 2
            + (y - ys[None, :]) ** 2
        )

        nearest = np.argmin(
            distances,
            axis=1
        )

        result[y] = colors[nearest]

    return Image.fromarray(result)