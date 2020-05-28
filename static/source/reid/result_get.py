import os, sys, json


def result_get(result_dir, save_json_dir):

    person_list = os.listdir(result_dir)    
    # print(person_list)  # 这些是reid
    all_data = []
    for person in person_list:
        reid = person
        person_data = []
        person_dir = result_dir+person+'\\'
        person_pic = os.listdir(person_dir)
        # print(person_pic)   # 这是每张图片，接下来要根据tid做归类
        tid_list = []
        for pic in person_pic:
            # print(pic)  # eg: c2_p1_t1_f1046.jpg
            camera = pic.split("_")[0]          # c1
            tid = camera + pic.split("_")[2]    # c1t2
            frame = pic.split("_")[3]           
            frame = frame.split(".")[0]           # f1046

            # 接下来提取不重复信息
            # 每一个tid视作一个目标
            # frame更新最先和最后
            if tid not in tid_list:
                tid_list.append(tid)
                # camera, reid, tid, first time, last time, pic_dir
                single_tid_person = [camera]
                single_tid_person.append(person)
                single_tid_person.append(tid)
                single_tid_person.append(frame)
                single_tid_person.append(frame)
                single_tid_person.append(person_dir + pic)
                person_data.append(single_tid_person)
            else:
                for i in range(len(tid_list)):
                    if tid_list[i] == tid:
                        person_data[i][-2] = frame  #更新最后时间
                        break
        # print(person_data)
        all_data.append(person_data)
    # print(all_data)
    with open(save_json_dir, "w") as f:
        f.write(json.dumps(all_data))
    f.close()


if __name__ == "__main__":
    path = sys.argv[0]
    path0 = path.split("\\")[:-2]
    if len(path0)==0:
        path0 = path.split('/')[:-2]
    result_dir0 = ""
    for i in range(len(path0)):
        result_dir0 = result_dir0+path0[i]+'\\'

    result_dir = result_dir0 +"reid_result\\"
    attri_dir = result_dir0 + "attribute_result\\"
    print(result_dir,"\n",attri_dir)

    save_json_dir = "../reid_data_for_neo4j.json"
    result_get(result_dir, save_json_dir)
