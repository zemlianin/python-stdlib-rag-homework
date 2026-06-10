# Tasklist

| Итерация | Задача | Проверка | Статус |
|---|---|---|---|
| 00 | Создать каркас проекта | `uv run python -c "import app.config"` | done |
| 01 | Подготовить данные | `uv run python scripts/prepare_datasets.py` | done |
| 02 | Реализовать ingestion | `uv run python scripts/ingest.py` | done |
| 03 | Реализовать chunking | `uv run pytest tests/test_chunking.py -v` | done |
| 04 | Построить TF-IDF index | `uv run python scripts/build_index.py` | done |
| 05 | Реализовать retrieval | `uv run python scripts/check_retrieval.py` | done |
| 06 | Реализовать demo-answer | `uv run python scripts/check_generator.py` | done |
| 07 | Реализовать Streamlit UI | `uv run streamlit run app/main.py` | done |
| 08 | Добавить тесты и README | `uv run pytest tests/ -v` | done |

## Текущая итерация

MVP завершен. Проект имеет полный pipeline от подготовки данных до UI.

## Критерии завершения MVP

- Есть 1000+ записей в `datasets.json` или 1000+ чанков после нарезки.
- Индекс собирается одной командой.
- Retrieval возвращает `doc_id`, `score`, `text`.
- Demo-answer отвечает только по контексту.
- Negative-вопрос дает отказ.
- README содержит команды запуска.
