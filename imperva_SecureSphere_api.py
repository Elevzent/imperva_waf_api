#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :imperva_SecureSphere_api.py
# @Time      :2022/7/18 17:06

import time
import requests

# 设备地址
host = "https://IP:Port"

# 登陆凭证
bs64_pwd = "base64"

# 策略应用站点配置

# 站点名
SiteName = "SiteName"

# 服务器组（配置IP的地方）
SvGroup = "serverGroupName"

# 服务（配置端口的地方）
WebService = "webServiceName"

# 应用程序（如果不需要使用Web应用程序自定义策略可不做配置）
WebApplication = "webApplicationName"  #中文为 "默认 Web 应用程序"


# imperva api
login_api = "/SecureSphere/api/v1/auth/session"
Get_All_Web_Application_Custom_Policies_api = "/SecureSphere/api/v1/conf/policies/security/webApplicationCustomPolicies"
Get_All_Web_Service_Custom_Policies_api = "/SecureSphere/api/v1/conf/policies/security/webServiceCustomPolicies"
Update_Web_Service_Custom_Policy_api = "/SecureSphere/api/v1/conf/policies/security/webServiceCustomPolicies/"
Update_Web_Application_Custom_Policy_api = "/SecureSphere/api/v1/conf/policies/security/webApplicationCustomPolicies/"

# 设置授权码(账号密码)
Authorization = {"Authorization": "Basic " + bs64_pwd}

# 忽略证书告警
requests.packages.urllib3.disable_warnings()

# print(Authorization)

# 获取登陆session,转换为json格式,并输出
login_session = requests.post((host + login_api), headers=Authorization, verify=False).json()

# 获取值session-id值
session = login_session['session-id']
# print(session)

# 设置cookie
cookie = {'Cookie': session}


def lgout():
    # 忽略证书告警
    requests.packages.urllib3.disable_warnings()

    # 登出操作
    logout = requests.delete((host + login_api), headers=cookie, verify=False)

    print(logout)
    print("已登出账号，并清除Session")
    return logout


# 获取所有Web服务自定义策略名称 并保存在当前目录，文件名为Web_Service_Custom_Policies.txt
def Get_All_Web_Service_Custom_Policies():
    # 忽略证书告警
    requests.packages.urllib3.disable_warnings()

    # 获取所有的服务器自定义策略
    Get_All_wscp = requests.get((host + Get_All_Web_Service_Custom_Policies_api), headers=cookie, verify=False).json()

    Get_All_Web_Service_Custom_Policies_Name = Get_All_wscp["customWebPolicies"]

    f = open("./config/Web_Service_Custom_Policies.txt", "w", encoding="UTF-8")
    for line in Get_All_Web_Service_Custom_Policies_Name:
        f.writelines(line + '\n')
    f.close()

    return Get_All_Web_Service_Custom_Policies_Name


# 获取所有Web应用自定义策略名称 并保存在当前目录，文件名为Web_Application_Custom_Policies.txt
def Get_All_Web_Application_Custom_Policies():
    # 忽略证书告警
    requests.packages.urllib3.disable_warnings()

    # 获取所有的服务器自定义策略
    Get_All_wacp = requests.get((host + Get_All_Web_Application_Custom_Policies_api), headers=cookie,
                                verify=False).json()

    Get_All_Web_Application_Custom_Policies_Name = Get_All_wacp["customWebPolicies"]

    # print(Get_All_Web_Application_Custom_Policies)

    f = open("./config/Web_Application_Custom_Policies.txt", "w+", encoding="UTF-8")
    for line in Get_All_Web_Application_Custom_Policies_Name:
        f.writelines(line + '\n')
    f.close()

    return Get_All_Web_Application_Custom_Policies_Name


