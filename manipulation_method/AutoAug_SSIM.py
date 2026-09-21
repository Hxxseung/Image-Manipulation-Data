# AutoAugment를 반복 적용하여 SSIM 기준으로 서로 다른 4개의 재현 가능한 변형 이미지를 생성하는 코드
# 기존의 AutoAug는 원본과 같은 이미지가 나오기도 함. 따라서 AutoAug한 뒤 SSIM을 통해 검사 후 재생성 함.


from PIL import Image
from torchvision import transforms
from skimage.metrics import structural_similarity as ssim
import numpy as np
import torch
import random


def _calculate_ssim(
    image1: Image.Image,
    image2: Image.Image
) -> float:
    """
    두 이미지의 구조적 유사도(SSIM)를 계산한다.
    계산 속도를 높이기 위해 grayscale 및 축소 이미지를 사용한다.
    """

    img1 = image1.convert("L")
    img2 = image2.convert("L")

    # 원본 결과에는 영향을 주지 않고 SSIM 계산용 이미지만 축소
    max_size = 512

    img1.thumbnail((max_size, max_size))
    img2.thumbnail((max_size, max_size))

    # 두 이미지 크기 통일
    if img1.size != img2.size:
        img2 = img2.resize(img1.size)

    arr1 = np.array(img1)
    arr2 = np.array(img2)

    score = ssim(
        arr1,
        arr2,
        data_range=255
    )

    return float(score)


def _generate_autoaug(
    image: Image.Image,
    candidate_seed: int
) -> Image.Image:
    """
    주어진 seed를 사용하여 하나의 AutoAugment 결과를 생성한다.
    """

    torch.manual_seed(candidate_seed)
    random.seed(candidate_seed)

    transform = transforms.AutoAugment(
        policy=transforms.AutoAugmentPolicy.IMAGENET
    )

    return transform(image)


def AutoAug(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:
    """
    AutoAugment 기반 이미지 변조

    level은 변조 강도가 아니라 서로 다른 결과를 구분하기 위한
    variant 번호(1~4)를 의미한다.

    각 variant는 앞서 생성된 결과와 SSIM을 비교하며,
    너무 유사한 경우 다른 seed로 다시 AutoAugment를 수행한다.

    동일한 seed와 입력 이미지를 사용하면 다시 실행해도
    동일한 결과가 생성되어 재현성이 유지된다.

    aux_image는 runner1 인터페이스 통일을 위해 받지만 사용하지 않는다.
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    image = image.convert("RGB")

    # seed가 전달되지 않았을 경우에도 고정값을 사용하여 재현성 유지
    base_seed = 0 if seed is None else seed

    # SSIM이 이 값 이상이면 너무 유사한 결과로 판단
    ssim_threshold = 0.97

    # 한 variant에서 최대 재시도 횟수
    max_attempts = 20

    # 현재 level까지의 최종 결과 저장
    accepted_images = []

    for variant in range(1, level + 1):

        accepted = False

        for attempt in range(max_attempts):

            # variant와 attempt마다 항상 동일하게 계산되는 seed
            candidate_seed = (
                base_seed
                + variant * 1000
                + attempt
            )

            candidate = _generate_autoaug(
                image=image,
                candidate_seed=candidate_seed
            )

            # 첫 번째 variant는 비교 대상이 없으므로 바로 사용
            if not accepted_images:
                accepted_images.append(candidate)
                accepted = True
                break

            # 기존 결과들과 SSIM 계산
            similarity_scores = [
                _calculate_ssim(candidate, prev_image)
                for prev_image in accepted_images
            ]

            max_similarity = max(similarity_scores)

            # 기존 결과들과 충분히 다르면 채택
            if max_similarity < ssim_threshold:
                accepted_images.append(candidate)
                accepted = True
                break

        if not accepted:
            raise RuntimeError(
                f"AutoAug variant {variant} 생성 실패: "
                f"{max_attempts}회 시도했지만 "
                f"SSIM < {ssim_threshold}인 결과를 찾지 못했습니다."
            )

    return accepted_images[level - 1]
