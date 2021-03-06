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
from functools import partial
from typing import Any, Callable, Dict, List, Optional, Union

import datasets
import torch
from datasets import DatasetDict, load_dataset
from torch import Tensor
from transformers import AutoTokenizer, default_data_collator

from flash.data.data_module import DataModule
from flash.data.data_source import DataSource, DefaultDataSources
from flash.data.process import Preprocess


class Seq2SeqDataSource(DataSource):

    def __init__(
        self,
        backbone: str,
        max_source_length: int = 128,
        max_target_length: int = 128,
        padding: Union[str, bool] = 'max_length'
    ):
        super().__init__()

        self.tokenizer = AutoTokenizer.from_pretrained(backbone, use_fast=True)
        self.max_source_length = max_source_length
        self.max_target_length = max_target_length
        self.padding = padding

    def _tokenize_fn(
        self,
        ex: Union[Dict[str, str], str],
        input: Optional[str] = None,
        target: Optional[str] = None,
    ) -> Callable:
        if isinstance(ex, dict):
            ex_input = ex[input]
            ex_target = ex[target] if target else None
        else:
            ex_input = ex
            ex_target = None

        return self.tokenizer.prepare_seq2seq_batch(
            src_texts=ex_input,
            tgt_texts=ex_target,
            max_length=self.max_source_length,
            max_target_length=self.max_target_length,
            padding=self.padding,
        )


class Seq2SeqFileDataSource(Seq2SeqDataSource):

    def __init__(
        self,
        filetype: str,
        backbone: str,
        max_source_length: int = 128,
        max_target_length: int = 128,
        padding: Union[str, bool] = 'max_length',
    ):
        super().__init__(backbone, max_source_length, max_target_length, padding)

        self.filetype = filetype

    def load_data(
        self,
        data: Any,
        use_full: bool = False,
        columns: List[str] = ["input_ids", "attention_mask", "labels"]
    ) -> 'datasets.Dataset':
        file, input, target = data
        data_files = {}
        stage = self._running_stage.value
        data_files[stage] = str(file)

        # FLASH_TESTING is set in the CI to run faster.
        if use_full and os.getenv("FLASH_TESTING", "0") == "0":
            dataset_dict = load_dataset(self.filetype, data_files=data_files)
        else:
            # used for debugging. Avoid processing the entire dataset   # noqa E265
            try:
                dataset_dict = DatasetDict({
                    stage: load_dataset(self.filetype, data_files=data_files, split=[f'{stage}[:20]'])[0]
                })
            except AssertionError:
                dataset_dict = load_dataset(self.filetype, data_files=data_files)

        dataset_dict = dataset_dict.map(partial(self._tokenize_fn, input=input, target=target), batched=True)
        dataset_dict.set_format(columns=columns)
        return dataset_dict[stage]

    def predict_load_data(self, data: Any) -> Union['datasets.Dataset', List[Dict[str, torch.Tensor]]]:
        return self.load_data(data, use_full=False, columns=["input_ids", "attention_mask"])


class Seq2SeqCSVDataSource(Seq2SeqFileDataSource):

    def __init__(
        self,
        backbone: str,
        max_source_length: int = 128,
        max_target_length: int = 128,
        padding: Union[str, bool] = 'max_length',
    ):
        super().__init__(
            "csv",
            backbone,
            max_source_length=max_source_length,
            max_target_length=max_target_length,
            padding=padding,
        )


class Seq2SeqJSONDataSource(Seq2SeqFileDataSource):

    def __init__(
        self,
        backbone: str,
        max_source_length: int = 128,
        max_target_length: int = 128,
        padding: Union[str, bool] = 'max_length',
    ):
        super().__init__(
            "json",
            backbone,
            max_source_length=max_source_length,
            max_target_length=max_target_length,
            padding=padding,
        )


class Seq2SeqSentencesDataSource(Seq2SeqDataSource):

    def load_data(
        self,
        data: Union[str, List[str]],
        dataset: Optional[Any] = None,
    ) -> List[Any]:

        if isinstance(data, str):
            data = [data]
        return [self._tokenize_fn(s) for s in data]


class Seq2SeqPreprocess(Preprocess):

    def __init__(
        self,
        train_transform: Optional[Dict[str, Callable]] = None,
        val_transform: Optional[Dict[str, Callable]] = None,
        test_transform: Optional[Dict[str, Callable]] = None,
        predict_transform: Optional[Dict[str, Callable]] = None,
        backbone: str = "sshleifer/tiny-mbart",
        max_source_length: int = 128,
        max_target_length: int = 128,
        padding: Union[str, bool] = 'max_length'
    ):
        self.backbone = backbone
        self.max_target_length = max_target_length
        self.max_source_length = max_source_length
        self.padding = padding

        super().__init__(
            train_transform=train_transform,
            val_transform=val_transform,
            test_transform=test_transform,
            predict_transform=predict_transform,
            data_sources={
                DefaultDataSources.CSV: Seq2SeqCSVDataSource(
                    self.backbone,
                    max_source_length=max_source_length,
                    max_target_length=max_target_length,
                    padding=padding,
                ),
                DefaultDataSources.JSON: Seq2SeqJSONDataSource(
                    self.backbone,
                    max_source_length=max_source_length,
                    max_target_length=max_target_length,
                    padding=padding,
                ),
                "sentences": Seq2SeqSentencesDataSource(
                    self.backbone,
                    max_source_length=max_source_length,
                    max_target_length=max_target_length,
                    padding=padding,
                ),
            },
            default_data_source="sentences",
        )

    def get_state_dict(self) -> Dict[str, Any]:
        return {
            **self.transforms,
            "backbone": self.backbone,
            "max_source_length": self.max_source_length,
            "max_target_length": self.max_target_length,
            "padding": self.padding,
        }

    @classmethod
    def load_state_dict(cls, state_dict: Dict[str, Any], strict: bool):
        return cls(**state_dict)

    def collate(self, samples: Any) -> Tensor:
        """Override to convert a set of samples to a batch"""
        return default_data_collator(samples)


class Seq2SeqData(DataModule):
    """Data module for Seq2Seq tasks."""

    preprocess_cls = Seq2SeqPreprocess
