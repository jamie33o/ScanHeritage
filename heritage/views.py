from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.text import slugify
from .models import HeritageSite, Category, SiteImage, SiteFact
from .forms import HeritageSiteForm, SiteImageForm, SiteFactForm


def home(request):
    featured_sites = HeritageSite.objects.filter(is_published=True, featured=True)[:6]
    recent_sites = HeritageSite.objects.filter(is_published=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
    
    context = {
        'featured_sites': featured_sites,
        'recent_sites': recent_sites,
        'categories': categories,
    }
    return render(request, 'heritage/home.html', context)

def site_list(request):
    sites = HeritageSite.objects.filter(is_published=True)
    categories = Category.objects.all()
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        sites = sites.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query)
        )
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        sites = sites.filter(category_id=category_id)
    
    # Site type filter
    site_type = request.GET.get('type')
    if site_type:
        sites = sites.filter(site_type=site_type)
    
    paginator = Paginator(sites, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'site_types': HeritageSite.SITE_TYPES,
        'current_query': query,
        'current_category': category_id,
        'current_type': site_type,
    }
    return render(request, 'heritage/site_list.html', context)

def site_detail(request, slug):
    site = get_object_or_404(HeritageSite, slug=slug, is_published=True)
    images = site.images.all()
    facts = site.facts.all()
    
    context = {
        'site': site,
        'images': images,
        'facts': facts,
    }
    return render(request, 'heritage/site_detail.html', context)

@login_required
def dashboard(request):
    user_sites = HeritageSite.objects.filter(owner=request.user)
    
    context = {
        'user_sites': user_sites,
        'total_sites': user_sites.count(),
        'published_sites': user_sites.filter(is_published=True).count(),
        'draft_sites': user_sites.filter(is_published=False).count(),
    }
    return render(request, 'heritage/dashboard.html', context)

@login_required
def create_site(request):
    if request.method == 'POST':
        form = HeritageSiteForm(request.POST, request.FILES)
        if form.is_valid():
            site = form.save(commit=False)
            site.owner = request.user
            site.slug = slugify(site.title)
            site.save()
            messages.success(request, 'Heritage site created successfully!')
            return redirect('heritage:site_edit', slug=site.slug)
    else:
        form = HeritageSiteForm()
    
    return render(request, 'heritage/create_site.html', {'form': form})

@login_required
def edit_site(request, slug):
    site = get_object_or_404(HeritageSite, slug=slug, owner=request.user)
    
    if request.method == 'POST':
        form = HeritageSiteForm(request.POST, request.FILES, instance=site)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site updated successfully!')
            return redirect('heritage:site_edit', slug=site.slug)
    else:
        form = HeritageSiteForm(instance=site)
    
    images = site.images.all()
    facts = site.facts.all()
    
    context = {
        'form': form,
        'site': site,
        'images': images,
        'facts': facts,
    }
    return render(request, 'heritage/edit_site.html', context)
