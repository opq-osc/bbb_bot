# -*- coding:utf-8 -*-

import json
import os
import time

from botoy import Action, GroupMsg, FriendMsg

import util.db.operate_data as db
from util.db.config import config

action = Action(
    qq=int(os.getenv('BOTQQ'))
)

friend_msg_table__pre = 'tb_c2cmsg_'
group_msg_table__pre = 'tb_troopmsg_'


def is_table_exist(table_name):
    res = db.query(f'''SHOW TABLES LIKE '{table_name}';''')
    return len(res) != 0


def find_group_list_by_group_owner(g, m):
    r = db.query(f'''SELECT GroupId FROM `tb_trooplist` WHERE GroupId={g} AND GroupOwner={m};''')
    return r


def find_group_list_by_group_admin(g, m):
    r = db.query(f'''SELECT MemberUin FROM `tb_group_member` WHERE GroupUin={g} AND MemberUin={m} AND GroupAdmin=1;''')
    return r


def find_qq_bot_master(current_qq, master_qq):
    res = db.query(f'''SELECT * FROM `tb_bot_config` WHERE current_qq={current_qq} AND master_qq={master_qq};''')
    return res


def check_friend_list(from_uin):
    try:
        r = find_friend_by_friend_uin(from_uin)
        if len(r) == 0 and config.friend_list_is_updating(0) is False:
            config.add_friend_list_updating(0)
            print(str(from_uin) + ' -> 检测到新的好友，刷新[好友列表]中...')
            delete_friend_list()  # 删除好友列表

            _field = dict(
                FriendUin=None,
                IsRemark=None,
                NickName=None,
                OnlineStr=None,
                Remark=None,
                Status=None,
            )
            _list = []
            ls = [k for k in _field]
            for friend_list in action.getUserList():
                _tup = []
                for i in ls:
                    _tup.append(friend_list[i])
                _list.append(_tup)
            insert_friend_list_many(_field, _list)
            config.remove_friend_list_updating(0)
            print(str(from_uin) + ' -> [好友列表]刷新完毕.')

    except Exception as e:
        print('Err -> check_group_list: ' + str(e))
        return


def check_group_list(from_group_id):
    try:
        r = find_group_by_group_id(from_group_id)
        if len(r) == 0 and config.troop_list_is_updating(0) is False:
            config.add_troop_list_updating(0)
            print(str(from_group_id) + ' -> 检测到新的群组，刷新[群组列表]中...')
            delete_troop_list()  # 删除群组列表

            _field = dict(
                GroupId=None,
                GroupMemberCount=None,
                GroupName=None,
                GroupNotice=None,
                GroupOwner=None,
                GroupTotalCount=None,
            )
            _list = []
            ls = [k for k in _field]
            for troop_list in action.getGroupList():
                _tup = []
                for i in ls:
                    _tup.append(troop_list[i])
                _list.append(_tup)
            insert_group_list_many(_field, _list)
            config.remove_troop_list_updating(0)
            print(str(from_group_id) + ' -> [群组列表]刷新完毕.')

    except Exception as e:
        print('Err -> check_group_list: ' + str(e))
        return


def check_group_member_list(msg_group_id, from_user_id):
    try:
        r = find_member_by_uin(msg_group_id, from_user_id)
        if len(r) == 0 and config.member_list_is_updating(0) is False:
            config.add_member_list_updating(0)
            if from_user_id == 0:
                print(str(msg_group_id) + ' -> 检测到[管理员变更]，刷新[群成员列表]中...')
            else:
                print(str(msg_group_id) + ' -> 检测到[新的群成员]，刷新[群成员列表]中...')
            delete_member_list(msg_group_id)  # 删除群成员列表

            _field = dict(
                GroupUin=None,
                MemberUin=None,
                Age=None,
                AutoRemark=None,
                CreditLevel=None,
                Email=None,
                FaceId=None,
                Gender=None,
                GroupAdmin=None,
                GroupCard=None,
                JoinTime=None,
                LastSpeakTime=None,
                MemberLevel=None,
                Memo=None,
                NickName=None,
                ShowName=None,
                SpecialTitle=None,
                Status=None,
            )
            _list = []
            ls = [k for k in _field]
            for group_user_list in action.getGroupMembers(msg_group_id):
                group_user_list['GroupUin'] = msg_group_id
                _tup = []
                for i in ls:
                    _tup.append(group_user_list[i])
                _list.append(_tup)
            insert_member_list_many(_field, _list)
            config.remove_member_list_updating(0)
            print(str(msg_group_id) + ' -> [群成员列表]刷新完毕.')
    except Exception as e:
        print('Err -> check_group_member_list: ' + str(e))
        return


