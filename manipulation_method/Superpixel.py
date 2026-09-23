# 색상 유사도와 공간적 근접성을 기준으로 인접 픽셀을 superpixel 영역으로 그룹화하는 코드
# level이 올라갈수록 각 superpixel 영역이 커지므로 원본 세부 정보가 더 많이 뭉개짐



from PIL import Image
import numpy as np
from skimage.segmentation import slic
from skimage.color import label2rgb


def Superpixel(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    image = image.convert("RGB")
    arr = np.array(image)

    height, width = arr.shape[:2]
    image_area = width * height

    # 한 superpixel이 차지하는 목표 면적 비율/ ↑= uperpixel 하나의 목표 면적 ↑, n_segments ↓, 이미지가 더 크게 뭉개짐
    region_ratio = {
        1: 0.0010,   
        2: 0.0020,   # 0.0020 ≈ 500개
        3: 0.0030,   
        4: 0.0040,   # 0.0040 ≈ 250개
    }

    # 전체 이미지 면적 / superpixel 하나의 목표 면적
    target_region_area = image_area * region_ratio[level]

    n_segments = max(
        10,
        int(image_area / target_region_area)
    )

    labels = slic(
        arr,
        n_segments=n_segments,
        compactness=10,
        start_label=0,
        channel_axis=-1
    )

    result = label2rgb(
        labels,
        arr,
        kind="avg"
    )

    result = np.clip(result, 0, 255).astype(np.uint8)

    return Image.fromarray(result)