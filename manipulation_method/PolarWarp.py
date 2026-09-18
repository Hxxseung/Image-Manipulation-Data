from PIL import Image
import math


def PolarWarp(image: Image.Image, level: int) -> Image.Image:
    """
    PolarWarp 변조

    level 1~4에 따라 극좌표 공간(polar-transformed space)에서의 
    왜곡 패턴 강도를 다르게 적용한 뒤 원래 이미지 크기로 resize한다.

    level 1: 미세한 극좌표 왜곡 (소용돌이 강도 0.05)
    level 2: 약한 극좌표 왜곡 (소용돌이 강도 0.10)
    level 3: 중간 극좌표 왜곡 (소용돌이 강도 0.15)
    level 4: 강한 극좌표 왜곡 (소용돌이 강도 0.20)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 왜곡 강도 계수
    coefficients = {
        1: 0.05,
        2: 0.10,
        3: 0.15,
        4: 0.20,
    }

    warp_factor = coefficients[level]
    width, height = image.size
    cx, cy = width / 2.0, height / 2.0
    max_radius = math.hypot(cx, cy)

    # 극좌표 변환 및 역매핑 메쉬 계산
    def distort_point(x, y):
        dx = x - cx
        dy = y - cy
        
        # 직교좌표 -> 극좌표 (반지름 r, 각도 theta)
        r = math.hypot(dx, dy)
        theta = math.atan2(dy, dx)
        
        # polar space에서 왜곡 패턴 적용 (중심으로부터 거리에 따른 각도 변위)
        distorted_theta = theta + warp_factor * (r / max_radius) * math.pi
        
        # 극좌표 -> 직교좌표 복원
        target_x = cx + r * math.cos(distorted_theta)
        target_y = cy + r * math.sin(distorted_theta)
        return target_x, target_y

    # 메쉬 변환용 사각형 구역 정의 (전체 영역 1개 구역 기준)
    x0, y0 = 0, 0
    x1, y1 = width, height

    dx0, dy0 = distort_point(x0, y0)
    dx1, dy1 = distort_point(x1, y0)
    dx2, dy2 = distort_point(x1, y1)
    dx3, dy3 = distort_point(x0, y1)

    # 4점 변환 매핑
    meshdata = [(
        (0, 0, width, height),
        (dx0, dy0, dx3, dy3, dx2, dy2, dx1, dy1)
    )]

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