#!usr/bin/env python
# -*- cording: utf-8 -*-

from surfboard.sound import Waveform
import librosa
from librosa.display import specshow
import librosa.feature as f
import pandas as pd
import numpy as np
from .features_columns import feature_columns


class FeaturesData:
    """
    音声特徴量の取得を行う
    """

    def __init__(self):

        # 取得した特徴量
        self.result_features = None

    def get_features_result(self):
        """
        特徴量取得結果のDataFrameを返す
        """
        return self.result_features

    def calc_features(self, path_list):
        """
        特徴量を取得する
        :param path_list:ファイルのパスのリスト
        """
        features_list = []
        for path in path_list:
            # print(path)
            tmp_list = []

            # 音声ファイル読み込み
            try:
                y, sr = librosa.load(path)
                sound = Waveform(path=path, sample_rate=44100)
            except ValueError as e:
                print(e)
                features_list.append(tmp_list)
                continue
            
            # RMS（音のエネルギーを算出．音量代わり）
            tmp_list += calc_rms(y=y)

            # 基本周波数の推定
            # 最小周波数と最大周波数（人の話し声が大体100Hzから300Hz）
            fmin, fmax = 100, 300
            # 基本周波数推定アルゴリズム　YIN，確率的YIN
            tmp_list += calc_yin(y, fmin=fmin, fmax=fmax)
            tmp_list += calc_pyin(y, fmin=fmin, fmax=fmax)

            # ZeroCrossingRateを算出
            tmp_list += calc_zero_crossing_rate(y)

            # jitterを算出
            tmp_list += calc_jitters(sound=sound)

            # shimmerを算出
            tmp_list += calc_shimmers(sound=sound)

            # harmonics-to-noise rateを算出
            tmp_list.append(calc_hnr(sound=sound))

            # mfccとmelspectrogramを算出
            n_mfcc = 20
            tmp_list += calc_mfcc(y, sr=sr, n_mfcc=n_mfcc)
            tmp_list += calc_melspectrogram(y, sr=sr, n_mfcc=n_mfcc)

            # 結果に格納する
            features_list.append(tmp_list)
        
        # 列名を設定する．
        columns = feature_columns
        columns += [f'mfcc{i}' for i in range(n_mfcc)]
        columns += [f'mel{i}' for i in range(n_mfcc)]
        self.result_features = pd.DataFrame(features_list, columns=columns)
        # print(self.result_features)


def calc_zero_crossing_rate(y):
    """
    音声信号が何回0を横切ったかの回数/フレームサイズのレートを算出する．
    librosaのフレーム数のデフォは2048
    :return: [rateの平均，rateの最大値，rateの最小値]
    """
    try:
        rate = f.zero_crossing_rate(y=y)[0]
        rate = rate[~np.isnan(rate)]
        return [rate.mean(), rate.max(), rate.min()]
    except:
        return [0] * 3


def calc_pyin(y, fmin, fmax):
    """
    基本周波数を推定する．アルゴリズムには確率的YINを使用．
    :param fmin: 周波数の下限
    :param fmax: 周波数の上限
    :return: [pyinの平均, pyinの最大値, pyinの最小値]
    """
    try:
        fo_pyin, voiced_flag, voiced_prob = librosa.pyin(y, fmin=fmin, fmax=fmax)
        fo_pyin = fo_pyin[~np.isnan(fo_pyin)]
        return [fo_pyin.mean(), fo_pyin.max(), fo_pyin.min()]
    except:
        return [0] * 3


def calc_yin(y, fmin, fmax):
    """
    基本周波数を推定する.アルゴリズムにはYINを使用.
    :param fmin: 周波数の下限
    :param fmax: 周波数の上限
    :return: [yinの平均, yinの最大値, yinの最小値]
    """
    try:
        fo_yin = librosa.yin(y, fmin=fmin, fmax=fmax)
        fo_yin = fo_yin[~np.isnan(fo_yin)]
        return [fo_yin.mean(), fo_yin.max(), fo_yin.min()]
    except:
        return [0] * 3


