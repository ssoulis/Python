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


class TutanotaPlugin(plugin_base.BotPluginBase):
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
 
     
     selected_username = self.generate_usernames(first_name, last_name, birth_year)
     selected_password = self.generate_random_valid_password()  
    
     #self.sleep(60*10)
     self.load_website("https://mail.tutanota.com/signup")
     page = self.get_default_page()
     self.sleep(5)
     self.run_script_and_return('document.getElementsByClassName("button-content flex items-center login plr-button justify-center")[0].click()')
     self.sleep(5)
     self.run_script_and_return('document.getElementsByClassName("icon svg-content-fg")[0].click()')
     self.run_script_and_return('document.getElementsByClassName("icon svg-content-fg")[1].click()')
     self.run_script_and_return('document.getElementsByClassName("limit-width noselect bg-transparent button-height")[0].click()')
     self.run_script_and_return('document.getElementsByClassName("input right")[0].click()')
     self.type('document.getElementsByClassName("input right")[0]', page, selected_username)
     self.run_script_and_return('document.getElementsByClassName("abs")[1].click()')
     self.type('document.getElementsByClassName("abs")[1]', page, selected_password)
     self.run_script_and_return('document.getElementsByClassName("flex flex-column")[3].click()')
     self.type('document.getElementsByClassName("flex flex-column")[3]', page, selected_password)
     self.sleep(5)
     self.run_script_and_return('document.getElementsByClassName("icon svg-content-fg")[0].click()')
     self.run_script_and_return('document.getElementsByClassName("icon svg-content-fg")[1].click()')
     self.sleep(3)
     self.run_script_and_return('document.getElementsByClassName("limit-width noselect bg-transparent button-height full-width")[0].click()')
     self.run_script_and_return('document.getElementsByClassName("limit-width noselect bg-transparent button-width-fixed button-height")[1].click()')
     self.sleep(1)  
     #edw yparxei mia mikrh periptwsh gia captcha me mia eikona oxi ths google synh8ws mia eikona me ena roloi me deiktes pou deixnoun thn wra kai prepei na 
     #grapseis ti wra leei to roloi
     #ayto ginete prin paroume ton recovery password code
     recovery=self.run_script_and_return('document.getElementsByClassName("text-break monospace selectable flex flex-wrap border pt pb plr").innerText.replaceAll()')
     self.run_script_and_return('document.getElementsByClassName("button-content flex items-center login plr-button justify-center")[0].click()')
               
     
        #ama den dexete username
     used_username=self.run_script_and_return('document.body.innerText.search("Email address is not available.") !=-1')
     while used_username:
        selected_username = self.generate_usernames(first_name, last_name, birth_year)
        self.run_script_and_return('document.getElementsByClassName("button-content flex items-center primary plr-button justify-center")[0].click()')
        self.run_script_and_return('document.getElementsByClassName("input right")[0].value = ""')
        self.type('document.getElementsByClassName("input right")[0]', page, selected_username)
        self.run_script_and_return('document.getElementsByClassName("limit-width noselect bg-transparent button-height full-width")[0].click()')
        self.sleep(5)
        used_username=self.run_script_and_return('document.body.innerText.search("Email address is not available") != -1')
        recovery=self.run_script_and_return('document.getElementsByClassName("text-break monospace selectable flex flex-wrap border pt pb plr").innerText.replaceAll()')
        self.run_script_and_return('document.getElementsByClassName("button-content flex items-center login plr-button justify-center")[0].click()')
        self.sleep(30)
      # self.type('document.getElementsByClassName("limit-width noselect bg-transparent button-height full-width")[0].click()')
     self.store_credentials("tutanota.com", selected_username, selected_password, phone_number, email="")
     self.new_account_to_log(selected_username, selected_password,recovery, "tutanota.com")
     return bot_core.RegistrationActionInstanceResult(self.get_user_profile_id(), True,"tutanota.com",selected_username,selected_password,phone_number)
  
    @classmethod
    def get_associated_domain(cls):
        return 'http://tutanota.com/'           

    @classmethod
    def get_account_domain(cls):
        return 'tutanota.com'


def get_plugin_class():
    return TutanotaPlugin