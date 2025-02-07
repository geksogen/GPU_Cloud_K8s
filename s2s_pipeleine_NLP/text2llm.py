from ollama import Client

client = Client(
  host='http://81.94.156.203:11434/',
  headers={'x-some-header': 'some-value'}
)


chat_response = client.chat(
    model='owl/t-lite',
    messages=[{
        'role': 'user',
        'content': 'Пример кода на Python'
    }]
)

print(chat_response['message']['content'])
