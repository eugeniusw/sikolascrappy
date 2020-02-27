"""
Author: eugene
Provided because of flawed sikola system!
"""

from bs4 import BeautifulSoup
import requests

session = requests.Session()

print("========= REQUEST SIKOLA LOGIN PAGE >")
BASE_URL = "https://sikola.unhas.ac.id"
login_url = "https://sikola.unhas.ac.id/index.php"
result = session.get(login_url)
html = BeautifulSoup(result.content, 'html.parser')
print("========= WELCOME TO SIKOLA LOGIN PAGE >")
print("========= INSERT YOUR USERNAME >")
username = input()
print("========= INSERT YOUR PASSWORD >")
password = input()

print("========= LOGIN IN >")
payload = {
    "login": username,
    "password": password,
    "_qf__form-login": ""
}
result = session.post(
    login_url,
    data = payload,
    headers = dict(referer=login_url)
)

login = None
try:
    html = BeautifulSoup(result.content, 'html.parser')
    username = html.select(".username-movil")[0].get_text()
    print("========= LOGIN SUCCESS >")
    print("HELLO, ", username)
    login = 1
except Exception as err:
    print("========= LOGIN FAILED >")
    print("RESPONSE CODE:", result.status_code)
    print("RESPONSE MESSAGE:", html.select(".alert")[0].get_text())
    print("DETAILS:", err)

def search_courses(course_name=""):
    mata_kuliah_semester = BASE_URL + "/main/auth/courses.php?action=display_sessions&category_code=&hidden_links=&pageCurrent=1&pageLength=12"
    result = session.get(mata_kuliah_semester)
    html = BeautifulSoup(result.content, 'html.parser')

    pagination = list(html.select(".pagination")[0].children)
    last_page = int(pagination[len(pagination)-1].get_text())

    find_ref = None
    current_page = None

    for i in range(1, last_page+1):
        mata_kuliah_semester = BASE_URL + "/main/auth/courses.php?action=display_sessions&category_code=&hidden_links=&pageCurrent={}&pageLength=12".format(i)
        result = session.get(mata_kuliah_semester)
        html = BeautifulSoup(result.content, 'html.parser')

        content = list(html.find(id="cm-content"))
        container_courses = list(list(list(content[1].children)[15].children)[1].children)[1]

        for ref in container_courses.select('.title'):
            title = ref.find('a')['title']
            if course_name.lower() in title.lower():
                find_ref = ref
                current_page = i
                break

    return find_ref, current_page

if login:
    print("========= INPUT COURSE NAME >")
    course_name = input()
    print("========= PLEASE WAIT... >")
    ref, current_page = search_courses(course_name)
    if ref:
        print("========= BERHASIL MENEMUKAN MATA KULIAH >")
        print("Nama:", ref.find('a')['title'])
        print("Halaman:", current_page)
        url = BASE_URL + "/main/auth/courses.php?action=display_sessions&category_code=&hidden_links=&pageCurrent={}&pageLength=12".format(current_page)
        print("Url:", url)
    else:
        print("========= MATA KULIAH TIDAK DITEMUKAN >")
        print("Nama:", course_name)
