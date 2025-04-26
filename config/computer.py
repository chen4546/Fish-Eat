FISH_CLASSES = {
    # 分类名称: (筛选条件, 各阶段权重[幼鱼期, 成长期, 成熟期, 霸主期])
    'small': [
        {'name': 'fish1', 'size_range': (20, 40), 'speed_range': (4, 6)},
        {'name': 'fish2', 'size_range': (30, 50), 'speed_range': (3, 5)},
    ],
    'medium': [
        {'name': 'fish3', 'size_range': (50, 80), 'speed_range': (3, 4)},
        {'name': 'fish4', 'size_range': (60, 100), 'speed_range': (2, 3)},
    ],
    'large': [
        {'name': 'fish5', 'size_range': (100, 160), 'speed_range': (1, 2)},
        {'name': 'fish6', 'size_range': (150, 200), 'speed_range': (1, 1)},
    ],
    'special': [
        {'name': 'fish7', 'size_range': (40, 60), 'speed_range': (5, 6)},
        {'name': 'fish8', 'size_range': (80, 120), 'speed_range': (2, 4)},
        {'name': 'fish9', 'size_range': (20, 80), 'speed_range': (3, 5)},
    ]
}

STAGE_WEIGHTS = {
    'class_weights': [
        [0.7, 0.2, 0.05, 0.05],  # 幼鱼期: 小70%, 中20%, 大5%, 特殊5%
        [0.4, 0.4, 0.1, 0.1],    # 成长期
        [0.2, 0.3, 0.3, 0.2],    # 成熟期
        [0.1, 0.2, 0.4, 0.3]     # 霸主期
    ],
    'inner_weights': {
        'small': [0.6, 0.4],      # fish1:60%, fish2:40%
        'medium': [0.5, 0.5],     # 中型鱼各50%
        'large': [0.7, 0.3],      # fish5:70%, fish6:30%
        'special': [0.4, 0.4, 0.2] # fish7:40%, fish8:40%, fish9:20%
    }
}