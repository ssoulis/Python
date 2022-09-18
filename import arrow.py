import arrow
import json

import bot_core
import errors
from plugins import Registry as PluginRegistry
import instances


bot_core.override_strorage_path('/tmp/test_pluginx')

from proxy_providers \
        import get_proxy_info, get_residential_proxy_info,\
        get_mobile_proxy_info

class PluginTester(object):
    def __init__(self,user_profile_id=None):
        if user_profile_id==None:
            self.sample_user=self.get_sample_user()
        else:
            self.sample_user=self.get_user_profile(user_profile_id)

        self.account_registration_dir='accounts.registry'

    def store_registered_account(self,registration_result_instance):
        params=registration_result_instance.get_result_params()

        if len(params['username'])==0:
            return

        now_timestamp=arrow.utcnow().float_timestamp
        filepath=self.account_registration_dir+'/'+params['account_domain']+'.'+str(now_timestamp)

        with open(filepath,'w') as w:
            w.write(json.dumps(params)+'\n')


    ### --- Bot Plugin Access and Management --- ####
    def get_available_bot_plugin_names(self):
        return PluginRegistry.get_available_plugin_names()

    def get_bot_imitation_levels(self):
        return [i for i in bot_core.ImitationLevels.__dict__.keys()\
                            if not i.startswith('__')]

    def construct_bot_info(self,
                           bot_plugin_name,
                           imitation_level,
                           background_mode=True):

        if background_mode==True:
            bot_mode=bot_core.BotModes.background
        else:
            bot_mode=bot_core.BotModes.foreground

        return bot_core.BotInfo(bot_mode,
                                bot_plugin_name,
                                imitation_level)

    ### --- NEW ACTIONS --- ###
    def construct_view_action_info(self,
                                  resource_id,
                                  affiliate_resource_ids,
                                  duration_limit_secs=20*60,
                                  ad_watch_ratio=1.0):
        return bot_core.ViewActionInfo(resource_id,
                                       affiliate_resource_ids,
                                       duration_limit_secs,
                                       ad_watch_ratio)


    def construct_view_engage_action_info(self,
                                         resource_id,
                                         affiliate_resource_ids,
                                         duration_limit_secs=20*60,
                                         ad_watch_ratio=1.0,
                                         ad_click_through_rate=0.03):
        return bot_core.ViewEngageActionInfo(resource_id,
                                       affiliate_resource_ids,
                                       duration_limit_secs,
                                       ad_watch_ratio,
                                       ad_click_through_rate)

    def construct_like_action_info(self,
                                   resource_id,
                                   affiliate_resource_ids):
        return bot_core.LikeActionInfo(resource_id,
                                       affiliate_resource_ids)

    def construct_dislike_action_info(self,
                                   resource_id,
                                   affiliate_resource_ids):
        return bot_core.DislikeActionInfo(resource_id,
                                       affiliate_resource_ids)

    def construct_share_action_info(self,
                                   resource_id,
                                   affiliate_resource_ids):
        return bot_core.ShareActionInfo(resource_id,
                                       affiliate_resource_ids)

    def construct_follow_action_info(self,
                                     resource_id,
                                     affiliate_resource_ids):
        return bot_core.FollowActionInfo(resource_id,
                                       affiliate_resource_ids)

    def construct_post_action_info(self,
                                   resource_id,
                                   affiliate_resource_ids,
                                   post_content):
        return bot_core.PostActionInfo(resource_id,
                                       affiliate_resource_ids,
                                       post_content)

    def construct_comment_action_info(self,
                                      resource_id,
                                      affiliate_resource_ids,
                                      comment_content):
        return bot_core.CommentActionInfo(resource_id,
                                       affiliate_resource_ids,
                                       comment_content)

    def construct_registration_action_info(self,
                                           resource_id):
        return bot_core.RegistrationActionInfo(resource_id)

    def construct_maintenance_action_info(self,
                                          resource_id,
                                          affiliate_resource_ids):
        return bot_core.MaintenanceActionInfo(resource_id,
                                              affiliate_resource_ids)

    def construct_engagement_action_info(self,
                                        resource_id,
                                        affiliate_resource_ids):
        return bot_core.EngagementActionInfo(resource_id,
                                            affiliate_resource_ids)

    ### --- USER GROUP ACCESS AND MANAGEMENT --- ###
    def get_user_profile(self,user_profile_id):
        up=bot_core.UserProfile(user_profile_id)
        up.load()
        print(up.__dict__)
        return up

    def get_sample_user(self):
        user_profile_id='demo_user0'
        country_code='us'
        up=bot_core.UserProfile(user_profile_id)
        print(up.__dict__)
        try:
            #up.load()
            raise FileNotFoundError
        except FileNotFoundError:
            up.set_country_code(country_code)
            up.set_profile_info('Robert','Smith','male',9,3,1974)
            pasok_ua='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
            pasok_ua=(pasok_ua,'1920x1080')
            print(pasok_ua)

            up.set_desktop_ua([pasok_ua for i in range(3)])
            up.set_mobile_ua([pasok_ua for i in range(2)])
            up.set_tablet_ua([pasok_ua for i in range(1)])

            up.set_windows_ua([pasok_ua for i in range(2)])
            up.set_macos_ua([pasok_ua for i in range(1)])
            up.set_linux_ua([pasok_ua for i in range(1)])
            up.set_ios_ua([pasok_ua for i in range(2)])
            up.set_android_ua([pasok_ua for i in range(2)])
            up.store()

        return up

    def submit_new_job(self,
                       bot_info,
                       action_info):
        bot_class=PluginRegistry.get_class_for_plugin(bot_info.get_bot_plugin())
        country_code='us'
        proxy_info=get_proxy_info(country_code,bot_class)
        instance_data=bot_core.StandardActionInstanceData(self.sample_user.get_user_id(),
                                                          bot_core.ViewerTypes.desktop,
                                                          proxy_info)
        instance=bot_class(0,
                           bot_info,
                           action_info,
                           instance_data)

        result=instance.run_action()

        #store registrations
        result=result[1]
        if  result.__class__==bot_core.RegistrationActionInstanceResult and\
                result.get_status()==True:
            self.store_registered_account(result)

        print(result)



if __name__=='__main__':
    import importlib
    import sys

    if len(sys.argv)==2:
        tester=PluginTester()
    else:
        print('using user profile id: '+sys.argv[2])
        tester=PluginTester(sys.argv[2])

    module_name=sys.argv[1].replace('/','.').replace('.py','')
    test_module=importlib.import_module(module_name)

    for test_function in test_module.get_tests():
        test_function(tester)