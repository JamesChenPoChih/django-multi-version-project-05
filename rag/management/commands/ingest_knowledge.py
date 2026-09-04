from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from rag.models import KnowledgeDocument


class Command(BaseCommand):
    help = 'Import one or more local text/markdown files into the RAG knowledge base.'

    def add_arguments(self, parser):
        parser.add_argument('paths', nargs='+', help='Local .txt, .md, or .html files to import.')
        parser.add_argument('--source-prefix', default='', help='Optional source prefix shown in chatbot citations.')

    def handle(self, *args, **options):
        imported = 0
        for raw_path in options['paths']:
            path = Path(raw_path).expanduser().resolve()
            if not path.exists() or not path.is_file():
                raise CommandError(f'File not found: {path}')

            content = path.read_text(encoding='utf-8', errors='ignore').strip()
            if not content:
                self.stdout.write(self.style.WARNING(f'Skipped empty file: {path}'))
                continue

            source = f"{options['source_prefix']}{path.name}"
            KnowledgeDocument.objects.update_or_create(
                source=source,
                defaults={
                    'title': path.stem,
                    'content': content,
                    'is_active': True,
                },
            )
            imported += 1

        self.stdout.write(self.style.SUCCESS(f'Imported {imported} knowledge document(s).'))
