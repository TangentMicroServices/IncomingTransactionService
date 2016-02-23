from django.conf import settings

## docker settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
ALLOWED_HOSTS = ['.consul']
DEBUG = True

settings.INSTALLED_APPS.extend([
    # DRF:
    'rest_framework',
    'rest_framework_swagger',
	'corsheaders',

    #3rd party:
    'django_jenkins',

    # custom:
    'webhook',
    'mandrill',
    'ifttt',
    'hipchat',
])

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',        
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        #'tokenauth.authbackends.RESTTokenAuthBackend',        
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}

# Services:

## Service base urls without a trailing slash:
USERSERVICE_BASE_URL = 'http://userservice.staging.tangentmicroservices.com'
HOURSSERVICE_BASE_URL = 'http://hoursservice.staging.tangentmicroservices.com'

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
)

PROJECT_APPS = (
    'api',
)

CORS_ORIGIN_ALLOW_ALL = True
VERSION = 1


SWAGGER_SETTINGS = {    
	'is_authenticated': True,
    'permission_denied_handler': 'api.permissions.swagger_permission_denied_handler',
    'info': {
        'contact': 'team-lead@tangentsolutions.co.za',
        'title': 'UserService API',
        'description': """
<h3>Welcome to the docs for the ProjectService</h3>

<ul>
<li>No authentication is required if accessing through the Kong Gateway</li>
<li>If accessing this API internally: e.g.: via a `service.consul` tld, then please ensure that the
user headers stay intact:
</ul>
<pre><code>X-Consumer-ID, the ID of the Consumer on Kong
X-Consumer-Custom-ID, the custom_id of the Consumer (if set)
X-Consumer-Username
</pre></code>

""",        
    },
}

STATIC_URL = '/static/'
STATIC_ROOT = '/code/static/'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--with-spec', '--spec-color', '-s',
             '--with-coverage', '--cover-html',
             '--cover-package=.', '--cover-html-dir=reports/cover',
             '--exclude-dir=ifttt/tests/integration/']
