#!/usr/bin/python=python3.6
# -*- coding: utf-8 -*-

import re,os,csv
import jieba
from collections import OrderedDict

# ==================== replace names function =================================

sol_p = re.compile('(?<!鼠大)王')
fxg_p = re.compile('(?<!疯)小狗')
sbz_p = re.compile('(?<!少)帮主')
nicknames = {"二珂":["二科","二柯"], "SOL君": ["Sol君",sol_p],"少帮主": [sbz_p,"少帮助"],"鼠大王": ["老鼠","鼠神"],"囚徒": ["囚大"], "小苍":["苍姐"], "风行云": ["云哥"], "疯小狗": [fxg_p], "酒神": ["2009","09","零九","大酒神"], "LOT29": ["LOT二九"], "大宝": ["大宝儿", "宝儿"]}

nick_dict = {}
for key, val in nicknames.items():
    for v in val:
        nick_dict[v]=key

numbers = OrderedDict({"十一号":"11号","十二号":"12号","一号":"1号","二号":"2号","三号":"3号","四号":"4号","五号":"5号","六号":"6号","七号":"7号","八号":"8号","九号":"9号","十号":"10号"})

chinese_numbers = OrderedDict({"十一":"11","十二":"12","一":"1","二":"2","三":"3","四":"4","五":"5","六":"6","七":"7","八":"8","九":"9","十":"10"})

chinese_characters = {"村民":"villager","神民":"god","普通狼人":"werewolf","白狼王":"white_wolf","预言家":"seer","女巫":"witch","猎人":"hunter","白痴":"idiot","禁言长老":"ancient","潜行者":"assassin","守卫":"savior"}

def replace_name(fichier, nick_dict, numbers):
    """ replace the names and nicknames of players by their numbers
        replace all ": " or " :" to ":", to split more conveniently
        9 = 9号 = 二科 = 二柯 = 二珂
    """

    f = open(fichier).read()
    name_num = {}
    dic = f.split("\n\n")[0]
    for line in dic.split("\n"):
        num, name = line.split("：")
        name_num[name] = num

    for nick in nick_dict:
        f = re.sub(nick, nick_dict[nick],f)

    for name in name_num:
        f = re.sub(name, name_num[name],f)

    for num in numbers:
        f = re.sub(num, numbers[num],f)

    f = re.sub("：",":",f)

    with open("r"+fichier, "w") as r:
        r.write(f)

    return



# =============== retrieve behavior part ======================================

