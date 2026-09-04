from .nemotron_client import chat_with_nemotron
from .retriever import retrieve_context


SYSTEM_PROMPT = '''
You are HackerMoose AI's website assistant.
Answer in English by default.
Use the provided context when it is relevant.
If the context does not contain the answer, say so clearly and give the best next step.
Keep answers concise and practical.
'''.strip()


def _format_context(context_items):
    if not context_items:
        return 'No matching local context was found.'

    blocks = []
    for index, item in enumerate(context_items, start=1):
        blocks.append(
            f"[{index}] Title: {item['title']}\nSource: {item['source']}\n{item['text']}"
        )
    return '\n\n'.join(blocks)


def answer_question(question):
    context_items = retrieve_context(question)
    sources = []
    seen_sources = set()
    for item in context_items:
        source_key = (item['title'], item['source'])
        if source_key in seen_sources:
            continue
        seen_sources.add(source_key)
        sources.append({
            'title': item['title'],
            'source': item['source'],
            'score': item['score'],
        })

    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {
            'role': 'user',
            'content': (
                'Local RAG context:\n'
                f'{_format_context(context_items)}\n\n'
                f'User question: {question}'
            ),
        },
    ]

    answer = chat_with_nemotron(messages)
    return {
        'answer': answer,
        'sources': sources,
    }
