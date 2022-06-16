from itemadapter import ItemAdapter
from news_blog.models import Post, Categorie
from users.models import CustomUser as User
from django.contrib.auth.models import Group
from news_blog.constants import INDIAN_EXPRESS_EDITOR_EMAIL, GROUP_EDITOR_NAME, POST_TYPE_CHOICES
from datetime import datetime



class ScraperPipeline:
    def process_item(self, item, spider):
        try:
            editor, created = User.objects.get_or_create(email=INDIAN_EXPRESS_EDITOR_EMAIL)
            if created:
                group = Group.objects.get(name=GROUP_EDITOR_NAME)
                editor.set_password('123')
                editor.save()
                group.user_set.add(editor)
            category = Categorie.objects.get(name=item['category'])
            Post.objects.create(
                title=item['title'],
                author=editor,
                content=item['content'],
                created_on=datetime.strptime(item['date'][:-3].strip(), '%B %d, %Y  %I:%M:%S').date(),
                category=category,
                image=item['image_url'],
                type=POST_TYPE_CHOICES[0][0]
            )
            print("\n")
            print(item)
        except Categorie.DoesNotExist as e:
            print("\n")
            print("\nCategorie not exists:{}".format(e))
            print(item)
        except Exception as e:
            print("\n")
            print("\nFailed to load quote, Reason For Failure:{}".format(e))
            print(item)
        return item
