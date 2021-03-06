# !/usr/bin/env python
# coding = 'utf-8'


"""
-------------------------环   境--------------------------------
windows == windows 7 64x
appium == 1.15.1
android_studio == 191.5977832 (adb == 29.0.6-6198805)
python == 3.7.6
jdk == 1.8.0_131
appium_python_client == 0.50
mumu模拟器 == 1.0.0 (andriod == 6.0.1, port 7555)


-------------------------主要按钮-------------------------------
resource-id	com.tbc.android.defaults:id/uc_help_activity_go_btn
登陆页面
id:
com.tbc.android.defaults:id/uc_login_corpcode_edittext  send_key
com.tbc.android.defaults:id/uc_login_username_edittext  send_key
com.tbc.android.defaults:id/uc_login_password_edittext  send_key
按钮:
com.tbc.android.defaults:id/login_login_btn   click

广告:
com.tbc.android.defaults:id/ivMineSignInPopupClose   click
com.tbc.android.defaults:id/cbxIndexAdvertPopupTips   click
com.tbc.android.defaults:id/ivIndexAdvertPopupClose   click

accessibility id	学习地图

elementId	55e04e7e-68f5-4cfa-b975-236c298eaee1    text	2020年一季度机关中台

分阶段：
resource-id	com.tbc.android.defaults:id/map_level_ll  list　　　find_element_by_id
elementId	6af9c9ea-be1e-47e1-a024-e50106a77cb4  返回键
详细页
resource-id	com.tbc.android.defaults:id/els_expandable_child_chapter_layout   list

学课页
resource-id	com.tbc.android.defaults:id/els_detail_study_course_study_layout    课程学习栏
resource-id com.tbc.android.defaults:id/els_detail_study_course_study_status_img   打勾（未完成没有）
elementId	24691931-9a25-4d18-9591-7dd37cabe4ba resource-id	com.tbc.android.defaults:id/els_expandable_child_chapter_name   点击进入学习 list 多个录像逐一学习，每半分钟判断有没有勾
resource-id	com.tbc.android.defaults:id/els_detail_back_img  回退
resource-id	com.tbc.android.defaults:id/els_expandable_child_chapter_status 锁 未开


def swipeUp(driver, t=500, n=1):
    # 向上滑动屏幕
    l = driver.get_window_size()
    x1 = l['width'] * 0.5 # x坐标
    y1 = l['height'] * 0.75 # 起始y坐标
    y2 = l['height'] * 0.25 # 终点y坐标
    for i in range(n):
        driver.swipe(x1, y1, x1, y2, t)


def swipeDown(driver, t=500, n=1):
    '# 向下滑动屏幕
    l = driver.get_window_size()
    x1 = l['width'] * 0.5 # x坐标
    y1 = l['height'] * 0.25 # 起始y坐标
    y2 = l['height'] * 0.75 # 终点y坐标
    for i in range(n):
        driver.swipe(x1, y1, x1, y2,t)


def swipRight(driver, t=500, n=1):
    # 向右滑动屏幕
    l = driver.get_window_size()
    x1 = l['width'] * 0.25
    y1 = l['height'] * 0.5
    x2 = l['width'] * 0.75
    for i in range(n):
        driver.swipe(x1, y1, x2, y1, t)
"""

from appium import webdriver
from time import sleep


def swipeUp(driver, t=500, n=1):
    # 向上滑动屏幕
    l = driver.get_window_size()
    x1 = l['width'] * 0.5  # x坐标
    y1 = l['height'] * 0.75  # 起始y坐标
    y2 = l['height'] * 0.25  # 终点y坐标
    for i in range(n):
        driver.swipe(x1, y1, x1, y2, t)


def swipLeft(driver, t=500, n=1):
    '''向左滑动屏幕'''
    l = driver.get_window_size()
    x1 = l['width'] * 0.75
    y1 = l['height'] * 0.5
    x2 = l['width'] * 0.25
    for i in range(n):
        driver.swipe(x1, y1, x2, y1, t)


def try_click(driver, button):
    try:
        driver.find_element_by_id(button).click()
    except:
        pass


def try_return(driver, element):
    try:
        driver.find_element_by_id(element)
    except:
        return 0
    else:
        return 1


