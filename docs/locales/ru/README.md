<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->

Языки: [English](../../../README.md) · [Italiano](../it/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [Deutsch](../de/README.md) · [Русский](README.md) · [中文](../zh/README.md).

<p align="center">
  <a href="https://onekit.org"><img src="https://raw.githubusercontent.com/mattiapiazzalunga/onekit/main/images/logo.png" alt="OneKit logo" width="112" height="112"></a>
</p>
<h1 align="center">OneKit</h1>
<p align="center">Один набор инструментов. Ваши файлы остаются вашими.</p>
<p align="center"><a href="https://github.com/mattiapiazzalunga/onekit/stargazers"><img alt="Звёзды на GitHub" src="https://img.shields.io/github/stars/mattiapiazzalunga/onekit"></a> <a href="https://pypi.org/project/onekit-tools/"><img alt="PyPI" src="https://img.shields.io/pypi/v/onekit-tools"></a> <img alt="PolyForm-Shield-1.0.0" src="https://img.shields.io/badge/license-PolyForm_Shield_1.0.0-blue"> <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue"></p>

Офлайн-набор инструментов Python с 230 инструментами для конвертации, PDF, изображений, архивов, шрифтов, проверки файлов, шифрования, утилит для разработчиков, OCR и сравнений. Используйте этот CLI или графический интерфейс на **[onekit.org](https://onekit.org)**.

**Исходная версия:** `0.6.1`. Стабильные загрузки становятся доступны только после завершения рабочего процесса релиза. Распространяемая версия — `onekit-tools`; отдельный проект PyPI под названием `onekit` не имеет отношения.

[Руководство по контактам и мультимедиа](docs/contact-media.md) описывает создание отдельных vCard, извлечение vCard из QR-кодов, увеличение разрешения изображений, удаление фона, сжатие и изменение скорости видео и GIF, а также локальную расшифровку аудио.

Проверка лицензий: проверяйте PDF, Word, PowerPoint, Excel, видео, аудио, изображения, шрифты, EPUB, код/проекты и наборы данных из файлов или публичных URL. Анализ остаётся локальным; отчёты — это **неподтверждённые оценки, а не свидетельства собственности или разрешение на использование**. Смотрите [использование проверки лицензий и ограничения](docs/cli.md#local-license-and-copyright-estimates).

**Ваш CLI. Ваш CLI для агентов.** Используйте OneKit самостоятельно или позвольте локальному агенту AI вызвать его через терминал или подпроцесс. Находите инструменты и требования как JSON, передавайте явные пути ввода/вывода и повторно используйте сохранённые рабочие процессы `.1kit` для повторяющихся задач с файлами. См. [локальные агенты и автоматизация](docs/cli.md#local-agents-and-automation).

<a id="install"></a>
## Install

Требуется Python 3.11 или новее. Универсальный пакет wheel поддерживает Windows, macOS и Linux на x64/ARM64. Для необязательных нативных библиотек и внешних движков действуют дополнительные требования к платформе.

После публикации:

```sh
python -m pip install onekit-tools
python -m pip install "onekit-tools[pdf,images,documents]"
onekit list
onekit doctor
```

Из локальной копии репозитория исходного кода:

```sh
python -m pip install -e ".[all,test]"
python -m onekit --help
python -m pytest -q
```

Базовая CLI **не имеет зависимостей во время выполнения**. Устанавливайте только те дополнительные элементы, которые вам нужны. `all` включает стандартные семейства Python; загрузка видео, удаление фона, транскрипция и криптографическая подпись используют отдельные дополнения `video`, `background`, `transcription` и `signing`. Устанавливайте нативные движки отдельно. Для инструментов разработки на основе Node установите Node.js 24+ и запустите `onekit engines install`. CLI готовит отсутствующие зависимости и внешние движки при первом использовании. Удаление фона и транскрипция загружают веса моделей при первом использовании, затем используют локальный кэш.

<a id="use"></a>
## Use

```sh
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit run pdf-extract-pages document.pdf --options '{"pages":"1,3-5"}' -o selected.pdf
onekit run image-convert image.png --options '{"format":"webp"}' -o image.webp
onekit run diff-notebook before.ipynb after.ipynb --options '{"mode":"code"}' -o changes.json
onekit run security-encrypt private-folder --ask-password -o private.zip
onekit run security-decrypt private.zip --ask-password -o restored
```

Опции — объекты JSON; передавайте их одной аргументной строкой в кавычках. Для секретов используйте `--ask-password`. Существующие результаты сохраняются, если вы не передадите `--force`.

`onekit list --group pdf`, `onekit list --json` и `onekit doctor TOOL_ID` показывают контракты и требования. Каждый инструмент имеет каталог в [tools](../../../tools), содержащий метаданные и ссылку на его общую реализацию. Смотрите руководство [CLI guide](docs/cli.md) для опций и ограничений.

<a id="toolkit"></a>
## Toolkit

| Семья | Возможности |
| --- | --- |
| Конвертеры | Markdown, HTML, LaTeX, PDF, Word, PowerPoint, изображения, Base64, Excel, CSV и JSON |
| PDF | Объединение/разделение, выбор/порядок/удаление страниц, сжатие, исправление, [прямое редактирование текста](docs/pdf-editing.md), текстовые наложения, вращение, цифровые подписи, шифрование/разблокировка, [локальное преобразование в PDF/A и проверка](docs/pdfa.md) |
| Изображения | Извлечь встроенные PDF изображения, сжать, обрезать и изменить формат |
| Медиа | Конвертация аудио/видео через отдельно установленный FFmpeg |
| Архивы / шрифты | Варианты ZIP/TAR; контейнеры TTF/OTF и WOFF/WOFF2 |
| Инспектор / безопасность | Введите подписи, структуру, метаданные, кодировку, хэши, количество текста; аутентифицированные зашифрованные архивы файлов/папок |
| Разработчик | Форматирование для конкретного языка, проверка парсера/компилятора и выбранное минимизирование |
| OCR | Отсканированные изображения/PDF в поисковые PDF, Word, Markdown, LaTeX, HTML и JSON |
| Отличие | Текст, код, нормализованный JSON, блокноты, LaTeX, PDF и Word текст |

<a id="pipelines-and-development"></a>
## Pipelines and development

`onekit pipeline --steps workflow.1kit INPUTS -o OUTPUT` принимает версионированный рабочий документ `.1kit`. Каждый шаг получает предыдущие результаты. Шаги с одним входом применяются к нескольким выходам; шаги с объединением получают всю коллекцию. Несовместимые типы останавливают обработку.

Сообщайте об ошибках и предложениях через [GitHub issues](https://github.com/mattiapiazzalunga/onekit/issues) или на [доске запросов сайта](https://onekit.org/requests/). Участники могут найти работу в любом из этих мест.

<a id="contribute-to-onekit"></a>
## Contribute to OneKit

Помогите строить открытую революцию OneKit: повседневные инструменты для всех, от ручных задач до рабочих процессов, управляемых локальными агентами AI. Вносите свой вклад, чтобы сделать инструменты более эффективными и результативными: улучшайте скорость и использование памяти, исправляйте неверные результаты, добавляйте примеры регрессии или уточняйте документацию и рабочие процессы агентов.

Ядро является Открытым Исходным Кодом (PolyForm Shield 1.0.0). Прочитайте [руководство для участников](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md) и найдите задачу в [задачах GitHub](https://github.com/mattiapiazzalunga/onekit/issues), или предложите улучшение на [доске запросов](https://onekit.org/requests/).

<a id="license-and-creator"></a>
## License and creator

Создано **[Mattia Piazzalunga](mailto:hello@mattiapiazzalunga.com)**. Авторские права © 2026 Mattia Piazzalunga. Открытый исходный код (PolyForm Shield 1.0.0), лицензирован под [PolyForm Shield 1.0.0](../../../LICENSE); см. [NOTICE](../../../NOTICE), [AUTHORS.txt](../../../AUTHORS.txt) и [CONTRIBUTORS.txt](../../../CONTRIBUTORS.txt). Компоненты сторонних разработчиков сохраняют свои лицензии. Внешние движки — это отдельные программы с собственными обязательствами по распространению.

Вы можете использовать, изменять и перераспределять ядро для разрешённых целей, включая коммерческое и внутреннее использование. Вы не можете использовать его для предоставления продукта или услуги, которая конкурирует с программным обеспечением или продуктом, который лицензиар или его аффилированные лица предоставляют с использованием этого программного обеспечения; бесплатные предложения и различные платформы или интерфейсы также могут конкурировать. При распространении копий включайте текст лицензии или её URL, а также любые строки Required Notice, предоставленные с программным обеспечением. Полная лицензия регулирует это, включая исключения для новых и снятых с производства продуктов, условия патента и отказ от гарантии. Здесь «Open Source (PolyForm Shield 1.0.0)» описывает опубликованный исходный код на этих условиях; ограничение на конкуренцию означает, что это программное обеспечение с доступным исходным кодом, а не неограниченный открытый исходный код по определению Open Source. См. [руководство по лицензированию](docs/licenses.md).

Экспорт и повторный импорт рабочих процессов без обработки входных файлов:

```sh
onekit workflow export workflow.1kit -o exported-workflow.1kit
onekit workflow import workflow.1kit -o saved-workflow.1kit
onekit pipeline --steps saved-workflow.1kit input.json -o output.json
```

Стандартные штрихкоды доступны в категории «QR-коды и штрихкоды» и в CLI: `text-to-barcode`, `scan-barcode`, `barcode-to-text`. Код 128, Код 39, EAN-13, EAN-8, UPC-A, ITF и ISBN-13 поддерживают PNG/SVG, настраиваемые размеры и проверку контрольной цифры. Установите `onekit-tools[barcode]` или `onekit-tools[qrcode]`.

[Необратимое скрытие данных в PDF и изображениях](docs/redaction.md) доступно через `pdf-redact` и `image-redact`. В новых файлах выбранные области заменяются непрозрачными чёрными пикселями. PDF пересоздаются как документы только с изображениями, без исходного текста, форм, комментариев, вложений и метаданных; изображения преобразуются в непрозрачные PNG без исходных метаданных и пикселей, скрытых прозрачностью. Исходные файлы не изменяются.

Добавляйте настраиваемые текстовые водяные знаки в PDF с помощью `pdf-watermark`: задавайте непрозрачность, цвет, шрифты, диапазоны страниц, положение, поворот и повторяющиеся сетки. Текст и графика сохраняются в PDF. См. [руководство по водяным знакам](docs/watermark.md).

<a id="contacts"></a>
## Contacts

- Общие вопросы и поддержка: [support@onekit.org](mailto:support@onekit.org).
- Вопросы по ядру Open Source (PolyForm Shield 1.0.0) и вкладу: [developers@onekit.org](mailto:developers@onekit.org).
- Конфиденциальность, GDPR и запросы по персональным данным: [privacy@onekit.org](mailto:privacy@onekit.org).
- Юридические вопросы, лицензирование и запросы разрешений: [legal@onekit.org](mailto:legal@onekit.org).
- Уязвимости в безопасности и отчёты о злоупотреблениях: [security@onekit.org](mailto:security@onekit.org).
