import pyaudio
import json
import os
from vosk import Model, KaldiRecognizer
import time

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

time.sleep(3)
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

    try:
        while True:
            data = stream.read(CHUNK)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_dict = json.loads(result)
                text = result_dict.get("text", "")
                print("Распознанный текст: ", text)

                # Проверка на слово "Стоп"
                if "стоп" in text.lower():
                    print("Программа остановлена.")
                    break
    except KeyboardInterrupt:
        print("Потоковая запись остановлена.")

# Останавливаем и закрываем поток
stream.stop_stream()
stream.close()
audio.terminate()
