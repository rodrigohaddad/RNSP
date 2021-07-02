from os import getenv
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, Boolean, create_engine
from sqlalchemy_utils import database_exists, create_database


__all__ = ["DBManager"]

Base = declarative_base()


class TrainTable(Base):

    __tablename__ = "train"

    # Columns
    id = Column(Integer, primary_key=True)
    wsd_cluster = Column(Boolean)
    random_seed = Column(Integer)
    train_validation_split = Column(Float)
    train_folds = Column(Integer)
    binarization = Column(String)
    binarization_threshold = Column(Integer)
    binarization_resolution = Column(Integer)
    wsd_address_size = Column(Integer)
    wsd_ignore_zero = Column(Boolean)
    wsd_verbose = Column(Boolean)
    clus_min_score = Column(Float)
    clus_threshold = Column(Integer)
    clus_discriminator_limit = Column(Integer)
    window_size = Column(Integer)
    constant_c = Column(Float)
    constant_k = Column(Float)
    val_accuracy = Column(Float)
    test_accuracy = Column(Float)

    def __repr__(self) -> str:
        return "<Wisard Train (accuracy={}, address_size={}, binarization={}, binarization_threshold={}, binarization_resolution={})>".format(
            self.accuracy, self.wsd_address_size, self.binarization, self.binarization_threshold, self.binarization_resolution)


class DBManager:

    def __init__(self):
        connection_url: str = getenv("DB_CONNECTION_URL", "")
        if connection_url == "":
            raise Exception(
                "Environment variable DB_CONNECTION_URL not set.")
        self._engine = create_engine(connection_url)
        if not database_exists(self._engine.url):
            create_database(self._engine.url)
            Base.metadata.create_all(self._engine)

        self._session: Session = sessionmaker(bind=self._engine)()

    def add_train_result(self, config: dict, val_accuracy: float, test_accuracy: float):
        train_result = TrainTable(
            val_accuracy=val_accuracy,
            test_accuracy=test_accuracy,
            **config
        )
        self._session.add(train_result)
        self._session.commit()
