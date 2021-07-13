# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from pathlib import Path
from unittest import mock

import pytest

import flash
from flash.core.utilities.imports import _SKLEARN_AVAILABLE
from tests.examples.utils import run_test
from tests.helpers.utils import _IMAGE_TESTING, _TABULAR_TESTING, _TEXT_TESTING, _VIDEO_TESTING


@mock.patch.dict(os.environ, {"FLASH_TESTING": "1"})
@pytest.mark.parametrize(
    "file",
    [
        pytest.param(
            "custom_task.py", marks=pytest.mark.skipif(not _SKLEARN_AVAILABLE, reason="sklearn isn't installed")
        ),
        pytest.param(
            "image_classification.py",
            marks=pytest.mark.skipif(not _IMAGE_TESTING, reason="image libraries aren't installed")
        ),
        pytest.param(
            "image_classification_multi_label.py",
            marks=pytest.mark.skipif(not _IMAGE_TESTING, reason="image libraries aren't installed")
        ),
        # pytest.param("finetuning", "object_detection.py"),  # TODO: takes too long.
        pytest.param(
            "semantic_segmentation.py",
            marks=pytest.mark.skipif(not _IMAGE_TESTING, reason="image libraries aren't installed")
        ),
        pytest.param(
            "style_transfer.py",
            marks=pytest.mark.skipif(not _IMAGE_TESTING, reason="image libraries aren't installed")
        ),
        pytest.param(
            "summarization.py", marks=pytest.mark.skipif(not _TEXT_TESTING, reason="text libraries aren't installed")
        ),
        pytest.param(
            "tabular_classification.py",
            marks=pytest.mark.skipif(not _TABULAR_TESTING, reason="tabular libraries aren't installed")
        ),
        pytest.param("template.py", marks=pytest.mark.skipif(not _SKLEARN_AVAILABLE, reason="sklearn isn't installed")),
        pytest.param(
            "text_classification.py",
            marks=pytest.mark.skipif(not _TEXT_TESTING, reason="text libraries aren't installed")
        ),
        # pytest.param(
        #     "text_classification_multi_label.py",
        #     marks=pytest.mark.skipif(not _TEXT_TESTING, reason="text libraries aren't installed")
        # ),
        pytest.param(
            "translation.py", marks=pytest.mark.skipif(not _TEXT_TESTING, reason="text libraries aren't installed")
        ),
        pytest.param(
            "video_classification.py",
            marks=pytest.mark.skipif(not _VIDEO_TESTING, reason="video libraries aren't installed")
        ),
    ]
)
def test_example(tmpdir, file):
    run_test(str(Path(flash.PROJECT_ROOT) / "flash_examples" / file))
