from typing import Dict

import transformers
from transformers import pipeline

# No fine-tunned model
DEFAULT_MODEL = "best_bert_finetuned_ner"


class NERModel:
    """This class encapsulates all functionalities to load and use a NER model
    If no model_folder passed, uses the default, no fine-tunned, model from spacy library

    Usage Example:
        ner = NERModel("ner_v0")
        tags = ner.retrieve_tags("Batata Frita Original 80g")
    """

    def __init__(self, model_folder: str = DEFAULT_MODEL) -> None:
        self._model_folder = model_folder
        self._model = None

    def load(self):
        self.model

    @property
    def model(self) -> transformers.pipelines.token_classification.TokenClassificationPipeline:
        if not isinstance(self._model, transformers.pipelines.token_classification.TokenClassificationPipeline):
            self._model = pipeline("token-classification", model=self._model_folder, aggregation_strategy="simple")
        return self._model

    def retrieve_tags(self, text: str) -> Dict:
        """Retrieve the tags for a given text
        Example:
            self.model.retrieve_tags("Batata Rustica 80g") ->
            {'text': 'Batata Rustica 80g', 'tags': {'B-PRO': ['Batata'], 'B-ESP': ['Rustica'], 'B-TAM': ['80g']}}

        Args:
            text: the text from which the tags have to be extracted
        Returns:
            Dict, a dict containing the original text, and the tags
        """
        pass
