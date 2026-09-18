from PIL import Image


def PerspChange(image: Image.Image, level: int) -> Image.Image:
    """
    PerspChange 변조

    level 1~4에 따라 원근감 변환(Perspective Change) 강도를 다르게 적용한다.

    level 1: 미세한 원근 왜곡 (2.5%)
    level 2: 약한 원근 왜곡 (5%)
    level 3: 중간 원근 왜곡 (10%)
    level 4: 강한 원근 왜곡 (15%)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 왜곡 계수 (이미지 크기 대비 모서리 이동 비율)
    distortion_factors = {
        1: 0.025,
        2: 0.05,
        3: 0.10,
        4: 0.15,
    }

    factor = distortion_factors[level]
    width, height = image.size

    dx = width * factor
    dy = height * factor

    # 변환 후 각 4개 모서리의 목표 좌표 (좌상, 좌하, 우하, 우상)
    # 네 귀퉁이를 안쪽으로 끌어당겨 원근 효과를 생성
    start_points = [
        (0, 0),
        (0, height),
        (width, height),
        (width, 0),
    ]

    end_points = [
        (dx, dy),                  # 좌상
        (dx, height - dy),         # 좌하
        (width - dx, height - dy), # 우하
        (width - dx, dy),          # 우상
    ]

    # 원근 변환 행렬(4-point transform) 계수 계산 함수
    def find_coeffs(pa, pb):
        import numpy as np

        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

        A = np.matrix(matrix, dtype=float)
        B = np.array(pb).reshape(8)
        res = np.dot(np.linalg.inv(A), B)
        return np.array(res).reshape(8)

    coeffs = find_coeffs(end_points, start_points)

    transformed = image.transform(
        (width, height),
        Image.PERSPECTIVE,
        coeffs,
        Image.Resampling.BICUBIC,
    )

    return transformed