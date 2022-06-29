from news_blog.models import Post, Categorie, PostStatus, PCMiddle
from news_blog.constants import POST_TYPE_CHOICES
from datetime import datetime
from django.core.files import File
import urllib.request
import os


class ScraperPipeline:
    def process_item(self, item, spider):
        try:
            category_obj = Categorie.objects.get(name=item['category'])
            status = PostStatus.objects.get(name='pending')
            post = Post.objects.create(
                title=item['title'],
                author=None,
                content=item['content'],
                status=status,
                created_on=datetime.strptime(item['date'][:-3].strip(), '%B %d, %Y  %I:%M:%S').date(),
                post_type=POST_TYPE_CHOICES[0][0],  # Scrapped
                author_display_name='IndiaExpress'
            )

            result = urllib.request.urlretrieve(item['image_url'])
            if result:
                post.image.save(os.path.basename(item['image_url']), File(open(result[0], 'rb')))
                post.save()
                PCMiddle(post=post, category=category_obj).save()

            print("\n")
            print(item)
        except Categorie.DoesNotExist as e:
            print("\n\nCategorie not exists:{}".format(e))
            print(item)
        except Exception as e:
            print("\n\nFailed to load news, Reason For Failure:{}".format(e))
            print(item)
        return item
