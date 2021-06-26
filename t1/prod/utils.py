from encoders import ThermometerEncoder, CircularThermometerEncoder

from os import path

import numpy as np


def load_data() -> tuple:
    """Loads train and test data"""

    def load(fname: str) -> np.ndarray:
        f: str = path.join("data/", fname)
        return np.load(f)["arr_0"]

    X_train: np.ndarray = load("kmnist-train-imgs.npz")
    X_test: np.ndarray = load("kmnist-test-imgs.npz")
    y_train: list = [str(i) for i in load("kmnist-train-labels.npz")]
    y_test: list = [str(i) for i in load("kmnist-test-labels.npz")]

    return X_train, X_test, y_train, y_test


class Binarizer():
    """Utility for KMNIST binarization"""

    def basic_bin(self, arr: np.ndarray, threshold: int = 128) -> list:
        return [list(np.where(x < threshold, 0, 1).flatten()) for x in arr]

    def simple_thermometer(self, arr: np.ndarray, minimum: int = 0, maximum: int = 255, resolution: int = 25) -> list:
        therm = ThermometerEncoder(
            maximum=maximum, minimum=minimum, resolution=resolution)
        return [therm.encode(x).flatten() for x in arr]

    def circular_thermometer(self, arr: np.ndarray, minimum: int = 0, maximum: int = 255, resolution: int = 20) -> list:
        therm = CircularThermometerEncoder(
            maximum=maximum, minimum=minimum, resolution=resolution)
        return [therm.encode(x).flatten() for x in arr]
