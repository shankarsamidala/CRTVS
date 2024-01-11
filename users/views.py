from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from datetime import timedelta
# Create your views here.
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import VideoUpload, UserProfile
from .forms import VideoUpdateForm
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse
from datetime import datetime


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            # Check if the user is a superuser
            if user.is_superuser:
                return redirect('userList')  # Redirect to the profile page for superusers
            else:
                return redirect('dashboard')  # Redirect to the dashboard for regular users
        else:
            # Handle invalid login credentials
            # You might want to display an error message
            return render(request, 'index.html', {'error_message': 'Invalid username or password'})

    return render(request, 'index.html')



@login_required
def dashboard(request):
    total_videos = VideoUpload.objects.filter(user=request.user).aggregate(total_videos=Sum('number_of_videos'))['total_videos'] or 0
    average_uploads_per_day = VideoUpload.objects.filter(user=request.user).aggregate(average_uploads_per_day=Avg('number_of_videos'))['average_uploads_per_day'] or 0
    videos_uploaded_today = VideoUpload.objects.filter(
        user=request.user,
        upload_datetime__date=timezone.now().date()
    ).aggregate(videos_uploaded_today=Sum('number_of_videos'))['videos_uploaded_today'] or 0

    current_day_videos = VideoUpload.objects.filter(user=request.user, upload_datetime__date=timezone.now().date()).first()
    date_time = timezone.now().date()
    # Retrieve other data for the user
    users_data = VideoUpload.objects.filter(user=request.user)


    users_video_data = VideoUpload.objects.filter(user=request.user,upload_datetime__date=timezone.now().date()- timedelta(days=1)).first()
    # Calculate the date one day before the current date
    target_date = timezone.now().date() - timedelta(days=1)

    # Query to get the video count for each user for the specified date
    video_counts = (
        VideoUpload.objects
        .all()
        .values('user')
        .annotate(total_videos=Sum('number_of_videos'))
        .order_by('-total_videos')
    )

    # Fetch usernames for the corresponding user IDs
    usernames = {user.id: user.username for user in User.objects.filter(id__in=[item['user'] for item in video_counts])}

    # Update the video_counts with usernames
    for video_count in video_counts:
        video_count['username'] = usernames.get(video_count['user'])


    return render(request,'userdashboard.html', {'current_date':users_video_data,'video_counts': video_counts ,'date_time':date_time,'users_data': users_data, 'total_videos': total_videos, 'videos_uploaded_today': videos_uploaded_today,'average_uploads_per_day':average_uploads_per_day,'current_day_videos':current_day_videos})


# @login_required
# def dashboard(request):
#     # user = get_object_or_404(User)
#     profile = UserProfile.objects.filter(user=request.user).first()
#     video_uploads = VideoUpload.objects.filter(user=request.user)

#     return render(request, 'userdashboard.html', {'date_time':date_time,'users_data': users_data, 'total_videos': total_videos, 'videos_uploaded_today': videos_uploaded_today,'average_uploads_per_day':average_uploads_per_day,'current_day_videos':current_day_videos})



@login_required
def update_video(request):
    if request.method == 'POST':
        subject_type = request.POST.get('subject_type')
        number_of_videos = request.POST.get('number_of_videos')
        remarks = request.POST.get('remarks')

        # Validate and save data as needed
        if subject_type and number_of_videos:
            video_update = VideoUpload.objects.create(
                user=request.user,
                subject_type=subject_type,
                number_of_videos=number_of_videos,
                upload_datetime = timezone.now(),
                
                remarks=remarks
            )
            # Additional logic as needed
            return redirect('dashboard')  # Redirect to the dashboard or another page after submission

    return render(request, 'update_video_modal.html')


@login_required
def usersList(request):
    users_data = VideoUpload.objects.all().order_by('-upload_datetime')

    # Apply filters
    employee_name_filter = request.POST.get('employee_name')
    subject_type_filter = request.POST.get('subject_type')
    date_time_filter = request.POST.get('end_date')

    print(date_time_filter)

    if employee_name_filter:
        users_data = users_data.filter(user__username__icontains=employee_name_filter)

    if subject_type_filter:
        users_data = users_data.filter(subject_type=subject_type_filter)

    if date_time_filter:
        try:
            date_time_filter = datetime.strptime(date_time_filter, '%d-%m-%Y')
            users_data = users_data.filter(upload_datetime__date=date_time_filter)
        except ValueError:
            # Handle invalid date format if necessary
            pass

    total_videos = users_data.aggregate(total_videos=Sum('number_of_videos'))['total_videos'] or 0

    average_uploads_per_day = users_data.aggregate(average_uploads_per_day=Avg('number_of_videos'))['average_uploads_per_day'] or 0

    # Filter VideoUpload objects for the current day and annotate the sum of number_of_videos
    daily_video_sum = VideoUpload.objects.filter(upload_datetime__date=timezone.now().date()).values('upload_datetime__date').annotate(total_videos=Sum('number_of_videos'))

    # Retrieve the total number of videos for the current day
    current_day_videos = daily_video_sum[0]['total_videos'] if daily_video_sum else 0

    # current_day_videos = users_data.filter(upload_datetime__date=timezone.now().date()).count()

    print(current_day_videos)

    return render(request, 'usersList.html', {'users_data': users_data, 'total_videos': total_videos,'average_uploads_per_day':average_uploads_per_day,'current_day_videos':current_day_videos})




def userprofile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = UserProfile.objects.filter(user=user).first()
    video_uploads = VideoUpload.objects.filter(user=user)
    daily_video_sum = VideoUpload.objects.filter(user=user,upload_datetime__date=timezone.now().date()).values('upload_datetime__date').annotate(total_videos=Sum('number_of_videos'))
    total_videos = video_uploads.aggregate(total_videos=Sum('number_of_videos'))['total_videos'] or 0

    current_day_videos = daily_video_sum[0]['total_videos'] if daily_video_sum else 0
    return render(request, 'profile.html', {'user': user, 'video_uploads': video_uploads,'userprofile':profile,'today':current_day_videos,'total_videos':total_videos})



from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone
from .models import VideoUpload




def custom_logout(request):
    logout(request)
    return redirect(reverse('login'))