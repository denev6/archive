import time
from queue import Queue

import cv2

from detector import Detector
from model import DataLoader, Model


def init_detector(cap):
    """카메라에 따라 Detector를 초기화한다."""
    while True:
        sucess, frame = cap.read()
        detector = Detector(frame.shape)
        if sucess:
            return detector


def load_data(cap, detector, fps):
    """5000 프레임의 데이터를 받아 DataLoader를 반환한다."""
    prev_time = 0
    queue_landmark = Queue()
    queue_pose = Queue()

    while cap.isOpened():
        sucess, frame = cap.read()
        current_time = time.time() - prev_time

        if sucess and (current_time > 1 / fps):
            prev_time = time.time()

            # Detector 내부에서 랜드마크 탐지
            frame, rgb_frame = detector.convert_frame(frame)
            is_detected = detector.detect_landmark(rgb_frame)

            if is_detected:
                landmark_2d = detector.get_68_landmark_cord()
                pose_angles = detector.get_face_angles()
            else:
                pass

            queue_landmark.put(landmark_2d)
            queue_pose.put(pose_angles)

            if len(queue_landmark) == 5000:  # and (len(queue_pose) == 5000):
                return DataLoader(queue_landmark, queue_pose)

        else:
            # 프레임 제한
            pass


def predict(data, model):
    """모델로부터 우울증 정도를 예측한다."""
    pred_y = model.predict(data)
    return pred_y


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    model = Model()
    detector = init_detector(cap)

    while True:
        data = load_data(cap, detector, 30)
        pred_y = predict(data)

        """이후 자연어 생성 모델에 정보를 전달하는 등 작업 수행
        """
