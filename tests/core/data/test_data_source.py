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
from flash.core.data.data_source import DatasetDataSource, DefaultDataKeys


def test_dataset_data_source():
    data_source = DatasetDataSource()

    input, target = 'test', 3

    assert data_source.load_sample((input, target)) == {DefaultDataKeys.INPUT: input, DefaultDataKeys.TARGET: target}
    assert data_source.load_sample(input) == {DefaultDataKeys.INPUT: input}