def is_group_owner(msg_group_id, member_id):
    try:
        r = find_group_list_by_group_owner(msg_group_id, member_id)
        if len(r) == 0:
            return False
        else:
            return True
    except Exception as e:
        print('Err -> is_group_owner: ' + str(e))
        return False


def is_group_admin(msg_group_id, member_id):
    try:
        r = find_group_list_by_group_admin(msg_group_id, member_id)
        if len(r) == 0:
            return False
        else:
            return True
    except Exception as e:
        print('Err -> is_group_admin: ' + str(e))
        return False


def is_bot_master(current_qq, master_qq):
    try:
        r = find_qq_bot_master(current_qq, master_qq)
        if len(r) == 0:
            return False
        else:
            return True
    except Exception as e:
        print('Err -> is_bot_master: ' + str(e))
        return False


def find_friend_by_friend_uin(friend_uin):
    res = db.query(f'''SELECT FriendUin FROM `tb_friendlist` WHERE FriendUin={friend_uin};''')
    return res


def find_group_by_group_id(group_id):
    res = db.query(f'''SELECT GroupId FROM `tb_trooplist` WHERE GroupId={group_id};''')
    return res


def insert_friend_list_many(_field, _list):
    db.insert_many('tb_friendlist', _field, _list)


def insert_group_list_many(_field, _list):
    db.insert_many('tb_trooplist', _field, _list)


def find_member_by_uin(group_id, user_id):
    res = db.query(f'''SELECT GroupUin FROM `tb_group_member` WHERE GroupUin={group_id} AND MemberUin={user_id};''')
    return res


def delete_friend_list():
    db.execute(f'''DELETE FROM `tb_friendlist` WHERE 1;''')


def delete_troop_list():
    db.execute(f'''DELETE FROM `tb_trooplist` WHERE 1;''')


def delete_member_list(group_uin):
    db.execute(f'''DELETE FROM `tb_group_member` WHERE `GroupUin` = {group_uin};''')


def insert_member_list_many(_field, _list):
    db.insert_many('tb_group_member', _field, _list)


def update_group_msg_is_revoked_by_msg_seq(msg_seq, group_id, admin_user_id, user_id):
    if is_table_exist(f'{group_msg_table__pre}{group_id}'):
        db.update(f'{group_msg_table__pre}{group_id}', dict(
            revoke_flag=1,
            revoke_AdminUserID=admin_user_id,
            revoke_UserID=user_id,
            revoke_time=int(time.time()),
        ), dict(
            msg_seq=msg_seq,
        ))


def find_group_msg_recent_flash_pic(gid, pno, uin=None):
    if uin is None:
        res = db.query(
            f'''SELECT * FROM `{group_msg_table__pre}{gid}` WHERE tips='[群消息-QQ闪照]' ORDER BY msg_time DESC LIMIT {int(pno) - 1},1;''')
    else:
        res = db.query(
            f'''SELECT * FROM `{group_msg_table__pre}{gid}` WHERE uin={uin} AND tips='[群消息-QQ闪照]' ORDER BY msg_time DESC LIMIT {int(pno) - 1},1;''')
    return res


def find_group_msg_recent_revoke(gid, pno, uin=None):
    if uin is None:
        res = db.query(
            f'''SELECT * FROM `{group_msg_table__pre}{gid}` WHERE revoke_flag=1 ORDER BY msg_time DESC LIMIT {int(pno) - 1},1;''')
    else:
        res = db.query(
            f'''SELECT * FROM `{group_msg_table__pre}{gid}` WHERE uin={uin} AND revoke_flag=1 ORDER BY msg_time DESC LIMIT {int(pno) - 1},1;''')
    return res


def create_table_friendmsg(from_uin):
    db.execute(f'''CREATE TABLE `{friend_msg_table__pre}{from_uin}`  (
  `msgId` bigint(20) NOT NULL AUTO_INCREMENT,
  `uin` bigint(20) NOT NULL,
  `TempUin` bigint(20) NULL,
  `flag` tinyint(1) NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `tips` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `msg_time` int(11) NULL DEFAULT NULL,
  `msg_type` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `msg_seq` int(11) NULL DEFAULT NULL,
  `redbag_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  PRIMARY KEY (`msgId`) USING BTREE,
  INDEX `{friend_msg_table__pre}{from_uin}_Idx_MsgTime`(`msg_time`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;''')


