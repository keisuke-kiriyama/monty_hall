# --- coding: utf-8 ---

import pandas as pd
from pandas import DataFrame, Series
import random


def explanation_of_expected_value():
    print('*' * 80)
    explain1 = '''
    
    ３つの扉をA,B,Cとする。
    プレーヤーが選択するドアをAとし、BとCの場合はAと同様なので
    Aのみ考慮した時の期待値と、３つのドアを選択した時の期待値は
    同じになるためAを選択した場合のみ考慮する。

    この時起こりうる事象は次の４通りである。
    ① 正解 : A(1/3)     モンティが選ぶドア : B       モンティが選ぶドアの確率 : 1/2
    ② 正解 : A(1/3)     モンティが選ぶドア : C       モンティが選ぶドアの確率 : 1/2
    ③ 正解 : B(1/3)     モンティが選ぶドア : C       モンティが選ぶドアの確率 : 1 (モンティが選ぶドアは正解でない、プレーヤーの選択でないものなのでCのみ)
    ④ 正解 : C(1/3)     モンティが選ぶドア : B       モンティが選ぶドアの確率 : 1 (モンティが選ぶドアは正解でない、プレーヤーの選択でないものなのでBのみ)
    それぞれの事象が起こる確率をまとめると、次の表のようになる。
    
    (これから出てくる表の各列名は以下に対応する
    correct = 正解の扉
    rate_of_correct_door = その扉が正解として選ばれる確率
    monty_choice = モンティの選択
    rate_of_monty_choice = モンティに選ばれる確率
    event_prob = このcaseが起こる確率
    no_change = 変更しない
    change = 変更する)
    
    '''
    print(explain1)
    events = {'correct': ['A', 'A', 'B', 'C'],
             'rate_of_correct_door': [1 / 3, 1 / 3, 1 / 3, 1 / 3],
             'monty_choice': ['B', 'C', 'C', 'B'],
             'rate_of_monty_choice': [1 / 2, 1 / 2, 1, 1]
             }
    pd.set_option('display.width', 300)
    df_event = DataFrame(events, index=['case1', 'case2', 'case3', 'case4'])
    event_prob = Series(df_event.loc[:,'rate_of_correct_door'] * df_event.loc[:, 'rate_of_monty_choice'])
    df_event['event_prob'] = event_prob
    print(df_event.ix[:, ['correct', 'rate_of_correct_door', 'monty_choice',
                          'rate_of_monty_choice', 'event_prob']])

    explain2 = '''
    
    
    プレーヤーが正解する時をTrue、不正解の時をFalseとするとそれぞれのcaseについて正解不正解は
    次のようになる。
    
    
    '''
    print(explain2)

    no_change = Series(df_event.loc[:,'correct'] == 'A')
    df_event['no_change'] = no_change
    change = Series(df_event.loc[:, 'correct'] != 'A')
    df_event['change'] = change
    print(df_event.ix[:, ['correct', 'rate_of_correct_door', 'monty_choice',
                          'rate_of_monty_choice', 'event_prob', 'no_change', 'change']])

    explain3 = '''
    
    
    扉を変えない場合と変えた場合の正解する期待値は、それぞれno_changeとchangeがTrueであるcaseの、event_probの和になる。
    それぞれの期待値は以下のようになる。
    
    
    '''
    print(explain3)
    no_change_expected_value = df_event.loc[df_event.loc[:, 'no_change'], 'event_prob'].sum()
    change_expected_value = df_event.loc[df_event.loc[:, 'change'], 'event_prob'].sum()

    print('扉を変更しない場合の期待値 : ', no_change_expected_value)
    print('扉を変更した場合の期待値 : ', change_expected_value)

    explain4 = '''
    
    
    以上の結果より、扉を変更した場合の期待値は、扉を変更しない場合の期待値の２倍になることがわかる。
    よって最も期待値が高くなるプレイヤーの行動は、
    「モンティが扉を開けた後に、残っている開けられていないドアに変更する」
    となる。
    
    '''
    print(explain4)
    print('*' * 80)


class Door:
    "ドアを表すクラス"


    def __init__(self, car, opend=False):
        '''
        self.car(bool) : インスタンスのドアに車があったらTrue
        self.opend(bool) : インスタンスのドアが開けられていたらTrue
        '''
        self.car = car
        self.opend = opend


    def open_door(self):
        "ドアを開けるメソッド"
        self.opend = True



class Doors:
    "ドアのセットを表すクラス"


    def __init__(self):
        '''
        self.door_list(list) : ドアのセット
        self.car_position(int) : 車のあるドア番号
        '''
        self.door_list = []
        self.car_position = random.randint(0, 2)
        for door_number in range(3):
            if door_number == self.car_position : self.door_list.append(Door(car=True))
            else : self.door_list.append(Door(car=False))


    def check_door_selected_by_player(self, player_select):
        "playerの選択が正解かどうか返すメソッド"
        return self.car_position == player_select


    def open_door_by_monty(self, player_select):
        "モンティが、正解でないかつ選択されていないドアを開けるメソッド"
        for door_num, door in enumerate(self.door_list):
            if door_num != player_select and not(door.car):
                door.open_door()
                break


    def return_closed_door(self):
        return [i for i in range(3) if not (self.door_list[i].opend)]


class MontyGame:
    "モンティホールゲームを表すクラス"

    def __init__(self, execution_times):
        "self.execution_times(int) : ゲームの試行回数"
        self.execution_times = execution_times


    def play_monty_hall_no_change(self):
        "モンティホール問題で、プレイヤーの変更がない場合の正解回数を返す関数"
        num_of_correct = 0
        for _ in range(self.execution_times):
            doors = Doors()
            player_select = random.randint(0, 2)
            doors.open_door_by_monty(player_select)
            if doors.check_door_selected_by_player(player_select): num_of_correct += 1
        return (num_of_correct / self.execution_times) * 100

    def play_monty_hall_change(self,):
        "モンティホール問題で、プレイヤーの変更がない場合の正解回数を返す関数"
        num_of_correct = 0
        for i in range(self.execution_times):
            doors = Doors()
            player_select = random.randint(0, 2)
            doors.open_door_by_monty(player_select)
            closed_door_list = doors.return_closed_door()
            player_select = closed_door_list[0] if closed_door_list[1] == player_select else closed_door_list[1]
            if doors.check_door_selected_by_player(player_select): num_of_correct += 1
        return (num_of_correct / self.execution_times) * 100




if __name__ == '__main__':
    explanation_of_expected_value()

    print('\n\n' + '*' * 80)
    execution_times = 1000
    print('実際にモンティホール問題の試行を' + str(execution_times) + '回行う。')
    monty_game = MontyGame(execution_times)
    print('\nプレイヤーが選択を変更しなかった場合の正解率は\t{0}%'.format(monty_game.play_monty_hall_no_change()))
    print('\nプレイヤーが選択を変更した場合の正解率は\t{0}%'.format(monty_game.play_monty_hall_change()))
    print('\n\n' + '*' * 80)
