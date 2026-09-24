import math
import random
from PIL import Image


def Swirl(image: Image.Image, level: int, aux_image: Image.Image = None, **kwargs) -> Image.Image:
    """
    Swirl 변조

    level 1~4에 따라 이미지에 random swirl effect를 생성한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세한 소용돌이 (반지름 0.1, 강도 0.5)
    level 2: 약한 소용돌이 (반지름 0.2, 강도 1.0)
    level 3: 중간 소용돌이 (반지름 0.3, 강도 2.0)
    level 4: 강한 소용돌이 (반지름 0.4, 강도 4.0)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 소용돌이 반지름 비율 및 강도 설정
    configs = {
        1: {"radius_ratio": 0.1, "strength": 0.5},
        2: {"radius_ratio": 0.2, "strength": 1.0},
        3: {"radius_ratio": 0.3, "strength": 2.0},
        4: {"radius_ratio": 0.4, "strength": 4.0},
    }

    config = configs[level]
    r_ratio = config["radius_ratio"]
    strength = config["strength"]

    width, height = image.size
    cx = width / 2.0
    cy = height / 2.0
    
    # 소용돌이 영향 배경 반지름 (대각선 길이 기준)
    swirl_radius = math.hypot(width, height) * r_ratio

    # 왜곡 함수 정의
    def distort(x, y):
        dx = x - cx
        dy = y - cy

        r = math.hypot(dx, dy)
        theta = math.atan2(dy, dx)

        if r < swirl_radius:
            angle_offset = strength * (swirl_radius - r) / swirl_radius
            distorted_theta = theta + angle_offset
            target_x = cx + r * math.cos(distorted_theta)
            target_y = cy + r * math.sin(distorted_theta)
            return target_x, target_y
        else:
            return x, y

    x0, y0 = 0, 0
    x1, y1 = width, height

    dx0, dy0 = distort(x0, y0)
    dx1, dy1 = distort(x1, y0)
    dx2, dy2 = distort(x1, y1)
    dx3, dy3 = distort(x0, y1)

    meshdata = [(
        (0, 0, width, height),
        (dx0, dy0, dx3, dy3, dx2, dy2, dx1, dy1)
    )]

    distorted_img = image.transform(
        (width, height),
        Image.MESH,
        meshdata,
        Image.Resampling.BICUBIC
    )

    resized = distorted_img.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized