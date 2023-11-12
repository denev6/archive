"""
$ python test_detector.py IMAGE_FILE
"""

import argparse
import os.path

import cv2
import matplotlib.pyplot as plt

from detector import Detector


class TestDetector(object):
    def __init__(self, img):
        self.__img = self.__read_img(img)
        self.__detector = Detector(self.__img.shape)
        self.__bgr_frame, self.__rgb_frame = self.__detector.convert_frame(self.__img)

    def __read_img(self, img):
        if os.path.exists(img):
            return cv2.imread(img)
        else:
            raise FileExistsError(f"'{img}' Not Exists")

    def test_detect_landmark(self):
        """Test
        - detect_landmark
        """
        is_detected = self.__detector.detect_landmark(self.__rgb_frame)
        assert is_detected is True, "Landmarks Not Detected"

    def test_get_face_angles(self):
        """Test
        - get_face_angles
        """
        res = self.__detector.get_face_angles()
        has_six_values = len(res) == 6
        is_float = all([isinstance(value, float) for value in res])
        assert (
            has_six_values and is_float
        ) is True, "'face_angles' Result Does Not Contain Proper Values"

    def test_get_68_landmark_cord(self, saved_figure="test_Figure.png"):
        """Test
        - get_68_landmark_cord
        """
        cords = self.__detector.get_68_landmark_cord()
        X = cords[:68]
        Y = cords[68:]

        for x, y in zip(X, Y):
            marked_img = cv2.circle(
                self.__bgr_frame,
                (int(x), int(y)),
                radius=6,
                color=(255, 0, 0),
                thickness=-1,
            )

        plt.figure(figsize=(10, 4))
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

        ax1.set_title("Before")
        ax1.imshow(self.__img)
        ax2.set_title("After")
        ax2.imshow(marked_img)
        plt.savefig(saved_figure)

        assert os.path.exists(saved_figure) is True, "'landmark_cord' Result Not Saved"


if __name__ == "__main__":

    # Init
    parser = argparse.ArgumentParser()
    parser.add_argument("img")
    args = parser.parse_args()

    # Test
    td = TestDetector(args.img)
    td.test_detect_landmark()
    td.test_get_face_angles()
    td.test_get_68_landmark_cord()

    # Message
    print("\n\n", "-" * 30)
    print("Please check 'test_Figure.png' for details.")
