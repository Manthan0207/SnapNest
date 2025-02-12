from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import Image, UserProfile , SavedPin , Notification
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .models import Image,Like
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
import json
from django.db.models import Count, Q
from django.utils.timezone import now
from .models import Report





@login_required(login_url='login-page')
@csrf_exempt
def index(request):
    user = request.user

    #value_list is used to only get the category values, instead of full objects
    liked_categories = set(Image.objects.filter(like__user=user).values_list('category', flat=True))
    saved_categories = set(Image.objects.filter(savedpin__user=user).values_list('category', flat=True))

    interested_categories = liked_categories | saved_categories

    interested_images = list(Image.objects.filter(category__in=interested_categories))

    other_images = list(Image.objects.exclude(image_id__in=[img.image_id for img in interested_images]))
    liked_images = list(Image.objects.filter(like__user=user))

    #updating liked_image to avoid duplicate image show on index page
    liked_images = [img for img in liked_images if img not in interested_images]

    images = interested_images + other_images + liked_images

    notifications = Notification.objects.filter(notification_receiver=user).order_by('-created_at')

    return render(request, 'boards/index.html', {'images': images, 'notifications': notifications})




@csrf_exempt
def profile(request):
    cur_user = request.user
    return render(request, 'boards/profile.html',{'user' :cur_user}) 




@csrf_exempt
def handleSignUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for erroneous input
        if len(username) > 10:
            messages.error(request, "Username must be 10 characters or fewer.")
            return redirect('signupPage')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric.")
            return redirect('signupPage')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('signupPage')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another.")
            return redirect('signupPage')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please use a different email.")
            return redirect('signupPage')

        # Create the user
        try:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()

            

            messages.success(request, "Your account has been successfully created.")
            return redirect('login-page')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('signupPage')

    # If the request method is not POST
    return HttpResponse('404 - Not Found', status=404)

