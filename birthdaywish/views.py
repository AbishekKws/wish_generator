from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import BirthdayWish, WishImage
from django.db.models import F

# -- FRONTEND VIEWS -- #
def create_wish(request):
    if request.method == "POST":
        sender = request.POST.get('sender_name')
        receiver = request.POST.get('receiver_name')
        msg = request.POST.get('message')
        music_file = request.FILES.get('music') 
        wish = BirthdayWish.objects.create(
            sender_name=sender,
            receiver_name=receiver,
            message=msg,
            music=music_file  
        )
        images = request.FILES.getlist('images')
        for img in images:
            WishImage.objects.create(wish=wish, image=img)

        return redirect('birthday:wish_success', slug=wish.slug) 
    
    return render(request, 'frontend/birthdaywish/create_wish.html')

def wish_success(request, slug):
    wish = get_object_or_404(BirthdayWish, slug=slug)
    full_url = request.build_absolute_uri(f'/wish/{wish.slug}/') 
    
    context = {
        'wish': wish,
        'full_url': full_url,
    }
    return render(request, 'frontend/birthdaywish/wish_success.html', context)

def surprise_page(request, slug):
    wish = get_object_or_404(BirthdayWish, slug=slug)
    
    # --- SEO & Stats Logic ---
    BirthdayWish.objects.filter(slug=slug).update(views=F('views') + 1)
    
    images = wish.images.all() 
    context = {
        'wish': wish,
        'images': images,
        'thumbnail': images.first().image.url if images.exists() else None
    }
    return render(request, 'frontend/birthdaywish/surprise_template.html', context)


# -- BACKEND VIEWS -- #
@staff_member_required
def admin_wish_list(request):
    wishes = BirthdayWish.objects.all().order_by('-created_at')
    return render(request, 'backend/birthdaywish/wishes_list.html', {'wishes': wishes})

@staff_member_required
def admin_wish_delete(request, pk):
    wish = get_object_or_404(BirthdayWish, pk=pk)
    wish.delete()
    return redirect('birthday:admin_wish_list')
