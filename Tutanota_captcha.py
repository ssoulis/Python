import bot_core
from . import plugin_base
import time
import random
from random import choices
import string
import json
import requests
import getpass
from settings import profile_hostname
from settings import profile_port
from settings import images_port
from settings import sms_service_hostname
from settings import sms_service_port
from settings import account_service_hostname
from settings import account_service_port
import signal
import urllib.request
from anticaptchaofficial.imagecaptcha import *

class AdbtcPlugin(plugin_base.BotPluginBase):
    def view_action(self):
        self.sleep(delay)
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                     True)

    def view_engage_action(self):
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                     True)

    def like_action(self):
        url = self.get_action_info().get_resource_id()
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                    True)

    def dislike_action(self):
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                     True)

    def share_action(self):
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                     True)
    def follow_action(self):
        url = self.get_action_info().get_resource_id()
        print(url)
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                            True)

    def post_action(self):
        print("POST ACTION")
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                     True)
    def comment_action(self):
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                     True)

    
    def shuffle_with_probs(self, revers_prob, elem1, elem1_upper_prob,elem2,
                                                first_upper_prob,
                                                random_num_prob):
        delimiters = [""]
        order = 0
        if random.random() < revers_prob:
            order = 1
        if random.random() < elem1_upper_prob:
            elem1 = elem1[0].upper() + elem1[1:]
        if order == 0:
            username = elem1 + random.choice(delimiters) + elem2
        else:
            username = elem2 + random.choice(delimiters) + elem1
        if random.random() < random_num_prob:
            username += random.choice(delimiters) + str(random.randint(1,250))
        return username

    def generate_random_valid_password(self):
        stringLength = random.randint(10,20)
        letters = 'abcdefghijklmnopqrstuvwxyz'
        upper_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        l1 = ''.join(random.choice(letters) for i in range(stringLength))
        to_capital = random.randint(1,5)
        to_numbers = random.randint(1,5)
        for i in range(to_capital):
            pos = random.randint(1,len(l1)-1)
            l2 = l1[:pos] + random.choice(upper_letters) + l1[pos+1:]
        for i in range(to_numbers):
            pos = random.randint(1,len(l2)-1)
            l3 = l2[:pos] + random.choice(digits) + l2[pos+1:]
        l3 += str(random.choices(upper_letters)[0])
        return l3

    def generate_usernames(self, first_name, last_name,  birth_year ):
        options = [1, 2, 3, 4, 5, 6, 7]
        weights = [0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14]
        choice = choices(options, weights)[0]

        if random.randint(0,1) == 1:
            birth_year = birth_year[2:]

        if choice == 1:
            username = self.shuffle_with_probs(0.06, first_name, 0.22, birth_year, 0, 0.05)
        elif choice == 2:
            username = self.shuffle_with_probs(0, first_name, 0.41, "", 0.07, 0.05)
        elif choice == 3:
            username = self.shuffle_with_probs(0, last_name, 0.3, "", 0.08, 0.05)
        elif choice == 4:
            username = self.shuffle_with_probs(0.44, first_name, 0.34, last_name, 0.18, 0.05)
        elif choice == 5:
            username = self.shuffle_with_probs(0.06, first_name[0], 0.22, last_name, 0, 0.05)
        elif choice == 6:
            username = self.shuffle_with_probs(0.44, first_name, 0.34, last_name[0], 0.18, 0.05)
        elif choice == 7:
            username = self.shuffle_with_probs(0.44, first_name[0], 0.34, last_name+birth_year, 0.18, 0.05)
        while len(username) < 6: 
            username += str(random.randint(0,9))
        #while len(username) < max(8,len(username)+3):
        #    username += str(random.randint(100,999))
        return username.lower()    
    
    
    #search, find and click method                        
    def find_and_click(self, text, tag, first=True, page=None):
        break_text = ""
        if first:
            break_text = "break;"
        if page==None:
            self.run_script_and_wait(\
                'var all=document.getElementsByTagName("*");var the_button;for(var i=0,max=all.length;i<max;i++){if(all[i].innerText=="'+text+'"&&all[i].tagName=="'+tag+'"){the_button=all[i];'+break_text+'} }the_button.click()',20)
        else:
            x = self.run_script_and_return_given('var all=document.getElementsByTagName("*");var the_button;for(var i=0,max=all.length;i<max;i++){if(all[i].innerText=="'+text+'"&&all[i].tagName=="'+tag+'"){the_button=all[i];'+break_text+'} }the_button.getBoundingClientRect().x', page)
            y = self.run_script_and_return_given('var all=document.getElementsByTagName("*");var the_button;for(var i=0,max=all.length;i<max;i++){if(all[i].innerText=="'+text+'"&&all[i].tagName=="'+tag+'"){the_button=all[i];'+break_text+'} }the_button.getBoundingClientRect().y', page)
            print(">>>>")
            print(x)
            print(y)
            print("<<<<<")
            self.mouse_click_given_page(x+20, y+20, page)
        self.sleep(2)

    def type_original(self, htmlobject, page, text, page_no):
        if page_no == 1:
            self.run_script_and_wait(\
                        ''+ htmlobject +'.focus()',20)
            self.run_script_and_wait(\
                        ''+ htmlobject +'.click()',20)
        else:
            self.run_script_and_return_page_2(\
                        ''+ htmlobject +'.focus()')
            self.run_script_and_return_page_2(\
                        ''+ htmlobject +'.click()')
        self.send_text(page, text)
        self.sleep(1)

    def type(self, htmlobject, page, text, page_no=1):
        exc=None
        for i in range(10):
            try:
                self.type_original(htmlobject,page,text, page_no)
            except Exception as e:
                exc=e
            else:
                return
            self.sleep(1)
        raise(exc)


    def engagement_action(self):
        print("ENGAGEMENT====")
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                        True)

    def login(self, username, password, page):
        pass

    #just login and stay here for a little while
    def maintenance_action(self):
        profile_id = self.get_user_profile_id()
        username, password, email, phone = self.get_credentials("tutanota.com")
        page = self.get_default_page()
        self.login(username, password,page)
        self.sleep(20)
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                        True)

    def handler(self, signum, frame):
        raise Exception("finished")
        
    #def get_random(self,length):
       # letters_and_digits = string.ascii_letters + string.digits
       # result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))   
       # return result_str
        
        
        

    def registration_action(self):
        signal.signal(signal.SIGALRM, self.handler)
        user_profile_obj = self.get_user_profile()
        first_name = user_profile_obj.get_first_name()
        last_name = user_profile_obj.get_last_name()
        gender = user_profile_obj.get_gender()
        birthdate = user_profile_obj.get_birthdate()
        birth_month = str(birthdate[0])
        birth_day = str(birthdate[1])
        birth_year = str(birthdate[2])
        user_profile_id = self.get_user_profile_id()

        
      # selected_username = self.generate_usernames(first_name, last_name, birth_year)
      # selected_password = self.generate_random_valid_password()  

        self.load_website("https://adbtc.top/index/reg")
        page=self.get_default_page()
        self.sleep(5)
        self.type(\
            'document.getElementById("etosovsemnikchemu")',page, #email)
        self.sleep(2)
        self.type(\
            'document.getElementById("password")')
        self.sleep(3)
        self.run_script_and_return(\
            'document.querySelectorAll(\'input[type="checkbox"]\')[1].click()')
        self.run_script_and_return(\
                'document.getElementsByClassName("button-content flex items-center primary plr-button justify-center")[0].click()')
        self.sleep(5)
        self.type(\
            'document.getElementsByClassName("input right")[0]', page, selected_username)
        self.sleep(1)
        self.type(\
            'document.querySelectorAll(\'input[type="password"]\')[0]', page, selected_password)
        self.sleep(1)
        self.type(\
            'document.querySelectorAll(\'input[type="password"]\')[2]', page, selected_password)
        self.sleep(1)
        self.run_script_and_return(\
            'document.getElementsByClassName("icon svg-content-fg")[0].click()')
        self.run_script_and_return(\
            'document.getElementsByClassName("pl content-fg")[0].click()')
        self.sleep(6)

        still_vefifing = self.run_script_and_return(\
            'document.body.innerText.search("Verifying email address ...") != -1')
        while still_vefifing:
            self.sleep(5)
            still_vefifing = self.run_script_and_return(\
                'document.body.innerText.search("Verifying email address ...") != -1')   

        #check for username 
        not_available_username = self.run_script_and_return(\
            'document.body.innerText.search("Email address is not available") != -1')
        while not_available_username:
            self.run_script_and_return(\
                'document.getElementsByClassName("input right")[0].value = ""')
            self.sleep(2)
            selected_username = self.generate_usernames(first_name, last_name, birth_year)
            self.type(\
                'document.getElementsByClassName("input right")[0]', page, selected_username)
            self.sleep(5)
            still_vefifing = self.run_script_and_return(\
                'document.body.innerText.search("Verifying email address ...") != -1')
            while still_vefifing:
                self.sleep(5)
                still_vefifing = self.run_script_and_return(\
                    'document.body.innerText.search("Verifying email address ...") != -1')       
            not_available_username = self.run_script_and_return(\
                'document.body.innerText.search("Email address is not available") != -1'
        #preparing = self.run_script_and_return(\
            #'document.body.innerText.search("Preparing account...") != -1')
        #while preparing:
            #print("paizei sthn preparing")
            #preparing = self.run_script_and_return(\
                #'document.body.innerText.search("Preparing account...") != -1')  
      #abuse = self.run_script_and_return(\
      #        'document.body.innerText.search("Registration is temporarily blocked for your IP address to avoid abuse. Please try again later or use a different internet connection.") != -1')
      #if abuse:
      #     return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
      #            False) 
                  
                  
        captcha_detect = self.run_script_and_return(\
                'document.body.innerText.search("Captcha") != -1') 
        if captcha_detect:
         #self.sleep(60*30)
         #letters = string.ascii_lowercase
         #fvalue= ( ''.join(random.choice(letters) for i in range(12)) )
         #fvalue= (fvalue+".png")
         #self.take_clipscreenshot(fvalue,x=764,y=416,width=400,height=277)
         #print("eimai mesa sthn detect kai h fwto exei onoma "+fvalue)
         #solver = imagecaptcha()
         #solver.set_verbose(1)
         #solver.set_key("b9d24fd762b469d96e20d392e4ed9387")
         #captcha_text = solver.solve_and_return_solution(fvalue)
        if captcha_text != 0:
             print ("captcha text "+captcha_text)
             self.type(\
     'document.getElementsByClassName("input")[3]',page,captcha_text)
             self.sleep(5)
             self.run_script_and_return('document.getElementsByClassName("button-content flex items-center primary plr-button justify-center")[0].click()')
        else:
             print ("task finished with error "+solver.error_code)
             return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
          False)


        self.run_script_and_return(\
            'document.getElementsByClassName("limit-width noselect bg-transparent button-height full-width")[0].click()')
                
        self.sleep(6)
        self.type('document.querySelector("input[type=password]")', page, selected_password)
        self.run_script_and_return(\
            'document.querySelector("input[type=checkbox]").click()')
        self.sleep(2)
        self.run_script_and_return(\
            'document.querySelector(\'button[title="Log in"]\').click()')
        self.sleep(30)
        self.store_credentials("adbtc.com", selected_username, selected_password,)
        self.new_account_to_log(selected_username, selected_password,, "adbtc.top/")
        return bot_core.RegistrationActionInstanceResult(self.get_user_profile_id(),
                    True,
                    "adbtc.top/",
                    selected_username,
                    selected_password)
  
    @classmethod
    def get_associated_domain(cls):
        return 'https://adbtc.top/'           

    @classmethod
    def get_account_domain(cls):
        return 'adbtc.top/'


def get_plugin_class():
    return AdbtcPlugin