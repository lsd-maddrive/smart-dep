# smart-dep
Smart Department project

# Тесты с pocketsphynx

Для работы необходимо скачать словарь для библиотеки по следующей ссылке: https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/Russian/zero_ru_cont_8k_v3.tar.gz/download
Архив нужно распаковать. Затем надо папку <your_folder>/zero_ru_cont_8k_v3/zero_ru.cd_cont_4000 переместить в папку <your_folder_2>/lib/python3.6/site-packages/pocketsphinx/model, где <your_folder> это папка в которую вы распаковали архив. Перемещенная папка — это акустическая модель, а <your_folder_2> это папка с виртуальным окружением вашего проекта. Такую же процедуру надо проделать с файлами ru.lm и ru.dic из папки <your_folder>/zero_ru_cont_8k_v3/. Файл ru.lm это языковая модель, а ru.dic это словарь.
