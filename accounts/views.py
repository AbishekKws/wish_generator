from magic_wish.models import Wish, VisitorCount, Rating, CelebrationTemplate, MusicLibrary
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from magical_wishes.models import InteractiveWish
from django.shortcuts import render, redirect
from birthdaywish.models import BirthdayWish 
from django.db.models import Avg


def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'backend/admin_custom/login.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('admin_login')



@staff_member_required
def admin_dashboard(request):
    # 1. Basic Stats
    total_standard_wishes = Wish.objects.count()
    total_birthday_wishes = BirthdayWish.objects.count()
    total_interactive_wishes = InteractiveWish.objects.count()
    
    # 2. Traffic & Engagement
    visitor_stats, _ = VisitorCount.objects.get_or_create(id=1)
    avg_rating = Rating.objects.aggregate(Avg('score'))['score__avg'] or 0
    
    # 3. Library Stats
    total_templates = CelebrationTemplate.objects.count()
    total_songs = MusicLibrary.objects.count()

    # 4. Recent Activity (Latest 5 wishes)
    recent_wishes = Wish.objects.all().order_by('-created_at')[:5]

    context = {
        'total_wishes': total_standard_wishes + total_birthday_wishes + total_interactive_wishes,
        'standard_count': total_standard_wishes,
        'interactive_count': total_interactive_wishes,
        'visitors': visitor_stats.total_visits,
        'rating': round(avg_rating, 1),
        'template_count': total_templates,
        'music_count': total_songs,
        'recent_wishes': recent_wishes,
    }
    
    return render(request, 'backend/admin_custom/dashboard.html', context)
