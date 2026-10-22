from django.http import JsonResponse, FileResponse
import mysql.connector
from django.shortcuts import render
from gtts import gTTS
import os

def chatbot(request):
    return render(request, 'chatbot.html')

def symptom_check(request):
    if request.method == 'POST':
        symptoms = request.POST.get('symptoms', '')
        severity = request.POST.get('severity', '')

        # Check if the values are being received
        print(f"Received symptoms: {symptoms}, severity: {severity}")

        if not symptoms or not severity:
            return JsonResponse({"message": "Symptoms and severity are required."}, status=400)

        try:
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="disease"
            )

            cursor = mydb.cursor()

            # Query the database
            cursor.execute("""
                SELECT diagnosis, recommended_treatment
                FROM healthcare_chatbot
                WHERE symptoms LIKE %s AND severity = %s
            """, [f"%{symptoms}%", severity])

            rows = cursor.fetchall()

            if rows:
                data = [{"diagnosis": row[0], "treatment": row[1]} for row in rows]
                return JsonResponse(data, safe=False)
            else:
                print("No matching records found.")
                return JsonResponse({"message": "No matching records found."}, status=404)

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({"message": f"Database error: {str(e)}"}, status=500)

        finally:
            cursor.close()
            mydb.close()

    return JsonResponse({"message": "Invalid request method."}, status=400)

from django.http import JsonResponse

from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
import os

@csrf_exempt
def text_to_speech(request):
    text = request.GET.get('text', '')

    if not text:
        return JsonResponse({"message": "No text provided"}, status=400)

    try:
        media_dir = "media"  # Define media directory
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)  # Create media folder if it doesn't exist

        audio_path = os.path.join(media_dir, "speech.mp3")

        # Generate and save speech file
        tts = gTTS(text=text, lang='mr')
        tts.save(audio_path)

        return FileResponse(open(audio_path, 'rb'), content_type='audio/mpeg')
    
    except Exception as e:
        print(f"❌ Error generating speech: {e}")
        return JsonResponse({"message": f"Error generating speech: {e}"}, status=500)
