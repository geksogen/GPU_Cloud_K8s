import pyaudio
import wave

# Параметры записи
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "recorded_audio.wav"

# Инициализация PyAudio
audio = pyaudio.PyAudio()

# Открываем поток для записи
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Запись началась...")

frames = []

# Записываем данные
try:
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
except KeyboardInterrupt:
    # Останавливаем запись при нажатии Ctrl+C
    print("Запись остановлена.")

print("Запись завершена.")

# Останавливаем и закрываем поток
stream.stop_stream()
stream.close()
audio.terminate()

# Сохраняем записанные данные в файл
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Запись сохранена в {WAVE_OUTPUT_FILENAME}")
