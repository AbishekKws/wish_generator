from .models import Wish, WishImage, VisitorCount, Rating, CelebrationTemplate, VisitorIP
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from magical_wishes.models import InteractiveWish
from .models import MusicLibrary, MusicCategory
from birthdaywish.models import BirthdayWish
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import MusicLibraryForm
from django.contrib import messages
from django.db.models import Avg, Q
from .forms import WishForm

#--- GLOBAL CONFIG ---#
ALL_TEMPLATES_CONFIG = {
    'heart_shape': {'id': 'heart_shape', 'name': 'Romantic Heart'},
    'floating_photos': {'id': 'floating_photos', 'name': 'Floating Memories'},
    'colorful_magic': {'id': 'colorful_magic', 'name': 'Color Blast'},
    'balloon_parade': {'id': 'balloon_parade', 'name': 'Balloon Parade'},
    'falling_leaves': {'id': 'falling_leaves', 'name': 'Autumn Whisper'},
    'matrix_rain': {'id': 'matrix_rain', 'name': 'Matrix Digital'},
    'snowy_winter': {'id': 'snowy_winter', 'name': 'Snowy Winter'},
    'firework_show': {'id': 'firework_show', 'name': 'Firework Show'},
    'sakura_bloom': {'id': 'sakura_bloom', 'name': 'Sakura Bloom'},
    'space_odyssey': {'id': 'space_odyssey', 'name': 'Space Odyssey'},
    'retro_polaroid': {'id': 'retro_polaroid', 'name': 'Retro Polaroid'},
    'golden_luxury': {'id': 'golden_luxury', 'name': 'Golden Luxury'},
    'underwater_vibes': {'id': 'underwater_vibes', 'name': 'Underwater World'},
    'glitch_art': {'id': 'glitch_art', 'name': 'Cyber Glitch'},
    'comic_pop': {'id': 'comic_pop', 'name': 'Comic Book Pop'},
    'neon_pulse': {'id': 'neon_pulse', 'name': 'Neon Pulse'},
    'festival_lights': {'id': 'festival_lights', 'name': 'Festival Lights'},
    'golden_glitter': {'id': 'golden_glitter', 'name': 'Golden Glitter Magic'}
}

WISH_TYPES_LIST = [
    'Birthday', 'Anniversary', 'Love', 'Sorry', 
    'Friendship', 'Good Luck', 'Graduation', 'Thank You', 
    'New Year', 'Miss You', 'Proposal', 'Festival'
]

