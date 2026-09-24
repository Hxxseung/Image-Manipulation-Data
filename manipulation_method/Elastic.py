import math
from PIL import Image


def Elastic(image: Image.Image, level: int, aux_image: Image.Image = None, **kwargs) -> Image.Image:
    """
    Elastic 변조

    level 1~4에 따라 탄성 왜곡(Jelly-like distortion) 강도를 다르게 적용한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세한 탄성 왜곡 (왜곡 계수 0.03)
    level 2: 약한 탄성 왜곡 (왜곡 계수 0.06)
    level 3: 중간 탄성 왜곡 (왜곡 계수 0.10)
    level 4: 강한 탄성 왜곡 (왜곡 계수 0.15)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 탄성 왜곡 강도 계수
    coefficients = {
        1: 0.03,
        2: 0.06,
        3: 0.10,
        4: 0.15,
    }

    distortion_factor = coefficients[level]
    width, height = image.size

    # 1. 이미지를 16x16 세밀한 격자로 나눔 (물결/탄성 굴곡 표현)
    grid_size = 16
    dx_step = width / grid_size
    dy_step = height / grid_size

    # sin 파형 기반 좌표 변환 함수 (X, Y 방향 모두 탄성 파형 추가)
    def distort_point(x, y):
        # Y축 위치에 따라 X축이 oscillating(물결)
        offset_x = distortion_factor * width * math.sin(2 * math.pi * y / height)
        # X축 위치에 따라 Y축도 미세하게 oscillating
        offset_y = distortion_factor * height * 0.5 * math.cos(2 * math.pi * x / width)
        
        return x + offset_x, y + offset_y

    meshdata = []
    for i in range(grid_size):
        for j in range(grid_size):
            # 타깃 사각형 영역
            box = (
                int(i * dx_step),
                int(j * dy_step),
                int((i + 1) * dx_step),
                int((j + 1) * dy_step)
            )

            # 격자의 4개 꼭짓점에 파형 왜곡 적용
            x0, y0 = distort_point(i * dx_step, j * dy_step)
            x1, y1 = distort_point((i + 1) * dx_step, j * dy_step)
            x2, y2 = distort_point((i + 1) * dx_step, (j + 1) * dy_step)
            x3, y3 = distort_point(i * dx_step, (j + 1) * dy_step)

            quad = (x0, y0, x3, y3, x2, y2, x1, y1)
            meshdata.append((box, quad))

    distorted = image.transform(
        (width, height),
        Image.MESH,
        meshdata,
        Image.Resampling.BICUBIC
    )

    resized = distorted.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized