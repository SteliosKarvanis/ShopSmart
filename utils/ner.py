from typing import Dict

import spacy

# No fine-tunned model
DEFAULT_MODEL = "pt_core_news_lg"


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
    def model(self) -> spacy.Language:
        if not isinstance(self._model, spacy.Language):
            self._model = spacy.load(self._model_folder)
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
        # Extract Tags
        tags = {}
        doc = self.model(text)
        entities = [(e.text, e.label_) for e in doc.ents]
        for value, tag in entities:
            if tag == "O":
                continue
            # If no tag field, create it
            if not tags.get(tag):
                tags[tag] = []
            tags[tag].append(value)

        response = {
            "text": text,
            "tags": tags,
        }
        return response