#--- FRONTEND VIEWS ---#
from django.db.models import Avg

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def landing_page(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        score = request.POST.get('score')
        Rating.objects.create(score=int(score))
        return JsonResponse({'status': 'success'})

    # --- UNIQUE VISITOR LOGIC START ---
    user_ip = get_client_ip(request)
    
    if not VisitorIP.objects.filter(ip_address=user_ip).exists():
        VisitorIP.objects.create(ip_address=user_ip)
        
        counter, _ = VisitorCount.objects.get_or_create(id=1)
        counter.total_visits += 1 
        counter.save()
    else:
        counter, _ = VisitorCount.objects.get_or_create(id=1)
    # --- UNIQUE VISITOR LOGIC END ---

    # Get Real Stats
    count_wish = Wish.objects.count()
    count_interactive = InteractiveWish.objects.count()
    count_birthday = BirthdayWish.objects.count()
    total_surprises = count_wish + count_interactive + count_birthday
    
    avg_rating = Rating.objects.aggregate(Avg('score'))['score__avg'] or 4.9

    context = {
        'types': WISH_TYPES_LIST,
        'count': counter.total_visits, 
        'surprises_count': total_surprises,
        'avg_rating': round(avg_rating, 1)
    }
    return render(request, 'frontend/landing.html', context)

def select_type(request):
    return render(request, 'frontend/magic_wish/select_type.html', {'types': WISH_TYPES_LIST})

def select_template(request, wish_type):
    category_map = {
        'birthday': ['balloon_parade', 'colorful_magic', 'firework_show', 'floating_photos', 'comic_pop', 'golden_glitter'],
        'anniversary': ['heart_shape', 'golden_luxury', 'firework_show', 'floating_photos', 'retro_polaroid'],
        'love': ['heart_shape', 'sakura_bloom', 'space_odyssey', 'floating_photos', 'neon_pulse'],
        'sorry': ['falling_leaves', 'underwater_vibes', 'snowy_winter', 'floating_photos'],
        'friendship': ['floating_photos', 'glitch_art', 'retro_polaroid', 'colorful_magic'],
        'good luck': ['firework_show', 'space_odyssey', 'neon_pulse'],
        'graduation': ['firework_show', 'golden_luxury', 'colorful_magic', 'matrix_rain'],
        'thank you': ['sakura_bloom', 'floating_photos', 'retro_polaroid'],
        'new year': ['firework_show', 'colorful_magic', 'neon_pulse', 'matrix_rain'],
        'miss you': ['snowy_winter', 'falling_leaves', 'space_odyssey', 'floating_photos'],
        'proposal': ['heart_shape', 'sakura_bloom', 'golden_luxury', 'firework_show'],
        'festival': ['festival_lights', 'firework_show', 'colorful_magic'],
        'default': ['floating_photos', 'colorful_magic']
    }
    
    template_ids = category_map.get(wish_type.lower(), category_map['default'])
    db_templates = CelebrationTemplate.objects.filter(template_id__in=template_ids)
    db_map = {t.template_id: t for t in db_templates}

    templates_data = []
    for tid in template_ids:
        if tid in ALL_TEMPLATES_CONFIG:
            temp_info = ALL_TEMPLATES_CONFIG[tid].copy()
            if tid in db_map and db_map[tid].preview_image:
                temp_info['preview_url'] = db_map[tid].preview_image.url
            else:
                temp_info['preview_url'] = f"/static/images/previews/{tid}.jpg"
            templates_data.append(temp_info)

    return render(request, 'frontend/magic_wish/select_temp.html', {
        'wish_type': wish_type,
        'templates': templates_data
    })

def create_wish(request, wish_type, template_name):
    template_info = ALL_TEMPLATES_CONFIG.get(template_name, {'name': 'Special Surprise'})
    
    if request.method == 'POST':
        form = WishForm(request.POST, request.FILES, wish_type=wish_type)
        if form.is_valid():
            wish = form.save(commit=False)
            wish.wish_type = wish_type
            wish.template_name = template_name 
            wish.save() 

            images = request.FILES.getlist('images')
            for img in images:
                WishImage.objects.create(wish=wish, image=img)
            
            return redirect('wish_success', slug=wish.slug)
    else:
        form = WishForm(wish_type=wish_type)
    
    return render(request, 'frontend/magic_wish/create.html', {
        'form': form,
        'wish_type': wish_type,
        'template_id': template_name,
        'display_name': template_info['name']
    })

def wish_detail(request, slug):
    wish = get_object_or_404(Wish, slug=slug)
    template_path = f"frontend/magic_wish/surprises/{wish.template_name}.html"
    
    # SEO context pass garne
    context = {
        'wish': wish,
        'meta_title': wish.meta_title,
        'meta_description': wish.meta_description
    }
    return render(request, template_path, context)

def wish_success(request, slug):
    wish = get_object_or_404(Wish, slug=slug)
    return render(request, 'frontend/magic_wish/success.html', {'wish': wish})


#--- BACKEND VIEWS ---#

@staff_member_required
def admin_wish_list(request):
    query = request.GET.get('q', '')
    wish_type = request.GET.get('type', '')
    wishes = Wish.objects.all().order_by('-created_at')

    if query:
        wishes = wishes.filter(Q(sender_name__icontains=query) | Q(receiver_name__icontains=query))
    if wish_type:
        wishes = wishes.filter(wish_type__iexact=wish_type)

    paginator = Paginator(wishes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'backend/magic_wish/wish_list.html', {
        'wishes': page_obj,
        'query': query,
        'wish_type': wish_type,
        'types': WISH_TYPES_LIST
    })

@staff_member_required
def admin_wish_delete(request, pk):
    wish = get_object_or_404(Wish, pk=pk)
    wish.delete()
    messages.warning(request, "Wish has been permanently deleted.")
    return redirect('admin_wish_list')

@staff_member_required
def admin_template_list(request):
    if request.method == "POST":
        tid = request.POST.get('template_id')
        name = request.POST.get('name')
        img = request.FILES.get('preview_image')
        
        obj, created = CelebrationTemplate.objects.get_or_create(template_id=tid)
        obj.name = name
        if img:
            obj.preview_image = img
        obj.save()
        messages.success(request, f"{name} updated successfully!")
        return redirect('admin_template_list')

    db_templates = {t.template_id: t for t in CelebrationTemplate.objects.all()}
    final_list = []
    for tid, info in ALL_TEMPLATES_CONFIG.items():
        final_list.append({
            'template_id': tid,
            'name': info['name'],
            'db_data': db_templates.get(tid)
        })

    return render(request, 'backend/magic_wish/templates_list.html', {'templates': final_list})

@staff_member_required
def admin_template_delete(request, pk):
    get_object_or_404(CelebrationTemplate, pk=pk).delete()
    messages.warning(request, "Template removed from database.")
    return redirect('admin_template_list')

@staff_member_required
def admin_music_list(request):
    for t_name in WISH_TYPES_LIST:
        MusicCategory.objects.get_or_create(name=t_name)

    if request.method == "POST":
        form = MusicLibraryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New song added successfully!")
            return redirect('admin_music_list')
    
    query = request.GET.get('q', '')
    cat_filter = request.GET.get('category', '')
    music_list = MusicLibrary.objects.all().order_by('-id')
    
    if query:
        music_list = music_list.filter(Q(title__icontains=query))
    if cat_filter:
        music_list = music_list.filter(category__name=cat_filter)

    paginator = Paginator(music_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = MusicLibraryForm()
    # SEO slug logic match garna category lookup
    form.fields['category'].queryset = MusicCategory.objects.filter(name__in=WISH_TYPES_LIST)
    form.fields['category'].widget.attrs.update({'class': 'form-select'})

    return render(request, 'backend/magic_wish/music_list.html', {
        'music': page_obj,
        'form': form,
        'wish_types': WISH_TYPES_LIST,
        'query': query,
        'cat_filter': cat_filter
    })

@staff_member_required
def admin_music_delete(request, pk):
    get_object_or_404(MusicLibrary, pk=pk).delete()
    return redirect('admin_music_list')