def find_initial_params(fichier,chinese_numbers, chinese_characters):
    """ initial params are the initial info of a game,
        includes player numbers, characters and character numbers, character functions
    """
    english_characters = {}
    for key,val in chinese_characters.items():
        english_characters[val]=key

    with open(fichier,"r") as f:

        """initial_params = {"村民":0,"神民":0,"普通狼人":0,"白狼王":0,"预言家":0,"女巫":0,"猎人":0,"白痴":0,"禁言长老":0,"潜行者":0,"守卫":0,"可以自救":0,"屠边局":1,"角色分配":[]}"""

        initial_params = {"n_villager":0,"n_god":0,"ordinary_werewolf":0,"white_wolf":0,"seer":0,"witch":0,"hunter":0,"idiot":0,"ancient":0,"assassin":0,"savior":0,"can_save_herself":1,"eliminate_partial":1, "character_dispo":[]}

        character_dispo = ["UNK"]*13

        line = f.readline()

        while line:
            if line.startswith("本期游戏共有"):

                m1 = re.search("\w(?=张[普通]*村民牌)",line)
                n_villager = m1.group(0)
                initial_params["n_villager"] = int(chinese_numbers.get(n_villager,n_villager))

                m2 = re.search("\w(?=张神民牌)", line)
                n_god = m2.group(0)
                initial_params["n_god"] = int(chinese_numbers.get(n_god,n_god))

                m4 = re.search("\w(?=张白狼王牌)", line)
                if m4:
                    n_white = m4.group(0)
                    initial_params["white_wolf"] = int(chinese_numbers.get(n_white,n_white))

                m3 = re.search("\w(?=张狼人牌)", line)
                n_wolf = m3.group(0)
                initial_params["ordinary_werewolf"] = int(chinese_numbers.get(n_wolf,n_wolf))-initial_params["white_wolf"]


                senses = line.split("。")
                for sen in senses:
                    if sen.startswith("神民包括"):
                        gods = sen.split("神民包括")[-1]
                        gods = gods.split("，")
                        for god in gods:
                            god = chinese_characters.get(god)
                            initial_params[god] = initial_params.get(god)+1
                    elif sen.startswith("女巫"):
                        if "不可以自救" in sen:
                            initial_params["can_save_herself"] = 0
                    elif "屠城局" in sen:
                        initial_params["eliminate_partial"] = 0
            elif line.startswith("本局游戏中"):
                senses = line.split("。")
                for sen in senses:
                    if "是狼人" in sen:
                        m5 = re.findall("[0-9]+(?=号)", sen)
                        m5 = set(m5)
                        for m in m5:
                            character_dispo[int(m)]="ordinary_werewolf"
                    if "是白狼王" in sen:
                        m6 = re.findall("[0-9]+(?=号)", sen)
                        m6 = set(m6)
                        for m in m6:
                            character_dispo[int(m)]="white_wolf"
                    if "预言家" in sen:
                        m6 = re.findall("[0-9]+(?=号)", sen)
                        m6 = set(m6)
                        for m in m6:
                            character_dispo[int(m)]="seer"
                    if "女巫" in sen:
                        m6 = re.findall("[0-9]+(?=号)", sen)
                        m6 = set(m6)
                        for m in m6:
                            character_dispo[int(m)]="witch"
                    if "猎人" in sen:
                        m6 = re.findall("[0-9]+(?=号)", sen)
                        m6 = set(m6)
                        for m in m6:
                            character_dispo[int(m)]="hunter"
                    if "守卫" in sen:
                        m6 = re.findall("[0-9]+(?=号)", sen)
                        m6 = set(m6)
                        for m in m6:
                            character_dispo[int(m)]="savior"
                    if "白痴" in sen:
                        m6 = re.findall("[0-9]+(?=号)", sen)
                        m6 = set(m6)
                        for m in m6:
                            character_dispo[int(m)]="idiot"
                    if "禁言长老" in sen:
                        m6 = re.findall("[0-9]+(?=号)", sen)
                        m6 = set(m6)
                        for m in m6:
                            character_dispo[int(m)]="ancient"
                    if "潜行者" in sen:
                        m6 = re.findall("[0-9]+(?=号)", sen)
                        m6 = set(m6)
                        for m in m6:
                            character_dispo[int(m)]="assassin"

            line = f.readline()
        for i in len(character_dispo):
            if i > 0 and character_dispo[i]=="UNK":
                character_dispo[i]="villager"
        initial_params["character_dispo"]=character_dispo
        return initial_params

def speech_order(speaker_list, start_speaker_index, clockwise=True):
    # by default, the speaker_list is clockwise order
    # there's some lists that have same items, so it's better to specify the index than the item
    if not clockwise:
        speaker_list = reversed(speaker_list)
    # return speaker_list[speaker_list.index(start_speaker):]+speaker_list[:speaker_list.index(start_speaker)]
    return speaker_list[start_speaker_index:]+speaker_list[:start_speaker_index]


clockwise = ["1","2","3","4","5","6","7","8","9","10","11","12"]
counterclockwise = reversed(clockwise)


