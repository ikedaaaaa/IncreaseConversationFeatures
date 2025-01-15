#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys
from unittest import result
import settings
import pandas as pd
from .signals import Signals
import numpy as np


class Indicator:
    """
    指標や発話シグナルを計算する．
    """

    def __init__(self, df_voice_info):
        """
        コンストラクタ．
        :param df_voice_info: 音声情報データ
        """
        self.df_voice_info = df_voice_info
        self.df_indicator = None


    def get_indicator_result(self):
        """
        指標計算結果のDataFrameを返す．
        """
        return self.df_indicator

    def get_indicator(self):
        """
        指標を算出する．
        """
        # 無音時間の算出
        self._calc_silent_time()

        # 発話シグナルと指標の算出
        self.df_indicator = pd.concat([self.df_voice_info, calc_indicator(self.df_voice_info)], axis=1)


    def _calc_silent_time(self):
        """
        無音時間を算出してデータに加える．
        """
        tmp = []
        columns = self.df_voice_info.columns
        before = None
        for index, row in self.df_voice_info.iterrows():
            # print(index)
            if index != 0 and before['end'] != row['start']:
            # if index != 0 and before['end'] < row['start']: #こうすれば会話のかぶせも考慮できる?
                tmp.append([before['end'], row['start'], 'silent', '0'])
            before = row
            tmp.append(list(row))
        self.df_voice_info = pd.DataFrame(tmp, columns=columns)


    def calc_interval_indicator(self, interval):
        """
        指定した秒数にデータを分割して指標を算出する．
        :param df_voice_info: 音声情報データ
        :param interval: 指標の算出を行う区間
        """
        # データの分割処理
        divided_data_list = divide_data(df_voice_info=self.df_voice_info, interval=interval)
        # print(divided_data_list)

        # 各データに対して指標計算処理を行う．
        interval_data_result = pd.DataFrame()
        for interval_data in divided_data_list:
            # print(interval_data)
            indicator = Indicator(interval_data)
            indicator.get_indicator()
            result_data = indicator.get_indicator_result()
            # 区間内最後のデータで統一する．
            last_index_num = len(result_data) - 1
            for index in range(0, last_index_num):
                result_data.loc[index] = result_data.loc[last_index_num]
            interval_data_result = pd.concat([interval_data_result, result_data])
            # print(interval_data_result)

        # 算出した区間データの部分だけ取り出す．
        interval_data_result.reset_index(inplace=True, drop=True)
        del interval_data_result['index']
        interval_data_result = interval_data_result.loc[:, "total_silent_time":]
        interval_data_result.columns = [f'interval_{i}' for i in interval_data_result.columns]
        self.df_indicator = pd.concat([self.df_indicator, interval_data_result], axis=1)


def init_accumulation_data(speaker_list):
    """
    会話の登場人物ごとの累積データを格納する辞書を作成．
    :param speaker_list:
    :return: speaker_data_dict: 各人の発話シグナルを格納した辞書
    """

    speaker_data_dict = {}
    for i in speaker_list:
        speaker_data_dict[i] = Signals()

    return speaker_data_dict


