.. _translation:

###########
Translation
###########

********
The Task
********

Translation is the task of translating text from a source language to another, such as English to Romanian.
This task is a subset of `Sequence to Sequence tasks <https://paperswithcode.com/method/seq2seq>`_, which requires the model to generate a variable length sequence given an input sequence.
In our case, the task will take an English sequence as input, and output the same sequence in Romanian.

------

*******
Example
*******

Let's look at an example.
We'll use `WMT16 English/Romanian <https://www.statmt.org/wmt16/translation-task.html>`_, a dataset of English to Romanian samples, based on the `Europarl corpora <http://www.statmt.org/europarl/>`_.
The data set contains a ``train.csv`` and ``valid.csv``.
Each CSV file looks like this:

.. code-block::

    input,target
    "Written statements and oral questions (tabling): see Minutes","Declaraţii scrise şi întrebări orale (depunere): consultaţi procesul-verbal"
    "Closure of sitting","Ridicarea şedinţei"
    ...

In the above the input/target columns represent the English and Romanian translation respectively.
Once we've downloaded the data using :func:`~flash.core.data.download_data`, we create the :class:`~flash.text.seq2seq.translation.data.TranslationData`.
We select a pre-trained backbone to use for our :class:`~flash.text.seq2seq.translation.model.TranslationTask` and finetune on the WMT16 data.
The backbone can be any Seq2Seq translation model from `HuggingFace/transformers <https://huggingface.co/models?filter=pytorch&pipeline_tag=translation>`_.

.. note::

    When changing the backbone, make sure you pass in the same backbone to the :class:`~flash.text.seq2seq.translation.data.TranslationData` and the :class:`~flash.text.seq2seq.translation.model.TranslationTask`!

Next, we use the trained :class:`~flash.text.seq2seq.translation.model.TranslationTask` for inference.
Finally, we save the model.
Here's the full example:

.. literalinclude:: ../../../flash_examples/translation.py
    :language: python
    :lines: 14-

------

*******
Serving
*******

The :class:`~flash.text.seq2seq.translation.model.TranslationTask` is servable.
This means you can call ``.serve`` to serve your :class:`~flash.core.model.Task`.
Here's an example:

.. literalinclude:: ../../../flash_examples/serve/translation/inference_server.py
    :language: python
    :lines: 14-

You can now perform inference from your client like this:

.. literalinclude:: ../../../flash_examples/serve/translation/client.py
    :language: python
    :lines: 14-
