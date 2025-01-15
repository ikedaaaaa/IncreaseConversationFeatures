#!usr/bin/env python
#-*- cording: utf-8 -*-

import os
import shutil

import pandas as pd


def remove_dir(path):
    """
    指定したディレクトリの存在を確認し，あれば削除する．
    :param path: ディレクトリのパス
    """
    if os.path.isdir(path):
        shutil.rmtree(path)


def create_dir(path):
    """
    指定したディレクトリの存在を確認し，なければ作る．
    :param path: ディレクトリのパス
    """
    if not os.path.isdir(path):
        os.makedirs(path)


def remove_dir(path):
    """
    指定したディレクトリを削除
    :param path: ディレクトリのパス
    """
    shutil.rmtree(path)


def get_file_paths(path):
    """
    指定したpath内にあるファイルのpathを取得します．
    :param path: パス
    :return: ファイル名のリスト
    """

    files = os.listdir(path)
    return [os.path.join(path, f) for f in files if not f.startswith('.') and os.path.isfile(os.path.join(path, f))]


def get_directory_paths(path):
    """
    指定したpath内にあるディレクトリのpathを取得します．
    :param path: パス
    :return: ディレクトリ名のリスト
    """

    directories = os.listdir(path)
    return [os.path.join(path, d) for d in directories if not os.path.isfile(os.path.join(path, d))]


def create_save_data(start_time_list, end_time_list, word_count_list, columns):
    """
    保存するデータを作成する
    :param columns: dfの列名リスト
    :param start_time_list: 発話開始時間のリスト
    :param end_time_list: 発話終了時間のリスト
    :param word_count_list: 文字数のリスト
    :return: 作成したデータフレーム
    """

    # 結果をまとめたリストを作成
    result_list = []
    for start, end, word in zip(start_time_list, end_time_list, word_count_list):
        tmp = [start, end, word]
        result_list.append(tmp)

    return pd.DataFrame(result_list, columns=columns)


def save_csv(path, df):
    """
    作成したデータフレームをcsv形式で保存します．
    :param path: 保存先
    :param df: データフレーム
    """

    df.to_csv(path, encoding='utf-8', index=False)

