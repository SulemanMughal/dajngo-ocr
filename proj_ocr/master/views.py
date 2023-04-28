import uuid, json, traceback, pytesseract as pt
from PIL import Image
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage

# Create your views here.

def index(request):
    template_name = 'master/index.html'
    context = {
    }
    return render(request, template_name, context)

def fileProcessing(request):
    if request.method != "POST" :
        return JsonResponse(
            json.loads(
                json.dumps({
                    "error" : "Invalid request method"
                })
            ),
            status =400
        )
    else:
        try:
            ocr_image = request.FILES.get('ocr_image')
            # print(ocr_image.size)

            filename = str(uuid.uuid4())
            # Save file to storage
            default_storage.save(filename, ocr_image)
            
            #  Reading file from storage 
            ocr_image = default_storage.open(filename)
            
            # # url for file
            ocr_image_url = default_storage.url(ocr_image.name)

            # Read Images
            img = Image.open(ocr_image.name)
            text = pt.image_to_string(img)
            # print(text)

            
        except:
            traceback.print_exc()
            return JsonResponse(
                json.loads(
                    json.dumps({
                        "error" : "There is an error while uploading image. Please try again."
                    })
                ),
                status =400
            )
            # messages.error(request, "There is an error while uploading image. Please try again.")
            # return redirect(reverse("master_index"))
        return JsonResponse(
            json.loads(
                json.dumps({
                    "text" :  text,
                    "url" : ocr_image_url
                })
            ),
            status =200
        )