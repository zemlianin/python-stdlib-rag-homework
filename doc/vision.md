# Vision

## Технологии

Проект написан на Python. Для управления окружением используется `uv`. Для индексации применяется `scikit-learn` и `TfidfVectorizer`. Для поиска используется cosine similarity. Для интерфейса используется Streamlit. Для тестов используется pytest.

## Как строится индекс

Сначала `scripts/prepare_datasets.py` извлекает docstring из стандартной библиотеки Python и сохраняет их в `data/raw/datasets.json`. Затем `scripts/ingest.py` преобразует записи в `data/processed/documents.jsonl`. После этого `app/chunker.py` нарезает документы на чанки. Скрипт `scripts/build_index.py` обучает TF-IDF vectorizer на текстах чанков и сохраняет `vectorizer.pkl`, `matrix.npz` и `chunks.jsonl` в `data/index/`.

## Как работает поиск

Пользовательский вопрос превращается в TF-IDF вектор тем же vectorizer. Затем считается cosine similarity между вопросом и каждым чанком. Система возвращает top-k фрагментов с полями `doc_id`, `name`, `score`, `text`, `source_file`.

## Что не используется в MVP

В MVP не используется внешняя LLM, платные API, векторная база данных, reranking и сложная генерация. Ответ формируется в demo-режиме только из найденных чанков. Если score ниже порога, система отказывается отвечать.

## Как запускать проект

Основной запуск:

```bash
uv sync
uv run python scripts/build_index.py
uv run streamlit run app/main.py
```

Проверка тестов:

```bash
uv run pytest tests/ -v
```
