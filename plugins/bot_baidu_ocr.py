"""百度ai的OCR接口
填写应用信息

使用: 发送ocr文字加图片
"""
import time

import requests
from aip import AipOcr
from botoy import GroupMsg
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, in_content, these_msgtypes
from botoy.refine import refine_pic_group_msg
from botoy.sugar import Text

APP_ID = ""
API_KEY = ""
SECRET_KEY = ""
assert all([APP_ID, API_KEY, SECRET_KEY]), "请填写"

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def ocr(image_url: str) -> str:
    try:
        image = requests.get(image_url, timeout=10).content
    except Exception:
        return "识别出错"
    try:
        resp = client.basicAccurate(image)
    except Exception:
        return "识别出错"
    if "error_code" not in resp:
        words = [word["words"] for word in resp["words_result"]]
        msg = "\n".join(words)
        return msg
    return "识别出错"


@ignore_botself
@these_msgtypes(MsgTypes.PicMsg)
@in_content("ocr", raw=False)
def receive_group_msg(ctx: GroupMsg):
    pic_ctx = refine_pic_group_msg(ctx)
    for pic in pic_ctx.GroupPic:
        Text(ocr(pic.Url))
        time.sleep(0.5)
