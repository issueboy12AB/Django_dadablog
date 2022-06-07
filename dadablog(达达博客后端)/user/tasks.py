# from dadablog.celery import app
# from tools.sms import YunTongXin
#
# @app.task
# def send_sms_c(phone, code):
#
#     config = {
#         "accountSid": "8aaf07086c6b60c5016c89a354f10f95",
#         "accountToken": "6fa62f2ff4d04fe7b11655dfcae54968",
#         "appId": "8aaf07086c6b60c5016c89a355410f9b",
#         "templateId": "1"
#     }
#     yun = YunTongXin(**config)
#     res = yun.run(phone, code)
#     return res