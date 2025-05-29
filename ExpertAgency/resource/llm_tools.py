from openai import AzureOpenAI
from typing import List, Dict, Optional, Union, Generator
import logging
import json

logging.basicConfig(level=logging.INFO)


class LLMTools:
    """
    A robust wrapper around Azure OpenAI's ChatCompletion API using the latest OpenAI SDK (>=1.0.0).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        api_version: Optional[str] = None,
        deployment_name: Optional[str] = None,
    ):
        self.api_key = api_key or "bf05d6ce0b6942e7aac9f66421152f76"
        self.endpoint = endpoint or "https://biolens.openai.azure.com/"
        self.api_version = api_version or "2025-01-01-preview"
        self.deployment_name = deployment_name or "biolens-4.1mini-vD"  # Not model name like gpt-4

        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
        )

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stream: bool = False,
        structured_output: bool = False,
    ) -> Union[str, Dict, Generator[str, None, None]]:
        """
        Call Azure ChatCompletion and return the result (streamed or full).
        """
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
            )

            if stream:
                return self._stream_response(response)
            else:
                raw_content = response.choices[0].message.content
                if structured_output:
                    try:
                        parsed = json.loads(raw_content)
                        return {
                            "response": parsed,
                            "usage": response.usage,
                        }
                    except:
                        return {
                            "response": raw_content,
                            "usage": response.usage,
                            "warning": "Failed to parse structured output.",
                        }
                else:
                    return {
                        "response": raw_content,
                        "usage": response.usage,
                    }
        except Exception as e:
            logging.exception("Chat completion failed.")
            return {"error": str(e)}

    def simple_chat(self, system_message: str, user_message: str) -> str:
        """
        Simple chat interface returning plain text response.
        """
        result = self.chat_completion(
            [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ]
        )
        return result.get("response", result)

    def _stream_response(self, response) -> Generator[str, None, None]:
        """
        Internal streaming handler.
        """
        try:
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"\n[Stream Error] {str(e)}"

    def usage_summary(self, system_message: str, user_message: str) -> Dict:
        """
        Returns token usage details.
        """
        result = self.chat_completion(
            [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ]
        )
        return {
            "tokens_used": result.get("usage", {}).dict() if hasattr(result.get("usage", {}), "dict") else result.get("usage", {}),
            "response": result.get("response", None),
        }



if __name__ == "__main__":
    llm = LLMTools()

    system = "You are a helpful assistant."
    user = "What is the capital of Nepal?"

    print("📘 Plain response:")
    print(llm.simple_chat(system, user))

    print("\n📊 Usage details:")
    print(llm.usage_summary(system, user))

    print("\n📡 Streaming response:")
    for part in llm.chat_completion(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        stream=True
    ):
        print(part, end="", flush=True)