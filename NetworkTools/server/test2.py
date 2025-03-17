data = {
    'Layer': 1,
    'FightData': {
        'Version': 'beta4-1',  # 版本号，固定参数
        'FightType': 2,  # 战斗类型固定
        'RandSeed': 929866,  # 随机种子(游戏服生成) -取S2C_StartFightRes返回的
        'LevelID': 50001,  # 关卡id，动态入参
        'ResultType': 1,  # 战斗结果 1：胜利 2失败，固定1
        'BlueUnitLog': [
            {'UnitID': 24008, 'Count': 1, 'FightValue': 426215, 'AtkDamage': 3946543, 'Star': 25, 'Level': 300},
            {'UnitID': 24019, 'Count': 1, 'FightValue': 452858, 'AtkDamage': 208736, 'ByDamage': 3, 'Star': 25,
             'Level': 300},
            {'UnitID': 24020, 'Count': 1, 'FightValue': 248675, 'AtkDamage': 193183, 'Star': 20, 'Level': 240},
            {'UnitID': 24026, 'Count': 1, 'FightValue': 260717, 'AtkDamage': 183105, 'Star': 20, 'Level': 240},
            {'UnitID': 24037, 'Count': 1, 'FightValue': 549608, 'Star': 25, 'Level': 300}],  # 蓝队战斗日志,我方
        'RedUnitLog': [
            {'UnitID': 23001, 'Count': 1, 'FightValue': 3208, 'AtkDamage': 3, 'ByDamage': 245293, 'Star': 4,
             'Level': 25},
            {'UnitID': 11001, 'Count': 19, 'FightValue': 1368, 'ByDamage': 4286274}],  # 红队战斗日志，对战阵容
        'FightTime': 2,  # 战斗耗时
        'FightFrame': 44,  # 战斗帧数
        'BlueUnitSum': {'Count': 5, 'FightValue': 1938073, 'AtkHurt': 4531567, 'ByHurt': 3,
                        'Heros': [{'CardGuid': 1730, 'CurHP': 9997, 'CurNuQi': 7719},
                                  {'CardGuid': 2516, 'CurHP': 9997, 'CurNuQi': 3178},
                                  {'CardGuid': 1050, 'CurHP': 10000, 'CurNuQi': 7758},
                                  {'CardGuid': 225, 'CurHP': 10000, 'CurNuQi': 4558},
                                  {'CardGuid': 21247, 'CurHP': 9997, 'CurNuQi': 2998}]},  # 蓝队战斗数据汇总,我方
        'RedUnitSum': {'Count': 20, 'FightValue': 4576, 'AtkHurt': 3, 'ByHurt': 4531567,
                       'Heros': [{'CardGuid': 23001, 'CurNuQi': 10000}]},  # 红队战斗数据汇总，敌方
        'FrameRate': 15,  # 当前战斗的时间帧率
        'LogicFrame': 44}  # 逻辑帧数
}
