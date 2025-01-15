#!usr/bin/env python
# -*- cording: utf-8 -*-

import sys
import settings
import azure.cognitiveservices.speech as speechsdk
import pandas as pd


class SpeechRecognizer:
    """
    Speech To Textを行う
    """

    def __init__(self):
        # サブスクリプションキー
        self.subscription = settings.SUB_KEY

        # 地域
        self.region = "japanwest"

        # 言語
        self.language = "ja-JP"

        # SpeechConfigオブジェクト
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.subscription,
            region=self.region,
            speech_recognition_language=self.language
        )

        # 変換結果
        self.result = []

    def get_recognize_result(self):
        """
        音声認識結果のDataframeを返す．
        """
        return self.result

    def recognize(self, path_list):
        """
        音声ファイルのテキスト変換を行う
        :param path_list: ファイルのパスが格納されたリスト
        """
        for path in path_list:
            # print(path)
            audio_input = speechsdk.AudioConfig(filename=path)
            recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_input)
            result = recognizer.recognize_once_async().get()
            # print(result.text)
            self.result.append(len(result.text))

        self.result = pd.DataFrame(self.result, columns=['word_count'])


def main(args):
    # 音声認識オブジェクト作成
    speech_recognizer = SpeechRecognizer()
    speech_recognizer.recognize(["../data/tmp/chunk-10.wav"])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
