SYSTEM_RULES = """
You answer only from retrieved context chunks.
Do not invent modules, functions, behavior, variables, periods, or sources.
If there is no relevant context, refuse clearly.
""".strip()

REFUSAL_EMPTY_QUESTION = "Введите вопрос."
REFUSAL_NO_CONTEXT = "В базе не найдено релевантных фрагментов. Ответить по данным невозможно."