@csrf_exempt
def handleLogin(request):
    if request.method == 'POST':
        login_username = request.POST.get('login-username')
        login_password = request.POST.get('pass')
        user = authenticate(username=login_username, password=login_password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('Home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('login-page')

    # If the request method is not POST, redirect or handle accordingly
    return redirect('login-page')


        
@csrf_exempt
def handleLogOut(request) :
    if request.method == "POST" :
        logout(request)
        messages.success(request,"Successfully Logged Out")
        print(f"Login successful for username: ")
        return redirect('Home')

    return HttpResponse('Handle Logout')

def aboutus(request) :
    return render(request, 'boards/aboutus.html') 

def pin(request, image_id):
    myid = image_id
    pin = Image.objects.filter(image_id=myid).first()  # Use `.first()` to avoid index errors if no pin is found

    if not pin:
        # Handle case where pin is not found
        return render(request, 'boards/404.html', {"message": "Pin not found"})

    # Safely access the author's profile
    author_profile = pin.author  # Use `getattr` to avoid errors if profile does not exist

    if author_profile and request.user != author_profile:
        author_profile.profile.monthly_views += 1
        author_profile.save()

    # Check if the pin is liked by the logged-in user (if the user is logged in)
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, pin=pin).exists()

    # Getting related pins
    related_pins = Image.objects.filter(category=pin.category).exclude(image_id=pin.image_id)
    is_saved = False
    if SavedPin.objects.filter(user=request.user, pin=pin).exists():
        is_saved = True
    

    return render(request, 'boards/pin.html', {
        "pin": pin,
        "related_pins": related_pins,
        'is_liked': is_liked , 
        'is_saved' : is_saved
    })




@login_required(login_url='login-page')
def upload_pin(request) :
    return render(request,'boards/upload_pin.html')

@login_required 
def upload_img(request):
    if request.method == 'POST':
        img_title = request.POST['img_title']
        category = request.POST['category']
        desc = request.POST['desc']
        pin_image = request.FILES['pin_image']

        # Get the current user
        user = request.user

        # Create the Image object
        new_pin = Image(
            img_title=img_title,
            category=category,
            desc=desc,
            pub_date=timezone.now().date(),  # Set the current date
            image=pin_image,
            author=user
        )
        new_pin.save()

        # Update the user's post_count in UserProfile
        user_profile = UserProfile.objects.get(user=user)
        user_profile.post_count += 1  # Increment the post count
        user_profile.save()


    return render(request, 'boards/upload_pin.html')



def user_profile(request, username):
    
    
    user = get_object_or_404(User, username=username)
    if request.user == user :
        return render(request , 'boards/profile.html')

    profile = user.profile
    user_pins = Image.objects.filter(author=user)  
    saved_pins = SavedPin.objects.filter(user=user)  
    
    return render(request, 'boards/other_user.html', {
        'user': user,
        'user_pins': user_pins,
        'saved_pins': saved_pins,
    })


@csrf_exempt
@login_required(login_url='login-page')
def toggle_like(request, image_id):
    if request.method == 'POST':
        #it will fetch the like object based on user = user(in Like) and pin = pin(in Like model if pin entry is avail for the current user)
        #ultimately checking if user have already liked post or not
        #so here if user have liked it returns the object if not then it creates object and store in Like table.
        #created returns true if user have already liked otherwise false.
        try:
            user = request.user
            pin = get_object_or_404(Image, image_id=image_id)  # Using get_object_or_404 for better error handling
            like, created = Like.objects.get_or_create(user=user, pin=pin)
            if not created:
                like.delete()
                Notification.objects.filter(
                    notification_sender = user,
                    notification_receiver = pin.author,
                    pin = pin , 
                    notification_type = 'like'
                ).delete()
                pin.like_count = max(0, pin.like_count - 1)
                pin.save()
                return JsonResponse({'status': 'disliked', 'like_count': pin.like_count})
            pin.like_count += 1
            pin.save()
            if user != pin.author :
                Notification.objects.create(
                notification_receiver=pin.author,  # The user who uploaded the pin
                notification_sender=user,  # The user who liked the pin
                pin=pin,  # The pin being liked
                notification_type='like',
                message=f"{user.username} liked your pin: {pin.img_title}"
            )
            return JsonResponse({'status': 'liked', 'like_count': pin.like_count})
        except Image.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Image not found'}, status=404)
    
    elif request.method == 'GET':
        try:
            pin = get_object_or_404(Image, image_id=image_id)
            return JsonResponse({
                'image_id': pin.image_id,
                'like_count': pin.like_count,
                'status': 'ok',
                'hi' :1,
            })
        except Image.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Image not found'}, status=404)
    
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])  # Return 405 Method Not Allowed for other methods


def search_page(request):
    query = request.GET.get('query', '').strip()

    if query:
        # Case-insensitive search in both category and img_title
        #Q is used when we have to filter with multiple values
        #Q is a query object that allows you to build complex queries using AND (&), OR (|), and NOT (~) operations.
        pins = Image.objects.filter(
            Q(category__icontains=query) | Q(img_title__icontains=query)
        )
        top_categories = None
        return render(request, 'boards/search_result.html', {'pins': pins})  # Search result page
    else:
        # Dynamically fetch the top 3 categories based on the number of images in each category
        categories = (
            Image.objects.values('category')
            .annotate(image_count=Count('image_id'))
            .order_by('-image_count')[:3]
        )

        # Fetch the images for each top category
        top_categories = {
            category['category']: Image.objects.filter(category=category['category'])[:5]
            for category in categories
        }
        pins = None
        
        return render(request, 'boards/search.html', {'top_categories': top_categories})  # Search page


def toggle_follow(request, username):
    if request.method == "POST":
        # Get the target user and their profile
        target_user = get_object_or_404(User, username=username)
        user_profile = request.user.profile
        target_profile = target_user.profile
    
        if request.user in target_profile.followers.all():
            # If user is already following, unfollow
            target_profile.followers.remove(request.user)
            if user_profile.follow_count > 0:
                user_profile.follow_count -= 1  
            is_following = False
            Notification.objects.filter(
                notification_receiver=target_user,
                notification_sender=request.user,
                notification_type='follow'
            ).delete()
        else:
            # If user is not following, follow
            target_profile.followers.add(request.user)
            user_profile.follow_count += 1  
            is_following = True
            
            Notification.objects.create(
                notification_receiver=target_user,
                notification_sender=request.user,
                notification_type='follow',
                message=f"{request.user.username} started following you."
            )


        target_profile.follower_count = target_profile.followers.count()#updating follower count
        
        # Save the updated profiles
        user_profile.save()
        target_profile.save()

        # Return updated follow status and counts
        return JsonResponse({
            "is_following": is_following,
            "follower_count": target_profile.follower_count,
            "following_count": user_profile.follow_count,
        })

    return JsonResponse({"error": "Invalid request"}, status=400)



