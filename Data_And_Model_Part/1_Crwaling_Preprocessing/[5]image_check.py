import pandas as pd
import numpy as np
import joblib
import re
import tkinter
from PIL import Image, ImageTk
import os
import copy

# 콜백함수 설정
def preprocessing_hashtags_list(hashtags_LS):
    '''해시태그 텍스트 전처리용 함수'''
    if hashtags_LS[-1] == '':
        del hashtags_LS[-1]

    if ' ' in hashtags_LS[-1]:
        del hashtags_LS[-1]

    for i in range(len(hashtags_LS)):
        hashtags_LS[i] = re.sub(r"^\s+|\s+$", "", hashtags_LS[i])

    for i in range(len(hashtags_LS)):
        try:
            hashtags_LS[i] = hashtags_LS[i].replace(',', '')
        except:
            pass
        try:
            hashtags_LS[i] = hashtags_LS[i].replace(', ', '')
        except:
            pass
    return hashtags_LS

def out_jpg(STR):
    output, _ = STR.split('.')
    return output

def open_image(PATH, basewidth=300):
    img1 = Image.open(PATH)
    wpercent = (basewidth / float(img1.size[1]))
    hsize = int((float(img1.size[0]) * float(wpercent)))
    img1 = img1.resize((hsize, basewidth), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img1)
    return img2


def next_page():
    global idx, IMG_NAME, img, hashtags_text, update_df, total_page
    get_idx = int(current_ENTRY.get()) - 1
    if (idx + 1) == total_page:
        idx += 0
    else:
        idx += 1

    IMG_NAME, _ = update_df.loc[idx, '이미지파일명'].split('.')
    img = open_image(f'{IMG_PATH}/{IMG_NAME}.png', basewidth=300)
    hashtags_text = ', '.join(update_df['해시태그'][idx])

    # current_page_num.config(text=f"{idx + 1} / {total_page}")
    current_ENTRY.delete(0, len(str(get_idx + 1)))
    current_ENTRY.insert(0, str(idx + 1))
    image_LABEL.config(image=img)
    hashtags_TEXT.delete(0.0, tkinter.END)
    hashtags_TEXT.insert(0.0, hashtags_text)

    if update_df.loc[idx, '확인여부'] == True:
        check_BUTTON1.select()
    else:
        check_BUTTON1.deselect()
    if update_df.loc[idx, '삭제여부'] == True:
        check_BUTTON2.select()
    else:
        check_BUTTON2.deselect()
    if update_df.loc[idx, '광고여부'] == True:
        check_BUTTON3.select()
    else:
        check_BUTTON3.deselect()


def backward_page():
    global idx, IMG_NAME, img, hashtags_text, update_df, total_page
    get_idx = int(current_ENTRY.get()) - 1
    if (idx + 1) == 1:
        idx -= 0
    else:
        idx -= 1

    IMG_NAME, _ = update_df.loc[idx, '이미지파일명'].split('.')
    img = open_image(f'{IMG_PATH}/{IMG_NAME}.png', basewidth=300)
    hashtags_text = ', '.join(update_df['해시태그'][idx])

    current_ENTRY.delete(0, len(str(get_idx + 1)))
    current_ENTRY.insert(0, str(idx + 1))
    image_LABEL.config(image=img)
    hashtags_TEXT.delete(0.0, tkinter.END)
    hashtags_TEXT.insert(0.0, hashtags_text)

    if update_df.loc[idx, '확인여부'] == True:
        check_BUTTON1.select()
    else:
        check_BUTTON1.deselect()
    if update_df.loc[idx, '삭제여부'] == True:
        check_BUTTON2.select()
    else:
        check_BUTTON2.deselect()
    if update_df.loc[idx, '광고여부'] == True:
        check_BUTTON3.select()
    else:
        check_BUTTON3.deselect()

def update_dataframe_func():
    global idx, UPDATE_DATAFRAME_PATH, update_df
    #우선 체크박스저장
    update_df.loc[idx, '확인여부'] = checkVar1.get()
    update_df.loc[idx, '삭제여부'] = checkVar2.get()
    update_df.loc[idx, '광고여부'] = checkVar3.get()
    #해시태그 변경 저장
    hashtags_text = hashtags_TEXT.get(0.0, tkinter.END)
    hashtags_LS = hashtags_text.split(', ')
    hashtags_LS = preprocessing_hashtags_list(hashtags_LS)

    columns_ = update_df.columns
    values_ = list(update_df.loc[idx])
    values_[4] = hashtags_LS #해시태그 부분
    update_df.loc[idx] = pd.Series(values_, index=columns_)
    print('통과0')
    joblib.dump(update_df, UPDATE_DATAFRAME_PATH)
    print('통과1')

def fast_next_page():
    global idx, IMG_NAME, img, hashtags_text, update_df, total_page
    while True:
        next_page()
        if (checkVar1.get() == False) | ((idx + 1) == total_page):
            break
def fast_backward_page():
    global idx, IMG_NAME, img, hashtags_text, update_df
    while True:
        backward_page()
        if (checkVar1.get() == False) | ((idx + 1) == 1):
            break

def change_page_func(event):
    global idx, total_page, IMG_NAME, img, hashtags_text, update_df
    get_idx = int(current_ENTRY.get()) - 1
    if ((get_idx + 1) > total_page) | ((get_idx + 1) < 1):
        pass
    else:
        idx = get_idx

    IMG_NAME, _ = update_df.loc[idx, '이미지파일명'].split('.')
    img = open_image(f'{IMG_PATH}/{IMG_NAME}.png', basewidth=300)
    hashtags_text = ', '.join(update_df['해시태그'][idx])

    current_ENTRY.delete(0, len(str(get_idx + 1)))
    current_ENTRY.insert(0, str(idx + 1))
    image_LABEL.config(image=img)
    hashtags_TEXT.delete(0.0, tkinter.END)
    hashtags_TEXT.insert(0.0, hashtags_text)

    if update_df.loc[idx, '확인여부'] == True:
        check_BUTTON1.select()
    else:
        check_BUTTON1.deselect()
    if update_df.loc[idx, '삭제여부'] == True:
        check_BUTTON2.select()
    else:
        check_BUTTON2.deselect()
    if update_df.loc[idx, '광고여부'] == True:
        check_BUTTON3.select()
    else:
        check_BUTTON3.deselect()



ROOT_PATH = './'
DATAFRAME_FILENAME = 'insta_df.pkl'
DATAFRAME_PATH = f'{ROOT_PATH}preprocessed/dataframe/{DATAFRAME_FILENAME}'
NEW_IMAGE_DIR_PATH = f'{ROOT_PATH}preprocessed/image_png'

df = joblib.load(DATAFRAME_PATH)
df['이미지파일명'] = df['이미지파일명'].apply(out_jpg)

# 수정용 파일과 비교해서 오픈(앵간하면 update_df.pkl업데이트 하고 시작하자.)
UPDATE_DATAFRAME_FILENAME = 'update_df.pkl'
UPDATE_DATAFRAME_PATH = f'{ROOT_PATH}preprocessed/dataframe/{UPDATE_DATAFRAME_FILENAME}'
try:
    update_df = joblib.load(UPDATE_DATAFRAME_PATH)
    print('기존 데이터(update_df.pkl)를 불러옵니다.')
    if len(update_df) != len(df):
        print('업데이트 되지 않은 update_df.pkl입니다. 업데이트를 먼저 실시하세요.')

except:
    print('update_df.pkl 생성.')
    update_df = df.copy()
    joblib.dump(update_df, UPDATE_DATAFRAME_PATH)


window = tkinter.Tk()
window.title("해시태그 수동 전처리")
window.geometry("1000x800+100+100")
window.resizable(True, True)

# 초기 셋팅
idx = 0 
total_page = len(update_df)
IMG_PATH = NEW_IMAGE_DIR_PATH
IMG_NAME, _ = update_df.loc[idx, '이미지파일명'].split('.')

img = open_image(f'{IMG_PATH}/{IMG_NAME}.png', basewidth=300)
hashtags_text = ', '.join(update_df['해시태그'][idx])


# 레이아웃
image_LABEL = tkinter.Label(window, image=img)

current_ENTRY = tkinter.Entry(window, width=10)
current_ENTRY.insert(0, str(idx + 1))
current_ENTRY.bind('<Return>', change_page_func)

current_page_num = tkinter.Label(window, text=f"/ {total_page}")

next_page_BUTTON = tkinter.Button(window,
                                  text='다음 게시글>',
                                  overrelief="solid", width=15,
                                  command=next_page, repeatdelay=1000, repeatinterval=100, borderwidth=4)

fast_next_page_BUTTON = tkinter.Button(window,
                                  text='다다음 게시글>>',
                                  overrelief="solid", width=15,
                                  command=fast_next_page, repeatdelay=1000, repeatinterval=100, borderwidth=4)
backward_page_BUTTON = tkinter.Button(window,
                                           text='<이전 게시글',
                                           overrelief="solid", width=15,
                                           command=backward_page, repeatdelay=1000, repeatinterval=100, borderwidth=4)

fast_backward_page_BUTTON = tkinter.Button(window,
                                           text='<<이이전 게시글',
                                           overrelief="solid", width=15,
                                           command=fast_backward_page, repeatdelay=1000, repeatinterval=100, borderwidth=4)


update_df_BUTTON = tkinter.Button(window,
                                   text='$수정사항 저장$',
                                   overrelief="solid", width=15, height=4,
                                   command=update_dataframe_func, repeatdelay=1000, repeatinterval=100, borderwidth=4)


checkVar1=tkinter.BooleanVar()
checkVar2=tkinter.BooleanVar()
checkVar3=tkinter.BooleanVar()
check_BUTTON1=tkinter.Checkbutton(window, text="확인여부", variable=checkVar1)
check_BUTTON2=tkinter.Checkbutton(window, text="삭제여부", variable=checkVar2)
check_BUTTON3=tkinter.Checkbutton(window, text="광고여부", variable=checkVar3)

hashtags_TEXT=tkinter.Text(window, wrap='word', height=10)
hashtags_TEXT.insert(tkinter.CURRENT, hashtags_text)

image_LABEL.place(x=200, y=50)
current_ENTRY.place(x=50, y=20)
current_page_num.place(x=110, y=20)

check_BUTTON1.place(x=50, y=250)
check_BUTTON2.place(x=50, y=270)
check_BUTTON3.place(x=50, y=290)

hashtags_TEXT.place(x=50, y=360)

next_page_BUTTON.place(x=425, y=500)
fast_next_page_BUTTON.place(x=425, y=546)
backward_page_BUTTON.place(x=175, y=500)
fast_backward_page_BUTTON.place(x=175, y=546)
update_df_BUTTON.place(x=300, y=500)

if update_df.loc[idx, '확인여부'] == True:
    check_BUTTON1.select()
else:
    check_BUTTON1.deselect()
if update_df.loc[idx, '삭제여부'] == True:
    check_BUTTON2.select()
else:
    check_BUTTON2.deselect()
if update_df.loc[idx, '광고여부'] == True:
    check_BUTTON3.select()
else:
    check_BUTTON3.deselect()
    
# 프로그램 실행
window.mainloop()