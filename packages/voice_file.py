#! usr/bin/env python
# -*- cording: utf-8 -*-

import os
import settings
import pandas as pd
from pydub import AudioSegment
from .files import create_dir, get_file_paths, remove_dir
from .natural_sort import natural_sort


class VoiceFile:
    """
    音声ファイル情報の管理を行う
    """
    def __init__(self, voice_file_path, info_file_path, file_name):
        """
        音声ファイルに関する情報を格納する．
        :param voice_file_path: 音声ファイルのパス
        :param info_file_path: 音声の発話情報のファイルのパス
        :param file_name: 音声ファイルのパス
        """
        # 発話情報
        self.df_speech_info = pd.read_csv(info_file_path)

        # 音声ファイル
        # もし音声ファイルがwavじゃなかったからこの関数を実行
        voice_file_path = self.convert_to_wav(voice_file_path)
        self.wav_file = AudioSegment.from_wav(voice_file_path)
        # return 0
        # 分割したファイル名のリスト
        self.file_path_list = None

        # 音声ファイル名
        self.file_name = file_name

        # 分割ファイルの保存先
        self.split_file_dir = None

    def convert_to_wav(self,voice_file_path):
        # ファイルの拡張子を確認
        file_name, file_extension = os.path.splitext(voice_file_path)
        
        # もし拡張子が.wavでない場合、変換する
        if file_extension.lower() != '.wav':
            # pydubでファイルを読み込む（拡張子に応じた読み込み）
            audio = AudioSegment.from_file(voice_file_path)
            
            # 新しい.wavファイル名を作成
            new_file_path = f"{file_name}.wav"
            
            # ファイルを.wav形式で保存
            audio.export(new_file_path, format="wav")
            print(f"変換完了: {new_file_path}")
            return new_file_path
        else:
            # 既にwavファイルの場合、そのまま返す
            print("ファイルはすでにWAV形式です。")
            return voice_file_path


    def get_conversation_file_name(self):
        """
        音声ファイル名を返す．
        """
        return self.file_name

    def get_sqlit_file_paths(self):
        """
        分割した音声ファイルのパスのリストを返す．
        """
        return self.file_path_list

    def get_conversation_info(self):
        """
        話者情報等のDataFrameを返す．
        """
        return self.df_speech_info

    def save_split_wav(self):
        """
        ファイルを分割して保存する．
        """
        # 分割ファイルの保存先
        self.split_file_dir = f"{settings.ROOT_DIR}{os.sep}data{os.sep}tmp"
        create_dir(self.split_file_dir)

        # 音声ファイルを分割して保存
        """
        現在は2人が同時にしゃべってしまった場合の処理ができず，どちらか片方の発話として処理するしかない
        """
        for index, row in self.df_speech_info.iterrows():
            # print(row['start'], row['end'])
            if row['end'] - row['start'] == 0:
                export_wav = self.wav_file[row['start']*1000-500: row['end']*1000+500]
            else:
                export_wav = self.wav_file[row['start']*1000:row['end']*1000]
            export_wav.export(f'{self.split_file_dir}{os.sep}{self.file_name}_{index}.wav', format="wav")

        # 分割したファイル名を取得
        self.file_path_list = get_file_paths(self.split_file_dir)
        self.file_path_list = natural_sort(self.file_path_list)

    def remove_split_file_dir(self):
        """
        分割したファイルのディレクトリを削除する．
        """
        remove_dir(self.split_file_dir)
