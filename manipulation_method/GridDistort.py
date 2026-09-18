from PIL import Image


def GridDistort(image: Image.Image, level: int) -> Image.Image:
    """
    GridDistort 변조

    level 1~4에 따라 grid 격자 수와 비선형 왜곡(nonlinear distortion) 강도를 
    다르게 적용한 뒤 원래 이미지 크기로 resize한다.

    level 1: 2x2 격자, 미세한 비선형 왜곡 (변위 비율 0.03)
    level 2: 3x3 격자, 약한 비선형 왜곡 (변위 비율 0.06)
    level 3: 4x4 격자, 중간 비선형 왜곡 (변위 비율 0.10)
    level 4: 5x5 격자, 강한 비선형 왜곡 (변위 비율 0.15)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 격자 분할 수(N x N) 및 왜곡 변위 비율
    configs = {
        1: {"grid_steps": 2, "distort_limit": 0.03},
        2: {"grid_steps": 3, "distort_limit": 0.06},
        3: {"grid_steps": 4, "distort_limit": 0.10},
        4: {"grid_steps": 5, "distort_limit": 0.15},
    }

    config = configs[level]
    steps = config["grid_steps"]
    limit = config["distort_limit"]

    width, height = image.size
    dx = width / steps
    dy = height / steps

    # 격자 교차점 이동 좌표 계산
    def get_distorted_point(i, j):
        x = i * dx
        y = j * dy
        
        # 테두리 점은 고정하고 내부 교차점만 비선형 축소/확장 왜곡
        if 0 < i < steps and 0 < j < steps:
            offset_x = (1 if (i + j) % 2 == 0 else -1) * width * limit
            offset_y = (1 if (i + j) % 2 == 1 else -1) * height * limit
            return x + offset_x, y + offset_y
        return x, y

    # PIL Image.MESH 형태에 맞춘 메쉬 데이터 생성
    meshdata = []
    for i in range(steps):
        for j in range(steps):
            box = (
                int(i * dx), 
                int(j * dy), 
                int((i + 1) * dx), 
                int((j + 1) * dy)
            )

            x0, y0 = get_distorted_point(i, j)
            x1, y1 = get_distorted_point(i + 1, j)
            x2, y2 = get_distorted_point(i + 1, j + 1)
            x3, y3 = get_distorted_point(i, j + 1)

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