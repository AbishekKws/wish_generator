from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import InteractiveWish, WishImage
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import WishCreateForm
from django.db.models import Q
from django.db.models import F

# -- FRONTEND VIEWS -- #
def create_wish(request):
    if request.method == 'POST':
        form = WishCreateForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')
        
        if form.is_valid():
            if 3 <= len(files) <= 6:
                wish = form.save()
                for f in files:
                    WishImage.objects.create(wish=wish, image=f)
                
                return render(request, 'frontend/magical_wishes/wish_success.html', {'wish': wish})
            else:
                form.add_error(None, 'Please upload between 3 and 6 images to make the magic work!')
    else:
        form = WishCreateForm()
    return render(request, 'frontend/magical_wishes/create_wish.html', {'form': form})

def surprise_view(request, slug):
    wish = get_object_or_404(InteractiveWish, slug=slug)
    
    # --- SEO Logic ---
    images = wish.images.all()
    first_image_url = None
    if images.exists():
        first_image_url = request.build_absolute_uri(images.first().image.url)

    context = {
        'wish': wish,
        'images': images,
        'meta_title': f"A Special Magic Surprise for {wish.receiver_name}! ✨",
        'meta_description': f"Open this link to see the interactive magic created by {wish.sender_name}.",
        'meta_image': first_image_url,
    }
    return render(request, 'frontend/magical_wishes/interactive_wish.html', context)


# -- BACKEND VIEWS -- #
@staff_member_required
def admin_interactive_wish_list(request):
    query = request.GET.get('q', '')
    
    wishes_list = InteractiveWish.objects.prefetch_related('images').all().order_by('-created_at')

    if query:
        wishes_list = wishes_list.filter(
            Q(sender_name__icontains=query) | 
            Q(receiver_name__icontains=query) |
            Q(slug__icontains=query)
        )

    paginator = Paginator(wishes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'backend/magical_wishes/interactive_list.html', {
        'wishes': page_obj,
        'query': query
    })

@staff_member_required
def admin_interactive_delete(request, slug):
    wish = get_object_or_404(InteractiveWish, slug=slug)
    sender = wish.sender_name
    wish.delete()
    messages.success(request, f"Interactive wish from {sender} deleted successfully.")

    return redirect('admin_interactive_list')
