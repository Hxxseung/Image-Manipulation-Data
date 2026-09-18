from PIL import Image
import math


def Elastic(image: Image.Image, level: int) -> Image.Image:
    """
    Elastic 변조

    level 1~4에 따라 탄성 왜곡(Jelly-like distortion) 강도를 다르게 적용한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세한 탄성 왜곡 (왜곡 계수 0.02)
    level 2: 약한 탄성 왜곡 (왜곡 계수 0.04)
    level 3: 중간 탄성 왜곡 (왜곡 계수 0.07)
    level 4: 강한 탄성 왜곡 (왜곡 계수 0.10)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 탄성 왜곡 강도 계수
    coefficients = {
        1: 0.02,
        2: 0.04,
        3: 0.07,
        4: 0.10,
    }

    distortion_factor = coefficients[level]
    width, height = image.size
    
    # 렌즈 왜곡 메쉬(Mesh) 좌표 계산
    def distort_point(x, y):
        dx = distortion_factor * width * math.sin(y * math.pi / height)
        dy = 0
        
        target_x = x + dx
        target_y = y + dy
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