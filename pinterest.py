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

PROFILE_SERVICE_ENDPOINT = 'http://'+profile_hostname+':'+profile_port
IMAGES_ENDPOINT = 'http://'+profile_hostname+':'+images_port

class PinterestPlugin(plugin_base.BotPluginBase):
    def view_action(self):
        url=self.get_action_info().get_resource_id()
        self.load_website(url)
        print(url)
        delay=self.get_action_info().get_action_params_dict().get('duration_limit_secs')
        self.sleep(delay)
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                     True)

    def view_engage_action(self):
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                     True)

    def like_action(self):
        url = self.get_action_info().get_resource_id()
        self.load_website(url)
        try:
            self.run_script_and_wait(\
                'document.querySelector(\'button[aria-label="reaction"]\').click()',20)
        except:
            self.run_script_and_return(\
                'document.querySelector("button[data-test-id=\'PinBetterSaveButton\'").click()')
        self.sleep(3)
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                     True)

    def dislike_action(self):
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                     True)

    def share_action(self):
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                     True)

    def download_pin_image(self, gender="M", birth_year="1999"):
        gen = "1" if (gender == "M" or gender ==
            "male" or gender == "Male") else "0"
        age = str(2020 - int(birth_year))
        politics = str(random.randint(0, 1))
        education = str(random.randint(0, 5))
        cover = str(1)
        quantity = str(random.randint(4, 10))

        gaming_photos_prob = random.random()
        twitch_no = "1"
        url = PROFILE_SERVICE_ENDPOINT+'/interests?age='+age+'&gender='+gen+'&politics=' + \
            politics+'&education='+education+'&cover='+cover+'&quantity='+quantity + \
            "&twitch="+twitch_no
        print(url)
        r = requests.get(url).content
        my_json = r.decode('utf8').replace("'", '')
        print(my_json)
        data = json.loads(my_json)
        tries = 5
        while data['status'] == 'failed':
            r = requests.get(url).content
            my_json = r.decode('utf8').replace("'", '')
            data = json.loads(my_json)
            if tries == 0:
                break
            tries -= 1
        if data['status'] == "no_photo":
            return
        profile_image_url = data['image']
        # download profile image
        pic = requests.get(profile_image_url).content
        profile_image_path = "/home/"+getpass.getuser()+"/temp/" + \
            data['image'].split('/')[2] + ".jpg"
        with open(profile_image_path, "wb") as f:
            f.write(pic)
        print(profile_image_path)
        return profile_image_path

    def problem_solver(self):
        print("starting problem solver")
        user_profile_obj = self.get_user_profile()
        self.load_website("https://pinterest.com/")
        self.sleep(15)
        login_text = self.run_script_and_return(\
                'document.body.innerText.search("Log in") != -1',20)
        signup_text = self.run_script_and_return(\
                'document.body.innerText.search("Sign up") != -1',20)

        logged_out = login_text and signup_text
        print("logged out: " + str(logged_out))
        if logged_out:
            self.login()
        gender = user_profile_obj.get_gender()
        in_welcome = self.run_script_and_return(\
            'document.body.innerText.search("Welcome to Pinterest") != -1')
        in_login_welcome = self.run_script_and_return(\
            'document.body.innerText.search("Find new ideas to try") != -1')
        if in_welcome and not in_login_welcome:
            self.add_interests(gender)

        last_step = self.run_script_and_return(\
            'document.body.innerText.search("Last step! Tell us what you\'re interested in") != -1')
        if last_step:
            print("LAST STEP..")
            interests_len = self.run_script_and_return(\
                'document.getElementsByClassName("interestCardWrapper").length')
            interests_quan = random.randint(5, min(8, interests_len-1))
            for _ in range(interests_quan):
                the_choice = str(random.randint(0,min(8, interests_len-1)))
                self.run_script_and_wait(\
                    'document.getElementsByClassName("interestCardWrapper")['+the_choice+'].click()',20)
            self.sleep(2)
            self.run_script_and_wait(\
                'document.querySelector("button[type=submit]").click()',20)
            self.sleep(5)


    def upload_pin(self):
        self.load_website("https://pinterest.com/pin-builder/")
        profile_image_path = self.download_pin_image()
        fileInput = self.querySelector('input[type="file"]')
        self.uploadFile(fileInput, profile_image_path)
        self.sleep(20)
        self.run_script_and_wait(\
            'document.querySelector("button[data-test-id=\'board-dropdown-select-button\']").click()',20)
        self.sleep(1)
        num_of_choices = self.run_script_and_return(\
            'document.getElementsByClassName("tBJ dyH iFc yTZ pBj DrD IZT mWe z-6").length')
        choice = str(random.randint(0,num_of_choices-1))
        self.run_script_and_wait(\
            'document.getElementsByClassName("tBJ dyH iFc yTZ pBj DrD IZT mWe z-6")['+choice+'].click()')
        self.sleep(1)
        is_secret = self.run_script_and_return(\
            'document.getElementsByClassName("jPl kVc Hsu XiG dD6 BsF")[0] != undefined')
        if is_secret:
            self.run_script_and_wait(\
                'document.getElementById("secret").click()',20)
        self.sleep(1)
        self.run_script_and_wait(\
            'document.querySelector(\'button[type="submit"]\').click()', 20)
        self.sleep(5)

    def random_follow(self):
        print("==RANDOM FOLLOW ACTION ===")
        self.load_website("https://pinterest.com/")
        self.sleep(3)
        no_of_photos = self.run_script_and_return(\
            'document.getElementsByClassName("hCL kVc L4E MIw").length')
        choice = str(random.randint(1,no_of_photos-1))
        self.run_script_and_wait(\
            'document.getElementsByClassName("hCL kVc L4E MIw")['+choice+'].click()',20)
        self.sleep(3)
        try:
            self.run_script_and_wait(\
                'document.getElementsByClassName("Lfz zI7 iyn Hsu")[0].click()',20)
        except:
            pass

    def follow_action(self):
        url = self.get_action_info().get_resource_id()
        print(url)
        self.problem_solver()

        if url == '' or url == None:
            self.random_follow()
            return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                True)
        else:
            self.load_website(url)
            try:
                self.run_script_and_wait(\
                    'var all=document.getElementsByTagName("*");var the_button;for(var i=0,max=all.length;i<max;i++){if(all[i].innerText=="Follow"&&all[i].tagName=="DIV"){the_button=all[i];} } the_button.parentElement.click()',20)
                self.sleep(3)
                #self.run_script_and_wait(\
                #    'document.getElementsByClassName("RCK Hsu USg Vxj aZc Zr3 hA- GmH adn Il7 Jrn hNT iyn BG7 gn8 L4E kVc")[0].click()',20)
            except:
                pass
                #self.run_script_and_wait(\
                #    'document.getElementsByClassName("RCK Hsu USg adn CCY czT F10 xD4 fZz hUC Il7 Jrn hNT BG7 NTm KhY")[0].click()',20)

        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                     True)
    def post_action(self):
        self.upload_pin()
        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                     True)


    def maintenance_action(self):
        profile_id = self.get_user_profile_id()
        maintenance_status = plugin_base.MaintenanceStatus(profile_id, "pinterest.com")
        maintenance_status.load()
        requires_maintanance = maintenance_status.requires_maitenance()
        print("REQUIRES MAINTENANCE: " + str(requires_maintanance))
        print("LAST MAINTENANCE: " + str(maintenance_status.get_latest_maitenance_timestamp()))
        if requires_maintanance: 
            self.problem_solver()
            self.upload_pin()
            self.random_follow()
            self.random_follow()
            self.random_follow()
            maintenance_status.set_maintenance_timestamp()
            maintenance_status.store()
            return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                                    True)
        else:
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
        return username.lower()    

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

    def download_profile_image(self, gender, birth_year):
        gen = "1" if (gender == "M" or gender ==
            "male" or gender == "Male") else "0"
        age = str(2020 - int(birth_year))
        politics = str(random.randint(0, 1))
        education = str(random.randint(0, 5))
        cover = str(1)
        quantity = str(random.randint(4, 10))

        #40% to get twitch like photos
        gaming_photos_prob = random.random()
        if gaming_photos_prob < 0.40:
            twitch_no = "1"
        else:
            twitch_no = "0"
        url = PROFILE_SERVICE_ENDPOINT+'/interests?age='+age+'&gender='+gen+'&politics=' + \
            politics+'&education='+education+'&cover='+cover+'&quantity='+quantity + \
            "&twitch="+twitch_no
        print(url)
        r = requests.get(url).content
        my_json = r.decode('utf8').replace("'", '')
        print(my_json)
        data = json.loads(my_json)
        tries = 5
        while data['status'] == 'failed':
            r = requests.get(url).content
            my_json = r.decode('utf8').replace("'", '')
            data = json.loads(my_json)
            if tries == 0:
                break
            tries -= 1
        if data['status'] == "no_photo":
            return
        if 'profile_image_provider' in data['image']:
            profile_image_url = IMAGES_ENDPOINT + \
                    '/' + data['image'].split('/')[2]
        else:
            profile_image_url = data['image']
        # download profile image
        pic = requests.get(profile_image_url).content
        profile_image_path = "/home/"+getpass.getuser()+"/temp/" + \
            data['image'].split('/')[2]
        with open(profile_image_path, "wb") as f:
            f.write(pic)
        return profile_image_path
   
    
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

    def login(self):
        page = self.get_default_page()
        html = self.get_default_page_html()

        n_username, n_password, n_email, n_phone = self.get_credentials("pinterest.com")
        fb_username, fb_password, fb_email, fb_phone = self.get_credentials("facebook.com")
        go_username, go_password, go_email, go_phone = self.get_credentials("google.com")
        
        print(n_username)
        print(n_email)
        print(n_password)
        print("======")
        print(fb_username)

        if n_email != None:
            try:
                self.run_script_and_wait(\
                    'document.getElementsByClassName("RCK Hsu USg F10 xD4 fZz hUC GmH adn a_A gpV hNT iyn BG7 NTm KhY")[0].click()',20)
            except:
                self.run_script_and_wait(\
                    'document.getElementsByClassName("RCK Hsu USg F10 xD4 fZz hUC GmH adn Il7 Jrn hNT iyn BG7 gn8 L4E kVc")[0].click()', 20)
            self.sleep(2)
            self.type('document.getElementsByName("id")[0]', page, n_email)
            self.sleep(1)
            self.type('document.getElementsByName("password")[0]', page, n_password)
            self.sleep(1)
            self.run_script_and_wait(\
                'document.getElementsByClassName("red SignupButton active")[0].click()',20)
            self.sleep(5)
        if fb_username != None:
            self.run_script_and_wait(\
                'document.getElementsByClassName("_8jan")[0].click()',20)

    def find_str(self, s, char):
        index = 0

        if char in s:
            c = char[0]
            for ch in s:
                if ch == c:
                    if s[index:index+len(char)] == char:
                        return index

                index += 1

        return -1

    def click_element(self, element_selector):
        x = self.run_script_and_return(element_selector+".getBoundingClientRect().x")
        y = self.run_script_and_return(element_selector+".getBoundingClientRect().y")
        self.mouse_click(x+2, y+2)
        self.sleep(random.random())

    def add_interests(self, gender):
        print("starting interests...")
        self.run_script_and_wait(\
            'document.querySelector("button[aria-label=Next]").click()',20)
        self.wait_for_text("How do you identify?")
        #0 female, 1 Male
        gen = "1" if (gender == "M" or gender ==
            "male" or gender == "Male") else "0"
        self.run_script_and_wait(\
            'document.getElementsByName("genderOptions")['+gen+'].click()',20)
        self.wait_for_text("Pick your language")
        try:
            self.press_button("Enter")
            self.run_script_and_wait(\
                'document.getElementsByClassName("RCK Hsu USg F10 xD4 fZz hUC GmH adn Il7 Jrn hNT iyn BG7 gn8 L4E kVc")[0].click()',20)
        except:
            try:
                #new
                self.run_script_and_wait(\
                    'document.getElementsByClassName("RCK Hsu USg adn CCY czT F10 xD4 fZz hUC Il7 Jrn hNT BG7 gn8 L4E kVc")[0].click()',20)
            except:
                pass


        self.sleep(30)
        print("before interest len")

        #interests_len = self.run_script_and_return(\
        #    'document.getElementsByClassName("interestCardWrapper").length')
        interests_len = self.run_script_and_return(\
            'document.getElementsByClassName("BXM BsF zI7 iyn Hsu").length')
        print("inrerests len: " + str(interests_len))

        if interests_len == 0:
            return

        interests_quan = random.randint(5, min(8, interests_len-1))            
        for _ in range(interests_quan):
            the_choice = str(random.randint(0,min(8, interests_len-1)))
            self.run_script_and_wait(\
                'document.getElementsByClassName("BXM BsF zI7 iyn Hsu")['+the_choice+'].click()',20)
            self.sleep(1)
        self.sleep(2)

        try:
            #next button
            self.run_script_and_wait(\
                'document.querySelector("button[type=submit]").click()',20)
            interests_len = self.run_script_and_return(\
                'document.getElementsByClassName("interestCardWrapper").length')
            interests_quan = random.randint(5, min(8, interests_len-1))
            for _ in range(interests_quan):
                the_choice = str(random.randint(0,min(8, interests_len-1)))
                self.run_script_and_wait(\
                    'document.getElementsByClassName("interestCardWrapper")['+the_choice+'].click()',20)
            self.sleep(2)
        except:
            pass

        #done button
        try:
            self.run_script_and_wait(\
                'document.querySelector("button[type=submit]").click()',20)
        except:
            pass

    def add_profile_image(self, gender, birth_year):
        self.load_website("https://pinterest.com/settings")        
        self.run_script_and_wait(\
            'document.getElementsByClassName("tBJ dyH iFc yTZ pBj tg7 mWe")[4].click()',20)
        self.sleep(5)
        fileInput = self.querySelector('input[type="file"]')
        profile_image_path = self.download_profile_image(gender, birth_year)
        self.uploadFile(fileInput, profile_image_path)
        self.sleep(25)

    def registration_action(self):
        domain = "pinterest.com"
        user_profile_obj = self.get_user_profile()
        #first_name = user_profile_obj.get_first_name()
        #last_name = user_profile_obj.get_last_name()
        gender = user_profile_obj.get_gender()
        birthdate = user_profile_obj.get_birthdate()
        #birth_month = str(birthdate[0])
        #birth_day = str(birthdate[1])
        birth_year = str(birthdate[2])
        user_profile_id = self.get_user_profile_id()

        fb_username, fb_password, fb_email, fb_phone = self.get_credentials("facebook.com")
        go_username, go_password, go_email, go_phone = self.get_credentials("google.com")

        goto_choice = "native"

        if fb_username != None:
            username = fb_username
            password = fb_password
            phone = fb_phone
            goto_choice = "facebook"
        
        if go_username != None:
            username = go_username
            password = go_password
            phone = go_phone 
            goto_choice = "google"

        print(go_username)
        print(go_password)
            
        print("GOTO CHOICE: " + goto_choice )

        if fb_username == None and go_username == None:
            password = self.generate_random_valid_password()
            username = ""
        #print(username)
        #print(password)
        #print(phone)

        try:
            self.load_website("https://temp-mail.org/", timeout = 20000)
        except:
            print("taking too long to load") 

        self.sleep(6)
        counter =  0
        email = self.run_script_and_return(\
            'document.getElementById("mail").value')
        #end page loading when email is ready
        #(temp-mail something take a while - or folever - to load)
        while (email == "" or email == "Loading.." or email == "Loading."):
            self.sleep(6)
            counter += 1
            email = self.run_script_and_return(\
                'document.getElementById("mail").value')
            if counter > 30:
                break
        
        print(email)
        if email == "" or email == "Loading.." or email == "Loading.":
            print("can't get email from temp-mail")
            return bot_core.RegistrationActionInstanceResult(user_profile_id,
                                            False,
                                            domain,
                                            username,
                                            password)

        self.load_website("https://pinterest.com/")
        self.load_website("https://pinterest.com/")
        page = self.get_default_page()


        print("sign up button and facebook login...")
        self.find_and_click('Sign up', "DIV", page=page)
        self.sleep(2)
        if goto_choice == "facebook":
            self.find_and_click('Continue with Facebook', 'SPAN')
        elif goto_choice == "google":
            self.find_and_click('Continue with Google', "SPAN")
        self.sleep(10)
 
        with_email = False

        try:
            if goto_choice == "facebook":
                print("clicking facebook name button(on popup)")
                popup = self.get_last_opened_page()
                self.run_script_and_return_given(\
                    'document.getElementsByClassName("_42ft _4jy0 layerConfirm _1fm0 _51_n autofocus _4jy3 _4jy1 selected _51sy")[0].click()', popup)
                #TODO fb login if it's logged out
                self.sleep(10)
            elif goto_choice == "google":
                print("google==")
                popup = self.get_last_opened_page()
                #test this..-->
                self.run_script_and_return_given(\
                    'document.getElementsByClassName("lCoei YZVTmd SmR8")[0].click()',popup)
                self.sleep(10)

                self.run_script_and_return_given(\
                    'document.getElementsByName("password")[0].focus()', popup)
                self.sleep(1)
                self.run_script_and_return_given(\
                    'document.getElementsByName("password")[0].click()', popup)

                print(go_password)
                self.send_text(popup, go_password)
                self.sleep(1)
                self.find_and_click('Next', 'SPAN')

                print("GOOGLE WAITING,,")
                self.sleep(60*10)
                # popup = self.get_last_opened_page()
                # self.run_script_and_return_given(\
                #     'document.getElementsByName("identifier")[0].focus()', popup)
                # self.run_script_and_return_given(\
                #     'document.getElementsByName("identifier")[0].click()', popup)
                # self.type(\
                #     'document.getElementsByName("identifier")[0]', popup, go_username)
                # self.sleep(2)
                # self.find_and_click("Next", "SPAN")
                # self.sleep(7)
                # self.run_script_and_return_given(\
                #     'document.getElementsByName("password")[0].focus()', popup)      
                # self.run_script_and_return_given(\
                #     'document.getElementsByName("password")[0].click()', popup)       
                # self.type(\
                #     'document.getElementsByName("password")[0]', popup, go_password)
                # self.find_and_click("Next", "SPAN")    
                # print("GOOGLE WAITING,,")
                # self.sleep(60*10)

                #TODO η περίπτωση όπου είναι οκ το τηλ αλλιώς exception
            elif goto_choice == "native":
                raise Exception
        except:
            print("===problem with facebook")
            print("trying with simple email ====")
            self.type('document.getElementsByName("id")[0]', page, email)
            self.type('document.getElementsByName("password")[0]', page, password)
            self.type('document.getElementsByName("age")[0]', page, str(2020-int(birth_year)))
            self.sleep(2)
            self.run_script_and_wait(\
                'document.getElementsByClassName("red SignupButton active")[0].click()', 20)
            with_email = True 

        try:
            if with_email == False:
                print("Continue to facebook - on pinterest")
                self.run_script_and_wait(\
                    'document.getElementsByClassName("_8jan")[0].click()',20)
                self.sleep(10)
        except:
            pass 
        
        try:
            if with_email == False:
                print("adding email....")
                self.type('document.getElementById("email")', page, email)
                self.sleep(1)
                self.find_and_click("Continue", "DIV")
                self.sleep(1)
        except:
            pass
        try:
            if with_email == False:
                print("continue...")
                self.find_and_click("Continue", "DIV")
        except:
            pass
        
        print("checking for interest page")
        if not self.wait_for_text("Welcome to Pinterest"):
            return bot_core.RegistrationActionInstanceResult(user_profile_id,
                                            False,
                                            domain,
                                            username,
                                            password)

        self.store_credentials(domain, username, password, email=email)
        self.sleep(15)
        self.add_interests(gender)
        self.sleep(10)
        self.add_profile_image(gender, birth_year)
        self.store_credentials(domain, username, password, email=email)
        self.new_account_to_log(username, password, domain)
        return bot_core.RegistrationActionInstanceResult(user_profile_id,
                                                    True,
                                                    domain,
                                                    username,
                                                    password)


            
    def engagement_action(self):
        self.load_website("https://www.pinterest.com")
        self.problem_solver()
        self.problem_solver_on = False       
        url = self.get_action_info().get_resource_id()
        #self.load_website(url)
        self.follow_action()
        
        num_of_posts = self.run_script_and_return(\
            'document.querySelectorAll("div[data-grid-item=\'true\']").length')

        post_urls = []
        for i in range(0, num_of_posts):
            pin_id = self.run_script_and_return(\
                'document.querySelectorAll("div[data-grid-item=\'true\']")['+str(i)+'].children[0].children[0].getAttribute("data-test-pin-id")')
            pin_url = "https://gr.pinterest.com/pin/" + pin_id
            post_urls.append(pin_url)

        print(post_urls)

        propabilities = []
        for i in range(len(post_urls)):
            prob = round(-0.11*i+1,2)
            if prob < 0: 
                prob = 0 
            propabilities.append(prob)        

        new_post_urls = []
        for i in range(len(propabilities)):
            if random.random() < propabilities[i]:
                new_post_urls.append(post_urls[i])

 
        post_urls = new_post_urls
        print(post_urls)       

        for url in post_urls:       
            self.get_action_info().set_resource_id(url)
            if random.random() < 0.9:
                self.like_action()


        return bot_core.StandardActionInstanceResult(self.get_user_profile_id(),
                                True)


    @classmethod
    def get_account_domain(cls):
        return 'pinterest.com'

    @classmethod
    def get_registration_dependency_domains(cls):
        return ["facebook.com", None]

    @classmethod
    def requires_sms_verification(cls):
        return False

def get_plugin_class():
    return PinterestPlugin
