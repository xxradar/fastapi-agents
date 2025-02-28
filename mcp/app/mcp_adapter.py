import requests
import os

class MCPAdapter:
    def __init__(self):
        self.endpoint = os.environ.get("MCP_ENDPOINT")
        self.api_key = os.environ.get("MCP_API_KEY")
        if not self.endpoint or not self.api_key:
            print("Warning: MCPAdapter could not be initialized: MCP_ENDPOINT and MCP_API_KEY must be set in the environment.")
        self.initialized = self.endpoint and self.api_key

    def send_context(self, context_data: dict) -> dict:
        """
        Sends context data to the MCP endpoint.
        """
        if not self.initialized:
            print("Warning: MCPAdapter not initialized. Returning original context.")
            return context_data

        url = f"{self.endpoint}/send"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"context": context_data}
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Warning: Error sending context to MCP: {e}")
            return context_data

    def get_response(self) -> dict:
        """
        Retrieves the response from the MCP endpoint.
        """
        if not self.initialized:
            print("Warning: MCPAdapter not initialized. Returning empty response.")
            return {}

        url = f"{self.endpoint}/response"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Warning: Error getting response from MCP: {e}")
            return {}
