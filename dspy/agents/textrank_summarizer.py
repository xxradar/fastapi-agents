# agents/textrank_summarizer.py
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Query
import re

class TextRankSummarizerAgent:
    """
    Summarizer Agent using a simplified TextRank algorithm.
    """

    def __init__(self):
        pass

    def _split_into_sentences(self, text: str) -> List[str]:
        """Splits the text into sentences."""
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
        return [s.strip() for s in sentences if s.strip()]

    def _calculate_similarity(self, sentence1: str, sentence2: str) -> float:
        """Calculates similarity between two sentences (simple word overlap)."""
        words1 = set(sentence1.lower().split())
        words2 = set(sentence2.lower().split())
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "of", "in", "on", "at", "to", "by", "and", "or"}
        words1 = words1 - stop_words
        words2 = words2 - stop_words
        common_words = words1.intersection(words2)
        return len(common_words) / (len(words1) + len(words2) + 1e-6)

    def _rank_sentences(self, sentences: List[str]) -> List[float]:
        """Simplified TextRank ranking (one iteration)."""
        num_sentences = len(sentences)
        similarity_matrix = [[0.0] * num_sentences for _ in range(num_sentences)]

        # Build the similarity matrix
        for i in range(num_sentences):
            for j in range(num_sentences):
                if i != j:
                    similarity_matrix[i][j] = self._calculate_similarity(sentences[i], sentences[j])

        # Normalize the rows of the similarity matrix (make them sum to 1)
        for i in range(num_sentences):
            row_sum = sum(similarity_matrix[i])
            if row_sum > 0:
                similarity_matrix[i] = [sim / row_sum for sim in similarity_matrix[i]]


        # Initialize scores (can start with equal scores or slightly favor the first sentence)
        scores = [1.0 / num_sentences] * num_sentences
        #scores[0] = 1.0  #  Optionally, give a slight boost to the first sentence.

        # One iteration of score updates.
        new_scores = [0.0] * num_sentences
        for i in range(num_sentences):
            for j in range(num_sentences):
                new_scores[i] += similarity_matrix[j][i] * scores[j]  # Note: j, i order
        return new_scores
        

    def summarize(self, text_to_summarize: Optional[str] = None, num_sentences: int = 2) -> Dict[str, Any]:
        """Summarizes the input text using TextRank."""
        if not text_to_summarize:
            return {"error": "TEXT_TO_SUMMARIZE is not provided or is not a valid string."}

        sentences = self._split_into_sentences(text_to_summarize)
        if not sentences:
            return {"summary": ""}
        if len(sentences) <= num_sentences:
            return {"summary": " ".join(sentences)}

        ranked_scores = self._rank_sentences(sentences)
        top_indices = sorted(range(len(ranked_scores)), key=lambda i: ranked_scores[i], reverse=True)
        top_sentences = [sentences[i] for i in top_indices[:num_sentences]]
        original_order_sentences = sorted(top_sentences, key=lambda x: sentences.index(x))

        summary = " ".join(original_order_sentences)
        return {"summary": summary}


def register_routes(router: APIRouter):
    """Registers the TextRank summarizer agent's routes."""
    agent = TextRankSummarizerAgent()

    @router.get("/textrank_summarizer", summary="Summarizes input text using TextRank", response_model=Dict[str, Any], tags=["Dspy Agents"])
    async def textrank_summarizer_route(
        TEXT_TO_SUMMARIZE: Optional[str] = Query(None, description="The text to be summarized"),
        num_sentences: int = Query(2, description="Number of sentences in summary")
    ):
        """
        Summarizes the provided text using the TextRank algorithm.

        **Input:**

        *   **TEXT_TO_SUMMARIZE (optional, string):** The text to be summarized.  If not provided, an error will be returned.
        *   **num_sentences (optional, int):** The desired number of sentences in the summary. Defaults to 2.

        **Process:**

        1.  **Sentence Splitting:** The input text is split into individual sentences.
        2.  **Similarity Calculation:**  A similarity score is calculated between each pair of sentences. This score is based on the number of common words (excluding common "stop words" like "the", "a", "is").
        3.  **Ranking:** A simplified version of the TextRank algorithm is applied to rank the sentences. Sentences that are similar to many other sentences receive higher scores.
        4.  **Summary Extraction:** The top-ranked sentences (up to `num_sentences`) are selected and combined to form the summary.  The sentences are returned in their original order within the input text.

        **Example Input (query parameters):**

        `?TEXT_TO_SUMMARIZE=This is the first sentence. This is the second sentence. This is the third sentence.&num_sentences=2`

        **Example Output:**

        ```json
        {
          "summary": "This is the first sentence. This is the second sentence."
        }
        ```

        **Example Input (no text):**

         `?TEXT_TO_SUMMARIZE=`

        **Example Output (no text):**

        ```json
        {
            "error": "TEXT_TO_SUMMARIZE is not provided or is not a valid string."
        }
        ```
        **Example Input (short text):**

         `?TEXT_TO_SUMMARIZE=short`

        **Example Output (short text):**

        ```json
        {
            "summary": "short"
        }
        ```

        """
        result = agent.summarize(TEXT_TO_SUMMARIZE, num_sentences)
        return {
            "agent": "textrank_summarizer",
            "result": result
        }