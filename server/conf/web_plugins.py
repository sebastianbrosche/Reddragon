"""
Darkstaff MUD - Web Plugins

This module is used by Evennia to configure web plugins.
"""

def start_plugin_services(web_root):
    """
    Called when the web server starts.
    
    Args:
        web_root: The web root service instance
    """
    pass

def at_webserver_root_creation(web_root):
    """
    This is called as the web server has finished building its default
    path tree. At this point, the media/ and static/ URIs have already
    been added to the web root.
    
    Args:
        web_root (twisted.web.resource.Resource): The root
            resource of the URI tree.
            
    Returns:
        web_root: The potentially modified root structure.
    """
    return web_root


def at_webproxy_root_creation(web_root):
    """
    This function can modify the portal proxy service.
    
    Args:
        web_root: The Evennia Website application.
        
    Returns:
        web_root: The modified web root.
    """
    return web_root
