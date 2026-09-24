import math
from PIL import Image


def OptDistort(image: Image.Image, level: int, aux_image: Image.Image = None, **kwargs) -> Image.Image:
    """
    OptDistort 변조 (격자 메쉬 기반 곡선 렌즈 왜곡)
    """
    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    coefficients = {
        1: 0.10,
        2: 0.20,
        3: 0.35,
        4: 0.50,
    }

    k = coefficients[level]
    width, height = image.size
    cx, cy = width / 2.0, height / 2.0

    # 1. 이미지를 10x10 조각 격자로 나눔 (곡선 표현을 위해 필수)
    grid_size = 10
    dx = width / grid_size
    dy = height / grid_size

    def distort_point(x, y):
        nx = (x - cx) / cx
        ny = (y - cy) / cy
        r2 = nx * nx + ny * ny
        factor = 1.0 + k * r2  # 배럴 왜곡
        return cx + (x - cx) * factor, cy + (y - cy) * factor

    meshdata = []
    for i in range(grid_size):
        for j in range(grid_size):
            # 원본 이미지상의 타깃 사각형
            box = (int(i * dx), int(j * dy), int((i + 1) * dx), int((j + 1) * dy))

            # 격자의 4개 꼭짓점에 곡선 좌표 왜곡 적용
            x0, y0 = distort_point(i * dx, j * dy)
            x1, y1 = distort_point((i + 1) * dx, j * dy)
            x2, y2 = distort_point((i + 1) * dx, (j + 1) * dy)
            x3, y3 = distort_point(i * dx, (j + 1) * dy)

            quad = (x0, y0, x3, y3, x2, y2, x1, y1)
            meshdata.append((box, quad))

    distorted = image.transform(
        (width, height),
        Image.MESH,
        meshdata,
        Image.Resampling.BICUBIC
    )

    return distorted.resize((width, height), Image.Resampling.LANCZOS)