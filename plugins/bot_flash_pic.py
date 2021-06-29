import json
import re
import time

from botoy import GroupMsg
from botoy import decorators as deco
from botoy.sugar import Text, Picture

import util.db.sql as op


@deco.ignore_botself
def receive_group_msg(ctx: GroupMsg):
    at_user_id = None
    if ctx.MsgType == 'AtMsg':
        content = json.loads(ctx.Content)
        msg = content['Content']
        at_user_id = content['UserID'][0] if "UserID" in content else None
    elif ctx.MsgType == 'TextMsg':
        msg = ctx.Content
    else:
        return

    info_ret = re.findall(r'闪照现\s*(\d.*)', msg)
    info_1 = re.findall(r'闪照现', msg)
    if info_1:
        page_no = info_ret[0] if info_ret else 1
        group = ctx.FromGroupId
        uin = ctx.FromUserId
        try:
            if op.is_group_owner(group, uin) is True or op.is_group_admin(group, uin) is True or op.is_bot_master(
                    ctx.CurrentQQ, uin) is True:
                msg_flash_pic = op.find_group_msg_recent_flash_pic(group, page_no, at_user_id)
                if len(msg_flash_pic) == 0:
                    Text('\n[呃，没有更多记录了]', True)
                else:
                    m = msg_flash_pic[0]
                    msg = f'''\n{m['nick_name']} {time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(m["msg_time"]))}'''
                    m_c_json = json.loads(m["content"])
                    Picture(pic_url=m_c_json['Url'], text=f'[ATUSER({uin})]{msg}[PICFLAG]')
            else:
                Text('\n只有群主和管理员可以使用“闪照现”指令', True)
        except Exception as e:
            print('flash_pic -> db.find returns null result')
            print(e)
            return
