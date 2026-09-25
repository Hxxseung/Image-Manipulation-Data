import random
import numpy as np
import cv2
from PIL import Image


def ColorSpace(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    ColorSpace 변조

    RGB 이미지를 HSV, HLS, LAB, YCrCb, LUV, XYZ 등의 color space로 무작위 변환한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 자연스러운 변환 (HSV, HLS)
    level 2: 휘도 분리 변환 (YCrCb, LAB)
    level 3: 채도/색상 변환 (LUV, XYZ)
    level 4: 모든 Color Space 중 완전 무작위 선택
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # ========================================================
    # Level별 Color Space 변환 플래그 후보군 설정
    # ========================================================

    colorspace_pool = {
        1: [cv2.COLOR_RGB2HSV, cv2.COLOR_RGB2HLS],
        2: [cv2.COLOR_RGB2YCrCb, cv2.COLOR_RGB2LAB],
        3: [cv2.COLOR_RGB2LUV, cv2.COLOR_RGB2XYZ],
        4: [
            cv2.COLOR_RGB2HSV,
            cv2.COLOR_RGB2HLS,
            cv2.COLOR_RGB2YCrCb,
            cv2.COLOR_RGB2LAB,
            cv2.COLOR_RGB2LUV,
            cv2.COLOR_RGB2XYZ,
        ],
    }

    selected_conversion = random.choice(colorspace_pool[level])
    width, height = image.size

    # ========================================================
    # OpenCV를 이용한 Color Space 변환
    # ========================================================

    # PIL Image -> Numpy (RGB) 변환
    target_rgb = image.convert("RGB")
    img_array_rgb = np.array(target_rgb)

    # 지정된 Color Space로 변환
    converted_array = cv2.cvtColor(img_array_rgb, selected_conversion)

    # 변환된 채널 값을 다시 RGB 형태의 PIL Image로 패킹
    converted_image = Image.fromarray(converted_array)

    # ========================================================
    # Resize 처리
    # ========================================================

    resized = converted_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized