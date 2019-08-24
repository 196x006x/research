import datetime

#入力ファイルの名前
readname = "test.txt"

#出力ファイルの名前
writename = "markdowntext.txt"

"""
キャラクターの呼び方を定義、複数を想定してリストを使用
当然ではあるがえつじの呼び方依存である。
"""
mario = ["マリオ"]
donky = ["ドンキー"]
link  = ["リンク"]
sams  = ["サムス"]
dams  = ["ダークサムス","ダムス"]
yossy = ["ヨッシー"]
carby = ["カービィ"]
fox   = ["フォックス"]
pika  = ["ピカチュウ"]
ruizi = ["ルイージ"]
nes   = ["ネス"]
cap   = ["ファルコン"]
prin  = ["プリン"] 
peach = ["ピーチ"]
deizy = ["デイジー"] 
cuppa = ["クッパ"]
ice   = ["アイクラ"]
shek  = ["シーク"]
zelda = ["ゼルダ"]
doctor= ["ドクターマリオ","ドクマリ"]
pityu = ["ピチュー"]
falco = ["ファルコ"]
marss = ["マルス"]
lucina= ["ルキナ"]
young = ["こどもリンク","ヤンリン"]
ganon = ["ガノン"]
myutu = ["ミュウツー"]
roi   = ["ロイ"]
krom  = ["クロム"]
game  = ["Mrゲーム＆ウォッチ","ゲムヲ"]
meta  = ["メタナイト"]
pit   = ["ピット"]
brapi = ["ブラックピット","ブラピ"]
zero  = ["ゼロスーツサムス","ゼロサム"]
wario = ["ワリオ"]
suneku= ["スネーク"]
ike   = ["アイク"]
poke  = ["ポケモントレーナー","ポケトレ"]
didi  = ["ディディー"]
lucas = ["リュカ"]
sonic = ["ソニック"]
dedede= ["デデデ"]
pikmin= ["ピクオリ","オリマー","ピクミン"]
ruka  = ["ルカリオ"]
robo  = ["ロボット"]
tun   = ["トゥーンリンク","トゥーン"]
wolf  = ["ウルフ"]
mura  = ["むらびと","村人"]
rock  = ["ロックマン"]
wifi  = ["フィットレ"]
roze  = ["ロゼチコ"]
mac   = ["リトルマック","リトマク"]
geko  = ["ゲッコウガ"]
sord  = ["剣術mii"]
kaku  = ["格闘mii"]
syage = ["射撃mii"]
pal   = ["パルテナ"]
pack  = ["パックマン"]
ruhure= ["ルフレ"]
shulk = ["シュルク"]
pajuni= ["パジュニ"]
duck  = ["ダックハント","ダクハン"]
ryu   = ["リュウ"]
ken   = ["ケン"]
cloud = ["クラウド"]
kamui = ["カムイ"]
beyo  = ["ベヨ"]
ink   = ["インクリング"]
ridry = ["リドリー"]
simon = ["シモン"]
rihita= ["リヒター"]
king  = ["キングクルール"]
sizue = ["シズエ"]
gaen  = ["ガオガエン"]
pakkun= ["パックンフラワー","パックン"]
joker = ["ジョーカー"]

#キャラクターをリストに格納(ルキナ、マルス、ディディーは入れない)
fighters =  [ike,ice,ink,wifi,wolf,carby,kamui,gaen,ganon,cap,cuppa,cloud,
             krom,king,geko,ken,young,sams,shek,sizue,simon,shulk,joker,
             zelda,zero,sonic,dams,duck,deizy,dedede,tun,doctor,donky,nes,
             pakkun,pack,pal,pajuni,pika,pikmin,peach,pityu,pit,fox,falco,
             prin,brapi,beyo,mario,game,myutu,mura,meta,yossy,mac,ryu,lucas,
             link,ruizi,ruka,ruhure,roi,roze,rock,robo,wario]

#分類用ワード
smash_word = ["回避","上スマ","下スマ","横スマ","復帰","上B","下B","横B",
              "空N","空後","空前","復帰"]

#えつじ使用キャラ
etuji_frends = [marss,lucina,didi]

