#!usr/bin/env python
# -*- cording: utf-8 -*-


class Signals:
    """
    発話シグナルを格納しておくクラス
    """

    def __init__(self):

        # 発話文字数
        self.word_count = []

        # 発話時間
        self.speech_time = []

        # 発話スピード
        self.speech_speed = []

        # 最長発話時間
        self.longest_speech_time = 0.0000001

