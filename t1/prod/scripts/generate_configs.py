import json
from pathlib import Path
from copy import deepcopy

# Defaults
DEFAULT_RANDOM_SEED = 8080
DEFAULT_TRAIN_VALIDATION_SPLIT = 0.2
DEFAULT_TRAIN_FOLDS = 10
DEFAULT_WSD_IGNORE_ZERO = False
DEFAULT_WSD_VERBOSE = False

# Parameters
BINARIZATION_OPTIONS = ["threshold"]
BINARIZATION_THRESHOLDS = [32, 64, 128, 192]
BINARIZATION_RESOLUTIONS = [16, 32, 64]
ADDRESS_SIZES = [25]
WSD_CLUSTER = [True, False]

CLUS_THRESHOLD = [1, 2, 3, 5, 10, 15, 20]
CLUS_DISCRIMINATOR_LIMIT = [1, 2, 3, 5, 10, 15, 20]
CLUS_MIN_SCORE = [0.1, 0.2, 0.3, 0.4, 0.5]

base_cfg = {
    "wsd_cluster": False,
    "random_seed": DEFAULT_RANDOM_SEED,
    "train_validation_split": DEFAULT_TRAIN_VALIDATION_SPLIT,
    "train_folds": DEFAULT_TRAIN_FOLDS,
    "binarization": "",
    "binarization_threshold": 0,
    "binarization_resolution": 0,
    "wsd_address_size": 0,
    "wsd_ignore_zero": False,
    "wsd_verbose": False,
    "clus_min_score": 0.1,
    "clus_threshold": 0,
    "clus_discriminator_limit": 0,
}


def save_config(id: int, cfg: dict) -> None:
    with open("configs/cfg_{}.json".format(id), "w") as f:
        json.dump(cfg, f)
        f.close()


i = 0
Path("configs/").mkdir(parents=True, exist_ok=True)
for binarization_option in BINARIZATION_OPTIONS:
    if binarization_option == "threshold":
        for binarization_threshold in BINARIZATION_THRESHOLDS:
            for address_size in ADDRESS_SIZES:
                for wsd_clus in WSD_CLUSTER:
                    cfg = deepcopy(base_cfg)
                    cfg["wsd_cluster"] = wsd_clus
                    cfg["binarization"] = binarization_option
                    cfg["binarization_threshold"] = binarization_threshold
                    cfg["wsd_address_size"] = address_size
                    if wsd_clus:   
                        for clus_t in CLUS_THRESHOLD:
                           for clus_d in CLUS_DISCRIMINATOR_LIMIT: 
                               for clus_m in CLUS_MIN_SCORE:
                                   cfg["clus_min_score"] = clus_m
                                   cfg["clus_threshold"] = clus_t
                                   cfg["clus_discriminator_limit"] = clus_d
                                   save_config(i, cfg)
                                   i += 1
                    else:
                        save_config(i, cfg)
                        i += 1
    elif binarization_option in ["thermometer", "circular_thermometer"]:
        for binarization_resolution in BINARIZATION_RESOLUTIONS:
            for address_size in ADDRESS_SIZES:
                for wsd_clus in WSD_CLUSTER:
                    if wsd_clus:   
                        for clus_t in CLUS_THRESHOLD:
                           for clus_d in CLUS_DISCRIMINATOR_LIMIT: 
                               for clus_m in CLUS_MIN_SCORE:
                                   cfg["clus_min_score"] = clus_m
                                   cfg["clus_threshold"] = clus_t
                                   cfg["clus_discriminator_limit"] = clus_d
                                   save_config(i, cfg)
                                   i += 1
                    else:
                        save_config(i, cfg)
                        i += 1
