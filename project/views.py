from django.shortcuts import render, redirect

# Create your views here.
# views.py

from django.views.generic import ListView
from .models import SheetMusic, Tag
from .forms import SheetMusicForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from pdf2image import convert_from_path
from django.core.files.base import ContentFile
from io import BytesIO
import os
from .models import FriendRequest, UserProfile
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Favorite
from django.contrib import messages
from .models import Rating, Comment
from django.http import JsonResponse
from .models import SheetMusic, Comment



from django.shortcuts import render



class SheetMusicListView(ListView):
    model = SheetMusic
    template_name = 'project/sheet_list.html'
    context_object_name = 'sheets'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filters
        difficulty = self.request.GET.get('difficulty')
        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')

        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        if category:
            queryset = queryset.filter(category=category)

        if tag:
            queryset = queryset.filter(tags__name__iexact=tag)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        context['all_difficulties'] = [choice[0] for choice in SheetMusic._meta.get_field('difficulty').choices]
        context['all_categories'] = [choice[0] for choice in SheetMusic._meta.get_field('category').choices]

        if self.request.user.is_authenticated:
            context['user_favorites'] = Favorite.objects.filter(user=self.request.user).values_list('sheet_id', flat=True)

            # 🟣 NEW: Precompute user ratings
            user_ratings = Rating.objects.filter(user=self.request.user)
            rating_dict = {rating.sheet_id: rating.score for rating in user_ratings}
            context['user_ratings'] = rating_dict

        else:
            context['user_favorites'] = []
            context['user_ratings'] = {}

        return context



def upload_sheet(request):
    if request.method == 'POST':
        form = SheetMusicForm(request.POST, request.FILES)
        if form.is_valid():
            sheet = form.save()
            generate_preview(sheet)
            return redirect('project:sheet_list')

    else:
        form = SheetMusicForm()
    return render(request, 'project/upload_sheet.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('project:sheet_list')
    else:
        form = UserCreationForm()
    return render(request, 'project/register.html', {'form': form})


class SheetMusicDeleteView(DeleteView):
    model = SheetMusic
    template_name = 'project/delete_sheet.html'
    success_url = reverse_lazy('project:sheet_list')

def generate_preview(sheet_obj):
    pdf_path = sheet_obj.pdf_file.path

    # Only generate a preview if the file is a PDF
    if not pdf_path.lower().endswith('.pdf'):
        return

    from pdf2image import convert_from_path
    from django.core.files.base import ContentFile
    from io import BytesIO
    import os

    try:
        images = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=150)
        if images:
            image_io = BytesIO()
            images[0].save(image_io, format='PNG')
            filename = os.path.basename(pdf_path).replace('.pdf', '_preview.png')
            sheet_obj.preview_image.save(filename, ContentFile(image_io.getvalue()), save=True)
    except Exception as e:
        print(f"Error generating preview: {e}")

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    from_user = request.user

    # Prevent sending to self
    if to_user == from_user:
        return redirect('project:view_users')

    # Prevent duplicate request
    existing_request = FriendRequest.objects.filter(
        from_user=from_user, to_user=to_user
    ).exists()

    reverse_request = FriendRequest.objects.filter(
        from_user=to_user, to_user=from_user
    ).exists()

    # Only create if no existing request in either direction
    if not existing_request and not reverse_request:
        FriendRequest.objects.create(from_user=from_user, to_user=to_user)

    return redirect('project:view_users')

@login_required
def accept_friend_request(request, request_id):
    f_request = get_object_or_404(FriendRequest, id=request_id)

    if f_request.to_user != request.user:
        return redirect('project:view_friend_requests')
    
    # ✅ Make sure both profiles are created first
    from_profile, _ = UserProfile.objects.get_or_create(user=f_request.from_user)
    to_profile, _ = UserProfile.objects.get_or_create(user=f_request.to_user)

    # ✅ Then compare to avoid duplicates
    if from_profile != to_profile:
        from_profile.friends.add(to_profile)
        to_profile.friends.add(from_profile)

    f_request.delete()
    return redirect('project:view_friend_requests')



