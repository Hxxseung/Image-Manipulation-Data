import random

from PIL import Image


def PerspChange(image: Image.Image, level: int, aux_image: Image.Image = None, **kwargs) -> Image.Image:
    """
    PerspChange 변조

    level 1~4에 따라 원근감 변환(Perspective Change) 강도를 다르게 적용한다.
    4개 모서리를 각각 독립적으로 이동시켜 비대칭 사다리꼴(키스톤) 왜곡을 생성한다
    (Padding의 등방향 축소와 달리, 실제 카메라 각도 변화와 유사한 형태).

    level 1: 미세한 원근 왜곡 (최대 2.5%)
    level 2: 약한 원근 왜곡 (최대 5%)
    level 3: 중간 원근 왜곡 (최대 10%)
    level 4: 강한 원근 왜곡 (최대 15%)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 왜곡 계수 (이미지 크기 대비 모서리 이동 최대 비율)
    distortion_factors = {
        1: 0.025,
        2: 0.05,
        3: 0.10,
        4: 0.15,
    }

    factor = distortion_factors[level]
    width, height = image.size

    max_dx = width * factor
    max_dy = height * factor

    # 원본 이미지의 네 꼭짓점 (좌상, 좌하, 우하, 우상)
    start_points = [
        (0, 0),
        (0, height),
        (width, height),
        (width, 0),
    ]

    # 각 모서리를 독립적으로 0~max만큼 안쪽으로 랜덤 이동
    # -> 대칭 축소가 아니라 비대칭 사다리꼴이 생겨 실제 원근 변화처럼 보임
    def jitter():
        return random.uniform(0, max_dx), random.uniform(0, max_dy)

    j_tl, j_bl, j_br, j_tr = jitter(), jitter(), jitter(), jitter()

    end_points = [
        (j_tl[0], j_tl[1]),                          # 좌상
        (j_bl[0], height - j_bl[1]),                 # 좌하
        (width - j_br[0], height - j_br[1]),         # 우하
        (width - j_tr[0], j_tr[1]),                  # 우상
    ]

    # 원근 변환 행렬(4-point transform) 계수 계산 함수
    def find_coeffs(pa, pb):
        import numpy as np

        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

        A = np.array(matrix, dtype=float)
        B = np.array(pb, dtype=float).reshape(8)
        res = np.linalg.solve(A, B)
        return res

    coeffs = find_coeffs(end_points, start_points)

    transformed = image.transform(
        (width, height),
        Image.PERSPECTIVE,
        coeffs,
        Image.Resampling.BICUBIC,
    )

    return transformed