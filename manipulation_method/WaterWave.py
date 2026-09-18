import math
from PIL import Image


def WaterWave(image: Image.Image, level: int) -> Image.Image:
    """
    WaterWave 변조

    level 1~4에 따라 물결 파동(water-wave effect)의 진폭과 주기를 
    다르게 적용한 뒤 원래 이미지 크기로 resize한다.

    level 1: 미세한 물결 효과 (진폭 3, 주기 0.05)
    level 2: 약한 물결 효과 (진폭 6, 주기 0.08)
    level 3: 중간 물결 효과 (진폭 10, 주기 0.12)
    level 4: 강한 물결 효과 (진폭 15, 주기 0.15)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 파동 진폭(amplitude) 및 주기(frequency) 설정
    configs = {
        1: {"amplitude": 3.0, "frequency": 0.05},
        2: {"amplitude": 6.0, "frequency": 0.08},
        3: {"amplitude": 10.0, "frequency": 0.12},
        4: {"amplitude": 15.0, "frequency": 0.15},
    }

    config = configs[level]
    amp = config["amplitude"]
    freq = config["frequency"]

    width, height = image.size

    # 메쉬 구역 생성을 위한 격자 분할
    grid_size = 10
    dx = width / grid_size
    dy = height / grid_size

    def wave_offset(x, y):
        # x, y 좌표 모두에 삼각함수 기반 물결 왜곡 적용
        offset_x = amp * math.sin(2 * math.pi * y * freq / height)
        offset_y = amp * math.cos(2 * math.pi * x * freq / width)
        return x + offset_x, y + offset_y

    meshdata = []
    for i in range(grid_size):
        for j in range(grid_size):
            box = (
                int(i * dx),
                int(j * dy),
                int((i + 1) * dx),
                int((j + 1) * dy)
            )

            x0, y0 = wave_offset(i * dx, j * dy)
            x1, y1 = wave_offset((i + 1) * dx, j * dy)
            x2, y2 = wave_offset((i + 1) * dx, (j + 1) * dy)
            x3, y3 = wave_offset(i * dx, (j + 1) * dy)

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