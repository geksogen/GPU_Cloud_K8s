import pyaudio
import json
import os
import requests
from vosk import Model, KaldiRecognizer

from ollama import Client

client = Client(
  host='http://81.94.156.203:11434/',
  headers={'x-some-header': 'some-value'}
)

# Параметры записи
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 8192

# Инициализация PyAudio
audio = pyaudio.PyAudio()

# Открываем поток для записи
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Потоковая запись началась. Скажите 'Стоп', чтобы остановить.")

# Путь к модели Vosk
model_path = "model"  # Укажите путь к папке с моделью Vosk

# Проверяем, существует ли модель
if not os.path.exists(model_path):
    print(f"Модель не найдена в {model_path}")
else:
    # Загружаем модель
    model = Model(model_path)

    # Создаем распознаватель
    recognizer = KaldiRecognizer(model, RATE)

    # URL для запроса к Ollama
    ollama_url = "http://81.94.156.203:11434/api/generate"

    try:
        while True:
            data = stream.read(CHUNK)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_dict = json.loads(result)
                text = result_dict.get("text", "")
                if len(text) > 0:
                    print("Распознанный текст: ", text)
                # Проверка на слово "Стоп"
                if "стоп" in text.lower():
                    print("Программа остановлена.")
                    break

                if len(text) > 0:
                    # Отправка запроса к Ollama
                    print("Обработка LLM")
                    response = client.chat(
                        model='owl/t-lite',
                        messages=[{
                            'role': 'user',
                            'content': text.lower()
                        }]
                    )
                    #if response.status_code == 200:
                        #response_data = response.json()
                    print(response['message']['content'] + '\n')
                    print("Следующий вопрос :)")
                    #else:
                    #    print("Ошибка при запросе к Ollama:", response.status_code, response.text)
                #else:
                #    print("Вы нечего не сказали")

    except KeyboardInterrupt:
        print("Потоковая запись остановлена.")

# Останавливаем и закрываем поток
stream.stop_stream()
stream.close()
audio.terminate()
