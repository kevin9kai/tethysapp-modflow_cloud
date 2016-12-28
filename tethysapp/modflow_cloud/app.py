from tethys_sdk.base import TethysAppBase, url_map_maker
#----------
from tethys_sdk.stores import PersistentStore
#----------

class ModflowCloud(TethysAppBase):
    """
    Tethys app class for MODFLOW Cloud.
    """

    name = 'MODFLOW Cloud'
    index = 'modflow_cloud:home'
    icon = 'modflow_cloud/images/icon.gif'
    package = 'modflow_cloud'
    root_url = 'modflow-cloud'
    color = '#24c93f'
    description = 'Place a brief description of your app here.'
    enable_feedback = False
    feedback_emails = []

        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='modflow-cloud',
                           controller='modflow_cloud.controllers.home'),
                    UrlMap(name='info',
                           url='info',
                           controller='modflow_cloud.controllers.info'),
                    UrlMap(name='map',
                           url='map',
                           controller='modflow_cloud.controllers.map'),
                    UrlMap(name='data',
                           url='data',
                           controller='modflow_cloud.controllers.data'),
                    UrlMap(name='temp',
                           url='temp',
                           controller='modflow_cloud.controllers.temp'),
                    UrlMap(name='download_hs_res',
                           url='download-hs-res',
                           controller='modflow_cloud.controllers.download_hs_res'),
                    #Here from data.js it goes into download-hs-res url because that is
                    #where the window.location is bringing the user to.
        )

        return url_maps

    #this is just from the tutorial-----------------------------------------------

    #------------------------------------------------------------------------------