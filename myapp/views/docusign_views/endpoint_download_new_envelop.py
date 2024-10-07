# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from myapp.views.docusign_views.completed_envelop_download import process_envelopes

# @csrf_exempt
# def download_new_envelopes(request):
#     if request.method == 'POST':
#         try:
#             process_envelopes()
#             return JsonResponse({'message': 'New envelopes processed and downloaded successfully!'}, status=200)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)