@login_required
def view_friend_requests(request):
    incoming_requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, 'project/friend_requests.html', {
        'incoming_requests': incoming_requests
    })

@login_required
def view_users(request):
    current_user = request.user
    current_profile, _ = UserProfile.objects.get_or_create(user=current_user) 

    users = User.objects.exclude(id=current_user.id)

    sent_requests = FriendRequest.objects.filter(from_user=current_user).values_list('to_user_id', flat=True)
    received_requests = FriendRequest.objects.filter(to_user=current_user).values_list('from_user_id', flat=True)
    current_friends = current_profile.friends.values_list('user_id', flat=True)

    return render(request, 'project/users.html', {
        'users': users,
        'sent_requests': sent_requests,
        'received_requests': received_requests,
        'current_friends': current_friends,
    })
@login_required
def toggle_favorite(request, sheet_id):
    sheet = SheetMusic.objects.get(id=sheet_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, sheet=sheet)

    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})

    return redirect('project:sheet_list')  # or wherever you want to go back
@login_required
def view_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    sheets = [favorite.sheet for favorite in favorites]
    return render(request, 'project/favorites.html', {'sheets': sheets})



@login_required
def toggle_favorite(request, sheet_id):
    sheet = get_object_or_404(SheetMusic, id=sheet_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, sheet=sheet)

    if not created:
        favorite.delete()
        messages.success(request, f'Removed "{sheet.title}" from your favorites.')
    else:
        messages.success(request, f'Added "{sheet.title}" to your favorites! ❤️')

    return redirect('project:sheet_list')



@login_required
def accept_friend_request(request, request_id):
    f_request = get_object_or_404(FriendRequest, id=request_id)

    if f_request.to_user != request.user:
        return redirect('project:view_friend_requests')
    
    from_profile, _ = UserProfile.objects.get_or_create(user=f_request.from_user)
    to_profile, _ = UserProfile.objects.get_or_create(user=f_request.to_user)

    # Prevent adding self as friend
    if from_profile != to_profile:
        from_profile.friends.add(to_profile)
        to_profile.friends.add(from_profile)

    f_request.delete()
    return redirect('project:view_friend_requests')


@login_required
def sheet_detail(request, sheet_id):
    sheet = get_object_or_404(SheetMusic, id=sheet_id)
    comments = Comment.objects.filter(sheet=sheet).order_by('-created_at')

    if request.method == 'POST':
        text = request.POST.get('comment')
        if text:
            Comment.objects.create(user=request.user, sheet=sheet, text=text)
            return redirect('project:sheet_detail', sheet_id=sheet.id)

    return render(request, 'project/sheet_detail.html', {
        'sheet': sheet,
        'comments': comments
    })

@login_required
def rate_sheet(request, sheet_id):
    if request.method == 'POST':
        sheet = get_object_or_404(SheetMusic, id=sheet_id)
        score = int(request.POST.get('rating'))
        Rating.objects.update_or_create(
            user=request.user,
            sheet=sheet,
            defaults={'score': score}
        )
        return JsonResponse({'success': True, 'rating': score})


@login_required
def status_page(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    friends_profiles = user_profile.friends.all()
    friends = [profile.user for profile in friends_profiles] 

    favorited = Favorite.objects.filter(user__in=friends).select_related('sheet', 'user')
    rated = Rating.objects.filter(user__in=friends).select_related('sheet', 'user')
    commented = Comment.objects.filter(user__in=friends).select_related('sheet', 'user')

    context = {
        'favorited': favorited,
        'rated': rated,
        'commented': commented
    }

    return render(request, 'project/status_page.html', context)

@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    friends = user_profile.friends.exclude(user=request.user)
    favorited_sheets = SheetMusic.objects.filter(favorite__user=request.user)
    return render(request, 'project/profile.html', {
        'friends': friends,
        'favorited_sheets': favorited_sheets,
    })