from qx_base.settings import get_settings


QX_COMMUNITY_SETTINGS = {
    "COMMENT_MODEL": None,
    "COMMENT_USER_SERIALIZER_CLASS": None,
    "POST_MODEL": None,
    "STAR_MODEL": None,
}

community_settings = get_settings(
    'QX_COMMUNITY_SETTINGS', QX_COMMUNITY_SETTINGS)