def create_table_troopmsg(group_id):
    db.execute(f'''CREATE TABLE `{group_msg_table__pre}{group_id}`  (
  `msgId` bigint(20) NOT NULL AUTO_INCREMENT,
  `uin` bigint(20) NOT NULL,
  `nick_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `cluster_id` bigint(20) NULL DEFAULT NULL,
  `flag` tinyint(1) NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `tips` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `msg_time` int(11) NULL DEFAULT NULL,
  `msg_type` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `msg_seq` int(11) NULL DEFAULT NULL,
  `msg_random` bigint(20) NULL DEFAULT NULL,
  `redbag_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `revoke_flag` tinyint(4) NULL DEFAULT NULL,
  `revoke_AdminUserID` bigint(20) NULL DEFAULT NULL,
  `revoke_UserID` bigint(20) NULL DEFAULT NULL,
  `revoke_time` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`msgId`) USING BTREE,
  INDEX `{group_msg_table__pre}{group_id}_Idx_MsgSeq`(`msg_seq`) USING BTREE,
  INDEX `{group_msg_table__pre}{group_id}_Idx_MsgTime`(`msg_time`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;''')


# friend_msg
def insert_friend_msg(ctx: FriendMsg):
    flag = 1  # 自己消息标志
    from_uin = ctx.FromUin
    if from_uin == ctx.CurrentQQ:
        from_uin = ctx.ToUin
        flag = 0

    table_name = f'{friend_msg_table__pre}{from_uin}'
    if is_table_exist(table_name):
        content_json = {}
        try:
            content_json = json.loads(ctx.Content)
        except Exception as e:
            pass

        tips = None
        try:
            if "Tips" in content_json:
                tips = content_json["Tips"]
        except Exception as e:
            pass

        db.insert(table_name, dict(
            uin=from_uin,
            TempUin=ctx.TempUin,
            flag=flag,
            content=ctx.Content,
            tips=tips,
            msg_time=int(time.time()),
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq,
            redbag_info=json.dumps(ctx.RedBaginfo) if ctx.RedBaginfo is not None else None,
        ))
    else:
        if config.table_is_creating(table_name) is False:
            config.add_table_creating(table_name)
            create_table_friendmsg(from_uin)
            print(f'{table_name} -> 创建[好友消息]表')
            config.remove_table_creating(table_name)


def insert_group_msg(ctx: GroupMsg):
    flag = 1  # 自己消息标志
    from_uin = ctx.FromUserId
    if from_uin == ctx.CurrentQQ:
        flag = 0

    table_name = f'{group_msg_table__pre}{ctx.FromGroupId}'
    if is_table_exist(table_name):
        content_json = {}
        try:
            content_json = json.loads(ctx.Content)
        except Exception as e:
            pass

        tips = None
        try:
            if "Tips" in content_json:
                tips = content_json["Tips"]
        except Exception as e:
            pass

        db.insert(table_name, dict(
            uin=from_uin,
            nick_name=ctx.FromNickName,
            cluster_id=ctx.FromGroupId,
            flag=flag,
            content=ctx.Content,
            tips=tips,
            msg_time=ctx.MsgTime,
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq,
            msg_random=ctx.MsgRandom,
            redbag_info=json.dumps(ctx.RedBaginfo) if ctx.RedBaginfo is not None else None,
        ))
    else:
        if config.table_is_creating(table_name) is False:
            config.add_table_creating(table_name)
            create_table_troopmsg(ctx.FromGroupId)
            print(f'{table_name} -> 创建[群组]消息表')
            config.remove_table_creating(table_name)


def get_user_greeting_data(uin):
    res = db.query(f'''SELECT model,time FROM `tb_good_morning` WHERE uin={uin};''')
    if len(res) == 0:
        return False
    return res[0]


def insert_user_greeting_data(data):
    res = db.query(f'''SELECT uin FROM `tb_good_morning` WHERE uin={data['uin']};''')
    if len(res) == 0:
        db.insert('tb_good_morning', data)
    else:
        db.update('tb_good_morning', dict(data), dict(uin=data['uin']))


def get_user_good_morning_rank(group_id, model, cur_time):
    r = db.query(
        f'''SELECT COUNT(*) FROM `tb_good_morning` WHERE group_id={group_id} AND time>=\'{cur_time}\' AND model={model};''')
    if len(r) == 0:
        return 1
    return r[0]['COUNT(*)']


def get_user_good_night_rank(group_id, model, last_time):
    r = db.query(
        f'''SELECT COUNT(*) FROM `tb_good_morning` WHERE group_id={group_id} AND time>=\'{last_time} 12:00:00\' AND model={model};''')
    if len(r) == 0:
        return 1
    return r[0]['COUNT(*)']
