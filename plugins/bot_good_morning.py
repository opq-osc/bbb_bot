# -*- coding:utf-8 -*-

RESOURCES_BASE_PATH = './resources/good-morning'

# ==========================================

# 屏蔽群 例：[12345678, 87654321]
blockGroupNumber = []
# 早安指令
goodMorningInstructionSet = ['早', '早安', '哦哈哟', 'ohayo', 'ohayou', '早安啊', '早啊', '早上好', '早w', '早呀']
# 晚安指令
goodNightInstructionSet = ['晚', '晚安', '哦呀斯密', 'oyasumi', 'oyasimi', '睡了', '睡觉了', '睡觉']

# ==========================================

import datetime
import json
import os
import random
from enum import Enum

from botoy import Action, GroupMsg
from dateutil.parser import parse

import util.db.sql as op


# ==========================================

def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId == ctx.CurrentQQ:
        return

    userGroup = ctx.FromGroupId
    userQQ = ctx.FromUserId
    msg = ctx.Content
    nickname = ctx.FromNickName
    group_name = ctx.FromGroupName

    if Tools.commandMatch(userGroup, blockGroupNumber):
        return

    if not Tools.textOnly(ctx.MsgType):
        return

    bot = Action(
        qq=ctx.CurrentQQ
    )

    mainProgram(bot, userQQ, userGroup, msg, nickname, group_name)


class Model(Enum):
    ALL = '_all'

    BLURRY = '_blurry'

    SEND_AT = '_send_at'

    SEND_DEFAULT = '_send_default'


class Status:
    SUCCESS = '_success'

    FAILURE = '_failure'


