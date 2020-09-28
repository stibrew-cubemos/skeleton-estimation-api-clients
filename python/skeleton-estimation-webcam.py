import json
import base64
import cv2
import numpy as np
import http.client
import time

keypoint_connections = [
    ["right_eye", "right_ear"],
    ["left_eye", "left_ear"],
    ["nose", "right_eye"],
    ["nose", "left_eye"],
    ["neck", "nose"],
    ["neck", "right_shoulder"],
    ["neck", "left_shoulder"],
    ["right_shoulder", "right_elbow"],
    ["left_shoulder", "left_elbow"],
    ["right_elbow", "right_wrist"],
    ["left_elbow", "left_wrist"],
    ["neck", "right_hip"],
    ["neck", "left_hip"],
    ["right_hip", "right_knee"],
    ["left_hip", "left_knee"],
    ["right_knee", "right_ankle"],
    ["left_knee", "left_ankle"]
]        

def render_result(skeletons, img, confidence_threshold):
    skeleton_color = (100, 254, 213)
    for skeleton in skeletons["skeletons"]:
        for connection in keypoint_connections:
            if skeleton["keypoints"][connection[0]]["coordinates"]["x"] > 0:
                if skeleton["keypoints"][connection[1]]["coordinates"]["x"] > 0:
                    pt_1 = (
                        int(skeleton["keypoints"][connection[0]]["coordinates"]["x"]), 
                        int(skeleton["keypoints"][connection[0]]["coordinates"]["y"])
                    )
                    pt_2 = (
                        int(skeleton["keypoints"][connection[1]]["coordinates"]["x"]), 
                        int(skeleton["keypoints"][connection[1]]["coordinates"]["y"])
                    )
                    cv2.line( img, pt_1, pt_2, skeleton_color, thickness=2, lineType=cv2.LINE_AA )

        actions = skeleton["actions"]
        if len(actions) > 0:
            start_pos_y = 40
            for action in actions: 
                cv2.putText(frame, action, (20,start_pos_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)
                start_pos_y = start_pos_y + 20      


try:
    # connect to the cubemos API
    conn = http.client.HTTPSConnection("api.cubemos.com")

    # start the webcam
    cap = cv2.VideoCapture(0)
    hasFrame, frame = cap.read()

    # continous acquisition
    frame_count = 0
    fps = 0
    fps_text = "calculating fps"
    while hasFrame:
        hasFrame, frame = cap.read()

        start_time = time.time()
        # get the opencv frame as a base64 byte stream 
        retval, buffer = cv2.imencode('.jpg', frame)
        byte_stream = base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode()

        # provide the input payload
        payload = {'image': {'bytes_b64': byte_stream}}
        headers = { 'x-api-key': "YOUR-API-KEY" }
        
        # make the POST call and get the response
        conn.request("POST", "/skeletons/estimate", json.dumps(payload), headers)
        res = conn.getresponse()
        data = res.read()
        
        if res.status == 200:
            skeletons = data.decode("utf-8")
            skeletons = json.loads(skeletons)

            # measure the fps for displaying
            end_time = time.time() - start_time

            fps = fps + (1/end_time)
            if frame_count == 10:    
                fps = fps/frame_count        
                fps_text = str(round(fps, 2)) + "fps"
                frame_count = 0
                fps = 0

            # render the result onto the image using the response obtained
            render_result(skeletons, frame, 0.1)
            cv2.putText(frame, fps_text, (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)      

        cv2.imshow("cubemos skeleton estimation api", frame)

        keyPressed = cv2.waitKey(1)
        if keyPressed == 27:
            break;
        frame_count = frame_count + 1

finally:
    cv2.destroyAllWindows()



