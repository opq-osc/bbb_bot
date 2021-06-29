from botoy import GroupMsg, FriendMsg

import util.db.sql as op


def receive_group_msg(ctx: GroupMsg):
    # 检查群列表及群成员数据是否存在, 不存在就建立
    op.check_group_list(ctx.FromGroupId)
    op.check_group_member_list(ctx.FromGroupId, ctx.FromUserId)
    # 群消息存入数据库
    op.insert_group_msg(ctx)


def receive_friend_msg(ctx: FriendMsg):
    # 检查好友数据是否存在, 不存在就建立
    op.check_friend_list(ctx.FromUin)
    # 好友消息存入数据库
    op.insert_friend_msg(ctx)
    pass