def behavior_log(fichier,chinese_numbers):
    """ time, vote, captain, death, suicide of werewolf log for every game
    """
    with open(fichier,"r") as f, open(fichier[:-3]+"csv","w") as w:
        """ in the csv file log the speech:
            row: "captain_election","player2","sentence1",character,meaning_sentence
            row: "captain_election","player2","sentence2",character,meaning_sentence
            row: "Day1_speech","player4","sentence1",character, meaning_sentence
        """
        wwriter = csv.writer(csvfile, delimiter='\t')
                            # ,quotechar='|', quoting=csv.QUOTE_MINIMAL)

        n_night = 0
        n_day   = 0

        player_status        = ["Occ"]+["alive"]*12
        # [proba_seer, proba_witch, proba_god1, proba_god2, proba_villager, proba_werewolf]
        player_chrt_proba    = {"1":[1/12,1/12,1/12,1/12,1/3,1/3],
                                "2":[1/12,1/12,1/12,1/12,1/3,1/3],
                                "3":[1/12,1/12,1/12,1/12,1/3,1/3],
                                "4":[1/12,1/12,1/12,1/12,1/3,1/3],
                                "5":[1/12,1/12,1/12,1/12,1/3,1/3],
                                "6":[1/12,1/12,1/12,1/12,1/3,1/3],
                                "7":[1/12,1/12,1/12,1/12,1/3,1/3],
                                "8":[1/12,1/12,1/12,1/12,1/3,1/3],
                                "9":[1/12,1/12,1/12,1/12,1/3,1/3],
                                "10":[1/12,1/12,1/12,1/12,1/3,1/3],
                                "11":[1/12,1/12,1/12,1/12,1/3,1/3],
                                "12":[1/12,1/12,1/12,1/12,1/3,1/3],
                                "13":[1/12,1/12,1/12,1/12,1/3,1/3],
                                "14":[1/12,1/12,1/12,1/12,1/3,1/3]
                                }

        electors             = []
        # elector_speak_orders = []
        captain_vote         = [] # list of list
        captains             = []
        night_death          = []
        day_speak_orders     = []
        day_vote             = []
        day_death            = []

        line = f.readline()
        while line:
            # captain election part:
            # 1. one turn speech
            if "天亮了" in line:
                n_night += 1
                n_day   += 1
                if "现在进行警长竞选" in line:
                    sens = line.split("。")
                    for sen in sens:
                        if "名玩家参与竞选" in sen:
                            # electors of captain election
                            first_electors = re.findall("[0-9]+(?=号)", sen)
                            voters = [a for a in clockwise and not in first_electors]
                            electors.append(first_electors)
                        elif "号玩家开始发言" in sen:
                            m3 = re.search("\w(?=号玩家开始发言)", sen)
                            start_speaker = m3.group(0)

                            # the speech order of the electors
                            start_speaker_index = first_electors.index(start_speaker)
                            first_elector_speech_order= speech_order(first_electors,start_speaker_index,True)
                            # elector_speak_orders.append(first_elector_speech_order)

                            line = f.readline()
                            while len(line.split(":"))==4: # there's not until a captain so is 4
                                # is a election speech
                                num,nume,speech,charact = line.split(":")

                                # each sentence has a meaning_sentence
                                for sp in speech.split("。"):
                                    row = ["captain_election",num,sp,charact]
                                    wwriter.writerow(row)
                                line = f.readline()

                    # if "仍在警上" in line:
                    #     # if "现在进行警长竞选" and "仍在警上" both in line, that means there was a wolf suicide in the previous captain election, so here is day2, and here we don't have another turn of election speech, all players except the rest electors vote directly
                    #     # finally if only player1 votes for player2, player12 discards, player9 dead in previous night, the rest vote for player4, and player5 is the suicided wolf: election_vote=['Occ',"2","stay_electors","4","stay_electors","suicided_wolf","4","4","4","eliminated","4","4","discard"]
                    #     election_vote = ["Occ"]*13
                    #     for sen in line.split("。"):
                    #         if "玩家自爆" in sen:
                    #             m3 = re.search("\w(?=号玩家自爆)", sen)
                    #             suicided = m3.group(0)
                    #             election_vote[int(suicided)]="suicided_wolf"
                    #         if "昨天晚上死亡的是" in sen:
                    #             eliminated = re.findall("[0-9]+(?=号)", sen)
                    #             for eli in eliminated:
                    #                 election_vote[int(eliminated)]="eliminated"
                    #         if "请留遗言" in sen:
                    #             line = f.readline()
                    #             num,nume,speech,charact = line.split(":")
                    #             # each sentence has a meaning_sentence
                    #             for sp in speech.split("。"):
                    #                 row = ["captain_election",num,sp,charact]
                    #                 wwriter.writerow(row)
                    #         elif "仍在警上" in sen:
                    #             stay_electors = re.findall("[0-9]+(?=号)", sen)
                    #             for el in stay_electors:
                    #                 election_vote[int(el)]="stay_electors"
                    #             electors.append(stay_electors)
                    #             voters = [a for a in ["11","12","1","2","3","4","5","6","7","8","9","10"] if a not in [suicided,eliminated] and a not in stay_electors] # different from general situations
                    #         elif "投给" in sen:
                    #             ss = sen.split("，")
                    #             for s in ss:
                    #                 if "投给" in s:
                    #                     s1,s2 = s.split("投给")
                    #                     if s1 != "其余所有玩家":
                    #                         supporters = [a for a in s.split("号") if a !='']
                    #                         for vo in supporters:
                    #                             election_vote[int(vo)]=s2
                    #                         voters = [a for a in voters if a not in supporters]
                    #                     else:
                    #                         supporters = voters
                    #                         for vo in supporters:
                    #                             election_vote[int(vo)]=s2
                    #                 elif "弃票" in s:
                    #                     m = re.findall("[0-9]+(?=号)", s)
                    #                     for quit in m:
                    #                         election_vote[int(quit)]="discard"
                    #     captain_vote.append(election_vote)
            if "发言完毕" and "仍在警上" in line:
                # finally if only player1 votes for player2, player12 discards, the rest vote for player4: election_vote=['Occ',"2","stay_electors","4","stay_electors","4","4","4","4","4","4","4","discard"]
                if "玩家当选警长" in line:
                    # no pk turn
                    m3 = re.search("\w(?=号玩家当选警长)", sen)
                    captain = m3.group(0)
                    captains.append(captain)
                    player_status[int(captain)]="captain"

                    for sen in line.split("。"):
                        if "仍在警上" in sen:
                            stay_electors = re.findall("[0-9]+(?=号)", sen)
                            for el in stay_electors:
                                election_vote[int(el)]="stay_electors"
                            electors.append(stay_electors)
                            # here the voters are still the ones up before
                        elif "投给" in sen:
                            ss = sen.split("，")
                            for s in ss:
                                if "投给" in s:
                                    s1,s2 = s.split("投给")
                                    if s1 != "其余所有玩家":
                                        supporters = [a for a in s.split("号") if a !='']
                                        for vo in supporters:
                                            election_vote[int(vo)]=s2
                                        voters = [a for a in voters if a not in supporters]
                                    else:
                                        supporters = voters
                                        for vo in supporters:
                                            election_vote[int(vo)]=s2
                                elif "弃票" in s:
                                    m = re.findall("[0-9]+(?=号)", s)
                                    for quit in m:
                                        election_vote[int(quit)]="discard"
                        elif "昨天晚上是平安夜" in sen:
                            night_death.append(["none"])
                        elif "昨天晚上死亡的是" in sen:
                            deads = re.findall("[0-9]+(?=号)", sen)
                            night_death.append(deads)
                            for d in deads:
                                player_status[int(d)]="eliminated"
                            if "请留遗言" in sen:
                                line = f.readline()
                                while len(line.split(":"))==4 or len(line.split(":"))==5: # possible that captain died the previous night
                                    elements   = line.split(":")
                                    num        = elements[0]
                                    speech     = elements[-2]
                                    charact    = elements[-1]
                                    for sp in speech.split("。"):
                                        row = ["night1_lastwords",num,sp,charact]
                                        wwriter.writerow(row)
                                    line = f.readline()
                                if "遗言结束" in line: # "警长请选择从警左或警右开始发言"
                                    line = f.readline()
                                    if "死左" in line: # 死左或右
                                        center          = deads[0]
                                        center_ind      = int(center)
                                        prelist         = speech_order(clockwise, center_ind, clockwise=True)
                                        # prelist=["6","7","8"...] "5" is dead,
                                        # player_status = ["occ", "alive","alive"...]
                                        day_speak_order = [a for a in prelist if player_status[int(a)] == "alive"]
                                        day_speak_orders.append(day_speak_order)
                                    elif "死右" in line:
                                        center          = deads[0]
                                        center_ind      = int(center)
                                        prelist         = speech_order(clockwise, center_ind, clockwise=False)
                                        day_speak_order = [a for a in prelist if player_status[int(a)] == "alive"]
                                        day_speak_orders.append(day_speak_order)
                                    elif "左" in line: # 警左或左
                                        center          = captain
                                        center_ind      = int(center)
                                        prelist         = speech_order(clockwise, center_ind, clockwise=True)
                                        # prelist=["2","3","4"...] "1" is captain,
                                        # player_status = ["occ", "captain","alive"...]
                                        day_speak_order = [a for a in prelist if player_status[int(a)] in ["alive","captain"]]
                                        day_speak_orders.append(day_speak_order)
                                    elif "右" in line: # 警右
                                        center          = captain
                                        center_ind      = int(center)
                                        prelist         = speech_order(clockwise, center_ind, clockwise=False)
                                        day_speak_order = [a for a in prelist if player_status[int(a)] in ["alive","captain"]]
                                        day_speak_orders.append(day_speak_order)
                                    lien = f.readline()
                                    m = re.search("\w(?=号玩家开始发言)",line)
                                    start_speaker = m.group(0)
                                    if start_speaker==day_speak_order[0]:
                                        print("correct order")
                                    while len(line.split(":"))>=4:
                                        elements   = line.split(":")
                                        num        = elements[0]
                                        speech     = elements[-2]
                                        charact    = elements[-1]
                                        for sp in speech.split("。"):
                                            row = ["day1_speech",num,sp,charact]
                                            wwriter.writerow(row)
                                        line = f.readline()
                                    # day1 speech over
                else:
                    # Pk turn exists



# ================ segmentation funcion ========================================

# jieba.load_userdict("userdict.txt")

def segmenter(sentence):
    """ segment a sentence by the userdict of jieba
    """
    seged = jieba.cut(sentence)
    seg = " ".join(seged)
    return seg



# =============== retrieve discourse part =====================================

if __name__ == '__main__':
    dossier_list = os.listdir(".")

    for d in dossier_list:
        if d[0]=="S" and d[-3:]=="txt":
            replace_name(d,nick_dict,numbers)


    # initial_params = find_initial_params("rS1E101.txt",chinese_numbers, chinese_characters)
    # print(initial_params)
