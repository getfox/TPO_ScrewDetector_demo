import cv2
from cvzone.ColorModule import ColorFinder


cap = cv2.VideoCapture(2)
cap.set(3, 800)
cap.set(4, 600)

myColorFinder = ColorFinder(False)
hsVals = {'hmin': 20, 'smin': 0, 'vmin': 255, 'hmax': 255, 'smax': 255, 'vmax': 255}



while True:

    success, img = cap.read()


    imgColor, mask = myColorFinder.update(img, hsVals)


    # 滤波
    mask = cv2.GaussianBlur(mask, (3, 3), 1)
    # 腐蚀
    #mask = cv2.erode(mask, (3, 3), iterations=1)
    # 膨胀
    mask = cv2.dilate(mask, (3, 3), iterations=1)
    # mask = cv2.erode(mask, (5, 5), iterations=1)
    #mask = cv2.adaptiveThreshold(mask, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11, 2)

    # 锐化

    mask = cv2.filter2D(mask, -1, (3, 3))
    # 获取轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # 排序
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 900:
            # #绘制轮廓
            # cv2.drawContours(imgColor, cnt, -1, (255, 0, 0), 3)
            # 获取轮廓周长
            peri = cv2.arcLength(cnt, True)
            # 获取轮廓点
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            # 获取矩形
            x, y, w, h = cv2.boundingRect(approx)

            # print(cv2.boundingRect(approx))
            if  w < 18 and 18 < h < 40and w<h*2/3 and(60<y<120 or 240<y<300 or 420<y<480):
                #绘制矩形
                # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # cv2.rectangle(img, (30, 60), (700, 120), (255, 200, 0), 2)
                #
                # cv2.rectangle(img, (30, 240), (700, 300), (255, 200, 0), 2)
                #
                # cv2.rectangle(img, (30, 420), (700, 480), (255, 200, 0), 2)
                #绘制中心点
                cv2.circle(img, (x + w // 2, y + h // 2), 5, (0, 255, 0), cv2.FILLED)
                # PCX = x + w // 2
                # PCY = y + h // 2
                # clist = []
                # for c in range(0, 500, 194):
                #     for r in range(0, 700, 108):
                #         ccx, ccy = 50 + r, 75 + c
                #         #cv2.circle(img, (ccx, ccy), 24, (225, 0, 0), 2)
                #         clist.append((ccx, ccy))

                # cv2.putText(img, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_PLAIN, 1,
                #             (0, 255, 0), 1)
                # cv2.putText(img, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 1,
                #             (0, 255, 0), 1)
                # cv2.putText(img, "width: " + str(w), (x + w + 20, y + 70), cv2.FONT_HERSHEY_PLAIN, 1,
                #             (0, 255, 0), 1)
                # cv2.putText(img, "height: " + str(h), (x + w + 20, y + 95), cv2.FONT_HERSHEY_PLAIN, 1,
                #             (0, 255, 0), 1)
            if w > 2.8*h and w>25 and h<12 and (100<y<160 or 280<y<340 or 460<y<520):
                # 绘制矩形
                # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                #
                # cv2.rectangle(img, (50, 100), (750, 160), (255, 0, 255), 2)
                #
                # cv2.rectangle(img, (50, 280), (750, 340), (255, 0, 255), 2)
                #
                # cv2.rectangle(img, (50, 460), (750, 520), (255, 0, 255), 2)
                # 绘制中心点
                cv2.circle(img, (x + w // 2, y + h // 2), 5, (0, 255, 0), cv2.FILLED)
                PCX = x + w // 2
                PCY = y + h // 2

                #cv2.rectangle(img, (PCX-70, PCY-80), (PCX-25, PCY-10), (0, 255, 255), 2)

                imgCrop = img[PCY-80:PCY-10, PCX-70:PCX-25]

                #获取imgCrop的灰度图
                imgCrop = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY)

                imgCrop = cv2.GaussianBlur(imgCrop, (3, 3), 1)

                imgCrop = cv2.erode(imgCrop, (3, 3), iterations=1)

                imgCrop = cv2.dilate(imgCrop, (3, 3), iterations=1)

                #过滤掉小于阈值的像素点
                ret, imgCrop = cv2.threshold(imgCrop, 230, 255, cv2.THRESH_BINARY)


                #边缘检测
                imgCrop = cv2.Canny(imgCrop, 50, 50)

                count = cv2.countNonZero(imgCrop)

                #cv2.imshow("imgCrop", imgCrop)

                #cv2.putText(img, "count: " + str(count), (PCX-90, PCY-90), cv2.FONT_HERSHEY_PLAIN, 1,
                 #           (0, 255, 0), 1)


                if count > 50:
                    cv2.rectangle(img, (PCX - 70, PCY - 80), (PCX - 25, PCY - 10), (0, 255, 0), 2)
                    cv2.putText(img, "OK", (PCX-70, PCY-90), cv2.FONT_HERSHEY_PLAIN, 2,
                                (0, 255, 0), 2)
                else:
                    cv2.rectangle(img, (PCX - 70, PCY - 80), (PCX - 25, PCY - 10), (0,0, 255), 2)
                    cv2.putText(img, "NG", (PCX-70, PCY-90), cv2.FONT_HERSHEY_PLAIN, 2,
                                (0, 0, 255), 2)


                #cv2.imshow("imgCrop", imgCrop)



                # clist = []
                # for c in range(0, 500, 194):
                #     for r in range(0, 700, 108):
                #         ccx, ccy = 50 + r, 75 + c
                #         #cv2.circle(img, (ccx, ccy), 24, (225, 0, 0), 2)
                #         clist.append((ccx, ccy))

                # cv2.putText(img, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_PLAIN, 1,
                #             (0, 255, 0), 1)
                # cv2.putText(img, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 1,
                #             (0, 255, 0), 1)
                # cv2.putText(img, "width: " + str(w), (x + w + 20, y + 70), cv2.FONT_HERSHEY_PLAIN, 1,
                #             (0, 255, 0), 1)
                # cv2.putText(img, "height: " + str(h), (x + w + 20, y + 95), cv2.FONT_HERSHEY_PLAIN, 1,
                #             (0, 255, 0), 1)

    # # 同时显示mask和img
    # imgStack = np.hstack([img, imgColor])
    #
    # cv2.imshow("Image", imgStack)

    cv2.imshow("Image", img)
    # cv2.imshow("Image", mask)
    cv2.waitKey(1)
    # ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

cap.release()
cv2.destroyAllWindows()
