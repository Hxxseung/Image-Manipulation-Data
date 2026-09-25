import random
import numpy as np
import cv2
from PIL import Image


def Heatmap(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    Heatmap 변조

    이미지에 random color map을 적용하여 heatmap 형태로 변환한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 부드러운 컬러맵 (예: JET, BONE)
    level 2: 대비가 있는 컬러맵 (예: HOT, PLASMA)
    level 3: 다채로운 컬러맵 (예: RAINBOW, OCEAN)
    level 4: 극적인 컬러맵 (예: HSV, COOL)
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # ========================================================
    # Level별 OpenCV ColorMap 후보군 설정
    # ========================================================

    # OpenCV COLORMAP constant mapping
    colormap_pool = {
        1: [cv2.COLORMAP_JET, cv2.COLORMAP_BONE, cv2.COLORMAP_AUTUMN],
        2: [cv2.COLORMAP_HOT, cv2.COLORMAP_PLASMA, cv2.COLORMAP_VIRIDIS],
        3: [cv2.COLORMAP_RAINBOW, cv2.COLORMAP_OCEAN, cv2.COLORMAP_SUMMER],
        4: [cv2.COLORMAP_HSV, cv2.COLORMAP_COOL, cv2.COLORMAP_PINK, cv2.COLORMAP_MAGMA],
    }

    # 해당 level에서 무작위 컬러맵 선택
    selected_cmap = random.choice(colormap_pool[level])
    width, height = image.size

    # ========================================================
    # OpenCV를 이용한 Heatmap 변환
    # ========================================================

    # PIL Image -> Numpy (BGR) 변환 (OpenCV 호환)
    target_rgb = image.convert("RGB")
    img_array_rgb = np.array(target_rgb)
    img_array_bgr = cv2.cvtColor(img_array_rgb, cv2.COLOR_RGB2BGR)

    # 그레이스케일 변환 (컬러맵 적용을 위해 필요)
    gray_image = cv2.cvtColor(img_array_bgr, cv2.COLOR_BGR2GRAY)

    # ColorMap 적용
    heatmap_array_bgr = cv2.applyColorMap(gray_image, selected_cmap)

    # Numpy (BGR) -> PIL Image (RGB) 변환
    heatmap_array_rgb = cv2.cvtColor(heatmap_array_bgr, cv2.COLOR_BGR2RGB)
    heatmap_image = Image.fromarray(heatmap_array_rgb)

    # ========================================================
    # Resize 처리
    # ========================================================

    resized = heatmap_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized