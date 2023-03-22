import random
import string
from django.utils.text import slugify


def get_random_string(size=4, chars=string.ascii_lowercase + string.digits, max_size=30):
	return "".join([random.choice(chars) for _ in range(size)])
	
def get_unique_slug(instance, new_slug=None, size=10):
	title = instance.title
	if new_slug is None:
		slug = slugify(title)
	else:
		slug = new_slug
	slug = slug[:max_size]
	Klass = instance.__class__
	parent = None
	try:
		parent = instance.parent
	except:
		pass
	if parent is not None:
		qs = Klass.objects.filter(parent=parent, slug=slug)
	else:
		qs = Klass.objects.filter(slug=slug)
	if qs.exist():
		new_slug = slugify(title) + get_random_string(size=size)
		return get_unique_slug(instance, new_slug=new_slug)
	return slug