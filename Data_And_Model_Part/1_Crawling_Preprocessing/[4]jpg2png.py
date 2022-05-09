'''
GUI도구(Tkinter)에서는 JPG파일을 지원하지 않기 때문에
'''
import joblib
from PIL import Image
import os
from multiprocessing import Process

ROOT_PATH = './'
DATAFRAME_FILENAME = 'insta_df.pkl'
DATAFRAME_PATH = f'{ROOT_PATH}preprocessed/dataframe/{DATAFRAME_FILENAME}'
IMAGE_DIR_PATH = f'{ROOT_PATH}preprocessed/image'
df = joblib.load(DATAFRAME_PATH)
PNG_DIR = f'{ROOT_PATH}preprocessed/image_png'

try:
    os.makedirs(PNG_DIR)
except OSError:
    print('이미 존재합니다')


def work(id, start, end, df):
    temp_df = df.loc[start:end]
    for idx, file_name in zip(temp_df.index, temp_df['이미지파일명'].values):
        im = Image.open(f'{IMAGE_DIR_PATH}/{file_name}').convert('RGB')
        origin_file_name, _ = file_name.split('.')
        im.save(f'{PNG_DIR}/{origin_file_name}.png', 'png')
        print(idx, file_name)
    return


if __name__ == "__main__":
    total_len = len(df)
    th1 = Process(target=work, args=(1, 0, total_len//4 * 1, df))
    th2 = Process(target=work, args=(2, total_len//4 * 1, total_len//4 * 2, df))
    th3 = Process(target=work, args=(3, total_len//4 * 2, total_len//4 * 3, df))
    th4 = Process(target=work, args=(4, total_len//4 * 3, total_len, df))

    th1.start()
    th2.start()
    th3.start()
    th4.start()
    
    th1.close()
    th2.close()
    th3.close()
    th4.close()
    
    th1.join()
    th2.join()
    th3.join()
    th4.join()