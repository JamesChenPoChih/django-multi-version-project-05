import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .services.rag_pipeline import answer_question


def chatbot(request):
    return render(request, 'rag/chatbot.html')


@require_POST
def chatbot_api(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid JSON body.'}, status=400)

    question = (payload.get('message') or '').strip()
    if not question:
        return JsonResponse({'error': 'Please enter a question.'}, status=400)

    try:
        result = answer_question(question)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=503)

    return JsonResponse(result)
