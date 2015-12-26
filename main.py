# -*- coding: utf-8 -*-
__author__ = 'ihey'

import urllib2
import cookielib
import urllib
import bs4
import os
from os.path import basename
from urlparse import urlsplit


cookie = cookielib.CookieJar()
handler=urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode({
            'userid': 'xu-wang11',
            'userpass': '#wangxu1993'})
loginUrl = 'https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp'
result = opener.open(loginUrl, postdata)
gradeUrl = 'http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp?typepage=2'
result = opener.open(gradeUrl)
content = result.read()
html = bs4.BeautifulSoup(content,  "html.parser")
courses = []
def url2name(url):
    return basename(urlsplit(url)[2])

def download(url, path, localFileName = None):
    try:
        localName = url2name(url)
        req = urllib2.Request(url)
        r = opener.open(url)
        if r.info().has_key('Content-Disposition'):
            # If the response has Content-Disposition, we take file name from it
            localName = r.info()['Content-Disposition'].split('filename=')[1]
            if localName[0] == '"' or localName[0] == "'":
                localName = localName[1:-1]
        elif r.url != url:
            # if we were redirected, the real file name we take from the final URL
            localName = url2name(r.url)
        if localFileName:
            # we can force to save the file as specified name
            localName = localFileName
        localName = localName.decode('gb2312')
        f = open(path + localName, 'wb')
        f.write(r.read())
        f.close()
    except Exception, e:
        print(str(e))


rootDir = "E:\\courses"
if not os.path.isdir(rootDir):
    os.mkdir(rootDir)
Status = True
for link in html.find_all('a'):
    course_url = link.get('href')
    if course_url.startswith('/MultiLanguage/lesson/student/course_locate.jsp'):
        course_name = link.get_text().strip()
        print course_url
        l = course_url.find('=')
        course_id = course_url[l+1:]
        print course_id
        course_name = course_name.replace(" ", "_")
        r = course_name.rfind('(')
        course_name = course_name[0:r]
        r = course_name.rfind('(')
        course_name = course_name[0:r]
        print course_name
        stop = u"科技英语阅读"
        if not (Status is False or (Status is True and course_name == stop)):
            continue
        Status = False
        course_dir = rootDir + "\\" + course_name
        if not os.path.isdir(course_dir):
            os.mkdir(course_dir)
        course_ware_url = "http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/download.jsp?course_id=" + course_id
        #open course_ware_url
        course_ware_content = opener.open(course_ware_url)
        course_ware_html = bs4.BeautifulSoup(course_ware_content, "html.parser")
        for material_link in course_ware_html.find_all('a'):
            material_url = material_link.get('href')

            if material_url.startswith('/uploadFile/downloadFile_student.jsp'):
                material_text = material_link.get_text()
                material_path = course_dir + "\\" + material_text.strip()
                #urllib.urlretrieve("http://learn.tsinghua.edu.cn" + material_url, material_path)
                download("http://learn.tsinghua.edu.cn" + material_url, course_dir + "\\")
                print material_url
                print material_path


