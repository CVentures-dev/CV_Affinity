"""
Module: decline_email_templates.py

This module provides four functions to generate email subjects and bodies for various decline scenarios:
1. Geographic restriction
2. Topic out of scope
3. Climate but food/agriculture tech
4. Stage out of scope
Each function returns a tuple: (subject, body)
"""

def generate_geo_decline(name, company_name, country):
    """
    Decline email for geographic outside Europe or Israel.

    Args:
        name (str): Recipient's name
        company_name (str): Name of the company
        country (str): Country of the company

    Returns:
        subject (str), body (str)
    """
    subject = "Thank You for Reaching Out"
    body = f"Hi {name},\n\n"
    body += f"Thanks for reaching out and for sharing more about {company_name}, we really appreciate your interest in working with Contrarian Ventures.\n"
    body += "At this time, we focus our investments on companies incorporated in Europe or Israel, "
    body += f"and {country} unfortunately falls outside that scope.\n\n"
    body += f"That said, we wish you and your team all the best as you build {company_name}. "
    body += "Keep pushing, the world needs more ambitious founders tackling tough challenges!\n\n"
    body += "All the best,\nThe Contrarian Ventures Team"
    return subject, body


def generate_topic_decline(name, company_name):
    """
    Decline email for topic out of scope.

    Args:
        name (str): Recipient's name
        company_name (str): Name of the company

    Returns:
        subject (str), body (str)
    """
    subject = "Thank You for Reaching Out"
    body = f"Dear {name},\n\n"
    body += "Thank you so much for reaching out to us, we really appreciate your interest in Contrarian Ventures.\n"
    body += f"Unfortunately, we can’t proceed as your company’s focus falls outside our current investment scope. "
    body += "We only invest in companies tackling the climate crisis through decarbonisation solutions.\n\n"
    body += f"We wish you all the success with {company_name} and hope to catch up down the road. Best of luck!\n\n"
    body += "All the best,\nThe Contrarian Ventures Team"
    return subject, body


def generate_sector_decline(name, company_name):
    """
    Decline email for climate sector but food/agriculture tech.

    Args:
        name (str): Recipient's name
        company_name (str): Name of the company

    Returns:
        subject (str), body (str)
    """
    subject = "Thank You for Reaching Out"
    body = f"Dear {name},\n\n"
    body += "Thank you so much for reaching out and for your interest in Contrarian Ventures, "
    body += f"we really appreciate you sharing about {company_name} with us.\n"
    body += "At this stage, food and agriculture are not part of our current investment scope. "
    body += "Our fund is focused on companies tackling the climate crisis through decarbonisation solutions "
    body += "across energy, mobility, industry, the built environment, carbon, and climate intelligence.\n\n"
    body += f"We wish you all the best with {company_name} and hope our paths cross again in the future. Best of luck!\n\n"
    body += "All the best,\nThe Contrarian Ventures Team"
    return subject, body


def generate_stage_decline(name, company_name):
    """
    Decline email for stage out of scope.

    Args:
        name (str): Recipient's name
        company_name (str): Name of the company

    Returns:
        subject (str), body (str)
    """
    subject = "Thank You for Reaching Out"
    body = f"Dear {name},\n\n"
    body += f"Thank you so much for sharing about {company_name} with us, we really appreciate your interest in Contrarian Ventures.\n"
    body += "At this point, we’re focused exclusively on early-stage investments,  typically as early as possible, "
    body += f"from pre-seed to Series A. Since {company_name} is already beyond that stage, we won’t be the right partner this time around.\n\n"
    body += "That said, if you ever start building something new, we’d love to hear from you. We’re always excited to partner with founders from day zero.\n\n"
    body += f"Wishing you and the team at {company_name} continued success!\n\n"
    body += "All the best,\nThe Contrarian Ventures Team"
    return subject, body
