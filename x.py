# -*-coding: utf-8 -*-

from linepy import *
from datetime import datetime
from time import sleep
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, qrcode, urllib, urllib.parse, timeit
#==============================================================================#
botStart = time.time()

cl = LINE()
cl.log("Auth Token : " + str(cl.authToken))

clMID = cl.profile.mid

clProfile = cl.getProfile()
mid = cl.getProfile().mid
lineSettings = cl.getSettings()

oepoll = OEPoll(cl)
#==============================================================================#
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")
banOpen = codecs.open("ban.json","r","utf-8")

read = json.load(readOpen)
settings = json.load(settingsOpen)
ban = json.load(banOpen)

msg_dict = {}
bl = [""]

#==============================================================================#
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    python = sys.executable
    os.execl(python, python, *sys.argv)
def logError(text):
    cl.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@! '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
def helpmessage():
    helpMessage = """╔══════════════
╠♥ ✿✿✿ 半Bot垢 ✿✿✿ ♥
║
╠══✪〘 Help Message 〙✪═══
║
╠✪〘 Help 〙✪══════════
╠➥ help コマンドを文字で出します。
╠➥ ヘルプ コマンドをファイルで出します。
║
╠✪〘 Status 〙✪════════
╠➥ 詳細 詳細を確認します。
╠➥ 稼働時間 動作時間を確認します。
╠➥ Speed 処理速度をはかります。
╠➥ 設定確認　BOTの設定を確認します。
╠➥ ログアウト ログアウトします。
╠➥ テスト 正常に動作しているか確認します。
╠➥ 作者 BOTの作者をだすよ
╠➥ 利用規約 利用規約を出します。
║
╠✪〘 Settings 〙✪═══════
╠➥ 自動追加 オン/オフ 友達を自動で追加します。
╠➥ 自動参加 オン/オフ グループに自動で参加します。
╠➥ 自動退出 オン/オフ グループを自動で退出します。
╠➥ 自動既読 オン/オフ 自動で既読します。
║
╠➥ 全保護 オン/オフ 全保護
╠➥ 蹴り保護 オン/オフ 蹴り保護
╠➥ うらる保護 オン/オフ URL保護
╠➥ 招待保護 オン/オフ 招待保護
║
╠➥ mid取得 オン/オフ midを取得します。
╠➥ 復元 オン/オフ 消去メッセージ読み込み
╠➥ メンション自動返信　オン/オフ メンション自動返信
╠➥ ノート オン/オフ ノート自動URl作成
╠➥ 共有 オン/オフ 共有自動URL作成
║
╠✪〘 Self 〙✪═════════
╠➥ Me 連絡先送信
╠➥ mid mid送信
╠➥ 名前 名前送信
╠➥ ステコメ ステメ送信
╠➥ トプ画 トプ画送信
╠➥ ホーム画 ホーム画送信
╠➥ 連絡先送信 @ 連絡先取得
╠➥ Mid @ mid取得
╠➥ 詳細取得 @ 詳細取得
║
╠✪〘 Blacklist 〙✪═══════
╠➥ ブラリス追加 @ ブラリス追加
╠➥ ブラリス削除 @ ブラリス削除
╠➥ ブラリス一覧 ブラックリストを名前で送信します。
╠➥ ブラリス一覧mid ブラックリストをmidで送信します。
╠➥ 全削除ブラリス ブラリス消去
╠➥ ブラリス排除 ブラリス蹴り
║
╠✪〘 Group 〙✪════════
╠➥ グル作成者 グル作成者の連絡先を表示します。
╠➥ グルID グルIDを表示します。
╠➥ グル名 グル名を表示します。
╠➥ グル画 グル画を表示します。
╠➥ うらる作成 グルURL取得
╠➥ うらる許可 うらるを許可します。
╠➥ うらる拒否 うらるを拒否します。
╠➥ グルリスト 入っているグループのリストを表示します。
╠➥ グルメンバー グルメンリスト
╠➥ グル詳細 グル詳細を表示します。
╠➥ Gn (文字) グル名変更
╠➥ Mk @ メンション蹴り
╠➥ Nk ネーム蹴り
╠➥ Zk ネーム空白蹴り
╠➥ 全蹴り 全蹴り
╠➥ Inv (mid) mid招待
╠➥ キャンセル 招待キャンセル
╠➥ Ri @ 蹴り招待
║
╠✪〘 Special 〙✪═══════
╠➥ 偽造 オン/オフ 偽造
╠➥ ※偽造＝トークを真似して送信します。
╠➥ 偽造リスト 偽造リスト
╠➥ 偽造追加 @ 偽造追加
╠➥ 偽造削除 @ 偽造削除
║
╠➥ 既読ポイントセット 既読ポイント設置
╠➥ 既読ポイント消去 既読ポイント消去
╠➥ 既読確認 既読ポイント確認
║
╠➥ オールメンション 全メンション
╠➥ Zt
╠➥ Zm
╠➥ コピー @ プロフィールコピー
╠➥ 初期化 プロフィール初期化
╠➥ 全グル送信:text 全グル送信
╠➥ 全個チャ送信:text 全送信
║
╠✪〘 Admin 〙✪═════════
╠➥ 権限追加 @ 権限者追加
╠➥ 権限削除 @ 権限者削除
╠➥ 権限リスト 権限者リスト
║
╠✪〘 Invite 〙✪════════
╠➥ 招待者追加 @ 招待者追加
╠➥ 招待者削除 @ 招待者削除
╠➥ 招待者リスト 招待者リスト
╠➥ 入室
║
╚═〘 Created By: 半BOT販売 〙"""
    return helpMessage

