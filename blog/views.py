from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, TipoUsuario, Category
from .forms import PostForm, EditForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.db.models import Count

#def home(request):
#	return render(request, 'home.html', {})

def FilterPostsView(request):
	qs = Post.objects.all()
	categories = Category.objects.all()
	titulo_search_query = request.GET.get('titulo_search')
	category = request.GET.get('category_search')
	fecha_min_query = request.GET.get('fecha_min')
	fecha_max_query = request.GET.get('fecha_max')
	order_search_query = request.GET.get('order_search')

	if titulo_search_query != '' and titulo_search_query is not None:
		qs = qs.filter(title__icontains=titulo_search_query)

	if fecha_min_query != '' and titulo_search_query is not None:
		qs = qs.filter(post_date__gte=fecha_min_query)

	if fecha_max_query != '' and titulo_search_query is not None:
		qs = qs.filter(post_date__lte=fecha_max_query)

	if category != '' and category is not None and category != 'Elegir...':
		qs = qs.filter(category__name= category)

	if order_search_query != '' and order_search_query is not None:
		if order_search_query == "mas recientes" :
			qs = qs.order_by('-post_date')
		elif order_search_query == "mas antiguos" :
			qs = qs.order_by('post_date')
		elif order_search_query == "mas comentados" :
			qs = qs.annotate(num_comments=Count('comments')).order_by('-num_comments')
		

	context = {
		'queryset':qs,
		'categories': categories
	}
	return render(request, "search_results.html",context)


class UserPostsView(ListView):
	model = Post
	template_name = 'user_posts.html'
	ordering = ['-post_date']


class HomeView(ListView):
	model = Post
	template_name = 'home.html'
	cats = Category.objects.all()
	ordering = ['-post_date']

	def get_context_data(self, *args, **kwargs):
					cat_menu = Category.objects.all()
					context = super(HomeView, self).get_context_data(*args, **kwargs)
					context["cat_menu"] = cat_menu
					return context


def CategoryView(request, cats):
	category_posts = Post.objects.filter(category__name=cats)
	return render(request, 'categories.html', {'cats':cats.title(), 'category_posts':category_posts})

class ArticleDetailView(DetailView):
	model = Post
	template_name = 'article_details.html'

	def get_context_data(self, *args, **kwargs):
					cat_menu = Category.objects.all()
					context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
					context["cat_menu"] = cat_menu
					return context



class AddPostView(CreateView):
	model = Post
	form_class = PostForm
	template_name = 'add_post.html'
	#fields = '__all__'

class AddCommentView(CreateView):
	model = Comment
	form_class = CommentForm
	template_name = 'add_comment.html'
	#fields = '__all__'
	success_url = reverse_lazy('home')
	def form_valid(self,form):
		form.instance.post_id = self.kwargs['pk']
		return super().form_valid(form)

class AddCategoryView(CreateView):
	model = Category
	#form_class = PostForm
	template_name = 'add_category.html'
	fields = '__all__'

class UpdatePostView(UpdateView):
	model = Post 
	form_class = EditForm
	template_name = 'update_post.html'
	#fields = ['title', 'title_tag','body']


class DeletePostView(DeleteView):
	model = Post 
	template_name = 'delete_post.html'
	success_url = reverse_lazy('home')