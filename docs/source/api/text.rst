##########
flash.text
##########

.. contents::
    :depth: 1
    :local:
    :backlinks: top

.. currentmodule:: flash.text

Classification
______________

.. autosummary::
    :toctree: generated/
    :nosignatures:
    :template: classtemplate.rst

    ~classification.model.TextClassifier
    ~classification.data.TextClassificationData

    classification.data.TextClassificationPostprocess
    classification.data.TextClassificationPreprocess
    classification.data.TextCSVDataSource
    classification.data.TextDataSource
    classification.data.TextDeserializer
    classification.data.TextFileDataSource
    classification.data.TextJSONDataSource
    classification.data.TextSentencesDataSource

Question Answering
__________________

.. autosummary::
    :toctree: generated/
    :nosignatures:
    :template: classtemplate.rst

    ~seq2seq.question_answering.model.QuestionAnsweringTask
    ~seq2seq.question_answering.data.QuestionAnsweringData

    seq2seq.question_answering.data.QuestionAnsweringPreprocess

Summarization
_____________

.. autosummary::
    :toctree: generated/
    :nosignatures:
    :template: classtemplate.rst

    ~seq2seq.summarization.model.SummarizationTask
    ~seq2seq.summarization.data.SummarizationData

    seq2seq.summarization.data.SummarizationPreprocess

Translation
___________

.. autosummary::
    :toctree: generated/
    :nosignatures:
    :template: classtemplate.rst

    ~seq2seq.translation.model.TranslationTask
    ~seq2seq.translation.data.TranslationData

    seq2seq.translation.data.TranslationPreprocess

General Seq2Seq
_______________

.. autosummary::
    :toctree: generated/
    :nosignatures:
    :template: classtemplate.rst

    ~seq2seq.core.model.Seq2SeqTask
    ~seq2seq.core.data.Seq2SeqData
    ~seq2seq.core.finetuning.Seq2SeqFreezeEmbeddings

    seq2seq.core.data.Seq2SeqBackboneState
    seq2seq.core.data.Seq2SeqCSVDataSource
    seq2seq.core.data.Seq2SeqDataSource
    seq2seq.core.data.Seq2SeqFileDataSource
    seq2seq.core.data.Seq2SeqJSONDataSource
    seq2seq.core.data.Seq2SeqPostprocess
    seq2seq.core.data.Seq2SeqPreprocess
    seq2seq.core.data.Seq2SeqSentencesDataSource
    seq2seq.core.metrics.BLEUScore
    seq2seq.core.metrics.RougeBatchAggregator
    seq2seq.core.metrics.RougeMetric