wait = {
    "myProfile": {
    "displayName": "",
    "coverId": "",
    "pictureStatus": "",
    "statusMessage": ""
    },
}
wait2 = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
}
setTime = {}
setTime = wait2['setTime']

wait["myProfile"]["displayName"] = clProfile.displayName
wait["myProfile"]["statusMessage"] = clProfile.statusMessage
wait["myProfile"]["pictureStatus"] = clProfile.pictureStatus
coverId = cl.getProfileDetail()["result"]["objectId"]
wait["myProfile"]["coverId"] = coverId

def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))

admin =['u356f45dcbdd5261625061f9f26d2004a',clMID]
owners = [""]
#if clMID not in owners:
#    python = sys.executable
#    os.execl(python, python, *sys.argv)
#==============================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            print ("[ 5 ] NOTIFIED ADD CONTACT")
            if settings["autoAdd"] == True:
                cl.findAndAddContactsByMid(op.param1)
                cl.sendMessage(op.param1, "友達追加ありがとうございます！".format(str(cl.getContact(op.param1).displayName)))
        if op.type == 11:
            group = cl.getGroup(op.param1)
            contact = cl.getContact(op.param2)
            if settings["qrprotect"] == True:
                if op.param2 in admin or op.param2 in ban["bots"]:
                    pass
                else:
                    gs = cl.getGroup(op.param1)
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    gs.preventJoinByTicket = True
                    cl.updateGroup(gs)
        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            if clMID in op.param3:
                group = cl.getGroup(op.param1)
                if settings["autoJoin"] == True:
                    cl.acceptGroupInvitation(op.param1)
            elif settings["invprotect"] == True:
                if op.param2 in admin or op.param2 in ban["bots"]:
                    pass
                else:
                    cl.cancelGroupInvitation(op.param1,[op.param3])
            else:
                group = cl.getGroup(op.param1)
                gInviMids = []
                for z in group.invitee:
                    if z.mid in ban["blacklist"]:
                        gInviMids.append(z.mid)
                if gInviMids == []:
                    pass
                else:
                    cl.cancelGroupInvitation(op.param1, gInviMids)
                    cl.sendMessage(op.param1,"ブラリスユーザーの為キャンセルしました。")
        if op.type == 17:
            if op.param2 in admin or op.param2 in ban["bots"]:
                return
            ginfo = str(cl.getGroup(op.param1).name)
            try:
                strt = int(3)
                akh = int(3)
                akh = akh + 8
                aa = """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(op.param2)+"},"""
                aa = (aa[:int(len(aa)-1)])
                cl.sendMessage(op.param1, "@wanping さんが参加しました！"+ginfo , contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
            except Exception as e:
                print(str(e))
        if op.type == 19:
            msg = op.message
            chiya = []
            chiya.append(op.param2)
            chiya.append(op.param3)
            cmem = cl.getContacts(chiya)
            zx = ""
            zxc = ""
            zx2 = []
            xpesan ='警告!'
            for x in range(len(cmem)):
                xname = str(cmem[x].displayName)
                pesan = ''
                pesan2 = pesan+"@x が"
                xlen = str(len(zxc)+len(xpesan))
                xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                zx2.append(zx)
                zxc += pesan2
            text = xpesan+ zxc + "を蹴りました！"
            try:
                cl.sendMessage(op.param1, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
            except:
                cl.sendMessage(op.param1,"Notified kick out from group")
            if op.param2 not in admin:
                if op.param2 in ban["bots"]:
                    pass
                elif settings["protect"] == True:
                    ban["blacklist"][op.param2] = True
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    cl.inviteIntoGroup(op.param1,[op.param3])
                else:
                    cl.sendMessage(op.param1,"")
            else:
                cl.sendMessage(op.param1,"")
        if op.type == 24:
            print ("[ 24 ] NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
#        if op.type == 25 :
#            if msg.toType ==2:
#                g = cl.getGroup(op.message.to)
#                print ("sended:".format(str(g.name)) + str(msg.text))
#            else:
#                print ("sended:" + str(msg.text))
#        if op.type == 26:
#            msg =op.message
#            pop = cl.getContact(msg._from)
#            print ("replay:"+pop.displayName + ":" + str(msg.text))
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
#==============================================================================#
            if sender in K0 or sender in owners:
                if text.lower() == 'help':
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                    cl.sendContact(to,"u356f45dcbdd5261625061f9f26d2004a")
                elif text.lower() == 'bye':
                    cl.sendMessage(to,"ByeBye")
                    cl.leaveGroup(msg.to)
#==============================================================================#
                elif text.lower() == 'speed':
                    start = time.time()
                    cl.sendMessage(to, "計測中...")
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,format(str(elapsed_time)) + "秒")
                elif text.lower() == 'ログアウト':
                    cl.sendMessage(to, "ログアウト中...")
                    time.sleep(5)
                    cl.sendMessage(to, "ログアウトしました。\n再ログインしてください。")
                    restartBot()
                elif text.lower() == '稼働時間':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    cl.sendMessage(to, "動作時間： {}".format(str(runtime)))
                elif text.lower() == '詳細':
                    try:
                        arr = []
                        owner ="u356f45dcbdd5261625061f9f26d2004a"
                        creator = cl.getContact(owner)
                        contact = cl.getContact(clMID)
                        grouplist = cl.getGroupIdsJoined()
                        contactlist = cl.getAllContactIds()
                        blockedlist = cl.getBlockedContactIds()
                        ret_ = "╔══[ 半BOT販売垢 ]"
                        ret_ += "\n╠ 使用者 : {}".format(contact.displayName)
                        ret_ += "\n╠ 参加グル : {}".format(str(len(grouplist)))
                        ret_ += "\n╠ 友達 : {}".format(str(len(contactlist)))
                        ret_ += "\n╠ ブロック : {}".format(str(len(blockedlist)))
                        ret_ += "\n╠══[ Adp半bot ]"
                        ret_ += "\n╠ バージョン : β2.2 試用バージョン"
                        ret_ += "\n╠ 製作者 : {}".format(creator.displayName)
                        ret_ += "\n╚══[ ご使用ありがとうございます ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
#==============================================================================#
                elif text.lower() == '設定確認':
                    try:
                        ret_ = "╔══[ 設定状態 ]"
                        if settings["autoAdd"] == True: ret_ += "\n╠ 自動追加 ✅"
                        else: ret_ += "\n╠ 自動追加 ❌"
                        if settings["autoJoin"] == True: ret_ += "\n╠ 自動参加 ✅"
                        else: ret_ += "\n╠ 自動参加 ❌"
                        if settings["autoLeave"] == True: ret_ += "\n╠ 強制自動退出 ✅"
                        else: ret_ += "\n╠ 強制自動退出 ❌"
                        if settings["autoRead"] == True: ret_ += "\n╠ 自動既読 ✅"
                        else: ret_ += "\n╠ 自動既読 ❌"
                        if settings["protect"] ==True: ret_+="\n╠ 蹴り保護 ✅"
                        else: ret_ += "\n╠ 蹴り保護 ❌"
                        if settings["qrprotect"] ==True: ret_+="\n╠ URL保護 ✅"
                        else: ret_ += "\n╠ URL保護 ❌"
                        if settings["invprotect"] ==True: ret_+="\n╠ 招待保護 ✅"
                        else: ret_ += "\n╠ 招待保護 ❌"
                        if settings["detectMention"] ==True: ret_+="\n╠ メンション自動返信 ✅"
                        else: ret_ += "\n╠ メンション自動返信 ❌"
                        if settings["reread"] ==True: ret_+="\n╠ 消去メッセージ読み込み ✅"
                        else: ret_ += "\n╠ 消去メッセージ読み込み ❌"
                        if settings["share"] ==True: ret_+="\n╠ 共有自動URL作成 ✅"
                        else: ret_ += "\n╠ 共有自動URL作成 ❌"
                        ret_ += "\n╚══[ Finish ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == '自動追加 オン':
                    settings["autoAdd"] = True
                    cl.sendMessage(to, "自動追加をオンにしました！")
                elif text.lower() == '自動追加 オフ':
                    settings["autoAdd"] = False
                    cl.sendMessage(to, "自動追加をオフにしました！")
                elif text.lower() == '自動参加 オン':
                    settings["autoJoin"] = True
                    cl.sendMessage(to, "自動参加をオンにしました！")
                elif text.lower() == '自動参加 オフ':
                    settings["autoJoin"] = False
                    cl.sendMessage(to, "自動参加をオフにしました！")
                elif text.lower() == '自動退出 オン':
                    settings["autoLeave"] = True
                    cl.sendMessage(to, "強制自動退出をオンにしました！")
                elif text.lower() == '自動退出 オフ':
                    settings["autoLeave"] = False
                    cl.sendMessage(to, "強制自動退出をオフにしました！")
                elif text.lower() == '自動既読 オン':
                    settings["autoRead"] = True
                    cl.sendMessage(to, "自動既読をオンにしました！")
                elif text.lower() == '自動既読 オフ':
                    settings["autoRead"] = False
                    cl.sendMessage(to, "自動既読をオフにしました！")
                elif text.lower() == '復元 オン':
                    settings["reread"] = True
                    cl.sendMessage(to,"消去メッセージ読み込みをオンにしました！")
                elif text.lower() == '復元 オフ':
                    settings["reread"] = False
                    cl.sendMessage(to,"消去メッセージ読み込みをオフにしました！")
                elif text.lower() == '蹴り保護 オン':
                    settings["protect"] = True
                    cl.sendMessage(to, "蹴り保護オンにしました！")
                elif text.lower() == '蹴り保護 オフ':
                    settings["protect"] = False
                    cl.sendMessage(to, "蹴り保護オフにしました！")
                elif text.lower() == '共有 オン':
                    settings["share"] = True
                    cl.sendMessage(to, "共有自動URL作成オン")
                elif text.lower() == '共有 オフ':
                    settings["share"] = False
                    cl.sendMessage(to, "共有自動URL作成オフ")
                elif text.lower() == 'メンション自動返信 オン':
                    settings["detectMention"] = True
                    cl.sendMessage(to, "メンション自動返信をオンにしました！")
                elif text.lower() == 'メンション自動返信 オフ':
                    settings["detectMention"] = False
                    cl.sendMessage(to, "メンション自動返信をオフにしました！")
                elif text.lower() == 'うらる保護 オン':
                    settings["qrprotect"] = True
                    cl.sendMessage(to, "うらる保護オンにしました！")
                elif text.lower() == 'うらる保護 オフ':
                    settings["qrprotect"] = False
                    cl.sendMessage(to, "うらる保護オフにしました！")
                elif text.lower() == '招待保護 オン':
                    settings["invprotect"] = True
                    cl.sendMessage(to, "招待保護をオンにしました！")
                elif text.lower() == '招待保護 オフ':
                    settings["invprotect"] = False
                    cl.sendMessage(to, "招待保護をオフにしました！")
                elif text.lower() == 'mid取得 オン':
                    settings["getmid"] = True
                    cl.sendMessage(to, "mid取得をオンにしました！")
                elif text.lower() == 'mid取得 オフ':
                    settings["getmid"] = False
                    cl.sendMessage(to, "mid取得をオフにしました！")
                elif text.lower() == 'ノート オン':
                    settings["note"] = True
                    cl.sendMessage(to, "ノート自動URL作成オン")
                elif text.lower() == 'ノート オフ':
                    settings["note"] = False
                    cl.sendMessage(to, "ノート自動URL作成オフ")
                elif text.lower() == '全保護 オン':
                    settings["protect"] = True
                    settings["qrprotect"] = True
                    settings["invprotect"] = True
                    cl.sendMessage(to, "蹴り、URL、招待保護をオンにしました")
                elif text.lower() == '作者':
                    cl.sendMessage(msg.to,"こちらが作者だよ。")
                    cl.sendContact(to,"u356f45dcbdd5261625061f9f26d2004a")
                if text.lower() == 'ヘルプ':
                    cl.sendFile(to,"help.py")
                    cl.sendContact(to,"u356f45dcbdd5261625061f9f26d2004a")
                    
                elif text.lower() == '利用規約':
                    cl.sendMessage(to, "利用規約および関連法規1.このBOTは有料半BOT4です。2.有料半BOTはログアウトしてしまったら何度でもログインできますので、ご安心ください。3.尚、半BOTはLINEの規約違反ですので、規制に掛かるこも稀にあります。ですが、こちらは責任は取りませんので、ご了承ください。4.規制についてはこちらも改善して行きます。m(_ _)m 5.もしログアウトしてしまったら下の連絡先又は半BOTグループなどで、再ログインできます。ご安心ください。m(_ _)m 6.このBOTの処理速度は0.01〜0.03前後です。ご確認ください。────以上が利用規約および関連法規でした。────")
                    cl.sendContact(to,"u356f45dcbdd5261625061f9f26d2004a")
                elif text.lower() == '全保護 オフ':
                    settings["protect"] = False
                    settings["qrprotect"] = False
                    settings["invprotect"] = False
                    cl.sendMessage(to, "蹴り、URL、招待保護をオフにしました")
#==============================================================================#
                elif msg.text.lower().startswith("権限追加 "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    admin.append(str(inkey))
                    cl.sendMessage(to, "権限者を追加しました！")
                elif msg.text.lower().startswith("権限削除 "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    admin.remove(str(inkey))
                    cl.sendMessage(to, "権限者を消去しました！")
                elif text.lower() == '権限リスト':
                    if admin == ['u356f45dcbdd5261625061f9f26d2004a']:
                        cl.sendMessage(to,"権限者はいません！")
                    else:
                        mc = "╔══[ Admin List ]"
                        for mi_d in admin:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")
                elif msg.text.lower().startswith("invite "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    G = cl.getGroup
                    cl.inviteIntoGroup(to,targets)
                elif ("Say " in msg.text):
                    x = text.split(' ',2)
                    c = int(x[2])
                    for c in range(c):
                        cl.sendMessage(to,x[1])
                elif msg.text.lower().startswith("tag "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    x = text.split(' ',2)
                    c = int(x[2])
                    for c in range(c):
                        sendMessageWithMention(to, inkey)
                elif msg.text.lower().startswith("招待者追加 "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    ban["bots"].append(str(inkey))
                    cl.sendMessage(to, "招待者を追加しました！")
                elif msg.text.lower().startswith("招待者削除 "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    ban["bots"].remove(str(inkey))
                    cl.sendMessage(to, "招待者を削除しました！")
                elif text.lower() == '招待者リスト':
                    if ban["bots"] == []:
                        cl.sendMessage(to,"招待者はいません！")
                    else:
                        mc = "╔══[ Inviter List ]"
                        for mi_d in ban["bots"]:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")
                elif text.lower() == '入室':
                    if msg.toType == 2:
                        G = cl.getGroup
                        cl.inviteIntoGroup(to,ban["bots"])
                elif msg.text.lower().startswith("ii "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    cl.createGroup("fuck",[inkey])
                    cl.leaveGroup(op.param1)
#==============================================================================#
                elif text.lower() == 'me':
                    if msg.toType == 2 or msg.toType == 1:
                        sendMessageWithMention(to, sender)
                        cl.sendContact(to, sender)
                    else:
                        cl.sendContact(to,sender)
                elif text.lower() == 'mid':
                    cl.sendMessage(msg.to,"[MID]\n" +  sender)
                elif text.lower() == '名前':
                    me = cl.getContact(sender)
                    cl.sendMessage(msg.to,"[Name]\n" + me.displayName)
                elif text.lower() == 'ステコメ':
                    me = cl.getContact(sender)
                    cl.sendMessage(msg.to,"[StatusMessage]\n" + me.statusMessage)
                elif text.lower() == 'トプ画':
                    me = cl.getContact(sender)
                    cl.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                elif text.lower() == 'myvideoprofile':
                    me = cl.getContact(sender)
                    cl.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                elif text.lower() == 'ホーム画':
                    me = cl.getContact(sender)
                    cover = cl.getProfileCoverURL(sender)
                    cl.sendImageWithURL(msg.to, cover)
                elif msg.text in ["テスト"]:
                    cl.sendMessage(msg.to,"正常に動作しています。")     
                elif msg.text.lower().startswith("連絡先送信 "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            mi_d = contact.mid
                            cl.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith("mid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = "[ Mid User ]"
                        for ls in lists:
                            ret_ += "\n" + ls
                        cl.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("詳細取得 "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.sendMessage(msg.to, "[ 名前 ]\n" + contact.displayName)
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.sendMessage(msg.to, "[ ステメ ]\n" + contact.statusMessage)
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + cl.getContact(ls).pictureStatus
                            cl.sendImageWithURL(msg.to, str(path))
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = cl.getProfileCoverURL(ls)
                                cl.sendImageWithURL(msg.to, str(path))

#==============================================================================#
                elif msg.text.lower().startswith("偽造追加 "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ban["mimic"]["target"][target] = True
                            cl.sendMessage(msg.to,"偽造に追加しました！")
                            break
                        except:
                            cl.sendMessage(msg.to,"偽造追加に失敗しました！")
                            break
                elif msg.text.lower().startswith("偽造削除 "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del settings["模仿名單"]["target"][target]
                            cl.sendMessage(msg.to,"偽造から削除しました！")
                            break
                        except:
                            cl.sendMessage(msg.to,"偽造削除に失敗しました！")
                            break
                elif text.lower() == '偽造リスト':
                    if ban["mimic"]["target"] == {}:
                        cl.sendMessage(msg.to,"偽造はいません！")
                    else:
                        mc = "╔══[ Mimic List ]"
                        for mi_d in ban["mimic"]["target"]:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(msg.to,mc + "\n╚══[ Finish ]")
                elif "偽造" in msg.text.lower():
                    sep = text.split(" ")
                    mic = text.replace(sep[0] + " ","")
                    if mic == "オン":
                        if ban["mimic"]["status"] == False:
                            ban["mimic"]["status"] = True
                            cl.sendMessage(msg.to,"偽造をオンにしました。")
                    elif mic == "オフ":
                        if ban["mimic"]["status"] == True:
                            ban["mimic"]["status"] = False
                            cl.sendMessage(msg.to,"偽造をオフにしました。")

#==============================================================================#
                elif text.lower() == 'グル作成者':
                    group = cl.getGroup(to)
                    GS = group.creator.mid
                    cl.sendContact(to, GS)
                elif text.lower() == 'グルID':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to, "[ ID Group ]\n" + gid.id)
                elif text.lower() == 'グル画':
                    group = cl.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'グル名':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to, "[ グル名　]\n" + gid.name)
                elif text.lower() == 'うらる作成':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ticket = cl.reissueGroupTicket(to)
                            cl.sendMessage(to, "[ Group Ticket ]\nline://ti/g/{}".format(str(ticket)))
                        else:
                            cl.sendMessage(to, "Grouplink未解放 {}openlink".format(str(settings["keyCommand"])))
                            cl.sendMessage(to, "URL参加をオンにしてください！")
                elif text.lower() == 'うらる許可':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            cl.sendMessage(to, "既にURL参加がオンです！")
                        else:
                            group.preventedJoinByTicket = False
                            cl.updateGroup(group)
                            cl.sendMessage(to, "URL参加をオンにしました！")
                elif text.lower() == 'うらる拒否':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            cl.sendMessage(to, "既にURL参加がオフです！")
                        else:
                            group.preventedJoinByTicket = True
                            cl.updateGroup(group)
                            cl.sendMessage(to, "URL参加をオフにしました！")
                elif text.lower() == 'グル詳細':
                    group = cl.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "不明"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "URL参加オフ"
                        gTicket = "無し"
                    else:
                        gQr = "URL参加オン"
                        gTicket = "line://ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ Group Info ]"
                    ret_ += "\n╠ グル名 : {}".format(str(group.name))
                    ret_ += "\n╠ グルId : {}".format(group.id)
                    ret_ += "\n╠ 作成者 : {}".format(str(gCreator))
                    ret_ += "\n╠ グル人数 : {}".format(str(len(group.members)))
                    ret_ += "\n╠ 招待人数 : {}".format(gPending)
                    ret_ += "\n╠ URL開閉 : {}".format(gQr)
                    ret_ += "\n╠ 参加URL : {}".format(gTicket)
                    ret_ += "\n╚══[ Finish ]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'グルメンバー':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        ret_ = "╔══[ グルメン ]"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n╚══[ 参加者： {} 人]".format(str(len(group.members)))
                        cl.sendMessage(to, str(ret_))
                elif text.lower() == 'グルリスト':
                        groups = cl.groups
                        ret_ = "╔══[ 参加グルリスト ]"
                        no = 0 + 1
                        for gid in groups:
                            group = cl.getGroup(gid)
                            ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n╚══[ 合計： {} グル ]".format(str(len(groups)))
                        cl.sendMessage(to, str(ret_))
                elif msg.text.lower().startswith("Mk "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            #cl.sendMessage(to,"Fuck you")
                            cl.kickoutFromGroup(msg.to,[target])
                        except:
                            cl.sendMessage(to,"Error")
                elif "Nk" in msg.text:
                    Nk0 = msg.text.replace("Nk ", "")
                    Nk1 = Nk0.lstrip()
                    Nk2 = Nk1.replace("@", "")
                    Nk3 = Nk2.rstrip()
                    _name = Nk3
                    gs = cl.getGroup(msg.to)
                    targets = []
                    for s in gs.members:
                        if _name in s.displayName:
                            targets.append(s.mid)
                    if targets == []:
                        cl.sendMessage(msg.to, "ユーザーが存在しません。")
                        pass
                    else:
                        targets.remove(mid)
                        for s in whitelist:
                            if s in targets:
                                targets.remove(s)
                        for target in targets:
                            try:
                                cl.kickoutFromGroup(msg.to, [target])
                            except:
                                cl.sendMessage(msg.to, "正常に処理できませんでした")
                elif "Zk" in msg.text:
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            if target in admin:
                                pass
                            else:
                                try:
                                    cl.kickoutFromGroup(to,[target])
                                except:
                                    cl.sendMessage(msg.to, "正常に処理できませんでした")

                elif msg.text.lower().startswith("ri "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.sendMessage(to,"蹴り後、招待します！")
                            cl.kickoutFromGroup(msg.to,[target])
                            cl.inviteIntoGroup(to,[target])
                        except:
                            cl.sendMessage(to,"Error")
                elif text.lower() == '全蹴り':
                    if msg.toType == 2:
                        print ("[ 19 ] KICK ALL MEMBER")
                        _name = msg.text.replace("全蹴り","")
                        gs = cl.getGroup(msg.to)
                        cl.sendMessage(msg.to,"全蹴り実行！")
                        targets = []
                        for g in gs.members:
                            if _name in g.displayName:
                                targets.append(g.mid)
                        if targets == []:
                            cl.sendMessage(msg.to,"Error")
                        else:
                            for target in targets:
                                try:
                                    cl.kickoutFromGroup(msg.to,[target])
                                    print (msg.to,[g.mid])
                                except:
                                    cl.sendMessage(msg.to,"")
                elif ("Gn " in msg.text):
                    if msg.toType == 2:
                        X = cl.getGroup(msg.to)
                        X.name = msg.text.replace("Gn ","")
                        cl.updateGroup(X)
                    else:
                        cl.sendMessage(msg.to,"グループ以外には使用できません。")
                elif text.lower() == 'キャンセル':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.invitee]
                    for _mid in gMembMids:
                        cl.cancelGroupInvitation(msg.to,[_mid])
                    cl.sendMessage(msg.to,"招待中をキャンセルしました！")
                elif ("Inv " in msg.text):
                    if msg.toType == 2:
                        midd = msg.text.replace("Inv ","")
                        cl.findAndAddContactsByMid(midd)
                        cl.inviteIntoGroup(to,[midd])
#==============================================================================#
                elif text.lower() == 'オールメンション':
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//100
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*100 : (a+1)*100]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        cl.sendMessage(to, "合計： {} メンション".format(str(len(nama))))
                if "qr:" in text:
                 try:
                   a = text.replace('qr:','')
                   img = qrcode.make(a)
                   img.save('qr.png')
                   cl.sendImage(to,"qe.png") 
                   os.remove('qr.png')
                 except:
                   cl.sendMessage(msg.to,"Error")
                elif text.lower() == 'zt':
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            sendMessageWithMention(to,target)
                elif text.lower() == 'zm':
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for mi_d in targets:
                           cl.sendContect(to,mi_d)
                elif text.lower() == '既読ポイントセット':
                    cl.sendMessage(msg.to, "既読ポイントを設置しました！")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                    except:
                        pass
                    now2 = datetime.now()
                    wait2['readPoint'][msg.to] = msg.id
                    wait2['readMember'][msg.to] = ""
                    wait2['setTime'][msg.to] = datetime.strftime(now2,"%H:%M")
                    wait2['ROM'][msg.to] = {}
                elif text.lower() == "既読ポイント消去":
                    cl.sendMessage(to, "既読ポイントを消去しました！")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                        del wait2['setTime'][msg.to]
                    except:
                        pass
                elif msg.text in ["既読確認","Checkread"]:
                    if msg.to in wait2['readPoint']:
                        if wait2["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait2["ROM"][msg.to].items():
                                chiya += rom[1] + "\n"
                        cl.sendMessage(msg.to, "[既読]%s\n\n[無視]:\n%s\n設置時間:\n[%s]" % (wait2['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        cl.sendMessage(msg.to, "既読ポイントを設置してください！")

#==============================================================================#
                elif msg.text.lower().startswith("ブラリス追加 "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ban["blacklist"][target] = True
                            cl.sendMessage(msg.to,"ブラック追加しました！")
                            break
                        except:
                            cl.sendMessage(msg.to,"ブラック追加に失敗しました！")
                            break
                elif "Ban:" in msg.text:
                    mmtxt = text.replace("Ban:","")
                    try:
                        ban["blacklist"][mmtext] = True
                        cl.sendMessage(msg.to,"ブラック追加しました！")
                    except:
                        cl.sendMessage(msg.to,"ブラック追加に失敗しました！")
                elif msg.text.lower().startswith("ブラリス削除 "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del ban["blacklist"][target]
                            cl.sendMessage(msg.to,"ブラック削除しました！")
                            break
                        except:
                            cl.sendMessage(msg.to,"ブラック削除に失敗しました！")
                            break
                elif text.lower() == 'ブラリス一覧':
                    if ban["blacklist"] == {}:
                        cl.sendMessage(msg.to,"ブラックはいません！")
                    else:
                        mc = "╔══[ Black List ]"
                        for mi_d in ban["blacklist"]:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(msg.to,mc + "\n╚══[ Finish ]")
                elif text.lower() == 'ブラリス排除':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                    for tag in ban["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    if matched_list == []:
                        cl.sendMessage(msg.to,"ブラックはいません！")
                        return
                    for jj in matched_list:
                        cl.kickoutFromGroup(msg.to,[jj])
                    cl.sendMessage(msg.to,"ブラックを蹴りました！")
                elif text.lower() == '全削除ブラリス':
                    for mi_d in ban["blacklist"]:
                        ban["blacklist"] = {}
                    cl.sendMessage(to, "ブラックリストを消去しました！")
                elif text.lower() == 'ブラリス一覧mid':
                    if ban["blacklist"] == {}:
                        cl.sendMessage(msg.to,"ブラックはいません！")
                    else:
                        mc = "╔══[ Black List ]"
                        for mi_d in ban["blacklist"]:
                            mc += "\n╠ "+mi_d
                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")


#==============================================================================#
                elif "全個チャ送信:" in msg.text:
                    bctxt = text.replace("全個チャ送信:","")
                    t = cl.getAllContactIds()
                    for manusia in t:
                        cl.sendMessage(manusia,(bctxt))
                elif "全グル送信:" in msg.text:
                    bctxt = text.replace("全グル送信:","")
                    n = cl.getGroupIdsJoined()
                    for manusia in n:
                        cl.sendMessage(manusia,(bctxt))
                elif "コピー " in msg.text:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            contact = cl.getContact(target)
                            X = contact.displayName
                            profile = cl.getProfile()
                            profile.displayName = X
                            cl.updateProfile(profile)
                            cl.sendMessage(to, "コピー中...")
                            Y = contact.statusMessage
                            lol = cl.getProfile()
                            lol.statusMessage = Y
                            cl.updateProfile(lol)
                            path = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                            P = contact.pictureStatus
                            cl.updateProfilePicture(P)
                        except Exception as e:
                            cl.sendMessage(to, "すべてのコピーが完了しました！")

                elif text.lower() == '初期化':
                        try:
                            lineProfile.displayName = str(myProfile["displayName"])
                            lineProfile.statusMessage = str(myProfile["statusMessage"])
                            lineProfile.pictureStatus = str(myProfile["pictureStatus"])
                            cl.updateProfileAttribute(8, lineProfile.pictureStatus)
                            cl.updateProfile(lineProfile)
                            sendMention(msg.to, sender, "「 Restore Profile 」\nNama ", " \nBerhasil restore profile")
                        except:
                            cl.sendMessage(msg.to, "プロフィールを初期化しました！")
#==============================================================================#
            if msg.contentType == 13:
                if settings["getmid"] == True:
                    if 'displayName' in msg.contentMetadata:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        cl.sendMessage(msg.to,"[mid]:\n" + msg.contentMetadata["mid"])
                    else:
                        cl.sendMessage(msg.to,"[mid]:\n" + msg.contentMetadata["mid"])
            elif msg.contentType == 16:
                if settings["note"] == True:
                    msg.contentType = 0
                    msg.text = "ノートが作成されました\n" + msg.contentMetadata["postEndUrl"]
                  #  detail = cl.downloadFileURL(to,msg,msg.contentMetadata["postEndUrl"])
                    cl.sendMessage(msg.to,msg.text)
#==============================================================================#
        if op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    cl.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in ban["mimic"]["target"] and ban["mimic"]["status"] == True and ban["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        cl.sendMessage(msg.to,text)
                if msg.contentType == 0 and sender not in clMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if clMID in mention["M"]:
                                if settings["detectMention"] == True:
                                    contact = cl.getContact(sender)
                                    sendMessageWithMention(to, contact.mid)
                                    cl.sendMessage(to, "どうなされましたか？")
                                break
            try:
                msg = op.message
                if settings["reread"] == True:
                    if msg.toType == 0:
                        cl.log("[%s]"%(msg._from)+msg.text)
                    else:
                        cl.log("[%s]"%(msg.to)+msg.text)
                    if msg.contentType == 0:
                        msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
                    elif msg.contentType == 7:
                        stk_id = msg.contentMetadata['STKID']
                        msg_dict[msg.id] = {"text":"貼圖id:"+str(stk_id),"from":msg._from,"createdTime":msg.createdTime}
                else:
                    pass
            except Exception as e:
                print(e)

#==============================================================================#
        if op.type == 65:
            print ("[ 65 ] REREAD")
            try:
                at = op.param1
                msg_id = op.param2
                if settings["reread"] == True:
                    if msg_id in msg_dict:
                        if msg_dict[msg_id]["from"] not in bl:
                            timeNow = datetime.now()
                            timE = datetime.strftime(timeNow,"(%y-%m-%d %H:%M:%S)")
                            try:
                                strt = int(3)
                                akh = int(3)
                                akh = akh + 8
                                aa = """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(msg_dict[msg_id]["from"])+"},"""
                                aa = (aa[:int(len(aa)-1)])
                                cl.sendMessage(at, "收回訊息者 @wanping ", contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
                            except Exception as e:
                                print(str(e))
                            cl.sendMessage(at,"[メッセージ取り消し者]\n%s\n[メッセージ內容]\n%s"%(cl.getContact(msg_dict[msg_id]["from"]).displayName,msg_dict[msg_id]["text"]))
                            cl.sendMessage(at,"/n發送時間/n"+strftime("%y-%m-%d %H:%M:%S")+"/n收回時間/n"+timE)

                        del msg_dict[msg_id]
                else:
                    pass
            except Exception as e:
                print (e)
#==============================================================================#
        if op.type == 55:
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                else:
                   pass
            except:
                pass
            try:
                if op.param1 in wait2['readPoint']:
                    Name = cl.getContact(op.param2).displayName
                    if Name in wait2['readMember'][op.param1]:
                        pass
                    else:
                        wait2['readMember'][op.param1] += "\n[※]" + Name
                        wait2['ROM'][op.param1][op.param2] = "[※]" + Name
                        print (time.time() + name)
                else:
                    pass
            except:
                pass
    except Exception as error:
        logError(error)
#==============================================================================#
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)

