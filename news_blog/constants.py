# FIXTURES: POST STATUS
POST_STATUS_PENDING = 'pending'
POST_STATUS_ACTIVE = 'active'
POST_STATUS_IN_ACTIVE = 'inactive'
POST_STATUS_DELETED = 'deleted'
POST_STATUS_IN_REVIEW = 'inreview'
POST_STATUS_REJECTED = 'rejected'

# FIXTURES: NOTIFICATION TYPE
NOTIFICATION_TYPE_MANAGER_REQUEST = 'manager request'
NOTIFICATION_TYPE_EDITOR_REQUEST = 'editor request'
NOTIFICATION_TYPE_POST_ADDED = 'post added'
NOTIFICATION_TYPE_POST_DELETED = 'post deleted'
NOTIFICATION_TYPE_POST_CHANGED = 'post changed'

# FIXTURES: NOTIFICATION STATUS
NOTIFICATION_STATUS_PENDING = 'pending'
NOTIFICATION_STATUS_ACCEPTED = 'accepted'
NOTIFICATION_STATUS_REJECTED = 'rejected'

# MODELS VARIABLES
POST_TYPE_CHOICES = [
    ("SCRAPED", "SCRAPED"),
    ("MANUAL", "MANUAL")
]
DEFAULT_IMAGE_NAME = 'default.jpg'
POST_IMAGE_UPLOAD_TO = 'news_images/'
DEFAULT_IMAGE_PATH = DEFAULT_IMAGE_NAME + POST_IMAGE_UPLOAD_TO

# news_blog.forms.ManagerApplicationForm
CHECK_BOX_LABEL = 'I have read and agree the terms and conditions.'
ALREADY_ONE_ROLE_EXISTS = u"You cannot apply because you already have one role as %s."
ALREADY_APPLIED_FOR__ROLE = f"You have already applied for %s. Current status: %s."
ALREADY_PREMIUM_USER = 'You cannot apply because you already are premium user.'





