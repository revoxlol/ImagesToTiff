import os
from django.shortcuts import render
from django.http import HttpResponse
from .forms import FolderInputForm
from PIL import Image

def collect_images_from_folders(folder_list):
    image_list = []
    for folder in folder_list:
        if not os.path.isdir(folder):
            continue
        for root, _, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                    file_path = os.path.join(root, file)
                    try:
                        image = Image.open(file_path)
                        image_list.append(image)
                    except Exception as e:
                        print(f"Error opening image {file_path}: {e}")
    return image_list

def save_images_as_tiff(image_list, output_path):
    if image_list:
        image_list[0].save(output_path, save_all=True, append_images=image_list[1:], compression='tiff_deflate')

def index(request):
    if request.method == 'POST':
        form = FolderInputForm(request.POST)
        if form.is_valid():
            folders = [folder.strip() for folder in form.cleaned_data['folders'].split(',')]
            output_file = form.cleaned_data['output_file']
            images = collect_images_from_folders(folders)
            save_images_as_tiff(images, output_file)
            return HttpResponse(f"Saved {len(images)} images to {output_file}")
    else:
        form = FolderInputForm()
    return render(request, 'tiffapp/index.html', {'form': form})
