***************************************本脚本使用python3编写，需要requests以及time库支持*****************************************

####################请勿在13.5.0.20使用，该版本有bug更新策略会清空策略内容，13.6.0.88经测试无异常###############

1、使用前请确定当前python脚本目录内是否存在log以及config文件夹，如不存在，请创建。

2、在第一次使用脚本或密码过期后，运行"imperva_session.py"脚本，输入账号密码获取session，并复制session值。粘贴至"imperva_SecureSphere_api.py"里bs64_pwd字段中。

3、在第一次使用脚本前或需要更改策略应用的站点时，请在"imperva_SecureSphere_api.py"内配置相关站点名、服务器组、服务、应用程序（如需要应用web应用自定义策略的话）。

4、在使用"Web_Service_Policy_ApplyTo.py"和"Web_Application_Policy_ApplyTo.py"脚本前请使用"Get_Custom_Policy_Name.py"获取策略信息，并在config内修改需要使用的策略类型（web服务自定义Web_Service_Custom_Policies.txt or web应用自定义Web_Application_Custom_Policies.txt），并将策略修改至仅剩需要自动应用策略至站点所需的策略名称。（未找到的自定义策略请在另一个文本中查看）

5、配置完毕后使用"python Web_Application_Policy_ApplyTo.py"(web应用自定义策略) or "python Web_Service_Policy_ApplyTo.py"(web服务自定义策略)进行自动化应用策略至站点

6、如需应用完后需应用新策略则可按照在相应配置表内新增策略（注意格式，注意策略名一致），或重新运行"Get_Custom_Policy_Name.py"。

#################强烈建议非测试过的版本首次使用脚本前，先新建自定义策略进行应用，测试是否有api bug（清空策略）###########################