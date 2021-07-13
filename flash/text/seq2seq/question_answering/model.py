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
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Type, Union

import torch
from torchmetrics import Metric

from flash.text.seq2seq.core.metrics import RougeMetric
from flash.text.seq2seq.core.model import Seq2SeqTask


class QuestionAnsweringTask(Seq2SeqTask):
    """The ``QuestionAnsweringTask`` is a :class:`~flash.Task` for Seq2Seq text question answering. For more details,
    see `question_answering`.

    You can change the backbone to any question answering model from `HuggingFace/transformers
    <https://huggingface.co/models?filter=pytorch&pipeline_tag=question-answering>`_ using the ``backbone`` argument.

    .. note:: When changing the backbone, make sure you pass in the same backbone to the :class:`~flash.Task` and the
        :class:`~flash.core.data.data_module.DataModule` object! Since this is a Seq2Seq task, make sure you use a
        Seq2Seq model.

    Args:
        backbone: backbone model to use for the task.
        loss_fn: Loss function for training.
        optimizer: Optimizer to use for training, defaults to `torch.optim.Adam`.
        metrics: Metrics to compute for training and evaluation. Defauls to calculating the ROUGE metric.
            Changing this argument currently has no effect.
        learning_rate: Learning rate to use for training, defaults to `3e-4`
        val_target_max_length: Maximum length of targets in validation. Defaults to `128`
        num_beams: Number of beams to use in validation when generating predictions. Defaults to `4`
        use_stemmer: Whether Porter stemmer should be used to strip word suffixes to improve matching.
        rouge_newline_sep: Add a new line at the beginning of each sentence in Rouge Metric calculation.
    """

    def __init__(
        self,
        backbone: str = "t5-small",
        loss_fn: Optional[Union[Callable, Mapping, Sequence]] = None,
        optimizer: Type[torch.optim.Optimizer] = torch.optim.Adam,
        metrics: Union[Metric, Callable, Mapping, Sequence, None] = None,
        learning_rate: float = 1e-5,
        val_target_max_length: Optional[int] = None,
        num_beams: Optional[int] = 4,
        use_stemmer: bool = True,
        rouge_newline_sep: bool = True
    ):
        self.save_hyperparameters()
        super().__init__(
            backbone=backbone,
            loss_fn=loss_fn,
            optimizer=optimizer,
            metrics=metrics,
            learning_rate=learning_rate,
            val_target_max_length=val_target_max_length,
            num_beams=num_beams
        )
        self.rouge = RougeMetric(
            rouge_newline_sep=rouge_newline_sep,
            use_stemmer=use_stemmer,
        )

    def compute_metrics(self, generated_tokens: torch.Tensor, batch: Dict, prefix: str) -> None:
        tgt_lns = self.tokenize_labels(batch["labels"])
        result = self.rouge(self._postprocess.uncollate(generated_tokens), tgt_lns)
        self.log_dict(result, on_step=False, on_epoch=True, prog_bar=True)

    @staticmethod
    def _ci_benchmark_fn(history: List[Dict[str, Any]]):
        """
        This function is used only for debugging usage with CI
        """
        assert history[-1]["rouge1_recall"] > 0.2
