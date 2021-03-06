from typing import Tuple

import numpy as np
import pytest
import torch

from flash import Trainer
from flash.data.data_pipeline import DataPipeline
from flash.data.data_source import DefaultDataKeys
from flash.vision import SemanticSegmentation
from flash.vision.segmentation.data import SemanticSegmentationPreprocess

# ======== Mock functions ========


class DummyDataset(torch.utils.data.Dataset):
    size: Tuple[int, int] = (224, 224)
    num_classes: int = 8

    def __getitem__(self, index):
        return {
            DefaultDataKeys.INPUT: torch.rand(3, *self.size),
            DefaultDataKeys.TARGET: torch.randint(self.num_classes - 1, self.size),
        }

    def __len__(self) -> int:
        return 10


# ==============================


def test_smoke():
    model = SemanticSegmentation(num_classes=1)
    assert model is not None


@pytest.mark.parametrize("num_classes", [8, 256])
@pytest.mark.parametrize("img_shape", [(1, 3, 224, 192), (2, 3, 127, 212)])
def test_forward(num_classes, img_shape):
    model = SemanticSegmentation(
        num_classes=num_classes,
        backbone='torchvision/fcn_resnet50',
    )

    B, C, H, W = img_shape
    img = torch.rand(B, C, H, W)

    out = model(img)
    assert out.shape == (B, num_classes, H, W)


@pytest.mark.parametrize(
    "backbone",
    [
        "torchvision/fcn_resnet50",
        "torchvision/fcn_resnet101",
    ],
)
def test_init_train(tmpdir, backbone):
    model = SemanticSegmentation(num_classes=10, backbone=backbone)
    train_dl = torch.utils.data.DataLoader(DummyDataset())
    trainer = Trainer(default_root_dir=tmpdir, fast_dev_run=True)
    trainer.finetune(model, train_dl, strategy="freeze_unfreeze")


def test_non_existent_backbone():
    with pytest.raises(KeyError):
        SemanticSegmentation(2, "i am never going to implement this lol")


def test_freeze():
    model = SemanticSegmentation(2)
    model.freeze()
    for p in model.backbone.parameters():
        assert p.requires_grad is False


def test_unfreeze():
    model = SemanticSegmentation(2)
    model.unfreeze()
    for p in model.backbone.parameters():
        assert p.requires_grad is True


def test_predict_tensor():
    img = torch.rand(1, 3, 10, 20)
    model = SemanticSegmentation(2)
    data_pipe = DataPipeline(preprocess=SemanticSegmentationPreprocess())
    out = model.predict(img, data_source="tensor", data_pipeline=data_pipe)
    assert isinstance(out[0], torch.Tensor)
    assert out[0].shape == (196, 196)


def test_predict_numpy():
    img = np.ones((1, 3, 10, 20))
    model = SemanticSegmentation(2)
    data_pipe = DataPipeline(preprocess=SemanticSegmentationPreprocess())
    out = model.predict(img, data_source="numpy", data_pipeline=data_pipe)
    assert isinstance(out[0], torch.Tensor)
    assert out[0].shape == (196, 196)
