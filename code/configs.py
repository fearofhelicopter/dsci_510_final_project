# this file is the configuration for api counts
# first endpoint
CAR_API_BASIC_URL = "https://carapi.app"
CAR_API_TOKEN = "e50d6b92-4cb1-4f35-a4f3-5cb0e3b8f1fc"
CAR_API_SECRET = "16aa159f1ee4c611d2372ad7b8413967"
CAR_API_LOGIN = '/api/auth/login'
CAR_API_YEARS = '/api/years'
CAR_API_MAKES = '/api/makes'
CAR_API_MODELS = '/api/models'
CAR_API_TRIMS = '/api/trims'

# second endpoint
CAR_MD_BASIC_URL = "http://api.carmd.com/v3.0"
CAR_MD_AUTH = "Basic ODY4ZDFlNDMtNmQxYy00YjJiLWJiMWUtNjIwYjAzYjE2OWRj"
CAR_MD_PARTNER = "753235dba9a34a8492fc18bcd22a40b9"
CAR_MD_HEADER = {
    "content-type": "application/json",
    "authorization": CAR_MD_AUTH,
    "partner-token": CAR_MD_PARTNER
}
CAR_MD_UPCOMING_REPAIR = "/upcoming"
CAR_MD_MAINTENANCE_LIST = "/maintlist"
CAR_MD_MAINTENANCE = "/maint"
