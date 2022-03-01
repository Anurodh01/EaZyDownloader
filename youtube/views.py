from django.http.response import HttpResponse
from django.shortcuts import render,redirect
import instaloader
from pytube import YouTube
from django.contrib import messages
from instaloader import Profile,Post
from PIL import Image, ImageTk
import os
# Create your views here.
instance=instaloader.Instaloader()

def home(request):
    return render(request,'blog/home.html')

def youtube(request):
    if request.method=='POST':
        link=request.POST.get('link')
        global yt
        yt=YouTube(link)
        title=yt.title
        uploaded_by=yt.author
        date=yt.publish_date
        channel=yt.channel_url
        minute=yt.length//60
        second=yt.length%60
        length=f"{minute}:{second}"
        views=round(yt.views/1000000,1)
        thumbnail=yt.thumbnail_url
        resol=yt.streams.filter(progressive=True)
        d={}
        for i in resol:
            d[i.resolution]=round(i.filesize/(1024*1024),1)
        
        context={
            'title':title,
            'thumbnail':thumbnail,
            'author':uploaded_by,
            'channel':channel,
            'length':length,
            'views':views,
            'date':date,
            'resol':d
            }
        return render(request,'blog/download.html',context)
    return render(request,'blog/youtube.html')

def download(request):
    if request.method=="POST":
        resolution=request.POST.get("resolution")
        print(resolution)
        count=0 
        resolu=yt.streams.filter(progressive=True)
        for i in resolu:
            if resolution==i.resolution:
                stream=yt.streams[count]
                stream.download('C:\\Users\\user\\Desktop\\Python_Projects\\Youtube_Video_Downloader\\video_downloader\\youtube_downloaded_videos')
                messages.success(request, 'Video downloaded Successfully!!')
                break
            else:
                count+=1
        return redirect('home')
    else:
        return HttpResponse(request,'Failed')

def instagram(request):
    return render(request,'blog/instagram.html')

def profile_pic(request):
    try:
        if request.method=="POST":
            global User
            user=request.POST.get('user')
            instance.download_profile(user,profile_pic_only=True)
            directory=f'{os.getcwd()}/{user}'
            to_be_del=[x for x in os.listdir(f'{os.getcwd()}/{user}') if not x.endswith('jpg')]
            for i in to_be_del:
                path_to_file=os.path.join(directory,i)
                os.remove(path_to_file)
            messages.success(request,f"Profile Pic has been downloaded Successfully. See the same directory with name {user}")
            return redirect('instagram')
    except Exception as e:
        return render(request,'blog/error.html',{'error':e})
    return render(request,'blog/profile_pic.html')
    
def post_download(request):
    try:
        if request.method=="POST":
            link=request.POST.get('link')
            x=-1
            x=link.find('reel')
            if x>0:
                y=x+3
            else:
                x=link.find('p')
                y=link.find('p',x+1)
            y=y+2
            string=""
            instance.login(user='your_instagram_username',passwd='your_instagram_password')
            while y <(len(link)-1):
                string+=link[y]
                y+=1
            print(string)
            post=Post.from_shortcode(instance.context,string)
            instance.download_post(post,target="Insta_Videos_and_Posts")
            directory="./Insta_Videos_and_Posts"
            files_in_dir=os.listdir(directory)
            filtered_files=[file for file in files_in_dir if file.endswith('.txt') or file.endswith('.xz')]
            for file in filtered_files:
                path_to_file=os.path.join(directory,file)
                os.remove(path_to_file)
            messages.success(request,"Post has been downloaded Successfully. It is in 'Insta_Videos_and_Posts'.")
            return redirect('instagram')
    except Exception as e:
        return render(request,'blog/error.html',{'error':e})
    return render(request,'blog/post_download.html')

def story_download(request):
    try:
        if request.method=="POST":
            user=request.POST.get('user')
            instance.login(user='your_instagram_username',passwd='your_instagram_password')
            profile=Profile.from_username(instance.context,username=user)
            instance.download_stories(userids=[profile.userid],filename_target=f"{profile.username}_story")
            directory=f'{os.getcwd()}\{user}_story'
            to_be_del=[x for x in os.listdir(f'{os.getcwd()}\{user}_story') if x.endswith('xz')]
            for i in to_be_del:
                path_to_file=os.path.join(directory,i)
                os.remove(path_to_file)

            messages.success(request,f"Story Downloaded Sucessfully. PLease visit {profile.username}_story to see downloaded story.")
            return redirect('instagram')
    except Exception as e:
        return render(request,'blog/error.html',{'error':e})
    return render(request,'blog/story_download.html')

def profile_download(request):
    try:
        if request.method=="POST":
            user=request.POST.get('user')
            instance.login(user='your_instagram_username',passwd='your_instagram_password')
            instance.download_profile(profile_name=user)
            directory=f'{os.getcwd()}/{user}'
            to_be_del=[x for x in os.listdir(f'{os.getcwd()}/{user}') if not (x.endswith('jpg') or x.endswith('mp4'))]
            for i in to_be_del:
                path_to_file=os.path.join(directory,i)
                os.remove(path_to_file)
            messages.success(request,f"{user} insta profile has been downloaded Successfully.")
            return redirect('instagram')
    except Exception as e:
        return render(request,'blog/error.html',{'error':e})
    return render(request,'blog/profile_download.html')