import os
from pathlib import Path

import django
from mcp.server.fastmcp import FastMCP


BASE_DIR = Path(__file__).resolve().parent.parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
django.setup()


mcp = FastMCP(
    'HackerMoose Django',
    instructions=(
        'Tools for querying the HackerMoose Django project, including products, '
        'RAG knowledge documents, and the local Nemotron-backed chatbot.'
    ),
)


def _serialize_product(product):
    return {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
        'image': product.image,
    }


def _serialize_knowledge_document(document):
    return {
        'id': document.id,
        'title': document.title,
        'source': document.source,
        'content': document.content,
        'is_active': document.is_active,
        'updated_at': document.updated_at.isoformat() if document.updated_at else None,
    }


@mcp.tool()
def list_products(limit: int = 50) -> list[dict]:
    """List products from the Django product catalog."""
    from products.models import Product

    safe_limit = max(1, min(limit, 100))
    return [
        _serialize_product(product)
        for product in Product.objects.all().order_by('name')[:safe_limit]
    ]


@mcp.tool()
def get_product(product_id: int) -> dict:
    """Get one product by its Django database id."""
    from products.models import Product

    product = Product.objects.get(pk=product_id)
    return _serialize_product(product)


@mcp.tool()
def search_knowledge(query: str, limit: int = 5) -> list[dict]:
    """Search RAG context across active knowledge documents, products, and project files."""
    from rag.services.retriever import retrieve_context

    safe_limit = max(1, min(limit, 10))
    return retrieve_context(query, limit=safe_limit)


@mcp.tool()
def list_knowledge_documents(limit: int = 50, active_only: bool = True) -> list[dict]:
    """List RAG knowledge documents stored in Django."""
    from rag.models import KnowledgeDocument

    queryset = KnowledgeDocument.objects.all()
    if active_only:
        queryset = queryset.filter(is_active=True)

    safe_limit = max(1, min(limit, 100))
    return [
        _serialize_knowledge_document(document)
        for document in queryset.order_by('title')[:safe_limit]
    ]


@mcp.tool()
def create_knowledge_document(title: str, content: str, source: str = 'mcp') -> dict:
    """Create a new active RAG knowledge document in Django."""
    from rag.models import KnowledgeDocument

    document = KnowledgeDocument.objects.create(
        title=title.strip(),
        source=source.strip(),
        content=content.strip(),
        is_active=True,
    )
    return _serialize_knowledge_document(document)


@mcp.tool()
def ask_rag_chatbot(question: str) -> dict:
    """Ask the same RAG + local Nemotron pipeline used by the website chatbot."""
    from rag.services.rag_pipeline import answer_question

    return answer_question(question.strip())


@mcp.tool()
def server_health() -> dict:
    """Return a compact health check for Django, RAG, and local Nemotron configuration."""
    from django.conf import settings
    from rag.models import KnowledgeDocument

    return {
        'django_settings_module': os.environ.get('DJANGO_SETTINGS_MODULE'),
        'knowledge_documents': KnowledgeDocument.objects.count(),
        'rag_llm_base_url': settings.RAG_LLM_BASE_URL,
        'rag_llm_model': settings.RAG_LLM_MODEL,
    }


def main():
    mcp.run()


if __name__ == '__main__':
    main()
