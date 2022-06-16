# models variable
POST_STATUS_CHOICES = [
    ('PEN', 'PENDING'),
    ('ACT', 'ACTIVE'),
    ('INACT', 'INACTIVE'),
]

POST_TYPE_CHOICES = [
    ("SCRAPED", "SCRAPED"),
    ("MANUAL", "MANUAL")
]
DEFAULT_IMAGE_NAME = 'default.jpg'
DEFAULT_IMAGE_PATH = 'news_images/default.jpg'
POST_IMAGE_UPLOAD_TO = 'news_images/'

# admin varible
GROUP_EDITOR_NAME = 'Editor'

#scrapy variables
INDIAN_EXPRESS_EDITOR_EMAIL = 'fakeindianexpress@abc.com'