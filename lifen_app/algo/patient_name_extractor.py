from lifen_app.models.document_input import DocumentInputSchema, PageSchema
from lifen_app.models.patient_info import PatientName
from lifen_app.labels.documents import KeywordsInNamesEnvironment


class PatientNameExtractorHeuristics:
    """
    A class containing different heuristic to extract patient
    names from a list of pages.

    This class provides methods to extract patient names from a collection
    of pages, each represented as a `PageSchema` object. It utilizes different
    heuristic techniques to identify and infer patient names from
    the textual content present in the provided pages.

    Attributes:
        pages (list[PageSchema]): A list of PageSchema objects
        containing the textual content of the pages.

    Methods:
        __init__(self, pages: list[PageSchema]):
            Constructor method to initialize the PatientNameExtractorHeuristics instance.

        _reorder_words_by_coordinates(self) -> None:
            Internal method to reorder words on each page based on their coordinates.

        keyword_proximity_heuristic(self) -> tuple[str | None, str | None]:
            Extracts patient names using a
            keyword proximity heuristic based on word coordinates.
    """

    def __init__(self, pages: list[PageSchema]):
        self.pages = pages
        self._reorder_words_by_coordinates()

    def _reorder_words_by_coordinates(
        self,
    ) -> None:
        """
        Reorders words on each page based on their coordinates.

        This method sorts the words on each page in ascending order of their x-coordinate (horizontal position)
        and y-coordinate (vertical position). This reordering helps in grouping words that are close to each
        other spatially, which can be beneficial in certain heuristic-based name extraction methods.
        """
        for page in self.pages:
            page.words = sorted(page.words, key=lambda x: (x.bbox.x_min, x.bbox.y_min))

    def keyword_proximity_heuristic(self) -> tuple[str | None, str | None]:
        """
        Extracts patient names using a keyword proximity heuristic based on word coordinates.

        This method attempts to extract patient names by looking for specific keywords that might indicate
        first and last names. It assumes that the patient names are located on the same line as these keywords.
        If successful, it returns a tuple containing the inferred first name and last name. If no names are
        found, it returns (None, None).

        Returns:
            tuple[str | None, str | None]: A tuple containing the inferred first name and last name (or None).
        """
        first_name = None
        last_name = None
        word_lines = {}

        for page in self.pages:
            for word in page.words:
                y_min = word.bbox.y_min
                word_lines.setdefault(y_min, []).append(word)

        for y_min, line_words in word_lines.items():
            for i, word in enumerate(line_words):
                if word.text.lower() in [
                    keyword.value for keyword in KeywordsInNamesEnvironment
                ]:
                    if i + 1 < len(line_words):
                        next_word = line_words[i + 1]
                        if abs(word.bbox.y_min - next_word.bbox.y_min) < 0.01:
                            name = next_word.text
                            if not first_name:
                                first_name = name

                    elif first_name and i + 2 < len(line_words) and not last_name:
                        last_name = line_words[i + 2].text

                    # TODO (Violette) Cover more edges cases by detecting underline starting
                    #  with same x_min and incrementing y_max

        return first_name, last_name

    # TODO(Violette) Implement consecutive capitalized heuristic
    # TODO(Violette) Implement Top Right heuristic
    # TODO(Violette) Implement negative keywords heuristic
    # TODO(Violette) Implement dictionary based heuristic

    # TODO(Violette) Reconcile weighted heuristics


class PatientNameExtractor(PatientNameExtractorHeuristics):
    """
    A class to extract patient names from a document.

    This class extends the functionality of the `PatientNameExtractorHeuristics`.
    Attributes:
        config (DocumentInputSchema): A DocumentInputSchema object containing the configuration
            parameters and the pages representing the textual content of the document.

    Methods:
        __init__(self, config: dict):
            Constructor method to initialize the PatientNameExtractor instance.

        extract_patient_name_by_keyword(self) -> PatientName:
            Extracts patient names using a keyword proximity heuristic.
    """

    def __init__(
        self,
        config: dict,
    ):
        self.config = DocumentInputSchema(**config)
        PatientNameExtractorHeuristics.__init__(self, pages=self.config.pages)

    def extract_patient_name_by_keyword(self) -> PatientName:
        first_name, last_name = self.keyword_proximity_heuristic()
        return PatientName(first_name=first_name, last_name=last_name)
