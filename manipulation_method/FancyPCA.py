import random
import numpy as np
from PIL import Image


def FancyPCA(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    FancyPCA 변조

    PCA를 이용하여 RGB channel intensity를 무작위로 변경한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세한 PCA 색상 변화 (std = 0.05)
    level 2: 약한 PCA 색상 변화 (std = 0.10)
    level 3: 중간 PCA 색상 변화 (std = 0.20)
    level 4: 강한 PCA 색상 변화 (std = 0.30)
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # ========================================================
    # Level별 변화량 표준편차(std) 설정
    # ========================================================

    std_map = {
        1: 0.05,
        2: 0.10,
        3: 0.20,
        4: 0.30,
    }

    std = std_map[level]
    width, height = image.size

    # Target 이미지 numpy 배열 변환 (0~1 범위 정규화)
    target = image.convert("RGB")
    img_array = np.array(target, dtype=np.float32) / 255.0

    # 픽셀 배열 재정렬 (N, 3)
    pixels = img_array.reshape(-1, 3)

    # ========================================================
    # PCA 계산 (공분산, 고유값, 고유벡터)
    # ========================================================

    mean = np.mean(pixels, axis=0)
    centered_pixels = pixels - mean
    cov = np.cov(centered_pixels, rowvar=False)

    eig_vals, eig_vecs = np.linalg.eigh(cov)

    # ========================================================
    # Random Perturbation 생성 및 적용
    # ========================================================

    # 평균 0, 표준편차 std를 갖는 가우시안 무작위 값 추출
    alpha = np.random.normal(0, std, size=3)

    # [p1, p2, p3] * [alpha1*lambda1, alpha2*lambda2, alpha3*lambda3]^T
    pca_offset = np.dot(eig_vecs, alpha * eig_vals)

    # RGB 채널에 노이즈 추가
    pca_array = img_array + pca_offset

    # 값 범위 클리핑 (0~255)
    pca_array = np.clip(pca_array * 255.0, 0, 255).astype(np.uint8)

    # ========================================================
    # PIL Image 변환 및 Resize
    # ========================================================

    pca_image = Image.fromarray(pca_array)

    resized = pca_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized