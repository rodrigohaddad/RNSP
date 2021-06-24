from utils import *

import json
import wisardpkg as wp
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, train_test_split


class Gym:
    """Class for training and getting results"""

    def __init__(self, config_file: str):

        # Load configuration file
        try:
            self._config: dict = None
            with open(config_file, "r") as f:
                self._config = json.load(f)
                f.close()
        except Exception as e:
            print(f"Failed to load configuration file: {e}")

        # Load data
        try:
            X_train, X_test, y_train, y_test = load_data()
            self.X_train: np.ndarray = X_train
            self.X_test: np.ndarray = X_test
            self.y_train: np.ndarray = y_train
            self.y_test: np.ndarray = y_test
        except Exception as e:
            print(f"Failed to load KMNIST data: {e}")

        # Binarization
        try:
            binarizer = Binarizer()
            if self._config["binarization"] == "threshold":
                self.X_train_binary = binarizer.basic_bin(
                    self.X_train, threshold=self._config["binarization_threshold"])
                self.X_test_binary = binarizer.basic_bin(
                    self.X_test, threshold=self._config["binarization_threshold"])
            elif self._config["binarization"] == "thermometer":
                self.X_train_binary = binarizer.simple_thermometer(
                    self.X_train, resolution=self._config["binarization_resolution"])
                self.X_test_binary = binarizer.simple_thermometer(
                    self.X_test, resolution=self._config["binarization_resolution"])
            elif self._config["binarization"] == "circular_thermometer":
                self.X_train_binary = binarizer.circular_thermometer(
                    self.X_train, resolution=self._config["binarization_resolution"])
                self.X_test_binary = binarizer.circular_thermometer(
                    self.X_test, resolution=self._config["binarization_resolution"])
            else:
                raise Exception(
                    f'Binarization type {self._config["binarization"]} unknown.')
        except Exception as e:
            print(f"Fail on data binarization: {e}")

        # Model
        self._model = None
        self._trained = False

    @property
    def trained(self):
        return self._trained

    def train(self, X_train: list, y_train: list) -> None:
        """Trains a brand new Wisard model"""

        # Reset trained flag
        self._trained = False

        # Build Wisard model
        try:
            self._model = wp.Wisard(
                self._config["wsd_address_size"],
                ignoreZero=self._config["wsd_ignore_zero"],
                verbose=self._config["wsd_verbose"]
            )
        except Exception as e:
            print(f"Fail on building wisard model: {e}")

        # Train model
        self._model.train(X_train, y_train)

        # Set trained flag
        self._trained = True

    def predict(self, X: list) -> list:
        """Makes classification for model"""
        if not self._trained:
            raise Exception("Model needs training before evaluation!")
        return self._model.classify(X)

    def evaluate(self, X: list, y: list) -> float:
        """Makes classification for model and returns accuracy"""
        y_pred: list = self.predict(X)
        return accuracy_score(y, y_pred)

    def train_full(self) -> None:
        """Trains using full train set"""
        self.train(self.X_train_binary, self.y_train)

    def train_with_split(self, validation_split: float = None) -> float:
        """Trains using `validation_split` percentage of train set 
        for validation. Returns accuracy for the validation set"""

        # Split into train and validation
        validation_split = validation_split if validation_split else self._config[
            "train_validation_split"]
        X_train, X_valid, y_train, y_valid = train_test_split(
            self.X_train_binary, self.y_train, test_size=validation_split, random_state=self._config["random_seed"])

        # Train model
        self.train(X_train, y_train)

        # Evaluate model and return
        return self.evaluate(X_valid, y_valid)

    def train_with_kfold(self, folds: int = None, verbose: bool = False) -> float:
        """Trains using `folds` for the number of K-folds. 
        Returns average accuracy for validation sets."""

        folds = folds if folds else self._config["train_folds"]
        kf = StratifiedKFold(n_splits=folds, shuffle=True,
                             random_state=self._config["random_seed"])
        scores = []
        for fold, (idxT, idxV) in enumerate(kf.split(self.X_train_binary, self.y_train)):
            if verbose:
                print("#" * 25)
                print(f"## FOLD {fold + 1}")
                print("#" * 25)

            X_train = [self.X_train_binary[i] for i in idxT]
            X_valid = [self.X_train_binary[i] for i in idxV]
            y_train = [self.y_train[i] for i in idxT]
            y_valid = [self.y_train[i] for i in idxV]

            self.train(X_train, y_train)
            score: float = self.evaluate(X_valid, y_valid)
            if verbose:
                print("- Accuracy: {:.4f}%".format(score*100))
            scores.append(score)

        return np.mean(scores)


if __name__ == "__main__":
    g = Gym("run_config.json")
    print(g.train_with_kfold(verbose=True))
