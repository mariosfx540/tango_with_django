from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import UserForm, UserProfileForm
from rango.forms import CategoryForm, PageForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
from django.http import HttpResponse

def index(request):
	
	category_list = Category.objects.order_by('-likes')[:5]
	topfive_list = Page.objects.order_by('-views')[:5]
	
	context_dict = {'categories': category_list, 'pages': topfive_list}
	
	#Get the number of visits to the site
	visits = request.session.get('visits')
	if not visits:
		visits = 1
	reset_last_visit_time = False
	
	last_visit = request.session.get('last_visit')
	if last_visit:
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		
		if (datetime.now() - last_visit_time).seconds > 0:
			visits = visits + 1
			reset_last_visit_time = True
			
	else:
		reset_last_visit_time = True
		
	if reset_last_visit_time:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = visits
	context_dict['visits'] = visits
	
	response = render(request, 'rango/index.html', context_dict)
	
	return response
	
    
def about(request):
	
	if request.session.get('visits'):
		count = request.session.get('visits')
	else:
		count = 0
	
	return render(request, 'rango/about.html', {'visits': count})

def category(request,category_name_slug):
	context_dict = {}
	
	try:
		# Can we find a category name slug with the given name?
        # So the .get() method returns one model instance or raises an exception.
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name
		
		#retrieve all of the associated pages
		pages = Page.objects.filter(category=category)
		
		# Adds our results list to the template context under name pages.
		context_dict['pages'] = pages
		
		# We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
		context_dict['category'] = category
		
		context_dict['slug'] = category_name_slug
	except Category.DoesNotExist:
		pass
	
	return render(request, 'rango/category.html', context_dict)



def add_category(request):
	# A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
		if form.is_valid():
            # Save the new category to the database.
			form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
			return index(request)
		else:
            # The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
        # If the request was not a POST, display the form to enter details.
		form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
	return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
	
	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()

				return category(request, category_name_slug)
		else:
			print form.errors
	else:
		form = PageForm()

		context_dict = {'form':form, 'category': cat}

		return render(request, 'rango/add_page.html', context_dict)


#Restricting access using a Decorator
@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text")

