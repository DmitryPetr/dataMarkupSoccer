teams = ['Gliders2016', 'HELIOS2016']
# teams = ['Oxsy', 'HELIOS2016']
# teams = ['Oxsy', 'HfutEngine2017']
sizeTeam = 11
gridLen = 6
gridWidth = 4
resultForPlayerColumn = [
    'time',
    'x',
    'y',
    'angle',
    'xBall',
    'yBall',
    'opponentVector',
    'teamVector',
    'sideTeam',
    'strategyOpponent'
]
strategyList = [
    {'label': 'Верхняя угловая атака', 'value': 'UpCornerAttack'},
    {'label': 'Нижняя угловая атака', 'value': 'DownCornerAttack'},
    {'label': 'Лобовая атака близи ворот', 'value': 'FrontalAttackNGate'},
    {'label': 'Верхняя боковая атака', 'value': 'UpSideAttack'},
    {'label': 'Нижняя боковая атака', 'value': 'DownSideAttack'},
    {'label': 'Лобовая атака (центр поля)', 'value': 'FrontalAttackGate'},
    {'label': 'Защита верхнего центрального участка', 'value': 'UpCenterSideSave'},
    {'label': 'Защита нижнего центрального участка', 'value': 'DownCenterSideSave'},
    {'label': 'Защита центра поля', 'value': 'CenterSideSave'},
    {'label': 'Защита верхнего угла поля', 'value': 'UpSaveGate'},
    {'label': 'Защита нижнего угла поля', 'value': 'DownSaveGate'},
    {'label': 'Защита от фронтальной атаки', 'value': 'FrontalSaveGate'}
]

strategyOnlyList = [
    'UpCornerAttack',
    'DownCornerAttack',
    'FrontalAttackNGate',
    'UpSideAttack',
    'DownSideAttack',
    'FrontalAttackGate',
    'UpCenterSideSave',
    'DownCenterSideSave',
    'CenterSideSave',
    'UpSaveGate',
    'DownSaveGate',
    'FrontalSaveGate',
]

strategyMergeList = [
    {
        'label': 'Атака вблизи ворот',
        'value': 'NearGateAttack',
        'valueMerge': ['UpCornerAttack', 'DownCornerAttack', 'FrontalAttackNGate']
     },
    {
        'label': 'Атака центра поля',
        'value': 'MiddleFieldAttack',
        'valueMerge': ['UpSideAttack', 'DownSideAttack', 'FrontalAttackGate']
     },
    {
        'label': 'Защита центра поля',
        'value': 'MiddleFieldSave',
        'valueMerge': ['UpCenterSideSave', 'DownCenterSideSave', 'CenterSideSave']
     },
    {
        'label': 'Защита вблизи ворот',
        'value': 'SaveNearGate',
        'valueMerge': ['UpSaveGate', 'DownSaveGate', 'FrontalSaveGate']
    },
]