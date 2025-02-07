import pyaudio
import json
import os
from vosk import Model, KaldiRecognizer
from ollama import Client
from speechkit import Session, SpeechSynthesis

client = Client(
  host='http://81.94.156.203:11434/',
  headers={'x-some-header': 'some-value'}
)

oauth_token = "y0_AgAAAAB6bN0mAATuwQAAAAEbnkPjAACg8TcmqidA7aRLT-uIt5s4VYaKJg"
catalog_id = "b1gho3om0lee0vkneq4e"

session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)
synthesizeAudio = SpeechSynthesis(session)

def pyaudio_play_audio_function(audio_data, num_channels=1,
                                sample_rate=16000, chunk_size=4000) -> None:
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=num_channels,
        rate=sample_rate,
        output=True,
        frames_per_buffer=chunk_size
    )

    try:
        for i in range(0, len(audio_data), chunk_size):
            stream.write(audio_data[i:i + chunk_size])
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

sample_rate = 16000 # частота дискретизации должна
                    # совпадать при синтезе и воспроизведении

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

    # Создаем распознаватель :)
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
                    print("Программа остановлена")
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

                    print(response['message']['content'] + '\n')
                    # Синтез речи
                    audio_data = synthesizeAudio.synthesize_stream(
                    text=response['message']['content'], # Ответ от LLM
                    voice='ermil', format='lpcm', sampleRateHertz=sample_rate
                    )
                    # Воспроизводим синтезированный файл
                    pyaudio_play_audio_function(audio_data, sample_rate=sample_rate)
                    print("Следующий вопрос :)" + '\n')


    except KeyboardInterrupt:
        print("Потоковая запись остановлена.")

# Останавливаем и закрываем поток
stream.stop_stream()
stream.close()
audio.terminate()