def login_page(request) :
    return render(request,'boards/login.html')

def signup_page(request) :
    return render(request,'boards/signup.html')



def save(request,image_id) :
    user = request.user
    pin = get_object_or_404(Image,image_id=image_id)
    saved, created = SavedPin.objects.get_or_create(user=user, pin=pin)
    if created :
        messages.success(request, "Pin saved successfully!")
        return JsonResponse({'saved' : True})
    else :
        saved.delete()
        return JsonResponse({'saved' : False})
    
    




def analytics(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    
    today = datetime.now()
    last_week = today - timedelta(days=6)  
    print(last_week) #2025-01-17 00:30:47.239593
    
    date_range = [last_week + timedelta(days=i) for i in range(7)]
    formatted_dates = [date.strftime('%Y-%m-%d') for date in date_range]
    
    #getting likes data for image ,grp by day
    likes_data = (
        #gte means >= , fetching past 7 day like data for post
        Like.objects.filter(pin=image, timestamp__date__gte=last_week)
        # timestamp field to just the date it ignores time details
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(like_count=Count('id'))
        .order_by('day')
    )
    # print(likes_data)
    
    # create a dictionary to store likes by date in dict 
    likes_dict = {entry['day'].strftime('%Y-%m-%d'): entry['like_count'] for entry in likes_data}
    
    # Prepare graph data, ensuring all 7 days are included (filling missing days with 0)
    graph_data = {
        'labels': formatted_dates,
        'data': [likes_dict.get(date, 0) for date in formatted_dates],
    }
    # print(graph_data)
    
    context = {
        'image': image,
        'graph_data': json.dumps(graph_data),  # Serialize to JSON for use in JavaScript
        #dumps works same as stringify it makes object in str format 
    }
    # print(context)
    
    return render(request, 'boards/analytics.html', context)




@login_required
def notifications(request):
    # Get notifications for the logged-in user
    notifications = Notification.objects.filter(notification_receiver=request.user).order_by('-created_at')

    
    notification_data = [
            {
                "message": notification.message,
                "created_at": notification.created_at.strftime("%B %d, %Y"),  # Formatted date
                "is_read": notification.is_read ,
                "image_url": notification.pin.image.url if notification.pin else None ,
            }
            for notification in notifications
        ]
    notifications.filter(is_read=False).update(is_read=True)

    return JsonResponse({"notifications": notification_data})



def delete_pin(request , image_id) :
    delete_image = get_object_or_404(Image, image_id=image_id)
    delete_image.delete()
    user = delete_image.author.profile
    user.post_count-=1
    user.save()
    return redirect('user-profile',username=delete_image.author.username)



@csrf_exempt  
@login_required
def report_pin(request, image_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            reason = data.get("reason")
            description = data.get("description", "")

            if not reason:
                return JsonResponse({"success": False, "message": "Reason is required"}, status=400)

            pin = get_object_or_404(Image, image_id=image_id)
            
            
            #when using update or create it will first check if user have reported or not according to field reporter & reported_pin.
            #and it will not check if user reported or not in default 
            report, created = Report.objects.update_or_create(  #report will get the report object , created will be bool val
                reporter=request.user,
                reported_pin=pin,
                defaults={
                    "reason": reason,
                    "description": description,
                    "status": "pending", 
                    "created_at": now(),
                    'reported_user' : pin.author
                }
            )

            return JsonResponse({
                "success": True,
                "message": "Report submitted successfully.",
                "report_count": Report.objects.filter(reported_pin=pin).count(),
                "updated": not created 
            })

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)



