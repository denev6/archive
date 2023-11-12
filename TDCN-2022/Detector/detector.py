import os

import cv2
import numpy as np
import mediapipe as mp

from constant import *


class Detector(object):
    """우울증 예측에 필요한 얼굴 정보를 추출하는데 사용된다.

    Args:
        size: 이미지의 (가로, 세로) 크기

    Functions:
        convert_frame(frame)
        detect_landmark(frame)
        get_face_angles()
        get_68_landmark_cord()
    """

    def __init__(self, size):
        self._landmark_indexes = INDEX_68_LANDMARK
        self._face_indexs = INDEX_FACE_LANDMARK
        self._w = size[1]
        self._h = size[0]
        self._cam_matrix = self._init_camera_matrix(self._w, self._h)
        self._dist_matrix = self._init_distortion_matrix()
        self._face_mesh = self._init_face_mesh()
        self.__landmarks = None

    def _init_camera_matrix(self, img_w, img_h):
        return np.array(
            [
                [img_w, 0, img_h / 2],
                [0, img_w, img_h / 2],
                [0, 0, 1],
            ],
            dtype=np.int32,
        )

    def _init_distortion_matrix(self):
        return np.zeros((4, 1), dtype=np.float64)

    def _init_face_mesh(self):
        return mp.solutions.face_mesh.FaceMesh(
            refine_landmarks=False,
            static_image_mode=False,
            max_num_faces=1,
        )

    def detect_landmark(self, frame):
        """이미지의 랜드마크 객체를 생성한다.

        Args:
            이미지(프레임)
        Return:
            bool
        """
        results = self._face_mesh.process(frame)
        landmarks = results.multi_face_landmarks
        if landmarks:
            self.__landmarks = landmarks[0].landmark
        return bool(landmarks)

    def get_face_angles(self):
        """solvePnP를 활용해 열굴 회전 방향 벡터를 반환한다.

        Return:
            [Tx, Ty, Tz, Rx, Ry, Rz]
        """
        object_points = np.array(
            [self._get_face_points(id) for id in self._face_indexs], dtype=np.float64
        )
        image_points = np.array(object_points[:, :2], dtype=np.float64)

        _, vec_rot, vec_trans = cv2.solvePnP(
            object_points, image_points, self._cam_matrix, self._dist_matrix
        )
        return np.array([*vec_trans, *vec_rot], dtype=np.float64).flatten()

    def _get_face_points(self, id):
        landmark = self.__landmarks[id]
        return [landmark.x * self._w, landmark.y * self._h, landmark.z]

    def get_68_landmark_cord(self):
        """68개의 랜드마크 좌표 정보를 반환한다.

        Return:
            [x1, x2, x3 ... y66, y67, y68]
        """
        landmarks_x = list()
        landmarks_y = list()

        for i in self._landmark_indexes:
            landmark = self.__landmarks[i]
            landmarks_x.append(landmark.x * self._w)
            landmarks_y.append(landmark.y * self._h)

        return [*landmarks_x, *landmarks_y]

    @staticmethod
    def convert_frame(frame):
        """좌우 반전한 BGR, RGB 이미지를 반환한다.

        Args:
            frame: 현재 프레임(BGR)

        Returns:
            BGR(테스트), RGB(랜드마크 추출)
        """
        bgr_frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        # rgb_frame.flags.writeable = False
        return bgr_frame, rgb_frame
