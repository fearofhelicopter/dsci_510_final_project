# this file is the configuration for api counts
# first endpoint
CAR_API_BASIC_URL = "https://carapi.app"
CAR_API_TOKEN = "e50d6b92-4cb1-4f35-a4f3-5cb0e3b8f1fc"
CAR_API_SECRET = "5d4677c7cec4251efe689a0458b128b2"
CAR_API_LOGIN = '/api/auth/login'
CAR_API_YEARS = '/api/years'
CAR_API_MAKES = '/api/makes'
CAR_API_MODELS = '/api/models'
CAR_API_TRIMS = '/api/trims'

# second endpoint
CAR_MD_BASIC_URL = "http://api.carmd.com/v3.0"
CAR_MD_AUTH = "Basic OWJmNTRlYzAtM2JlNi00Njg0LThiN2QtZGU5MzVlODk0ZWM5"
CAR_MD_PARTNER = "443bf0ea4c5947e1a0ff1a2b5ef44023"
CAR_MD_HEADER = {
    "content-type": "application/json",
    "authorization": CAR_MD_AUTH,
    "partner-token": CAR_MD_PARTNER
}
CAR_MD_UPCOMING_REPAIR = "/upcoming"
CAR_MD_MAINTENANCE_LIST = "/maintlist"
CAR_MD_MAINTENANCE = "/maint"

