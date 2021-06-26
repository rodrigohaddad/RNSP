from encoders import ThermometerEncoder, CircularThermometerEncoder

from os import path

import numpy as np
from skimage.filters import threshold_niblack, threshold_sauvola

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

    def sauvola(self, arr: np.ndarray, window_size: int = 11) -> list:
        bin_imgs = list()
        for x in arr:
            thresh_s = threshold_sauvola(x, window_size=window_size)
            binary_s = np.array( x > thresh_s, dtype=int)
            bin_imgs.append(binary_s.flatten())
        return bin_imgs

    def niblack(self, arr: np.ndarray, window_size: int = 11, k: float = 0.8) -> list:
        bin_imgs = list()
        for x in arr:
            thresh_n = threshold_niblack(x, window_size=window_size, k=k)
            binary_n = np.array( x > thresh_n, dtype=int)
            bin_imgs.append(binary_n.flatten())
        return bin_imgs
    

