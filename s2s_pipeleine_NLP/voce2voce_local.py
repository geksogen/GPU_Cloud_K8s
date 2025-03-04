import pyaudio
import json
import os
from vosk import Model, KaldiRecognizer
import torch
import numpy as np
import time
from ollama import Client

client = Client(
  host='http://81.94.156.147:11434/',
  headers={'x-some-header': 'some-value'}
)

device = torch.device('cpu')
torch.set_num_threads(4)
local_file = 'tts_model/v4_ru.ptt'

model_tts = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model_tts.to(device)

sample_rate = 48000
speaker='aidar' # 'aidar', 'baya', 'kseniya', 'xenia', 'random'


def play_tensor(tensor, sample_rate):
    # Преобразуем тензор в numpy массив
    audio_data = tensor.numpy()

    # Создаем объект PyAudio
    p = pyaudio.PyAudio()

    # Открываем поток для воспроизведения
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    # Воспроизводим аудио
    stream.write(audio_data.astype(np.float32).tobytes())

    # Закрываем поток и освобождаем ресурсы
    stream.stop_stream()
    stream.close()
    p.terminate()


sample_rate = 48000 # частота дискретизации должна
                    # совпадать при синтезе и воспроизведении

# Параметры записи
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
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

    # Создаем распознаватель :)
    recognizer = KaldiRecognizer(model, RATE)

    # URL для запроса к Ollama
    ollama_url = "http://81.94.156.147:11434/api/generate"

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
                    print("Программа остановлена")
                    break
                # Проверка на наличие вопроса
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
                    print("Ответ от LLM" + '\n')
                    print(response['message']['content'] + '\n')
                    # Синтез речи
                    print("Синтез речи" + '\n')
                    start_time = time.time()
                    audio_data = model_tts.apply_tts(response['message']['content'],
                             speaker=speaker,
                             sample_rate=sample_rate)
                    # Воспроизводим синтезированный файл
                    print("Воспроизведение ответа" + '\n')
                    play_tensor(audio_data, sample_rate)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(f"Result Time: {elapsed_time} секунд" + '\n')
                    print("Следующий вопрос :)" + '\n')

    except KeyboardInterrupt:
        print("Потоковая запись остановлена.")

# Останавливаем и закрываем поток
stream.stop_stream()
stream.close()
audio.terminate()
