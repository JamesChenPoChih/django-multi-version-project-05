from django.contrib import admin

from .models import KnowledgeDocument


@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'is_active', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'source', 'content')
