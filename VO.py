import cv2, os
import numpy as np


# mtx:
#  [[492.34411736   0.         313.7871541 ]
#  [  0.         491.11982789 228.91887934]
#  [  0.           0.           1.        ]]
def find_point_pair(img_train, img_query, show=False):
    orb = cv2.ORB_create()
    kp_train, des_train = orb.detectAndCompute(img_train, None)
    kp_query, des_query = orb.detectAndCompute(img_query, None)
    
    if des_query is None or des_train is None:
        return
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des_query, des_train)
    
    matches = sorted(matches, key=lambda x: x.distance)
    
    good_matches = []
    # distance 一般在50以下就是比较好的, 100以内都算能用
    points_train, points_query = [], []
    for match in matches:
        if match.distance <= max(2 * matches[0].distance, 30):
            good_matches.append(match)
            points_train.append(kp_train[match.train_Idx].pt)
            points_query.append(kp_query[match.query_Idx].pt)
    
    # scores = [match.distance for match in good_matches]
    
    # 这个函数是img1是query,img2是train
    if show:
        img3 = cv2.drawMatches(img_query, kp_query, img_train, kp_train, good_matches, None, flags=2)
        cv2.imshow('match result', img3)
        cv2.waitKey(4000)
    
    return points_train, points_query


K = np.array([[492.34411736, 0, 313.7871541], [0, 491.11982789, 228.91887934], [0, 0, 1]])
for i in range(1, 28):
    image_current, image_next = os.path.join('image_1', '{}.jpg'.format(i)), os.path.join('image_1',
                                                                                          '{}.jpg'.format(i + 1))
    img_train, img_query = cv2.imread(image_current), cv2.imread(image_next)
    
    # 找到对应的点对
    points_train, points_query = find_point_pair(img_train, img_query)
    
    mask = None
    E = cv2.findEssentialMat(points_train, points_query, K, cv2.LMEDS, 0.99, mask=mask)
    
    R, t = None, None
    cv2.recoverPose(E, points_train, points_query, K, R, t, mask)
    
    #
    cv2.solvePnP()

# cv2.findEssentialMat()
