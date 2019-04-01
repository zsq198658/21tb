# -*- encoding='utf-8'

from selenium import webdriver
from time import sleep
import sys
import pandas as pd
from os import system, getcwd


def kill_process():
    print('正在清理进程')
    if system('tasklist | find "firefox.exe"') == 0:
        system('taskkill /F /T /IM firefox.exe')
    print('清理完成\n')


# 登录操作
def login(web, username, password):
    web.find_element_by_name("loginName").clear()
    web.find_element_by_name("loginName").send_keys(username)
    web.find_element_by_name("swInput").clear()
    web.find_element_by_name("swInput").send_keys(password)
    web.find_element_by_css_selector("button").click()
    sleep(2)
    try:
        web.find_element_by_css_selector("button").click()
    except:
        pass
    else:
        print('\n用户名密码错误.')
        kill_process()
        system('pause')
        sys.exit()


# 清理页面
def clear_page(web):
    if web.find_elements_by_class_name('btn-primary'):
        web.find_elements_by_class_name('btn-primary')[0].click()
    else:
        pass
    sleep(1)
    try:
        web.find_element_by_xpath("//span/a[@title='关闭']")
    except:
        pass
    else:
        web.find_element_by_xpath("//span/a[@title='关闭']").click()
    sleep(1)
    web.find_element_by_xpath('//span[@guid="new_messages"]').click()
    sleep(1)


# 学习课程名称
def subject_name():
    mypath = getcwd()
    input_xlsx = pd.read_excel(mypath + '\\input.xlsx', sheet_name='Sheet1', header=0)
    username = input_xlsx.values[0, 1]
    password = input_xlsx.values[0, 3]
    type_subject = input_xlsx.values[1, 2]
    year = str(input_xlsx.values[2, 2])
    quarter = input_xlsx.values[3, 2]
    subjects_name = year + '年' + quarter + type_subject
    return username, password, subjects_name


# 找到课程列表栏目框
def find_learn_list_page(web, sub_name):
    try:
        web.find_element_by_xpath("//div[@title='我的学习']").click()
    except:
        print('打开我的学习超时，将关闭程序')
        kill_process()
        system('pause')
        sys.exit()
    sleep(1)
    try:
        web.find_element_by_xpath("//div[@title='学习地图']").click()
    except:
        print('打开学习地图超时，将关闭程序')
        kill_process()
        system('pause')
        sys.exit()
    sleep(1)
    iframe = web.find_element_by_xpath('//iframe[@class="tbc-window-iframe"]')
    try:
        web.switch_to.frame(iframe)
    except:
        print('切换到课程列表页超时，将关闭程序')
        kill_process()
        system('pause')
        sys.exit()
    sleep(3)
    xpath_sub = '//a[text()="' + sub_name + '"]'
    try:
        web.find_element_by_xpath(xpath_sub).click()
    except:
        print('未找到课程或打开课程超时，将关闭程序')
        kill_process()
        system('pause')
        sys.exit()
    sleep(2)


# 获取课程的列表
def get_subjects_list(web, sub_list):
    for i in range(1, 40):
        try:
            sub_list.append(web.find_element_by_xpath('//ul/li[' + str(i) + ']/a'))
        except:
            pass
    return sub_list


# 关闭学习页面
def close_learn_page(web):
    if len(web.window_handles) != 1:
        for i in range(0, len(web.window_handles) - 1):
            web.switch_to.window(web.window_handles[i + 1])
            web.close()
    else:
        pass


# 关闭web页面
def close_web_page(web):
    if len(web.window_handles) == 1:
        web.switch_to.window(web.window_handles[0])
    else:
        pass
    web.switch_to.default_content()
    web.find_element_by_css_selector("button").click()
    sleep(1)
    web.find_element_by_css_selector("button[class='new-tbc-btn']").click()


# 学课
def virtual_learn(web, sub, learn_time=0):
    web.switch_to.window(web.window_handles[1])
    sleep(2)
    try:
        web.find_element_by_xpath('//a[@class="cs-again-btn"]')
    except:
        sleep(1)
        try:
            web.find_element_by_xpath('//li[@id="goNextStep"]').click()
        except:
            while learn_time < 120:
                print('学习中...')
                learn_time += 30
                sleep(30)
                virtual_learn(web, sub, learn_time)
                if len(web.window_handles) == 1:
                    return
                else:
                    pass
            web.close()
            web.switch_to.window(web.window_handles[0])
            sub.click()
            virtual_learn(web, sub, 0)
        else:
            sleep(1)
            print('完成:下一步')
            web.close()
            return
    else:
        web.close()
        print('完成:课程评估')
        return


if __name__ == '__main__':
    kill_process()
    # 选用firefox作为浏览器引擎，设置参数
    print(
        '\n欢迎 (*\'O\'*)ノ\n\n'
        '本程序用于课程学习，不负责课程测试。\n'
        '网速不好的情况下容易出现超时报错。\n\n'
        '使用前请确保已安装：\n'
        '1.Virtual C++ 2015\n'
        '2.FireFox和FireFox的webdriver程序\n'
    )
    opts = webdriver.FirefoxOptions()

    # 设置自动加载flash,禁用图片
    opts.set_preference("plugin.state.flash", 2)
    opts.set_preference("permissions.default.image", 2)
    opts.add_argument('-headless')

    # 网址及用户名密码,课程
    page_name = 'http://gynsh.21tb.com'
    subjects = []  # 科目列表
    user_username, user_password, subjects_name = subject_name()
    print(subjects_name)
    # 打开网页
    print('\n处理网页中...\n')
    browser = webdriver.Firefox(options=opts)
    browser.get(page_name)

    sleep(1)

    # 登录及清理页面

    login(browser, user_username, user_password)
    print('\n正在登陆...')
    sleep(1)
    clear_page(browser)

    # 切换到课程页面
    print('正在切换到课程页面...\n')
    find_learn_list_page(browser, subjects_name)

    # 获取课程列表
    get_subjects_list(browser, subjects)
    subjects_number = len(subjects)

    # 学习课程
    print('ok,我们开始课程学习')
    for i in range(0, len(subjects)):
        browser.execute_script("arguments[0].scrollIntoView();", subjects[i])  # 使subjects[i]能够点击到
        subjects[i].click()
        print('\n当前学习课程：' + subjects[i].text)
        browser.switch_to.window(browser.window_handles[1])
        virtual_learn(browser, subjects[i])
        browser.switch_to.window(browser.window_handles[0])

    # 关闭学习页面
    close_learn_page(browser)

    # 主页面退出登录
    close_web_page(browser)

    # 关闭浏览器
    browser.close()
    print('\n恭喜，全部课程已学完。\n')
    kill_process()
    system('pause')