# 学课
def virtual_learn(driver, lesson_this, part_this, part_number, stages_number, learn_time=0):
    sleep(2)
    if try_return(part_this, 'com.tbc.android.defaults:id/els_detail_study_course_study_status_img'):
        return  # 完成情况1
    if try_return(part_this, 'com.tbc.android.defaults:id/els_expandable_child_chapter_status'):
        return  # 完成情况2
    sleep(30)
    learn_time += 30
    print('┃┣已学习 ' + str(learn_time) + '秒')
    # driver.find_element_by_id('com.tbc.android.defaults:id/els_detail_back_img').click()  # 课程页返回
    driver.back()
    sleep(2)
    if stages_number == 3:
        pass
    else:
        lesson_this.click()
    sleep(2)
    if try_return(lesson_this, 'com.tbc.android.defaults:id/els_expandable_child_chapter_status'):
        return
    try:
        part_this_new = driver.find_elements_by_id('com.tbc.android.defaults:id/els_expandable_child_chapter_layout')[part_number]
    except:
        swipeUp(driver_zsq)
        part_this_new = driver.find_elements_by_id('com.tbc.android.defaults:id/els_expandable_child_chapter_layout')[
            part_number]
    part_this_new.click()
    virtual_learn(driver, lesson_this, part_this_new, part_number, stages_number, learn_time)
    return


def virtual_learn_shizheng(driver, lesson_this, part_number, stages_number, parts_of_part_number, learn_time=0):
    sleep(30)
    learn_time += 30
    print('┃┣已学习 ' + str(learn_time) + '秒')
    driver.back()
    sleep(2)
    if try_return(lesson_this, 'com.tbc.android.defaults:id/els_expandable_child_chapter_status'):
        return
    try:
        part_this_new = driver.find_elements_by_id('com.tbc.android.defaults:id/els_expandable_child_chapter_layout')[part_number]
    except:
        swipeUp(driver_zsq)
        part_this_new = driver.find_elements_by_id('com.tbc.android.defaults:id/els_expandable_child_chapter_layout')[
            part_number]
    part_this_new.click()
    parts_of_part = driver_zsq.find_elements_by_id('com.tbc.android.defaults:id/els_child_alisco_layout')
    parts_of_part_status = driver_zsq.find_elements_by_id('com.tbc.android.defaults:id/els_child_alisco_selectstatus')
    if parts_of_part_status[parts_of_part_number] == 'iVBORw0KGgoAAAANSUhEUgAAABoAAAAQCAIAAACHs/j/AAAAA3NCSVQICAjb4U/gAAABWklEQVQ4\njWP8//8/A17w/9PH/29eMzAwMIqIMvLx41fMgtuY/39vXf+5bP7fq5cZIFYyMjJr67JHJTKraTIw\nMmLVxIjddX///Fw6/9fGNVj1sPmHsEcnMjBjcQoTVnfhMYuBgeHXxjU/l85nwOYOLMb9vXUd2SxW\ndx9mPSNME//euk6UcT+XzUfmsrp4cNW2sOeVooUXmjLsxv3/9PHv1cuoYowMTMxs9i7c/TOZpGQQ\nnrh6+f+nj4SMe/Maa6AwMDAwycpz9UxlMbWEKf0PSUD4jKMQoEc2o4goAyMjVgf+e/zwe1fTv2dP\nYEoZGUVECbiOkY+fWVsXVew/w7+/vw7u+VqYjjCLgYFZWxczk2BJiuxRid+qCuHc33t2/Hz+9O+l\n85jKMPViyxX///9cPAdPMmaAZIzYFMyshi0qGBnZoxPZ/EPwmRWdiDXb4sizDNQtApCNJaWAAgCC\n1Z+5RvcjXgAAAABJRU5ErkJggg==\n':
        return
    parts_of_part(parts_of_part_number).click()
    virtual_learn_shizheng(driver, lesson_this, part_number, stages_number, parts_of_part_number, learn_time)
    return


desired_caps = {'device': 'SELENDROID',
                'platformName': 'Android',  # 平台名称
                'platformVersion': '6.0.1',  # 系统版本号
                'deviceName': '127.0.0.1:7555',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
                "newCommandTimeout": 120,
                'appPackage': 'com.tbc.android.defaults',  # apk的包名
                'appActivity': 'com.tbc.android.defaults.MainActivity'  # activity 名称
                }

