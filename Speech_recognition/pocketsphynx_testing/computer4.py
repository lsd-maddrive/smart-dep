import os
from pocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path()

speech = LiveSpeech(
    verbose=False,
    sampling_rate=8000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'zero_ru.cd_cont_4000'),
    lm=os.path.join(model_path, 'ru.lm'),
    keyphrase='компьютер',
    kws_threshold=1e-20,
    dic=os.path.join(model_path, 'ru.dic')
)


print("Say something!")

for phrase in speech:
    print(phrase)
