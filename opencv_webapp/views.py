from django.shortcuts import render, redirect
from  opencv_webapp.forms import SimpleUploadForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from opencv_webapp.cv_functions import cv_detect_face

# Create your views here.
def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})


def simple_upload(request):

    if request.method == 'POST':

        form = SimpleUploadForm(request.POST, request.FILES)

        if form.is_valid():
            myfile = request.FILES['image']

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            # fs.save('경로명을 포함할 파일 저장시 활용할 이름', 파일 객체)

            uploaded_file_url = fs.url(filename)

            context = {'form': form, 'uploaded_file_url': uploaded_file_url}

        return render(request, 'opencv_webapp/simple_upload.html', context)


    else:

        form = SimpleUploadForm()
        context = {'form':form}

        return render(request, 'opencv_webapp/simple_upload.html', context)


def detect_face(request):
    if request.method == 'POST' :

        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid(): # 비어있는 Form에 사용자가 업로드한 데이터를 넣고 검증합니다.
            post = form.save(commit=False)
            # save() 함수는 DB에 저장될 ImageUploadModel 클래스 객체 자체를 리턴함 (== record 1건)
            # Form에 채워진 데이터를 DB에 실제로 저장하기 전에 변경/추가할 수 있음 (commit=False)

            # form.save() # 후처리 하지 않을 경우
            post.save() # 후처리 진행할 경우

            imageURL = settings.MEDIA_URL + form.instance.document.name

            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL)

            return render(request, 'opencv_webapp/detect_face.html', {'form':form, 'post':post})
    else:

        form = ImageUploadForm()

        return render(request, 'opencv_webapp/detect_face.html', {'form':form})
