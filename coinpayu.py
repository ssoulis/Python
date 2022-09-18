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
import csv
from csv import writer 
import pandas as pd
import os.path
from os import path



class CoinPayUPlugin(plugin_base.BotPluginBase):
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
        #self.load_website('https://coinpayu.com/')
        self.load_website('https://coinpayu.com/dashboard/')
        self.sleep(10)
        need_login = self.run_script_and_return(\
            'document.body.innerText.search("Login to Your Account")!=-1')
        if not need_login:
            return

        self.sleep(5)
        self.run_script_and_return(\
            'document.getElementsByClassName("login-btn nav-scroll")[0].children[0].click()')
        self.sleep(3)
        self.type('document.getElementsByClassName("form-control")[0]', page, email)
        self.sleep(1)
        #back to recaptcha
        try:
            self.run_script_and_return(\
                'document.getElementsByClassName("form-group form-code")[0].children[0].click()')
        except:
            pass
        self.sleep(1)
        self.type('document.getElementsByClassName("form-control")[1]', page, password)

        is_capthca = self.run_script_and_wait_retry(\
            'document.body.innerText.search("Solving is in process...") != -1')
        while is_capthca:
            capcha_solved = self.run_script_and_wait_retry('document.body.innerText.search("Solved") != -1')
            counter = 0
            while not capcha_solved:
                print("captcha solving...")
                self.sleep(15)
                capcha_solved = self.run_script_and_wait_retry(\
                    'document.body.innerText.search("Solved") != -1')
                counter += 1
                if counter > 60:
                    print("captcha took too long.. :(")
                    return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),False)
            is_capthca = self.run_script_and_wait_retry(\
                'document.body.innerText.search("Solving is in process...") != -1')

        self.find_and_click("Login", "BUTTON")
        self.sleep(10)
    
    def changePageAndClickAds(self):
        try:
            change_page_buttons = self.run_script_and_return(\
                'document.getElementsByClassName("coinpayu-pagination")[0].children[0].childElementCount') -1
            for i in range(change_page_buttons-1):
                self.run_script_and_return(\
                    'document.getElementsByClassName("coinpayu-pagination")[0].children[0].children['+str(change_page_buttons)+'].click()')
                for _ in range(14):
                    self.press_button("ArrowUp")
                    self.sleep(0.8)
                self.clickAllAds()
                self.sleep(20) 
        except:
            pass

    def clickAllAds(self, startAt = 0):
        i = startAt
        while i < 10:
        #for i in range(startAt,10):
            print("Trying ad no #" + str(i))
            try:
                already_clicked = self.run_script_and_return(\
                    'document.getElementsByClassName("col-12 text-overflow ags-description pull-left")['+str(i)+'].parentElement.parentElement.parentElement.className.includes("gray-all")')
                if not already_clicked:
                    print("Trying to click it....")
                    x = self.run_script_and_return(\
                        'document.getElementsByClassName("col-12 text-overflow ags-description pull-left")['+str(i)+'].getBoundingClientRect().x')
                    y = self.run_script_and_return(\
                        'document.getElementsByClassName("col-12 text-overflow ags-description pull-left")['+str(i)+'].getBoundingClientRect().y')
                    print("mouse clicked!")
                    self.mouse_click(x+20, y+12)
                else:
                    print("Ad is already clicked")
                    i += 1
                    continue
                if i == 5:
                    for _ in range(14):
                        self.press_button("ArrowDown")
                        self.sleep(0.8)
            except:
                pass
            print("waiting...")
            self.sleep(20)
            isGoogleCapthca = self.run_script_and_return(\
                'document.body.innerText.search("GoogleRecapt") != -1')
            if not isGoogleCapthca:
                self.sleep(random.randint(50,70))

            #captcha check
            isGoogleCapthca = self.run_script_and_return(\
                'document.body.innerText.search("GoogleRecapt") != -1')
            isQbkCapthca = self.run_script_and_return(\
                'document.body.innerText.search("QbkRecaptcha") != -1')
            isHCaptcha = self.run_script_and_return(\
                'document.body.innerText.search("Hcaptcha")  != -1')
            isSolveMedia = self.run_script_and_return(\
                'document.body.innerText.search("SolveMedia")  != -1')

            if isGoogleCapthca or isQbkCapthca or isHCaptcha:
                if isGoogleCapthca:
                    second_tab_text = self.run_script_and_return(\
                        'document.getElementsByClassName("recaptcha-checked")[0].parentElement.children[1].innerText')
                    if "GoogleRecap" in second_tab_text:
                        self.run_script_and_return(\
                            'document.getElementsByClassName("recaptcha-checked")[0].parentElement.children[1].click()')
                        self.sleep(10)
                    self.waitForGoogleCaptha()
            
            if isSolveMedia:
                print("SolveMedia Detected")
                second_tab_text = self.run_script_and_return(\
                        'document.getElementsByClassName("recaptcha-checked")[0].parentElement.children[1].innerText')
                if "SolveMedia" in second_tab_text:
                    self.run_script_and_return(\
                            'document.getElementsByClassName("recaptcha-checked")[0].parentElement.children[1].click()')
                    self.sleep(2)
                    #TODO
                    print("TODO Solve SolveMedia??!!")


            if isHCaptcha:
                print("HCapthca detected!")
                print("waiting for 20 minutes...")
                self.sleep(60*20)        
                #i =- 1
                continue

            # if isSolveMedia:
            #     second_tab_text = self.run_script_and_return(\
            #             'document.getElementsByClassName("form-group form-code")[0].children[1].innerText')
            #     if second_tab_text == "SolveMedia":
            #         self.run_script_and_return(\
            #             'document.getElementsByClassName("form-group form-code")[0].children[1].click()')
            #         self.sleep(10)
            #     print("in SolveMedia..")
            #     #TODO IMPLEMENT ME
            #     self.sleep(60*10)
                    
            ##same for open tab
            tab_page = self.get_last_opened_page()
            isGoogleCapthca = self.run_script_and_return_given(\
                'document.body.innerText.search("GoogleRecapt") != -1', tab_page)
            isQbkCapthca = self.run_script_and_return_given(\
                'document.body.innerText.search("QbkRecaptcha") != -1', tab_page)
            isHCaptcha = self.run_script_and_return_given(\
                'document.body.innerText.search("Hcaptcha")  != -1', tab_page)
            isSolveMedia = self.run_script_and_return_given(\
                'document.body.innerText.search("SolveMedia")  != -1', tab_page)

            if isGoogleCapthca or isQbkCapthca or isHCaptcha:
                if isGoogleCapthca:
                    try:
                        second_tab_text = self.run_script_and_return_given(\
                            'document.getElementsByClassName("recaptcha-checked")[0].parentElement.children[1].innerText', tab_page)
                        if "GoogleRecap" in second_tab_text:
                            self.run_script_and_return_given(\
                                'document.getElementsByClassName("recaptcha-checked")[0].parentElement.children[1].click()', tab_page)
                            self.sleep(10)
                    except:
                        pass
                    self.waitForGoogleCaphcainTab(page=tab_page)          

            if isHCaptcha:
                print("HCapthca detected!")
                print("waiting for 20 minutes...")
                self.sleep(60*20)        
                self.run_script_and_return('window.location.reload();')
                self.sleep(40)
                if i >= 5:
                    for _ in range(14):
                        self.press_button("ArrowDown")
                        self.sleep(0.8)
                i =- 1

            infinite_loading = self.run_script_and_return(\
                'document.getElementsByClassName("loader-inner ball-pulse-sync").length!= 0')
            if infinite_loading:
                return False

            print("closing open tabs...")
            self.close_all_tabs()

            i += 1
            #capthca stuff
            #document.body.innerText.search("Hcaptcha")
            #self.run_script_and_return('location.reload()')

    def maintenance_action(self):
        profile_id = self.get_user_profile_id()
        username, password, _, email = self.get_credentials("coinpayu.com")
        print("--------------------")
        print(username)
        print(password)
        print(email)
        print("--------------------")
        page = self.get_default_page()

        #self.load_website("https://coinpayu.com/")
        #self.sleep(60)
        
        self.login(email, password,page)
        self.sleep(20)

        #create csv file if not exist 
        if_create = path.exists('satoshi_report.csv')
        if if_create == False :
            satoshi_report = pd.DataFrame(columns=['USER ID',"SATOSHI EARNED"])
            satoshi_report.to_csv('satoshi_report.csv', index=False)
            print("'satoshi_report.csv' file created")
        else :
            print("'satoshi_report.csv' file already exists")
      
        #ADDING OR UPDATING CSV FILE             
        k = 0
        p = 0
        index = -1
        self.wait_for_text("Main Balance")
        if_name = self.get_user_profile_id()
        satoshi = self.run_script_and_return(\
            'document.getElementsByClassName("mo mo-main fz-number")[0].innerText')
        data = [{'USER ID': if_name,'SATOSHI EARNED': satoshi}]
        with open("satoshi_report.csv", "rt") as csvfile:
            csvreader = csv.reader(csvfile, delimiter=",")
            for row in csvreader:
                if if_name in row[0]:
                    k = 1
                    p = index 
                    print( if_name , "found in satoshi_report file at row " ,p)
                    print("updating column 'SATOSHI EARNED' for " +if_name)
                else :
                    index+=1
            
                    
        if k == 1 :
            #updating satoshi of user id
            df = pd.read_csv('satoshi_report.csv')
            df.loc[p,'SATOSHI EARNED'] = satoshi
            df.to_csv('satoshi_report.csv', index=False)
            print("Updated column 'SATOSHI EARNED' for " +if_name)
            print("new satoshi balance = " +satoshi)
        else :
            #adding new user id
            df = pd.read_csv("satoshi_report.csv")
            df.loc[len(df.index)]=list(data[0].values())
            df.to_csv('satoshi_report.csv',index=False)
            print("New user id added with their satoshi balance the user id is "+if_name)

        #print("testing...")
        #self.sleep(60*150)

        self.run_script_and_return(\
            'document.getElementsByClassName("nav-item")[4].children[0].click()')

        #simple ads
        self.sleep(3)
        self.run_script_and_return(\
            'document.getElementById("viewads").children[0].children[0].click()')
        self.sleep(9)  
        res = self.clickAllAds()
        if res == False:
            return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                False)

        #Window Ads
        self.run_script_and_return(\
            'document.getElementById("viewads").children[1].children[0].click()')
        self.sleep(20)
        self.clickAllAds()
        self.changePageAndClickAds()
    
        #change page
        self.changePageAndClickAds()

        #Video Ads
        self.run_script_and_return(\
            'document.getElementById("viewads").children[2].children[0].click()')
        self.sleep(10)
        no_of_videos = self.run_script_and_return(\
            'document.getElementsByClassName("videoList-msg-title").length')
        for i in range(no_of_videos):
            self.run_script_and_return(\
                'document.getElementsByClassName("videoList-msg-title")['+str(i)+'].click()')
            self.sleep(20)
            print("clicking")
            video_page = self.get_last_opened_page()
            self.mouse_click_given_page(400,400,video_page) #TODO test that
            self.sleep(random.randint(50,120))
            try:
                self.find_and_click("Visit Website", "BUTTON", page=self.get_last_opened_page())
            except:
                pass
            self.sleep(20)
            self.close_all_tabs()
    
        ###TODO close all tabs

        #TODO capthcas and pless play button


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
       
        # self.load_website("https://sobhog.com/")
        # self.sleep(5)
        # #click the random one
        # self.run_script_and_return('document.querySelectorAll("input[type=submit]")[1].click()')
        # self.sleep(5)
        # selected_email = self.run_script_and_return('document.getElementById("current-id").value')
        proton_username, proton_password , _, _   = self.get_credentials("protonmail.com")
        selected_email = proton_username +  "@protonmail.com"

        print("proton----")
        print(proton_username)
        print(proton_password)
        print("-------")

        selected_username = self.generate_usernames(first_name, last_name, birth_year)
        selected_password = self.generate_random_valid_password()        

        #complete the form
        self.load_website("https://coinpayu.com/")
        self.sleep(10)
        self.find_and_click("Register", "A")
        self.sleep(5)
        page = self.get_default_page()
        self.type('document.getElementsByClassName("form-control")[0]', page, selected_username)
        self.type('document.getElementsByClassName("form-control")[1]', page, selected_email)
        self.type('document.getElementsByClassName("form-control")[2]', page, selected_password)
        self.type('document.getElementsByClassName("form-control")[3]', page, selected_password)
        self.run_script_and_return('document.getElementsByClassName("checkbox icheck-orange")[0].children[0].click()')
        
        #wait for the capthca
        print("waiting for capthca...")
        #TODO logic dor the waiting
        self.sleep(10)
        self.wait_for_capthca()
        self.sleep(5)
        self.find_and_click("Register", "BUTTON")
        self.sleep(3)
        username_exists = self.run_script_and_return(\
            'document.body.innerText.search("The username is already used") != -1')
        if username_exists:
            print("username exists")
            selected_username = self.generate_usernames(first_name, last_name, birth_year)
            selected_username += str(random.randint(10,100))
            self.type('document.getElementsByClassName("form-control")[0]', page, selected_username)
            self.wait_for_capthca()
            self.run_script_and_return('document.getElementsByClassName("checkbox icheck-orange")[0].children[0].click()')
            #if is still not availalalble #TODO 

        email_already_used = self.run_script_and_return(\
            'document.body.innerText.search("The email is already used") != -1')
        if email_already_used:
            print("email used")
            return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                        False)

        #confirm email
        #ip used from other user
        #email doen't come.
        self.open_new_tab()
        self.load_website_on_page2("https://mail.protonmail.com/login")
        self.sleep(20)
        self.run_script_and_return_page_2('document.getElementById("username").value = "'+ proton_username   +'"')
        self.sleep(2)
        self.run_script_and_return_page_2('document.getElementById("password").value = "' +proton_password+'" ')
        self.sleep(2)
        self.run_script_and_return_page_2('document.getElementById("login_btn").click()')
        self.wait_for_text("CoinPayU.com - Please confirm registration")
        #self.sleep(60*20)

        email_here = self.run_script_and_return_page_2(\
            'document.getElementsByClassName("conversation hasLabels")[0].innerText.includes("CoinPayU.com - Please confirm registration")')
        counter = 0       
        while not email_here:
            self.sleep(10)
            email_here = self.run_script_and_return_page_2(\
                        'document.getElementsByClassName("conversation hasLabels")[0].innerText.includes("CoinPayU.com - Please confirm registration")')
            counter += 1
            if counter == 30:
                print("Took too long to receive the mail")
                return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                False)

        self.run_script_and_return_page_2(\
            'document.getElementsByClassName("conversation hasLabels")[0].click()')                        
        self.sleep(5)
        verification_code = self.run_script_and_return_page_2(\
            "document.querySelectorAll('table[role=presentation]')[5].children[1].children[1].innerText.split(" ").slice(-1)[0]")
        verification_code = re.sub("[^0-9]", "", verification_code)
        print("Email Verification Code " + verification_code)
       

        #write back the verification code
        self.type('document.getElementsByClassName("form-control")[0]', page, verification_code)
    
        self.find_and_click("Confirm", "BUTTON")
        self.sleep(20)

        self.store_credentials("coinpayu.com", selected_username, selected_password,
                                email=selected_email)
        self.new_account_to_log(selected_username, selected_password, "coinpayu.com")

        #completed = self.run_script_and_return(\
        #    'document.body.innerText.search("Withdraw") != -1')

        #if completed:
           
        return bot_core.RegistrationActionInstanceResult(self.get_user_profile_id(),
                                                    True,
                                                    "coinpayu.com",
                                                    selected_username,
                                                    selected_password)

        #return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
        #                            True)
 
    @classmethod
    def get_associated_domain(cls):
        return 'http://coinpayu.com/'           

    @classmethod
    def get_account_domain(cls):
        return 'coinpayu.com'

    # @classmethod
    # def get_registration_dependency_domains(cls):
    #     return ["protonmail.com"]

    @classmethod
    def requires_no_web_security(cls):
        return True

    @classmethod
    def requires_social_proxy(cls):
        return False

    def protonmail_registration(self):
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

        #self.load_website("https://sobhog.com/")
        #self.sleep(5)
        #click the random one
        #self.run_script_and_return('document.querySelectorAll("input[type=submit]")[1].click()')
        #self.sleep(5)
        #selected_email = self.run_script_and_return('document.getElementById("current-id").value')
        
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
        #self.sleep(60*20)

        captcha_iframe = 'document.getElementById("captchaFrame").children[1].contentWindow.'
        
        flag =self.run_script_and_return(\
            'document.body.innerText.search("CAPTCHA") != -1') 
            
        if flag == True :
           in_captcha1 = self.run_script_and_return(\
            captcha_iframe + 'document.body.innerText.search("Solving is in process...") != -1')
           in_captcha2 = self.run_script_and_return(\
            captcha_iframe + 'document.body.innerText.search("Solved") != -1')
           in_captcha = in_captcha1 or in_captcha2

           print(in_captcha1)
           print(in_captcha2)

           is_capcha_active = self.run_script_and_return(\
            captcha_iframe + 'document.body.innerText.search("Solving is in process...") != -1')
        
           while is_capcha_active:
             in_captcha = True
             capcha_solved = self.run_script_and_return(captcha_iframe +   'document.body.innerText.search("Solved") != -1')
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
captcha_iframe + 'document.body.innerText.search("Solving is in process...") != -1')
            #self.sleep(60*20)
             self.run_script_and_return(\
            'document.getElementsByClassName("pm_button primary large humanVerification-completeSetup-create")[0].click()')
            
        #self.sleep(60*20)
        page = self.get_default_page()
        #a = 1
        #if a==1 :
        if flag == False :
            self.sleep(2)
            self.run_script_and_return('document.getElementById("id-signup-radio-sms").click()')
            print("changing to ru")
           # req = requests.get(\
           # 'https://sms-activate.ru/stubs/handler_api.php?             #api_key=4b6520de7602181de853201229dA7c6d&action=getNumber&service=dp&forward=$forward&operator=$operator&ref=$ref&country=12&phoneException=$phoneException')
            print("requesting number...")
            self.sleep(5)
            res = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=4b6520de7602181de853201229dA7c6d&action=getNumber&service=dp&country=0')
            #requests.post(\
            #'https://sms-activate.ru/stubs/handler_api.php?#api_key=4b6520de7602181de853201229dA7c6d&action=setStatus&status=1&id=my_id')
            data1=res.text
            print(data1)
            data = data1.split(":")
            my_id = data[1]
            #my_id = int(my_id1)
            number = data[2]
            self.sleep(5)
            print("my id is :"+my_id)
            self.sleep(5)
            print("my number is :"+number)
            #self.sleep(60*20)
            self.run_script_and_return('document.getElementsByClassName("selected-flag")[0].click()')
            self.sleep(2)
            self.run_script_and_return('document.getElementsByClassName("country")[178].click()')
            self.sleep(5)
            self.type('document.getElementsByName("smsVerification")[0]',page,number)
            self.sleep(5)
            #self.find_and_click('Send','button')
            self.run_script_and_return('document.getElementsByClassName("pm_button primary codeVerificator-btn-send")[0].click()')
            #requests.post(\
            #'https://sms-activate.ru/stubs/handler_api.php?#api_key=4b6520de7602181de853201229dA7c6d&action=setStatus&status=1&id='+my_id)
            self.sleep(5)
            print("requesting code with sms...")
            code = requests.get(\
            'https://sms-activate.ru/stubs/handler_api.php?api_key=4b6520de7602181de853201229dA7c6d&action=getStatus&id='+my_id)
            my_code = code.text
            print("code status is :"+my_code)
            waiting = 0
            while my_code == "STATUS_WAIT_CODE" and waiting<=600 :
               print("waiting for code...")
               code = requests.get(\
              'https://sms-activate.ru/stubs/handler_api.php?   api_key=4b6520de7602181de853201229dA7c6d&action=getStatus&id='+my_id)
               my_code = code.text
               print("code status is still STATUS_WAIT_CODE")
               waiting +=1     
            if my_code == "STATUS_CANCEL" or waiting>=600 :
                 requests.post(\
                'https://sms-activate.ru/stubs/handler_api.php?api_key=4b6520de7602181de853201229dA7c6d&action=setStatus&status=8&id='+my_id)
                 print(my_code)
                 print("reporting number and exiting...")                                    
                 return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                            False)
            elif my_code == "STATUS_WAIT_RESEND" :
                 print("resending code...")
                 self.run_script_and_return('document.getElementsByClassName("pm_button link codeVerificator-new-code-button")[0].click()')
                 requests.post(\
                'https://sms-activate.ru/stubs/handler_api.php?api_key=4b6520de7602181de853201229dA7c6d&action=setStatus&status=6&id='+my_id)
                 code = requests.get(\
              'https://sms-activate.ru/stubs/handler_api.php?   api_key=4b6520de7602181de853201229dA7c6d&action=getStatus&id='+my_id)
                 code_split = my_code.split(":")
                 my_status = code_split[0]
                 my_code1 = code_split[1]
                 print("my code status is :" +my_code)
                 text1 = requests.get(\
            'https://sms-activate.ru/stubs/handler_api.php?api_key=4b6520de7602181de853201229dA7c6d&action=getFullSms&id='+my_id)
                 my_text = text1.text
                 print("code is :"+my_text)
                 self.type('document.getElementById("codeValue")',page,my_code1)
                 self.sleep(5)
                 self.run_script_and_return('document.getElementsByClassName("pm_button primary large humanVerification-completeSetup-create")[0].click()')
            else :  
                 
                 text1 = requests.get(\
                 'https://sms-activate.ru/stubs/handler_api.php?api_key=4b6520de7602181de853201229dA7c6d&action=getFullSms&id='+my_id)
                 my_text = text1.text
                 print("code is :"+my_text)
                 code_split = my_code.split(":")
                 my_status = code_split[0]
                 my_code1 = code_split[1]
                 #self.requests.post(\
             #  'https://sms-activate.ru/stubs/handler_api.php?#api_key=4b6520de7602181de853201229dA7c6d&action=setStatus&status=1&id=my_id')
                 self.type('document.getElementById("codeValue")',page,my_code1)
                 self.sleep(5)
                 #self.find_and_click('Complete setup','BUTTON')
                 self.run_script_and_return('document.getElementsByClassName("pm_button primary large humanVerification-completeSetup-create")[0].click()')
                 self.sleep(5)
            requests.post(\
           'https://sms-activate.ru/stubs/handler_api.php?api_key=4b6520de7602181de853201229dA7c6d&action=setStatus&status=6&id='+my_id)
            print("verification completed")
          
            

             
            




        #use email in this case
      #if in_captcha == False:
      #    try:
      #        self.run_script_and_return(\
      #            'document.getElementsByClassName("humanVerification-block-email")[0].children[0].click()')
      #    except:
      #        pass
      #    self.type('document.getElementById("emailVerification")', page, selected_email)
      #    self.find_and_click("SEND", "BUTTON")
      #    self.sleep(10)
      #    mail_send = self.run_script_and_return(\
      #        'document.body.innerText.search("Verification code sent") != -1')
      #    if not mail_send:
      #        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
      #                        False)
      #    self.sleep(10)
      #    
      #    self.load_website_on_page2("https://sobhog.com/mailbox/" + selected_email)
      #    self.sleep(5)
      #    email_received1  = self.run_script_and_return_page_2(\
      #        'document.getElementById("mails").children[0].innerText != "Your emails will display here"')
      #    email_received2 = self.run_script_and_return_page_2(\
      #        'document.getElementById("mails").children[0].innerText != "No mails found"')
      #    email_received = email_received1 and email_received2
      #    counter = 0
      #    while not email_received:
      #        self.sleep(10)
      #        print("waiting for email...")
      #        email_received1  = self.run_script_and_return_page_2(\
      #            'document.getElementById("mails").children[0].innerText != "Your emails will display here"')
      #        email_received2 = self.run_script_and_return_page_2(\
      #            'document.getElementById("mails").children[0].innerText != "No mails found"')
      #        email_received = email_received1 and email_received2
      #        counter += 1
      #        if counter > 60:
      #            print("email took too long... :(")
      #            return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
      #                        False)
      #    
      #    #email is here
      #    self.run_script_and_return_page_2(\
      #        'document.getElementById("mails").children[0].click()')
      #    self.sleep(5)
      #    verification_code = self.run_script_and_return_page_2(\
      #        'document.getElementsByClassName("mail-download")[0].nextElementSibling.children[0].children[1].innerText')
      #    print("Email Verification Code " + verification_code)       
      #    self.type('document.getElementById("codeValue")', page, verification_code)

        #self.run_script_and_return(\
            #'document.getElementsByClassName("pm_button primary large humanVerification-#completeSetup-create")[0].click()')

        self.sleep(25)

        try:
            self.find_and_click("FINISH", "BUTTON")
        except:
            pass

        self.store_credentials("protonmail.com", selected_username, selected_password,
                            email="")
        self.new_account_to_log(selected_username, selected_password, "protonmail.com")

        return bot_core.RegistrationActionInstanceResult(self.get_user_profile_id(),
                                                    True,
                                                    "protonmail.com",
                                                    selected_username,
                                                    selected_password)
 


def get_plugin_class():
    return CoinPayUPlugin

