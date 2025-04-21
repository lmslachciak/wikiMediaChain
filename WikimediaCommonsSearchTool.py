from pydantic import BaseModel, Field
import requests
from langchain_core.tools.base import BaseTool
from typing import Type, Optional

# Output schema definition
class WikimediaCommonsInput(BaseModel):
    """Input for the Wikimedia Commons search tool."""
    query: str = Field(description="The search term to look for files on Wikimedia Commons")
    limit: Optional[int] = Field(default=10, description="Maximum number of results to return")

# Definition of tool
class WikimediaCommonsSearchTool(BaseTool):
    """Tool that searches for files (images, videos, audio) on Wikimedia Commons."""

    name: str = "wikimedia_commons_search"
    description: str = (
        "Useful for searching for files (images, videos, audio) on Wikimedia Commons. "
        "Returns a list of file titles found."
    )
    args_schema: Type[WikimediaCommonsInput] = WikimediaCommonsInput

    def _run(self, query: str, limit: int = 10) -> str:
        """Use the tool synchronously."""
        api_url = "https://commons.wikimedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srnamespace": 6,  # Namespace 6 corresponds to "File"
            "srlimit": limit,
            "srsort": "relevance"
        }
        headers = {
            'User-Agent': 'LangchainTool/1.0 (https://www.google.com; example@example.com)' # Dobrą praktyką jest identyfikacja klienta API
        }

        try:
            response = requests.get(api_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()  # Rzuci wyjątkiem dla złych odpowiedzi (4xx, 5xx)
            data = response.json()

            search_results = data.get("query", {}).get("search", [])

            if not search_results:
                return f"No files found on Wikimedia Commons for query: '{query}'"

            file_titles = [result["title"] for result in search_results]

            formatted_results = []
            base_url = "https://commons.wikimedia.org/wiki/"
            for title in file_titles:
                encoded_title = requests.utils.quote(title.replace(" ", "_"))
                formatted_results.append(f"- {title} ({base_url}{encoded_title})")


            return f"Found files on Wikimedia Commons for '{query}':\n" + "\n".join(formatted_results)

        except requests.exceptions.RequestException as e:
            return f"Error connecting to Wikimedia Commons API: {e}"
        except Exception as e:
            return f"An error occurred: {e}"

    async def _arun(self, query: str, limit: int = 10) -> str:
        """Use the tool asynchronously."""
        api_url = "https://commons.wikimedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srnamespace": 6,
            "srlimit": limit,
            "srsort": "relevance"
        }
        headers = {
            'User-Agent': 'LangchainTool/1.0 (https://www.google.com; example@example.com)'
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url, params=params, headers=headers, timeout=10) as response:
                    response.raise_for_status()
                    data = await response.json()

                    search_results = data.get("query", {}).get("search", [])
                    if not search_results:
                        return f"No files found on Wikimedia Commons for query: '{query}'"

                    file_titles = [result["title"] for result in search_results]
                    base_url = "https://commons.wikimedia.org/wiki/"
                    formatted_results = [
                        f"- {title} ({base_url}{requests.utils.quote(title.replace(' ', '_'))})"
                        for title in file_titles
                    ]
                    return f"Found files on Wikimedia Commons for '{query}':\n" + "\n".join(formatted_results)

            except aiohttp.ClientError as e:
                return f"Error connecting to Wikimedia Commons API: {e}"
            except Exception as e:
                return f"An error occurred: {e}"