def calc_indicator(df):

    # 各人の累計データ
    speaker_list = list(set(df['person']))
    person_list = list(set(df['person']) - set(['silent']))
    speaker_data_dict = init_accumulation_data(speaker_list=speaker_list)

    # 算出結果
    df_calculated = pd.DataFrame()

    # 指標と発話シグナルを算出
    change_speaker_counter = 0
    tmp_speaker = None
    tmp_speech_time = []
    first_time = None
    row_count = 0
    for index, row in df.iterrows():
        if index == 0:first_time = row['start']
        # print(row)
        # 発話時間
        speech_time = calc_speech_time(end=row['end'], start=row['start'])
        speaker_data_dict[row['person']].speech_time.append(speech_time)
        df_calculated.loc[index, 'speech_time'] = speech_time

        # # 合計の発話時間
        # df_calculated.loc[index, 'total_speech_time'] = row['end'] - first_time

        # 発話速度
        speech_speed = calc_speech_speed(df_calculated.loc[index, 'speech_time'], row['word_count'])
        speaker_data_dict[row['person']].speech_speed.append(speech_speed)
        df_calculated.loc[index, 'speech_speed'] = speech_speed

        # 無音時間合計
        try:
            df_calculated.loc[index, 'total_silent_time'] = sum(speaker_data_dict['silent'].speech_time)
        except KeyError:
            df_calculated.loc[index, 'total_silent_time'] = 0


        # 話者交代回数と最長連続発話時間
        if row['person'] == "silent":
            pass
        elif index == 0:
            tmp_speaker = row['person']
            tmp_speech_time.append(speech_time)
        elif row['person'] == tmp_speaker:
            tmp_speech_time.append(speech_time)
        elif row['person'] != tmp_speaker:
            if speaker_data_dict[tmp_speaker].longest_speech_time < sum(tmp_speech_time):
                speaker_data_dict[tmp_speaker].longest_speech_time = sum(tmp_speech_time)
            tmp_speech_time = [speech_time]
            tmp_speaker = row['person']
            change_speaker_counter += 1

        df_calculated.loc[index, 'count_change_speaker'] = change_speaker_counter


        # ここから下は今まで通り話者が二人の場合を想定して書いてます．
        if len(person_list) > 2:
            continue
        
        # 発話比率
        df_calculated.loc[index, 'speech_balance'] = calc_speech_balance(
            sum(speaker_data_dict[person_list[0]].speech_time),
            sum(speaker_data_dict[person_list[1]].speech_time)
        )

        # 発話速度比率
        df_calculated.loc[index, 'speech_earnest'] = calc_speech_earnest(
            sum(speaker_data_dict[person_list[0]].speech_speed),
            sum(speaker_data_dict[person_list[1]].speech_speed)
        )

        # 最長発話時間比率
        df_calculated.loc[index, 'speech_advantage'] = calc_speech_advantage(
            speaker_data_dict[person_list[0]].longest_speech_time,
            speaker_data_dict[person_list[1]].longest_speech_time,
        )

        # OKデータとの相関係数
        ok_data_set = pd.read_csv(f'{settings.ROOT_DIR}{os.sep}data{os.sep}ok_ng_data{os.sep}ok_data.csv')
        for j, ok_data in ok_data_set.iterrows():
            corrcoef = np.corrcoef(
                list(ok_data),
                list(df_calculated.loc[index, ['speech_balance', 'speech_advantage', 'speech_earnest']])
            )
            df_calculated.loc[index, f'correlation_coefficient_ok{j}'] = corrcoef[0][1]
            # print(corrcoef)

        # NGデータとの相関係数
        ng_data_set = pd.read_csv(f'{settings.ROOT_DIR}{os.sep}data{os.sep}ok_ng_data{os.sep}ng_data.csv')
        for j, ng_data in ng_data_set.iterrows():
            corrcoef = np.corrcoef(
                list(ng_data),
                list(df_calculated.loc[index, ['speech_balance', 'speech_advantage', 'speech_earnest']])
            )
            df_calculated.loc[index, f'correlation_coefficient_ng{j}'] = corrcoef[0][1]
            # print(corrcoef)

        # ここから下で区間ごとの計算を行う．


    # print(df_calculated)

    return df_calculated


def calc_speech_time(end, start):
    """
    発話時間を算出する.
    発話時間が1秒に満たない場合は1秒にする.
    """
    diff = float(end) - float(start)
    diff = 1 if diff == 0 else diff
    return diff


def calc_speech_speed(speech_time, word_count):
    """
    発話速度を算出する．
    :param speech_time: 発話時間
    :param word_count: 発話文字数
    :return: 発話速度
    """
    try:
        return float(word_count) / float(speech_time)
    except ZeroDivisionError:
        return 0


def calc_speech_balance(speech_time_1, speech_time_2):
    """
    発話時間比率を算出する
    :param speech_time_1: 一人目のデータ
    :param speech_time_2: 二人目のデータ
    :return: 発話時間比率
    """

    sum_speech_time = speech_time_1 + speech_time_2
    try:
        return (speech_time_1 / sum_speech_time) / (speech_time_2 / sum_speech_time)
    except ZeroDivisionError:
        return 0


def calc_speech_earnest(speech_speed_1, speech_speed_2):
    """
    発話時間比率を算出する
    :param speech_speed_1: 一人目のデータ
    :param speech_speed_2: 二人目のデータ
    :return: 発話速度比率
    """

    sum_speech_speed = speech_speed_1 + speech_speed_2
    try:
        return (speech_speed_1 / sum_speech_speed) / (speech_speed_2 / sum_speech_speed)
    except ZeroDivisionError:
        return 0


def calc_speech_advantage(longest_speech_time_1, longest_speech_time_2):
    """
    最長発話時間比率
    :param longest_speech_time_1: 一人目のデータ
    :param longest_speech_time_2: 二人目のデータ
    :return: 最長発話時間比率
    """
    sum_longest_speech_time = longest_speech_time_1 + longest_speech_time_2
    try:
        return (longest_speech_time_1 / sum_longest_speech_time) / (longest_speech_time_2 / sum_longest_speech_time)
    except ZeroDivisionError:
        return 0


def divide_data(df_voice_info, interval):
    """
    指定した秒数にデータを分割してリストに格納していく
    :param df_voice_info: 音声情報データ
    :param interval: 指標の算出を行う区間
    """
    # データの分割処理
    divided_data_list = []
    interval_data = pd.DataFrame()
    for index, row in df_voice_info.iterrows():
        if index == 0:
            tmp_time = row['start']
        elif row['start'] - tmp_time > interval:
            interval_data.reset_index(inplace=True)
            divided_data_list.append(interval_data)
            interval_data = pd.DataFrame()
            tmp_time = row['start']
        
        interval_data = pd.concat([interval_data, pd.DataFrame([row])])
    
    return divided_data_list


def main():
    data = pd.read_csv(f'{settings.ROOT_DIR}{os.sep}data{os.sep}test_file.csv')
    # indicator = Indicator(data, 300)
    # indicator.calc_indicator()


if __name__ == '__main__':
    sys.exit(main())


