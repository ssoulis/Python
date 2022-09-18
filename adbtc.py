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
import re

class AdbtcPlugin(plugin_base.BotPluginBase):
    def view_action(self):
        url=self.get_action_info().get_resource_id()
        self.load_website(url)
        print(url)
        delay=self.get_action_info().get_action_params_dict().get('duration_limit_secs')
        if delay == None:
            delay = random.randint(10,50)
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
        return l3[:20]

    def generate_usernames(self, first_name, last_name,  birth_year ):
        options = [1, 2, 3, 4, 5, 6, 7]
        weights = [0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14]
        choice = choices(options, weights)[0]

        if random.randint(0,1) == 1:
            birth_year = birth_year[2:]

        if choice == 1:
            username = self.shuffle_with_probs(0.06, first_name, 0.22, birth_year, 0, 0.35)
        elif choice == 2:
            username = self.shuffle_with_probs(0, first_name, 0.41, "", 0.07, 0.35)
        elif choice == 3:
            username = self.shuffle_with_probs(0, last_name, 0.3, "", 0.08, 0.45)
        elif choice == 4:
            username = self.shuffle_with_probs(0.44, first_name, 0.34, last_name, 0.18, 0.55)
        elif choice == 5:
            username = self.shuffle_with_probs(0.06, first_name[0], 0.22, last_name, 0, 0.45)
        elif choice == 6:
            username = self.shuffle_with_probs(0.44, first_name, 0.34, last_name[0], 0.18, 0.45)
        elif choice == 7:
            username = self.shuffle_with_probs(0.44, first_name[0], 0.34, last_name+birth_year, 0.18, 0.45)
        while len(username) < 6: 
            username += str(random.randint(0,9))
        #while len(username) < max(8,len(username)+3):
        #    username += str(random.randint(100,999))
        username = username[:11]
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

    def waitForGoogleCaptha(self):
        is_capthca = self.run_script_and_return(\
            'document.body.innerText.search("Solving is in process...") != -1')
        while is_capthca:
            capcha_solved = self.run_script_and_return('document.body.innerText.search("Solved") != -1')
            counter = 0
            while not capcha_solved:
                print("captcha solving...")
                self.sleep(15)
                capcha_solved = self.run_script_and_return(\
                    'document.body.innerText.search("Solved") != -1')
                counter += 1
                if counter > 60:
                    print("captcha took too long.. :(")
                    return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),False)
            is_capthca = self.run_script_and_return(\
                'document.body.innerText.search("Solving is in process...") != -1')

    def waitForGoogleCaphcainTab(self, page):
        is_capthca = self.run_script_and_return_given(\
            'document.body.innerText.search("Solving is in process...") != -1', page)
        while is_capthca:
            capcha_solved = self.run_script_and_return_given(\
                'document.body.innerText.search("Solved") != -1', page)
            counter = 0
            while not capcha_solved:
                print("captcha solving...")
                self.sleep(15)
                capcha_solved = self.run_script_and_return_given(\
                    'document.body.innerText.search("Solved") != -1', page)
                counter += 1
                if counter > 60:
                    print("captcha took too long.. :(")
                    return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),False)
            is_capthca = self.run_script_and_return_given(\
                'document.body.innerText.search("Solving is in process...") != -1', page)    

    def login(self, email, password, page):
        pass        


    def maintenance_action(self):
        profile_id = self.get_user_profile_id()
        username, password, _, email = self.get_credentials("adbtc.top")
        print("--------------------")
        print(username)
        print(password)
        print(email)
        print("--------------------")
        page = self.get_default_page()

        self.login(email, password,page)
        self.sleep(20)
        
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                        True)

    def handler(self, signum, frame):
        raise Exception("finished")

    def wait_for_capthca(self):
        is_capthca = True
        counter = 0
        is_capthca = self.run_script_and_return(\
            'document.body.innerText.search("Solving is in process...") != -1')
        while is_capthca:
            capcha_solved = self.run_script_and_return('document.body.innerText.search("Solved") != -1')
            counter = 0
            while not capcha_solved:
                print("captcha solving...")
                self.sleep(15)
                capcha_solved = self.run_script_and_return(\
                    'document.body.innerText.search("Solved") != -1')
                counter += 1
                if counter > 60:
                    print("captcha took too long.. :(")
                    return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),False)
            is_capthca = self.run_script_and_return(\
                'document.body.innerText.search("Solving is in process...") != -1')

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

        proton_username, proton_password , _, _   = self.get_credentials("protonmail.com")
        if proton_username == None:
            self.protonmail_registration()
       

        proton_username, proton_password , _, _   = self.get_credentials("protonmail.com")
        selected_email = proton_username +  "@protonmail.com"

        print("proton----")
        print(proton_username)
        print(proton_password)
        print("-------")

        selected_username = self.generate_usernames(first_name, last_name, birth_year)
        selected_password = self.generate_random_valid_password()        

        #complete the form
        self.load_website("https://adbtc.top/index/reg")
        page=self.get_default_page()
        user_password= self.generate_random_valid_password()
        self.type('document.getElementById("etosovsemnikchemu")',page,selected_email)
        self.type('document.getElementById("password")',page,user_password)
      # captcha_detect = self.run_script_and_return(\
      # 'document.body.innerText.search("Ι") != -1')
      # if captcha_detect: 
              #wait for the capthca
        print("waiting for capthca...")
        #TODO logic dor the waiting
        self.sleep(10)
        self.wait_for_capthca()
        self.sleep(5)
        #sign up button
        self.run_script_and_return(\
   'document.getElementsByClassName(" btn light-blue darken-4")[0].click()')
        self.sleep(5)
       
        

        #TODO check username existance 

        #TODO confirm
        #click confirm button
        self.run_script_and_return(\
    'document.getElementsByClassName("btn")[0].click()')
        self(5)

      
        #confirm email
        self.open_new_tab()
        self.load_website_on_page2("https://mail.protonmail.com/login")
        self.sleep(20)
        self.run_script_and_return_page_2('document.getElementById("username").value = "'+ proton_username   +'"')
        self.sleep(2)
        self.run_script_and_return_page_2('document.getElementById("password").value = "' +proton_password+'" ')
        self.sleep(2)
        self.run_script_and_return_page_2('document.getElementById("login_btn").click()')
        self.sleep(30)
        self.run_script_and_return_page_2('document.getElementsByClassName("navigationItem-item ptDnd-dropzone-container")[5].click()')
        self.sleep(2)
        email_here = self.run_script_and_return_page_2(\
             'document.getElementsByClassName("conversation hasLabels")[0].innerText.includes("Bitcoin advertising adBTC.top")')
        counter = 0       
        while not email_here:
             self.sleep(10)
             email_here = self.run_script_and_return_page_2(\
                         'document.getElementsByClassName("conversation hasLabels")[0].innerText.includes("Bitcoin advertising adBTC.top")')
             counter += 1
             if counter == 30:
                 print("Took too long to receive the mail")
                 return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                 False)

        #clicks first mail
        self.run_script_and_return_page_2(\
             'document.getElementsByClassName("conversation hasLabels")[0].click()')                        
        self.sleep(5)

        #verification  with click in link
        self.run_script_and_return_page_2(\
        'document.getElementsByClassName("bodyDecrypted email message-body-container")[0].children[2].click()')
        self.sleep(5)
        self.run_script_and_return_page_2(\
        'document.getElementsByClassName("pm_button primary modal-footer-button")[0].click()')
        self.sleep(60*10)
        #verification with code

        #verification_code = self.run_script_and_return_page_2(\
        #    "document.querySelectorAll('table[role=presentation]')[5].children[1].children[1].innerText.split(" ").slice(-1)[0]")
        # verification_code = re.sub("[^0-9]", "", verification_code)
        # print("Email Verification Code " + verification_code)
       

        #write back the verification code TODO 
        #self.type('document.getElementsByClassName("form-control")[0]', page, verification_code)
    
        #self.find_and_click("Confirm", "BUTTON")
        #self.sleep(20)


        self.store_credentials("abbtc.top", selected_username, selected_password,
                                email=selected_email)
        self.new_account_to_log(selected_username, selected_password, "adbtc.top")
           
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                    True)
 
    @classmethod
    def get_associated_domain(cls):
        return 'http://adbtc.top/'           

    @classmethod
    def get_account_domain(cls):
        return 'adbtc.top'

    @classmethod
    def requires_no_web_security(cls):
        return True

    @classmethod
    def requires_social_proxy(cls):
        return False

    def protonmail_registration(self):
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

        iframe = 'document.getElementsByClassName("pm_panel wide signUpProcess-step-1 signupUserForm-container")[0].children[1].children[0].children[1].children[2].children[0].children[1].children[0].contentWindow.'
        iframe2 = 'document.getElementsByClassName("pm_panel wide signUpProcess-step-1 signupUserForm-container")[0].children[1].children[1].children[0].children[2].children[1].children[0].contentWindow.'

        #complete the form
        self.load_website("https://mail.protonmail.com/create/new?language=en")
        self.sleep(20)
        page = self.get_default_page()
        self.type(iframe + 'document.getElementById("username")', page, selected_username)
        self.type('document.getElementById("password")', page, selected_password)
        self.type('document.getElementById("passwordc")', page, selected_password)
        self.run_script_and_return(iframe2 + 'document.getElementsByName("submitBtn")[0].click()')
        self.sleep(10)

        used_username = self.run_script_and_return(iframe + 'document.body.innerText.search("Username already used") != -1')
        while used_username:
            selected_username = self.generate_usernames(first_name, last_name, birth_year)
            self.run_script_and_return(iframe + 'document.getElementById("username").value = ""')
            self.type(iframe + 'document.getElementById("username")', page, selected_username)
            self.run_script_and_return(iframe2 + 'document.getElementsByName("submitBtn")[0].click()')
            self.sleep(10)
            used_username = self.run_script_and_return(iframe + 'document.body.innerText.search("Username already used") != -1')

        self.run_script_and_return('document.getElementById("confirmModalBtn").click()')
        self.sleep(30)

        captcha_iframe = 'document.getElementById("captchaFrame").children[1].contentWindow.'

        in_captcha1 = self.run_script_and_return(\
            captcha_iframe + 'document.body.innerText.search("Solving is in process...") != -1')
        in_captcha2 = self.run_script_and_return(\
            captcha_iframe + 'document.body.innerText.search("Solved") != -1')

        print(in_captcha1)
        print(in_captcha2)

        in_captcha = in_captcha1 or in_captcha2

        is_capcha_active = self.run_script_and_return(\
            captcha_iframe + 'document.body.innerText.search("Solving is in process...") != -1')

        while is_capcha_active:
            in_captcha = True
            capcha_solved = self.run_script_and_return(captcha_iframe + 'document.body.innerText.search("Solved") != -1')
            counter = 0
            while not capcha_solved:
                print("captcha solving...")
                self.sleep(15)
                capcha_solved = self.run_script_and_return(\
                    captcha_iframe + 'document.body.innerText.search("Solved") != -1')
                counter += 1
                if counter > 60:
                    print("captcha took too long.. :(")
                    return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),False)
            is_capcha_active = self.run_script_and_return(\
                captcha_iframe +'document.body.innerText.search("Solving is in process...") != -1')

        self.run_script_and_return(\
            'document.getElementsByClassName("pm_button primary large humanVerification-completeSetup-create")[0].click()')

        self.sleep(25)

        try:
            self.find_and_click("FINISH", "BUTTON")
        except:
            pass

        self.store_credentials("protonmail.com", selected_username, selected_password,
                            email="")
        self.new_account_to_log(selected_username, selected_password, "protonmail.com")


def get_plugin_class():
    return AdbtcPlugin