def calc_rms(y):
    """
    音のエネルギー, RMS（root-mean-square）を算出する
    :return: [rmsの平均, rmsの最大値, rmsの最小値]
    """
    try:
        rms = f.rms(y=y)[0]
        rms = rms[~np.isnan(rms)]
        return [rms.mean(), rms.max(), rms.min()]
    except:
        return [0] * 3


def calc_mfcc(y, sr, n_mfcc):
    """
    メル周波数ケプストラム係数を算出する
    :return: メル周波数ケプストラム係数の平均
    """
    try:
        mfcc = f.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        result = []
        for data in mfcc:
            result.append(data.mean())
        return result
    except:
        return [0] * n_mfcc


def calc_melspectrogram(y, sr, n_mfcc):#calc_log_melspectrogramからcalc_melspectrogramに変更
    """
    melspectrogramを算出する. mfccの離散コサイン変換を行わないバージョン．
    :return: melspectrogramの各次元の平均
    """
    try:
        melspectrogram = f.melspectrogram(y=y, sr=sr, n_mels=n_mfcc)
        result = []
        for data in melspectrogram:
            result.append(data.mean())
        return result
    except:
        return [0] * n_mfcc


def calc_jitters(sound):
    """
    jitterを算出する．
    :return: jitterの値を格納したリスト
    """
    try:
        jitter = sound.jitters()
        # print(jitter)
        result = []
        for key, value in jitter.items():
            if value is None:
                result.append(0)
            else:
                result.append(value*100) #*1000から100に変更
        return result
        # print(result)
    except:
        return [0] * 5


def calc_shimmers(sound):
    """
    shimmersを算出する．
    :return: shimmerの値を格納したリスト
    """
    try:
        shimmers = sound.shimmers()
        # print(shimmers)
        result = []
        for key, value in shimmers.items():
            # print(value)
            if value is None:
                result.append(0)
            elif key == 'localdbShimmer': #dBの場合は%ではないため*100をしない
                result.append(value)
            else:
                result.append(value*100)#*1000から*100に変更
        # print(result)

        return result
    except:
        return [0] * 5


def calc_hnr(sound):
    """
    Harmonics-to-noise rateを算出する．
    :return: hnrの値
    """
    try:
        hnr = sound.hnr()
        return hnr
    except:
        return 0


# def calc_chroma_stft(y, sr):
#     """
#     フーリエ変換でクロマグラムの算出．各Binの平均を算出する．
#     :return: 算出結果[クロマ1，クロマ2，..., クロマ12]
#     """
#     chroma = f.chroma_stft(y=y, sr=sr)
#     result = []
#     for data in chroma:
#         # print(len(data))
#         result.append(data.mean())
#     return result


# def calc_chroma_constant_q(y, sr):
#     """
#     定Q変換でクロマグラムを算出．各Binの平均を算出する．
#     :return: 算出結果[クロマ1，クロマ2，..., クロマ12]
#     """
#     chroma = f.chroma_cqt(y=y, sr=sr)
#     result = []
#     for data in chroma:
#         # print(len(data))
#         result.append(data.mean())
#     return result


# def calc_chroma_cens(y, sr):
#     """
#     正規化したクロマグラムを算出．各Binの平均を算出する．
#     :return: 算出結果[クロマ1，クロマ2，..., クロマ12]
#     """
#     chroma = f.chroma_cens(y=y, sr=sr)
#     result = []
#     for data in chroma:
#         # print(len(data))
#         result.append(data.mean())
#     return result


# def test_plot(data, sr):
#     fig, ax = plt.subplots()
#     data = librosa.power_to_db(data, ref=np.max)
#     # print(pd.DataFrame(data))
#     img = librosa.display.specshow(data, x_axis='time',
#                                    y_axis='mel', sr=sr, ax=ax)
#     fig.colorbar(img, ax=ax, format='%+2.0f dB')
#     ax.set(title='Mel-frequency spectrogram')
#     plt.show()
