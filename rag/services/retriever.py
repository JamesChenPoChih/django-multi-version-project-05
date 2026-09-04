import re
from pathlib import Path

from django.conf import settings

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None


def _tokenize(text):
    return re.findall(r'[\w]+', text.lower())


def _chunk_text(text, chunk_size=900, overlap=150):
    clean_text = re.sub(r'\s+', ' ', text).strip()
    if len(clean_text) <= chunk_size:
        return [clean_text]

    chunks = []
    start = 0
    while start < len(clean_text):
        chunks.append(clean_text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks


def _make_docs(source, text, title=None):
    return [
        {
            'title': title or source,
            'source': source,
            'text': chunk,
        }
        for chunk in _chunk_text(text)
        if chunk
    ]


def _project_documents():
    docs = []
    for relative_path in ['README.md', 'templates/index.html']:
        path = Path(settings.BASE_DIR) / relative_path
        if path.exists():
            docs.extend(_make_docs(
                source=relative_path,
                text=path.read_text(encoding='utf-8', errors='ignore'),
                title=path.name,
            ))
    return docs


def _knowledge_documents():
    try:
        from rag.models import KnowledgeDocument
    except Exception:
        return []

    docs = []
    for item in KnowledgeDocument.objects.filter(is_active=True)[:200]:
        docs.extend(_make_docs(
            source=item.source or f'KnowledgeDocument #{item.pk}',
            text=item.content,
            title=item.title,
        ))
    return docs


def _product_documents():
    try:
        from products.models import Product
    except Exception:
        return []

    docs = []
    for product in Product.objects.all()[:100]:
        docs.extend(_make_docs(
            source=f'Product #{product.pk}',
            title=product.name,
            text=(
                f'Product name: {product.name}\n'
                f'Price: {product.price}\n'
                f'Quantity: {product.quantity}\n'
                f'Image: {product.image}'
            ),
        ))
    return docs


def load_documents():
    docs = _knowledge_documents() + _product_documents() + _project_documents()
    unique_docs = []
    seen = set()
    for doc in docs:
        key = doc['text']
        if key in seen:
            continue
        seen.add(key)
        unique_docs.append(doc)
    return unique_docs


def retrieve_context(question, limit=4):
    docs = [doc for doc in load_documents() if doc['text'].strip()]
    if not docs:
        return []

    query_tokens = _tokenize(question)
    corpus_tokens = [_tokenize(doc['text']) for doc in docs]

    if BM25Okapi is not None:
        scores = BM25Okapi(corpus_tokens).get_scores(query_tokens)
    else:
        query_set = set(query_tokens)
        scores = [len(query_set.intersection(tokens)) for tokens in corpus_tokens]

    ranked_docs = sorted(zip(scores, docs), key=lambda item: item[0], reverse=True)
    return [
        {
            'title': doc['title'],
            'source': doc['source'],
            'text': doc['text'],
            'score': float(score),
        }
        for score, doc in ranked_docs[:limit]
        if score > 0
    ]
