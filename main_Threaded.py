try:
    import random, string, time, os, socket, threading
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import NoSuchElementException
    from msedge.selenium_tools import Edge, EdgeOptions
except Exception:
    import random, string, time, os, socket, threading
    print("-Required packages not installed, installing now...")
    os.system("pip install selenium")
    os.system("pip install msedge-selenium-tools")
    time.sleep(1)
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import NoSuchElementException
    from msedge.selenium_tools import Edge, EdgeOptions

# ///////////////////////////////////////
#     Browser Driver Name/Path Here:
webdriver_location="MicrosoftWebDriver.exe"
# ///////////////////////////////////////

bt=input("Browser [E=Edge;C=Chrome]: ")
qp=input("Quiz Pin: ")
nb=input("Number of bots per thread: ")
th=input("Number of threads: ")

try:
    host=socket.gethostbyname("quizizz.com")
    before=time.perf_counter()
    time.sleep(0.3)
    s=socket.create_connection((host, 80), 2)
    after=time.perf_counter()
    pingms=after-before
    pingms=round(pingms, 2)+1
except:
    pingms=2

print("-Calculated action delay: "+str(pingms))

def JoinThread():
    global webdriver_location
    global bt
    if bt.lower() == "c":
        ### .add_argument('headless')
        options=webdriver.ChromeOptions()
        options.use_chromium=True
        options.binary_location=r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        browser=webdriver.Chrome(options=options,executable_path=webdriver_location)
    else:
        options=EdgeOptions()
        options.use_chromium=True
        options.binary_location=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
        browser=Edge(options=options,executable_path=webdriver_location)
    for i in range(int(nb)):
        try:
            browser.get("https://quizizz.com/join")
            time.sleep(pingms)
            search=browser.find_element_by_class_name("check-room-input")
            search.send_keys(qp)
            search.send_keys(Keys.RETURN)
            print("-Joined Game")
            time.sleep(pingms)
            if browser.find_elements_by_css_selector('.secondary-button.start-over'):
                g=browser.find_elements_by_css_selector('.secondary-button.start-over')
                print("-Start-Over button found")
                g[0].click()
            time.sleep(0.5)
            print("-Entering name option")
            search=browser.find_element_by_class_name("enter-name-field")
            time.sleep((pingms/2))
            search.send_keys(Keys.CONTROL+"A")
            search.send_keys(''.join(random.choice(string.ascii_letters) for _ in range(10)))
            search.send_keys(Keys.RETURN)
        except (Exception,NoSuchElementException):
            print("-Failed Join")
        finally:
            time.sleep(pingms)
        browser.close()

for i in range(int(th)):
    jointhread=threading.Thread(target=JoinThread)
    jointhread.start()