def Web_Service_Policy_ApplyTo():
    # 创建日志文本（如有则不重复创建），并以append模式写入
    WebServiceLog = open("./log/Web_Service_Policy_ApplyTo.log", "a+", encoding="UTF-8")
    # 读取策略
    Web_Service_Custom_Policy_Name = open("./config/Web_Service_Custom_Policies.txt", "r", encoding="UTF-8")
    Read_Web_Service_Custom_Policy_Name = [i.strip("\n") for i in Web_Service_Custom_Policy_Name.readlines()]
    # 获取策略应用开始时间锚点
    Policy_Start = time.perf_counter()
    # 应用web服务自定义策略
    Update_site_service = {
        "applyTo":
            [{
                "operation": "add",
                "siteName": SiteName,
                "serverGroupName": SvGroup,
                "webServiceName": WebService,
            }]
    }
    for Policy_Name in Read_Web_Service_Custom_Policy_Name:
        Update_WebServiceCustomPolicy = requests.put(
            (host + Update_Web_Service_Custom_Policy_api + Policy_Name), json=Update_site_service, headers=cookie,
            verify=False)

        # .center() 控制输出的样式，宽度为 170//2(整除)，即 85，汉字居中，两侧填充 -
        Policy_Name_Center = Policy_Name.center(170 // 2, "-")
        print(Policy_Name_Center)
        Progress_Bar()
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        WebServiceLog.write(now_time + " : ")

        if Update_WebServiceCustomPolicy.status_code == requests.codes.ok:
            WebServiceLog.write(
                Policy_Name + " 已应用至 " + "， 站点: " + SiteName + "， 服务器组: " + SvGroup + "， web服务: " + WebService + "。 应用成功。\n")
        else:
            WebServiceLog.write(
                Policy_Name + " 应用至 " + "， 站点: " + SiteName + "， 服务器组: " + SvGroup + "， web服务: " + WebService + "。 应用失败！\n")
    Policy_Num = len(Read_Web_Service_Custom_Policy_Name)
    Policy_Time = "{}条Web服务自定义策略已应用至站点,耗时: {:.2f}s".format(Policy_Num, time.perf_counter() - Policy_Start)
    WebServiceLog.write(Policy_Time)
    WebServiceLog.write("\n" + '*' * 200 + "\n" * 2)
    WebServiceLog.close()
    print(Policy_Time)


def Web_Application_Policy_ApplyTo():
    # 创建日志文本（如有则不重复创建），并以append模式写入
    WebApplicationLog = open("./log/Web_Application_Policy_ApplyTo.log", "a+", encoding="UTF-8")
    # 读取策略
    Web_Application_Custom_Policy_Name = open("./config/Web_Application_Custom_Policies.txt", "r", encoding="UTF-8")
    Read_Web_Application_Custom_Policy_Name = [i.strip("\n") for i in Web_Application_Custom_Policy_Name.readlines()]
    # 获取策略应用开始时间锚点
    Policy_Start = time.perf_counter()
    # 应用web应用自定义策略
    Update_site_application = {
        "applyTo":
            [{
                "operation": "add",
                "siteName": SiteName,
                "serverGroupName": SvGroup,
                "webServiceName": WebService,
                "webApplicationName": WebApplication
            }]
    }
    for Policy_Name in Read_Web_Application_Custom_Policy_Name:
        Update_WebApplicationCustomPolicy = requests.put(
            (host + Update_Web_Application_Custom_Policy_api + Policy_Name), json=Update_site_application,
            headers=cookie,
            verify=False)

        # .center() 控制输出的样式，宽度为 170//2(整除)，即 85，汉字居中，两侧填充 -
        Policy_Name_Center = Policy_Name.center(170 // 2, "-")
        print(Policy_Name_Center)

        Progress_Bar()

        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        WebApplicationLog.write(now_time + " : ")
        if Update_WebApplicationCustomPolicy.status_code == requests.codes.ok:
            WebApplicationLog.write(
                Policy_Name + " 已应用至 " + "， 站点: " + SiteName + "， 服务器组: " + SvGroup + "， web服务: " + WebService + "， web应用程序: " + WebApplication  + "。 应用成功。\n")
        else:
            WebApplicationLog.write(
                Policy_Name + " 应用至 " + "， 站点: " + SiteName + "， 服务器组: " + SvGroup + "， web服务: " + WebService + "， web应用程序: " + WebApplication + "。 应用失败！\n")
    Policy_Num = len(Read_Web_Application_Custom_Policy_Name)
    Policy_Time = "{}条Web应用自定义策略已应用至站点,耗时: {:.2f}s".format(Policy_Num,time.perf_counter() - Policy_Start)
    WebApplicationLog.write(Policy_Time)
    WebApplicationLog.write("\n" + '*' * 200 + "\n" * 2)
    WebApplicationLog.close()

    print(Policy_Time)


def Progress_Bar():
    num = 80
    # 设置开始时间
    start = time.perf_counter()
    for i in range(num + 1):
        # 光标样式以及光标
        finsh = "#" * i
        # 待跑进度样式以及待跑进度
        need_do = "_" * (num - i)
        # 进度条百分比
        progress = (i / num) * 100
        # 执行结束时间点减去开始时间点
        dur = time.perf_counter() - start
        # \r用来在每次输出完成后，将光标移至行首，这样保证进度条始终在同一行输出，即在一行不断刷新的效果；{:^5.0f}，输出格式为居中，占5位，小数点后0位，浮点型数，对应输出的数为progress（百分比数字显示）；
        # {}，对应输出的数为finsh（光标）；{}，对应输出的数为need_do（待跑进度条）；{:.2f}，输出有两位小数的浮点数，对应输出的数为dur（单次进度时长）；end=''，用来保证不换行，不加这句默认换行。
        print("\r{:^5.0f}% [{}->{}] {:.2f}s".format(progress, finsh, need_do, dur), end="")
    # 换行用
    print("")


if __name__ == "__main__":
    # 获取所有web服务自定义策略
    #    Get_All_Web_Service_Custom_Policies()

    # 获取所有web应用自定义策略
    #    Get_All_Web_Application_Custom_Policies()

    # Web服务自定义策略应用站点
    Web_Service_Policy_ApplyTo()

    # Web应用自定义策略应用站点
    #    Web_Application_Policy_ApplyTo()

    # 登出
    lgout()
