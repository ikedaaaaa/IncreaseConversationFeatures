#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys
from packages.files import save_csv
import settings
import pandas as pd

from packages.conversation_analyser import ConversationAnalyser


def main(args):
    # 音声ファイル名取得
    file_name = os.path.splitext(os.path.basename(args[0]))[0]

    # ファイルの情報を管理するオブジェクトを作成
    conversation_analyser = ConversationAnalyser(
        voice_file_path=args[0],
        info_file_path=args[1],
        file_name=file_name
    )

    # 分析を実行
    conversation_analyser.analyse()

    #結果をcsvに保存
    result = conversation_analyser.get_analyze_result()
    save_csv(df=result, path=f'{settings.ROOT_DIR}{os.sep}data{os.sep}{file_name}_result.csv')


if __name__ == '__main__':
    # python main.py {音声ファイルのパス} {話者情報のcsvのパス}
    # 例：python main.py ./data/test_file.wav ./data/test_file_info.csv
    sys.exit(main(sys.argv[1:3]))