class Tools():

    @staticmethod
    def textOnly(msgType):
        return True if msgType == 'TextMsg' else False

    @staticmethod
    def readJsonFile(p):
        if not os.path.exists(p):
            return Status.FAILURE
        with open(p, 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    @staticmethod
    def commandMatch(msg, commandList, model=Model.ALL):
        if model == Model.ALL:
            for c in commandList:
                if c == msg:
                    return True
        if model == Model.BLURRY:
            for c in commandList:
                if msg.find(c) != -1:
                    return True
        return False


class Utils:

    @staticmethod
    def get_user_info(userQQ):
        return op.get_user_greeting_data(userQQ)

    @staticmethod
    def read_conf(model):
        content = ''
        if model == GoodMorningModel.MORNING_MODEL.value:
            content = Tools.readJsonFile(f'{RESOURCES_BASE_PATH}/Config/GoodMorning.json')
        if model == GoodMorningModel.NIGHT_MODEL.value:
            content = Tools.readJsonFile(f'{RESOURCES_BASE_PATH}/Config/GoodNight.json')
        if content == Status.FAILURE:
            raise Exception('缺少早晚安配置文件！')
        return content

    @classmethod
    def get_a_words(cls, model, nickname):
        return random.choice((cls.read_conf(model))['statement'])['content'].replace(r'{name}', nickname)

    @classmethod
    def get_conf_by_para(cls, parameter, model):
        return (cls.read_conf(model))[parameter]


class TimeUtils:

    @staticmethod
    def convert_time_Y_m_d(t):
        nowDate = str(datetime.datetime.strftime(t, '%Y-%m-%d'))
        return nowDate

    @staticmethod
    def get_now_time_Y_m_d():
        nowDate = str(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))
        return nowDate

    @staticmethod
    def get_last_time_for_goodnight_check_Y_m_d():
        today = datetime.datetime.today()
        today_time_start = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
        last_time = datetime.datetime.now() + datetime.timedelta(hours=-12)
        if today_time_start < last_time:
            check_time = today_time_start
        else:
            check_time = last_time
        return str(datetime.datetime.strftime(check_time, '%Y-%m-%d %H:%M:%S'))

    @staticmethod
    def get_now_time():
        nowDate = str(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
        return nowDate

    @classmethod
    def calc_time_hour_lag(cls, lastTime):
        timeNow = cls.get_now_time()
        a = parse(datetime.datetime.strftime(lastTime, '%Y-%m-%d %H:%M:%S'))
        b = parse(timeNow)
        return int((b - a).total_seconds() / 3600)

    @staticmethod
    def get_now_hour():
        return int(str(datetime.datetime.strftime(datetime.datetime.now(), '%H')))

    @classmethod
    def calc_duration(cls, lastTime):
        timeNow = cls.get_now_time()
        a = parse(datetime.datetime.strftime(lastTime, '%Y-%m-%d %H:%M:%S'))
        b = parse(timeNow)
        seconds = int((b - a).total_seconds())
        return [int(seconds / 3600), int((seconds % 3600) / 60), int(seconds % 60)]

    @staticmethod
    def format_time_para(parameterList, msg):
        return (msg.replace(r'{hour}', str(parameterList[0]))
                .replace(r'{minute}', str(parameterList[1]))
                .replace(r'{second}', str(parameterList[2])))


def mainProgram(bot, userQQ, userGroup, msg, nickname, group_name):
    # Good morning match
    if Tools.commandMatch(msg, goodMorningInstructionSet):
        sendMsg = good_morning_information(userQQ, userGroup, nickname, group_name)
        bot.sendGroupText(userGroup, sendMsg, atUser=userQQ)
        return

    # Good night detection
    if Tools.commandMatch(msg, goodNightInstructionSet):
        sendMsg = good_night_information(userQQ, userGroup, nickname, group_name)
        bot.sendGroupText(userGroup, sendMsg, atUser=userQQ)
        return


class GoodMorningModel(Enum):
    MORNING_MODEL = 100
    NIGHT_MODEL = 200


def userRegistration(uin, group_id, nick_name, group_name, model):
    data = dict(
        uin=uin,
        nick_name=nick_name,
        group_id=group_id,
        group_name=group_name,
        model=model,
        time=TimeUtils.get_now_time(),
    )
    op.insert_user_greeting_data(data)
    return Status.SUCCESS


def getRanking(from_group_id, model):
    if model == GoodMorningModel.MORNING_MODEL.value:
        return op.get_user_good_morning_rank(from_group_id, model, TimeUtils.get_now_time_Y_m_d())

    if model == GoodMorningModel.NIGHT_MODEL.value:
        return op.get_user_good_night_rank(from_group_id, model, TimeUtils.get_last_time_for_goodnight_check_Y_m_d())


def greeting_handle(userQQ, userGroup, nickname, group_name, model):
    # registered and get replay words
    userRegistration(userQQ, userGroup, nickname, group_name, model)
    rank = getRanking(userGroup, model)
    send = Utils.get_a_words(model, nickname) + '\n' + (Utils.get_conf_by_para('suffix', model)).replace(r'{number}',
                                                                                                         str(rank))
    return send


def good_morning_information(userQQ, userGroup, nickname, group_name):
    # Check if registered
    registered = Utils.get_user_info(userQQ)
    send = ''
    if registered is False:
        # registered
        send += greeting_handle(userQQ, userGroup, nickname, group_name, GoodMorningModel.MORNING_MODEL.value)
        return send
    # Already registered
    if registered['model'] == GoodMorningModel.MORNING_MODEL.value:
        # too little time
        if TimeUtils.calc_time_hour_lag(registered['time']) <= 4:
            send += Utils.get_conf_by_para('triggered', GoodMorningModel.MORNING_MODEL.value)
            return send
        # Good morning no twice a day
        if TimeUtils.convert_time_Y_m_d(registered['time']) != TimeUtils.get_now_time_Y_m_d():
            send += greeting_handle(userQQ, userGroup, nickname, group_name, GoodMorningModel.MORNING_MODEL.value)
            return send
        else:
            send += '您今天已经早安过啦！\n发送 晚安 试试吧~'
            return send
    if registered['model'] == GoodMorningModel.NIGHT_MODEL.value:
        sleeping_time = TimeUtils.calc_time_hour_lag(registered['time'])
        # too little time
        if sleeping_time <= 4:
            send += Utils.get_conf_by_para('unable_to_trigger', GoodMorningModel.MORNING_MODEL.value)
            return send
        # Sleep time cannot exceed 24 hours
        if sleeping_time < 24:
            send += greeting_handle(userQQ, userGroup, nickname, group_name,
                                    GoodMorningModel.MORNING_MODEL.value) + '\n'
            # Calculate precise sleep time
            sleepPreciseTime = TimeUtils.calc_duration(registered['time'])
            if sleepPreciseTime[0] >= 9:
                send += TimeUtils.format_time_para(sleepPreciseTime,
                                                   (Utils.read_conf(GoodMorningModel.MORNING_MODEL.value))[
                                                       'sleeping_time'][1]['content'])
            elif sleepPreciseTime[0] >= 7:
                send += TimeUtils.format_time_para(sleepPreciseTime,
                                                   (Utils.read_conf(GoodMorningModel.MORNING_MODEL.value))[
                                                       'sleeping_time'][0]['content'])
            else:
                send += TimeUtils.format_time_para(sleepPreciseTime,
                                                   (Utils.read_conf(GoodMorningModel.MORNING_MODEL.value))[
                                                       'too_little_sleep'])
        else:
            send += greeting_handle(userQQ, userGroup, nickname, group_name, GoodMorningModel.MORNING_MODEL.value)
        return send
    return Status.FAILURE


def good_night_information(userQQ, userGroup, nickname, group_name):
    # Check if registered
    registered = Utils.get_user_info(userQQ)
    send = ''
    if registered is False:
        # registered
        send += greeting_handle(userQQ, userGroup, nickname, group_name, GoodMorningModel.NIGHT_MODEL.value)
        return send
    # Already registered
    if registered['model'] == GoodMorningModel.NIGHT_MODEL.value:
        # too little time
        if TimeUtils.calc_time_hour_lag(registered['time']) <= 4:
            send += Utils.get_conf_by_para('triggered', GoodMorningModel.NIGHT_MODEL.value)
            return send
        # Two good nights can not be less than 12 hours
        if TimeUtils.calc_time_hour_lag(registered['time']) >= 12:
            send += greeting_handle(userQQ, userGroup, nickname, group_name, GoodMorningModel.NIGHT_MODEL.value)
            return send
        else:
            send += '您今天已经晚安过啦！\n发送 早安 试试吧~'
            return send
    if registered['model'] == GoodMorningModel.MORNING_MODEL.value:
        soberTime = TimeUtils.calc_time_hour_lag(registered['time'])
        # too little time
        if soberTime <= 4:
            send += Utils.get_conf_by_para('unable_to_trigger', GoodMorningModel.NIGHT_MODEL.value)
            return send
        # sober time cannot exceed 24 hours
        if soberTime < 24:
            send += greeting_handle(userQQ, userGroup, nickname, group_name, GoodMorningModel.NIGHT_MODEL.value) + '\n'
            soberAccurateTime = TimeUtils.calc_duration(registered['time'])
            if soberAccurateTime[0] >= 12:
                send += TimeUtils.format_time_para(soberAccurateTime,
                                                   (Utils.read_conf(GoodMorningModel.NIGHT_MODEL.value))[
                                                       'working_hours'][2]['content'])
            else:
                send += TimeUtils.format_time_para(soberAccurateTime, random.choice(
                    (Utils.read_conf(GoodMorningModel.NIGHT_MODEL.value))['working_hours'])['content'])
        else:
            send += greeting_handle(userQQ, userGroup, nickname, group_name, GoodMorningModel.NIGHT_MODEL.value)
        return send
    return Status.FAILURE
