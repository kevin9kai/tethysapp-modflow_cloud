from tethys_sdk.base import TethysAppBase, url_map_maker


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
        )

        return url_maps