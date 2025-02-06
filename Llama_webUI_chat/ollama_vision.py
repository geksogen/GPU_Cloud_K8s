from ollama import Client
from pydantic import BaseModel
import time

start_time = time.time()
client = Client(
  host='http://176.99.130.225:11434/',
  headers={'x-some-header': 'some-value'}
)

class Country(BaseModel):
  total_cost: float

error_llm = []

for i in range(500):
    chat_response = client.chat(
        model='llama3.2-vision',
        messages=[{
            'role': 'user',
            'content': 'What is the total cost receipt? The result is only a digital value.',
            'images': ['image.jpg']
        }],
        format=Country.model_json_schema(),
    )

    data = Country.model_validate_json(chat_response.message.content)
    if data.total_cost != 82.80:
        error_llm.append('TRUE')

print(f"LLM Error: {len(error_llm)}")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Result Time: {elapsed_time} секунд")
