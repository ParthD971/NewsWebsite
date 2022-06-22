from news_blog.models import Post, Categorie, PostStatus
from news_blog.constants import POST_TYPE_CHOICES
from datetime import datetime
from django.core.files import File
import urllib.request
import os


class ScraperPipeline:
    def process_item(self, item, spider):
        try:
            category = Categorie.objects.get(name=item['category'])
            status = PostStatus.objects.get(name='pending')
            post = Post.objects.create(
                title=item['title'],
                author=None,
                content=item['content'],
                status=status,
                created_on=datetime.strptime(item['date'][:-3].strip(), '%B %d, %Y  %I:%M:%S').date(),
                category=category,
                post_type=POST_TYPE_CHOICES[0][0]  # Scrapped
            )

            result = urllib.request.urlretrieve(item['image_url'])
            if result:
                post.image.save(os.path.basename(item['image_url']), File(open(result[0], 'rb')))
                post.save()

            print("\n")
            print(item)
        except Categorie.DoesNotExist as e:
            print("\n\nCategorie not exists:{}".format(e))
            print(item)
        except Exception as e:
            print("\n\nFailed to load news, Reason For Failure:{}".format(e))
            print(item)
        return item
