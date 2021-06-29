import json
import os
import re
import time

from botoy import GroupMsg, EventMsg
from botoy import decorators as deco
from botoy.sugar import Text, Picture, Voice

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

    info_ret = re.findall(r'最近撤回\s*(\d.*)', msg)
    info_1 = re.findall(r'最近撤回', msg)
    if info_1:
        page_no = info_ret[0] if info_ret else 1
        group = ctx.FromGroupId
        uin = ctx.FromUserId
        try:
            if op.is_group_owner(group, uin) is True or op.is_group_admin(group, uin) is True or op.is_bot_master(
                    ctx.CurrentQQ, uin) is True:
                msg_revoke = op.find_group_msg_recent_revoke(group, page_no, at_user_id)
                if len(msg_revoke) == 0:
                    Text('\n[呃，没有更多记录了]', True)
                else:
                    t = ''
                    m = msg_revoke[0]
                    t += f'''{m['nick_name']} {time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(m["msg_time"]))}\n'''

                    if m["msg_type"] == 'TextMsg':
                        t += m["content"]
                        Text(t, True)
                    elif m["msg_type"] == 'VoiceMsg':
                        m_c_json = json.loads(m["content"])
                        Text(t, True)
                        Voice(voice_url=m_c_json['Url'])
                    elif m["msg_type"] == 'AtMsg':
                        m_c_json = json.loads(m["content"])
                        t += m_c_json["Content"]
                        Text(t, True)
                    elif m["msg_type"] == 'PicMsg':
                        m_c_json = json.loads(m["content"])
                        t += m_c_json["Content"] if "Content" in m_c_json else ""
                        if m_c_json["Tips"] == '[群消息-QQ闪照]':
                            Picture(pic_url=m_c_json['Url'], text=f'[ATUSER({uin})]{t}[PICFLAG]')
                        elif m_c_json["Tips"] == '[群图片]':
                            for pic in m_c_json["GroupPic"]:
                                Picture(pic_url=pic['Url'], text=f'[ATUSER({uin})]{t}[PICFLAG]')
                                time.sleep(0.5)
                        elif m_c_json["Tips"] == '[好友图片]':
                            for pic in m_c_json["FriendPic"]:
                                Picture(pic_url=pic['Url'], text=f'[ATUSER({uin})]{t}[PICFLAG]')
                                time.sleep(0.5)
            else:
                Text('\n只有群主和管理员可以使用“最近撤回”指令', True)
        except Exception as e:
            print('anti_revoke -> db.find returns null result')
            print(e)
            return


def receive_events(ctx: EventMsg):
    if ctx.EventName == 'ON_EVENT_GROUP_ADMINSYSNOTIFY':

        msg_group_id = ctx.EventData['GroupId']
        # 管理员变更，强制刷新成员列表
        op.check_group_member_list(msg_group_id, 0)

    elif ctx.EventName == 'ON_EVENT_GROUP_REVOKE' and ctx.EventData['UserID'] != int(os.getenv('BOTQQ')):
        msg_seq = ctx.EventData['MsgSeq']
        msg_group_id = ctx.EventData['GroupID']
        admin_user_id = ctx.EventData['AdminUserID']
        user_id = ctx.EventData['UserID']

        try:
            # 置群消息为撤回状态
            op.update_group_msg_is_revoked_by_msg_seq(msg_seq, msg_group_id, admin_user_id, user_id)
        except Exception as e:
            print('anti_revoke -> db.find returns null result')
            return
