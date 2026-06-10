# Python Stdlib RAG

Учебный RAG на текстовых docstring стандартной библиотеки Python.

Pipeline: данные → documents → chunks → TF-IDF index → retrieval → demo-answer → Streamlit UI.

## Требования

- Python 3.10+
- uv

## Быстрый старт

```bash
uv sync
uv run python scripts/build_index.py
uv run streamlit run app/main.py
```

После запуска Streamlit откройте адрес, который будет показан в консоли, обычно `http://localhost:8501`.

## Что делает `build_index.py`

Команда `uv run python scripts/build_index.py` выполняет весь pipeline:

1. Проверяет `data/raw/datasets.json`.
2. Если данных меньше 1000 записей, автоматически запускает `scripts/prepare_datasets.py`.
3. Преобразует `datasets.json` в `data/processed/documents.jsonl`.
4. Нарезает документы на чанки в `data/processed/chunks.jsonl`.
5. Строит TF-IDF индекс.
6. Сохраняет артефакты в `data/index/`:
   - `vectorizer.pkl`
   - `matrix.npz`
   - `chunks.jsonl`

## Данные

Источник данных — docstring модулей, классов и функций из локально установленной стандартной библиотеки Python. Данные извлекаются скриптом `scripts/prepare_datasets.py` через `ast`. Обычно получается больше 1000 текстовых записей, точное число зависит от версии Python.

Подробнее: `doc/DATA.md`.

## Demo-вопросы

| Вопрос | Ожидаемое поведение |
|---|---|
| `How does gzip open compressed files?` | Ответ с источниками про `gzip` |
| `How does argparse parse command line arguments?` | Ответ с источниками про `argparse` |
| `What does pathlib provide for filesystem paths?` | Ответ с источниками про `pathlib` |
| `Как приготовить борщ?` | Отказ, потому что такого контекста нет |

## Проверка из консоли

```bash
uv run pytest tests/ -v
uv run python scripts/check_retrieval.py
uv run python scripts/check_generator.py
```

## Структура проекта

```text
python-stdlib-rag-homework/
├── app/
│   ├── config.py
│   ├── chunker.py
│   ├── retriever.py
│   ├── generator.py
│   ├── prompts.py
│   └── main.py
├── scripts/
│   ├── prepare_datasets.py
│   ├── ingest.py
│   ├── build_index.py
│   ├── check_retrieval.py
│   └── check_generator.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── index/
├── tests/
├── doc/
├── homework/
├── pyproject.toml
└── README.md
```

## Ограничения MVP

- Используется TF-IDF, поэтому поиск больше зависит от совпадения слов, чем от смысла.
- Внешняя LLM не используется.
- Ответ в demo-режиме составляется из найденных фрагментов.
- Если score ниже порога, система отказывается отвечать.

## Как сдавать

1. Загрузить этот проект в свой GitHub-репозиторий.
2. Проверить запуск команд из README.
3. Сделать fork учебного репозитория `MaratNotes/rag-tutorial`.
4. В fork добавить или изменить файл `homework/SUBMISSION.md`.
5. В `SUBMISSION.md` указать ссылку на свой репозиторий с решением.
6. Создать Pull Request в исходный репозиторий.
