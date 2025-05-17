from django.shortcuts import render
from recipe.models import Recipe
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

def home(request):
    query = request.GET.get('q')
    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).order_by('-created_at')
    else:
        recipes = Recipe.objects.all().order_by('-created_at')
    
    context = {'recipes': recipes}
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def add_recipe(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES.get('image')

        Recipe.objects.create(
            title=title,
            description=description,
            image=image
        )
        return render(request, 'home.html', {'success': True})

    return render(request, 'add_recipe.html')

def update(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        recipe.title = request.POST['title']
        recipe.description = request.POST['description']
        if 'image' in request.FILES:    
            recipe.image = request.FILES['image']
        recipe.save()
        return redirect('home')

    return render(request, 'update.html', {'recipe': recipe})

def delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return redirect('home')

def log_out(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login') 

def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'log_in.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')  # Make sure you have 'login' URL
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})
