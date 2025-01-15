#!usr/bin/evn python
# -*- cording: utf-8 -*-

import os
import sys

import pandas as pd
from packages.voice_file import VoiceFile
from packages.features_data import FeaturesData
from packages.indicator import Indicator
from packages.speech_recognizer import SpeechRecognizer


class ConversationAnalyser:
    """
    会話の分析を行うクラス
    """

    def __init__(self, voice_file_path, info_file_path, file_name):
        """
        コンストラクタ
        :param voice_file_path: 音声ファイルのパス
        :param info_file_path: 音声ファイルの発話情報
        :param file_name: 音声ファイル名
        """
        # 分析結果
        self.df_result = pd.DataFrame()

        # 音声ファイル処理オブジェクト
        self.voice_file = VoiceFile(
            voice_file_path=voice_file_path,
            info_file_path=info_file_path,
            file_name=file_name
        )

        # 音声認識オブジェクト
        self.speech_recognizer = SpeechRecognizer()

        # 特徴量オブジェクト
        self.features = FeaturesData()

    def get_analyze_result(self):
        """
        分析結果のDataFrameを返す
        """
        return self.df_result

    def analyse(self):
        """
        分析処理を実行する
        """
        # ファイルの分割
        self.voice_file.save_split_wav()

        # 音声認識
        self.speech_recognizer.recognize(self.voice_file.get_sqlit_file_paths())

        # 特徴量を取得
        self.features.calc_features(self.voice_file.get_sqlit_file_paths())

        # 分割したファイルを削除
        self.voice_file.remove_split_file_dir()

        # 発話情報と音声認識結果を結合
        self.df_result = pd.concat([self.voice_file.get_conversation_info(), self.speech_recognizer.get_recognize_result()], axis=1)
        # 特徴量を結合
        self.df_result = pd.concat([self.df_result, self.features.get_features_result()], axis=1)
        # print(self.df_result)

        # 指標を算出する
        indicator = Indicator(df_voice_info=self.df_result)
        indicator.get_indicator()
        # print(self.df_result)

        # 指定した秒数ごとの指標を算出する
        # indicator.calc_interval_indicator(60)

        self.df_result = indicator.get_indicator_result()