if __name__ == '__main__':
    driver_zsq = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)  # 连接Appium
    driver_zsq.implicitly_wait(4)

    swipLeft(driver_zsq)
    swipLeft(driver_zsq)
    swipLeft(driver_zsq)

    driver_zsq.find_element_by_id('com.tbc.android.defaults:id/uc_help_activity_go_btn').click()
    driver_zsq.find_element_by_id('com.tbc.android.defaults:id/uc_login_corpcode_edittext').send_keys('单位代码')
    driver_zsq.find_element_by_id('com.tbc.android.defaults:id/uc_login_username_edittext').send_keys('账号')
    driver_zsq.find_element_by_id('com.tbc.android.defaults:id/uc_login_password_edittext').send_keys('密码')
    driver_zsq.find_element_by_id('com.tbc.android.defaults:id/login_login_btn').click()

    sleep(1)
    try_click(driver_zsq, 'com.tbc.android.defaults:id/ivMineSignInPopupClose')
    try_click(driver_zsq, 'com.tbc.android.defaults:id/cbxIndexAdvertPopupTips')
    try_click(driver_zsq, 'com.tbc.android.defaults:id/ivIndexAdvertPopupClose')

    sleep(1)
    driver_zsq.find_element_by_xpath('//android.view.View[@content-desc="学习地图"]').click()
    # 季度页面
    driver_zsq.find_element_by_id('com.tbc.android.defaults:id/map_index_list_item_title').click()  # 季度表
    # 季度分阶段页面
    stages = driver_zsq.find_elements_by_xpath(
        '//androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout')
    for i in range(len(stages)):  # 季度分阶段页
        stages = driver_zsq.find_elements_by_xpath(
            '//androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout')
        stages[i].click()
        try:
            lessons_learned = driver_zsq.find_elements_by_id(
                'com.tbc.android.defaults:id/els_expandable_child_chapter_status')
        except:
            pass
        else:
            lessons = driver_zsq.find_elements_by_id('com.tbc.android.defaults:id/els_expandable_child_chapter_layout')
            if len(lessons_learned) == len(lessons):
                driver_zsq.find_element_by_id('com.tbc.android.defaults:id/return_btn').click()  # 季度分阶段页返回
                sleep(1)
                continue
        lessons = driver_zsq.find_elements_by_id(
            'com.tbc.android.defaults:id/els_expandable_child_chapter_layout')  # 课程列表
        for each_lesson in lessons:
            each_lesson_name = each_lesson.find_element_by_id(
                'com.tbc.android.defaults:id/els_expandable_child_chapter_name').text
            # 判断课程是否学完
            try:
                driver_zsq.find_element_by_id('com.tbc.android.defaults:id/els_detail_study_course_study_status_img')
            except:
                pass
            else:
                print('┗' + each_lesson_name + ':课程完成')
                driver_zsq.find_element_by_id('com.tbc.android.defaults:id/els_detail_back_img').click()  # 课程页返回
                sleep(1)
                continue
            each_lesson.click()
            print('┏' + each_lesson_name + ':开始课程')
            sleep(1)
            if i == 3:
                parts = driver_zsq.find_elements_by_id('com.tbc.android.defaults:id/els_child_alisco_layout')
            elif i == 4:
                pass
            else:
                parts = driver_zsq.find_elements_by_id(
                    'com.tbc.android.defaults:id/els_expandable_child_chapter_layout')  # 课程章节
            for j in range(len(parts)):
                if i == 3:
                    parts = driver_zsq.find_elements_by_id('com.tbc.android.defaults:id/els_child_alisco_layout')
                else:
                    parts = driver_zsq.find_elements_by_id(
                        'com.tbc.android.defaults:id/els_expandable_child_chapter_layout')  # 课程章节
                # 文化课阶段没有打勾，定期返回
                part_name = parts[j].find_element_by_id(
                    'com.tbc.android.defaults:id/els_expandable_child_chapter_name').text
                print('┣┳' + part_name + ':正在学习')
                try:
                    parts[j].click()
                except:
                    swipeUp(driver_zsq)
                    parts[j].click()
                if i != 4:
                    virtual_learn(driver_zsq, each_lesson, parts[j], j, i)
                else:
                    parts_of_part = driver_zsq.find_elements_by_id('com.tbc.android.defaults:id/els_child_alisco_layout')
                    parts_of_part_status = driver_zsq.find_elements_by_id(
                        'com.tbc.android.defaults:id/els_child_alisco_selectstatus')
                    for k in range(len(parts_of_part)):
                        virtual_learn_shizheng(driver_zsq, each_lesson, j, i, k)
                print('┃┗' + part_name + ':章节完成')
                # 判断有没有课程按钮，没有则返回上一层
                sleep(1)
            print('┗' + each_lesson_name + ':学课已完成')
            driver_zsq.find_element_by_id('com.tbc.android.defaults:id/els_detail_back_img').click()  # 课程页返回
            sleep(1)
        driver_zsq.find_element_by_id('com.tbc.android.defaults:id/return_btn').click()  # 季度分阶段页返回
        sleep(1)
    driver_zsq.quit()

# com.tbc.android.defaults:id/els_child_alisco_layout
# com.tbc.android.defaults:id/els_detail_alivcplayer
# com.tbc.android.defaults:id/els_child_alisco_layout 4
# com.tbc.android.defaults:id/els_child_alisco_selectstatus 勾
# 判断阶段标题，"企业文化专题"，"时政知识专题"开头的课程

