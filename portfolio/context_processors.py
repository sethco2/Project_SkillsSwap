"""Inject site-wide identity values so templates don't hard-code them."""


def site_meta(request):
    return {
        "SITE_OWNER": "Seth Grant",
        "SITE_TAGLINE": (
            "I use AI to organize information, automate work, "
            "and build sharper business systems."
        ),
        "SITE_EMAIL": "sethgrant2003@gmail.com",
        "SITE_LINKEDIN": "https://www.linkedin.com/in/sethngrant/",
        "SITE_GITHUB": "https://github.com/sethco1",
        "SITE_INSTAGRAM": "https://www.instagram.com/sethngrant/",
        "SITE_TIKTOK": "https://www.tiktok.com/@seethlifts",
    }
