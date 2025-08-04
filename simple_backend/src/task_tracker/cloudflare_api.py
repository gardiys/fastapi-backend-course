import os, requests

class CloudflareClient:
    def __init__(self):
        self.api_url = os.getenv("CLOUDFLARE_API_URL")
        self.api_key = os.getenv("CLOUDFLARE_API_KEY")
        if not self.api_url or not self.api_key:
            raise RuntimeError("Cloudflare API URL or API key not set in environment")

    def get_solution(self, task_text: str) -> str:
        prompt = f"Explain step-by-step how to solve the following task:\n{task_text}"
        try:
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]}
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error querying Cloudflare LLM API: {e}")
            return "(Error fetching solution.)"

        data = response.json()
        solution_text = data.get("result", {}).get("response")
        if not solution_text:
            return "(No solution found.)"
        return solution_text
