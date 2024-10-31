# voice_recognition/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AudioUploadForm
from .audio_processing import convert_audio, get_audio_properties, transcribe_audio
import os

def upload_audio(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES['audio']
            file_extension = os.path.splitext(audio_file.name)[1].lower()
            temp_file_path = f"temp_audio{file_extension}"

            # Save the uploaded file to a temporary location
            with open(temp_file_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            converted_file_path = "converted_audio.wav"

            # Convert the audio if necessary
            if file_extension == '.mp3':
                print("Converting MP3 to WAV...")
                convert_audio(temp_file_path, converted_file_path)
            else:
                # Check and convert WAV if needed
                try:
                    sample_rate, num_channels, sample_width = get_audio_properties(temp_file_path)
                    if num_channels != 1:
                        print("The audio file is not mono.")
                        convert_audio(temp_file_path, converted_file_path, sample_rate)
                    else:
                        converted_file_path = temp_file_path
                except Exception as e:
                    return HttpResponse(f"Error processing the file: {e}")

            # Transcribe the audio
            json_key_path = "C:\\Users\\Manoj\\Downloads\\eyusecase-04f8e4494dce.json"  # Update this path
            try:
                transcripts = transcribe_audio(converted_file_path, json_key_path)
                transcript_text = "\n".join(transcripts)
            except Exception as e:
                return HttpResponse(f"Error during transcription: {e}")

            # Clean up temporary files
            os.remove(temp_file_path)
            if os.path.exists(converted_file_path) and converted_file_path != temp_file_path:
                os.remove(converted_file_path)

            return render(request, 'result.html', {'transcript': transcript_text})

    else:
        form = AudioUploadForm()

    return render(request, 'home.html', {'form': form})
