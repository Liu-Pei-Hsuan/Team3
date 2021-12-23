import numpy as np
nameALL = ['Tibame站',
           '中原大學站',
           '陽明高中站',
           '武陵高中站',
           '大竹站',
           '桃園站',
           '大園站',
           '觀音站',
           '平鎮站',
           '龍潭站',
           '中壢站']


loltALL_center = np.matrix([[24.95751197184294, 121.22551106723652],
                            [24.958805774784295, 121.24072463527128],
                            [24.982924128648815, 121.30367714328167],
                            [24.9897342944462, 121.28532722916015],
                            [25.02639793172484, 121.2583080637309],
                            [24.99533464800778, 121.3206622541847],
                            [25.0491238247511, 121.22565191105879],
                            [25.0196261801303, 121.15380733911256],
                            [24.89662498823873, 121.21300755233322],
                            [24.870086460185718, 121.2212538811682],
                            [24.978200965830627, 121.25568725233511]])


def np_getDistance(A, B):  # 先緯度後經度
    ra = 6378140  # radius of equator: meter
    rb = 6356755  # radius of polar: meter
    flatten = 0.003353  # Partial rate of the earth
    # change angle to radians

    radLatA = np.radians(A[:, 0])
    radLonA = np.radians(A[:, 1])
    radLatB = np.radians(B[:, 0])
    radLonB = np.radians(B[:, 1])
    pA = np.arctan(rb / ra * np.tan(radLatA))
    pB = np.arctan(rb / ra * np.tan(radLatB))

    x = np.arccos(np.multiply(np.sin(pA), np.sin(pB)) + np.multiply(np.multiply(np.cos(pA), np.cos(pB)),
                                                                    np.cos(radLonA - radLonB)))
    c1 = np.multiply((np.sin(x) - x), np.power((np.sin(pA) + np.sin(pB)), 2)) / np.power(np.cos(x / 2), 2)
    c2 = np.multiply((np.sin(x) + x), np.power((np.sin(pA) - np.sin(pB)), 2)) / np.power(np.sin(x / 2), 2)
    dr = flatten / 8 * (c1 - c2)
    distance = 0.001 * ra * (x + dr)
    return distance