#曜日
dayOfWeek = ["月曜日","火曜日","水曜日","木曜日","金曜日","土曜日","日曜日"]

"""
stateによる分類を行う
state == 0 初期状態
state == 1 分類待ち状態
state == 2 文章読み込み状態
"""
state = 0
data = []
data_list = []
today = datetime.date.today()
for line in open(readname,"r"):
    if("■" in line and len(data) > 2):
        state = 1
        data_list.append(data)
        data = []
        data.append(date)
    """
    日付情報かどうかの判定
    「えつじ2019/oo/oo」という形式しかないので「えつじ」で判定
    """
    if("えつじ" in line):
        #data_listへの挿入と、データの更新
        if(len(data) > 0):
            data_list.append(data)
            data = []

        #前週〇曜日などの処理
        for i in range(7):
            if(dayOfWeek[i] in line):
                dif = abs(today.weekday() - i)
                date = datetime.datetime(today.year,today.month,(today.day-dif),0,0,0)
                data.append(date)

        if("昨日" in line):
            date = datetime.datetime(today.year,today.month,(today.day-1),0,0,0)
            data.append(date)

        if("今日" in line):
            date = datetime.datetime(today.year,today.month,today.day,0,0,0)
            data.append(date)

        if(len(data) == 0):
            date_str = line[3:13]
            date = datetime.datetime.strptime(date_str, "%Y/%m/%d")
            data.append(date)

        state = 1

    elif(state == 1):
        #無意味な文字列(-----など)を消す
        char = line[0]
        if((char*4) not in line):
            cluster = 0

            #何かのfighterの名前が含まれていたらそれに対する対策メモである
            for fighter in fighters:
                for name in fighter:
                    if(name in line):
                        information = fighter[0]
                        cluster = 2

            if(cluster == 0):
                for fighter in etuji_frends:
                    for name in fighter:
                        if(name in line):
                            information = fighter[0]
                            cluster = 1

            #たま～に意味不明な文章を書くのでそれの処理
            for word in smash_word:
                if(word in line):
                    cluster = 0
                    
            #全般メモは分類情報なしのパターンが多い。
            if(cluster == 0):
                information = line

            data.append(cluster)
            data.append(information)
            state = 2

    elif(state == 2):
        data.append(line)

#ラストのデータ
data_list.append(data)

#data_listを日付順にソートする
for i in range(len(data_list)):
    for j in range(len(data_list)-1,i,-1):
        if data_list[j][0] < data_list[j-1][0]:
            data_list[j],data_list[j-1] = data_list[j-1],data_list[j]


#出力
fout = open(writename,"w")
fout.write("# スマブラメモ\n")
#cluster順に出力する
cluster = 0
fout.write("## スマブラSP全般のメモ\n")
fout.write("\n")
fout.write("---\n")
for data in data_list:
    if(data[1] == cluster):
        fout.write("\n")
        fout.write(data[0].strftime("%Y/%m/%d") + "\n")
        for i in range(2,len(data)):
            fout.write(data[i] + "\n")
        fout.write("---\n")

fout.write("\n")

cluster = 1
fout.write("## 使用キャラのメモ\n")
for fighter in etuji_frends:
    i = 0
    for data in data_list:
        #該当のファイターのデータがあれば出力する
        if(data[2] == fighter[0]):
            i += 1
            if(i == 1):
                fout.write("###" + fighter[0] + "\n")
            fout.write(data[0].strftime("%Y/%m/%d") + "\n")
            for i in range(3,len(data)):
                fout.write(data[i] + "\n")

            fout.writelines("---\n")

cluster = 2
fout.writelines("## ルキナ使用時のキャラ対策\n")
for fighter in fighters:
    i = 0
    for data in data_list:
        if(data[2] == fighter[0]):
            i += 1
            if(i == 1):
                fout.writelines("###" + fighter[0] + "\n")
            fout.write(data[0].strftime("%Y/%m/%d") + "\n")
            for i in range(3,len(data)):
                fout.write(data[i] + "\n")

            fout.write("---\n")

fout.close()
        
                


