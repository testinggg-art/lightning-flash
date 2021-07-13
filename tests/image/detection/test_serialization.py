import pytest
import torch

from flash.core.data.data_source import DefaultDataKeys
from flash.core.utilities.imports import _FIFTYONE_AVAILABLE
from flash.image.detection.serialization import FiftyOneDetectionLabels


@pytest.mark.skipif(not _FIFTYONE_AVAILABLE, reason="fiftyone is not installed for testing")
class TestFiftyOneDetectionLabels:

    @staticmethod
    def test_smoke():
        serial = FiftyOneDetectionLabels()
        assert serial is not None

    @staticmethod
    def test_serialize_fiftyone():
        labels = ['class_1', 'class_2', 'class_3']
        serial = FiftyOneDetectionLabels()
        filepath_serial = FiftyOneDetectionLabels(return_filepath=True)
        threshold_serial = FiftyOneDetectionLabels(threshold=0.9)
        labels_serial = FiftyOneDetectionLabels(labels=labels)

        sample = {
            DefaultDataKeys.PREDS: [
                {
                    "boxes": [torch.tensor(20), torch.tensor(30),
                              torch.tensor(40), torch.tensor(50)],
                    "labels": torch.tensor(0),
                    "scores": torch.tensor(0.5),
                },
            ],
            DefaultDataKeys.METADATA: {
                "filepath": "something",
                "size": (100, 100),
            },
        }

        detections = serial.serialize(sample)
        assert len(detections.detections) == 1
        assert detections.detections[0].bounding_box == [0.2, 0.3, 0.2, 0.2]
        assert detections.detections[0].confidence == 0.5
        assert detections.detections[0].label == "0"

        detections = filepath_serial.serialize(sample)
        assert len(detections["predictions"].detections) == 1
        assert detections["predictions"].detections[0].bounding_box == [0.2, 0.3, 0.2, 0.2]
        assert detections["predictions"].detections[0].confidence == 0.5
        assert detections["filepath"] == "something"

        detections = threshold_serial.serialize(sample)
        assert len(detections.detections) == 0

        detections = labels_serial.serialize(sample)
        assert len(detections.detections) == 1
        assert detections.detections[0].bounding_box == [0.2, 0.3, 0.2, 0.2]
        assert detections.detections[0].confidence == 0.5
        assert detections.detections[0].label == "class_1"
