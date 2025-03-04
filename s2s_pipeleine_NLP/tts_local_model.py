import os
import torch
import pyaudio
import wave

device = torch.device('cpu')
torch.set_num_threads(4)
local_file = 'tts_model/v4_ru.ptt'

def play_wav(file_path):
    # Открываем WAV файл
    wf = wave.open(file_path, 'rb')

    # Создаем объект PyAudio
    p = pyaudio.PyAudio()

    # Открываем поток для воспроизведения
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Читаем данные из WAV файла и воспроизводим их
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # Закрываем поток и освобождаем ресурсы
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()


if not os.path.isfile(local_file):
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v4_ru.pt',
                                   local_file)

model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)

example_text = 'В недрах тундры выдры в г+етрах т+ырят в вёдра ядра кедров.'
sample_rate = 48000
speaker='aidar'

audio_paths = model.save_wav(text=example_text,
                             speaker=speaker,
                             sample_rate=sample_rate)

play_wav('test.wav')
