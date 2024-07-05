import os
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageUploadForm
from PIL import Image
from django.conf import settings

def save_images_as_tiff(images, output_path):
    image_list = []
    for image in images:
        try:
            img = Image.open(image)
            image_list.append(img)
        except Exception as e:
            print(f"Error opening image {image.name}: {e}")
    
    if image_list:
        image_list[0].save(output_path, save_all=True, append_images=image_list[1:], compression='tiff_deflate')

def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            output_file = form.cleaned_data['output_file']
            if not output_file.lower().endswith('.tiff'):
                output_file += '.tiff'
            output_path = os.path.join(settings.MEDIA_ROOT, output_file)
            images = request.FILES.getlist('images')
            save_images_as_tiff(images, output_path)
            return HttpResponse(f"Saved {len(images)} images to {output_path}")
    else:
        form = ImageUploadForm()
    return render(request, 'tiffapp/index.html', {'form': form})
