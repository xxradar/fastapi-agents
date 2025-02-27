# agents/summarizer.py
from typing import Optional, Dict, Any
from fastapi import APIRouter, Query

class SummarizerAgent:
    """
    Summarizer Agent
    ----------------
    Purpose: Summarize the input text.

    Usage (within FastAPI):
        The agent is designed to be used within a FastAPI application.  It expects
        the input text to be passed as a query parameter named `TEXT_TO_SUMMARIZE`.

        Example API call:
        `/agent/summarizer?TEXT_TO_SUMMARIZE=This is a long text that needs to be summarized.`

    Usage (standalone - for testing):
        # In a Python shell:
        from agents import summarizer
        agent = summarizer.SummarizerAgent()
        result = agent.summarize("This is a long text that needs to be summarized.")
        print(result)
        # Expected output: { "summary": "This is a long text..." }

    """

    def __init__(self, max_length: int = 10):
        self.max_length = max_length

    def summarize(self, text_to_summarize: Optional[str] = None) -> Dict[str, Any]:
        """
        Summarizes the input text.

        Args:
            text_to_summarize: The text to summarize.

        Returns:
            A dictionary containing the summary.
            Returns an error if input is invalid
        """
        if not text_to_summarize or not isinstance(text_to_summarize, str):
            return {"error": "TEXT_TO_SUMMARIZE is not provided or is not a valid string."}

        # Simple summarization: Truncate and add ellipsis.
        if len(text_to_summarize) > self.max_length:
            summary = text_to_summarize[:self.max_length].strip() + "..."
        else:
            summary = text_to_summarize
        return {"agent": "summarizer", "result": {"summary": summary, "explanation": "This is a simple summarization agent."}}

def register_routes(router: APIRouter):
    """Registers the summarizer agent's routes with the provided APIRouter."""

    
    @router.get("/summarizer", summary="Summarizes input text", response_model=Dict[str, Any])
    async def summarizer_route(
        TEXT_TO_SUMMARIZE: Optional[str] = Query(None, description="The text to be summarized"),
        max_length: int = Query(10, description="Maximum length of the summary")
    ):
        """
        Summarizes the provided text.

        **Input:**

        *   **TEXT_TO_SUMMARIZE (optional, string):**  The text to summarize.

        **Process:**  An instance of `SummarizerAgent` is used.  The `summarize`
        method is called.

        **Example Input (query parameter):**

        `?TEXT_TO_SUMMARIZE=This is a very long text that we want to shorten to a reasonable length.`

        **Example Output:**

        ```json
        {
          "summary": "This is a very long text..."
        }
        ```

        **Example Output (if no input is provided):**
        ```json
        {
            "error": "TEXT_TO_SUMMARIZE is not provided or is not a valid string."
        }
        ```
        """
        agent = SummarizerAgent(max_length=max_length)
        result = agent.summarize(TEXT_TO_SUMMARIZE)
        return result