"""文件的处理模块"""
import json
import os
import copy
import time

# 全局变量
res_list = list()


# 文件的读写
def read_file_data(file_path):
    """
    读取文件的数据
    :param file_path:
    :return file_data_list:
    """
    with open(file_path, "r", encoding="utf8") as f:
        content = json.load(f)
        return content


def save_file_data(file_path, save_data):
    """
    保存文件数据
    :param file_path: 文件路径
    :param save_data: 要保存的数据
    :return:
    """
    with open(file_path, "w", encoding="utf8") as f:
        json.dump(save_data, f, ensure_ascii=False)


def save_file_into_dir(dir_path, file_title, file_content):
    # title_head = time.strftime("%Y%m%d%")
    full_title = file_title
    file_path = os.path.join(dir_path, full_title)
    with open(file_path, "w", encoding="utf8") as f:
        f.write(json.dumps(file_content, ensure_ascii=False))


def trans_file_to_list(file_path):
    """
    文件转为列表
    :param file_path: 文件路径
    :return data_list: 列表包列表 [[数据1]，[数据n]]
    """
    # 读取数据
    file_obj = open(file_path, "r", encoding="utf8")
    content_list = file_obj.readlines()
    file_obj.close()
    # print(content_list)
    # 转换为列表包字典
    res_list = list()

    d = list()
    for line in content_list:
        # 非空行情况
        if len(line) != 1:
            d.append(line)
        # 空行情况
        else:
            if len(d) != 0:
                res_list.append(d)
                d = list()  # 性能可再优化
    if len(d): res_list.append(d)
    return res_list


def trasn_get_knowledge(file_path):
    """
    转换知识点，根据文件的路径转换
    :param file_path: 文件路径
    :return data_list: 知识点列表，[{},{}]
    """
    know_ledge_list = trans_file_to_list(file_path)

    data_list = list()
    data = dict()
    for know in know_ledge_list:
        data["ask"] = know[0]
        data["ans"] = know[1:]
        data_list.append(data)
        data = dict()
    return data_list


def trans_file_path_to_multi_knowledge(file_path):
    """
    文件路径转换为文件数据
    结果为多行提问，多行回答，多行注释的结合体
    :param file_path: 文件路径
    :return:
    [{'ask': ['问题题目\n', '支持多行\n'], 'ans': ['答案\n', '多行\n'], 'tips': ['提示\n', '备注\n', '多行']}]

    """
    step2key = {1: "ask", 2: "ans", 3: "tips"}
    knowledge_list = trans_file_to_list(file_path)
    knowledge_data_list = list()
    for knowledge in knowledge_list:
        step = 1  # 阶段，1-问题。2-答案。3-备注
        knowledge_dict = {"ask": [], "ans": [], "tips": []}  # 1问题，2答案，3备注
        # knowledge_dict = {"1": [], "2": [], "3": []}  # 1问题，2答案，3备注
        for item in knowledge:
            if item.strip() in ["?", "？"]:
                step = 2
                continue
            elif item.strip() in ["!", "！"]:
                step = 3
                continue
            key = step2key[step]
            knowledge_dict[key].append(item)
        knowledge_data_list.append(knowledge_dict)
    return knowledge_data_list


def cd_dir_recursion(path, deep=0, data={}, file_path_dict_list=[]):
    """
    01-根据目录，获取文件列表，递归的深入到目录中，获得文件路径列表
    :param path:
    :return:文件路径详情列表
    [{1: 'python', 2: '综合知识', 3: '1907.txt', 'file_path': 'G:\\1907.txt'}]
    """
    # 文件深度
    temp_deep = deep
    # 当前目录下的内容列表
    list_dir = os.listdir(path)
    for member in list_dir:
        new_path = os.path.join(path, member)
        temp_deep = deep + 1
        data[str(temp_deep)] = member
        if os.path.isdir(new_path):
            file_path_dict_list = cd_dir_recursion(new_path, temp_deep, data)
        else:
            temp_data = copy.deepcopy(data)
            temp_data["file_path"] = new_path
            file_path_dict_list.append(temp_data)
            # todo 完成这里的畹辑
    return file_path_dict_list


def select_dir_or_file(path, deep=0, data_dict={}):
    """
    根据操作选择目录或文件
    :param path:
    :return:
    """

    # 判断路径的类型
    # 如果是目录,可以让用户继续选择下一级
    if os.path.isdir(path):
        # 获取列表
        list_dir = os.listdir(path)

        # 显示列表
        for idx, item in enumerate(list_dir, 1):
            print(idx, item)
        # 用户选择
        choice = input("请输入需要的操作：q退出，a添加,数字选择》")
        # 选择分情况
        if choice.lower() == "q":
            # 返回结果
            return res_list
            print('返回结果')
        elif choice.lower() == "a":
            res_list.append(data_dict)
            print('添加成功', res_list)
        elif choice.lower() == "..":
            data_dict.pop(str(deep))
            new_deep = deep - 1
            new_path = os.path.dirname(path)
            print('向上一级\n %s' % new_path)
            print('向上一级，当前深度%s当前状态%s' % (new_deep, data_dict))
            select_dir_or_file(new_path, new_deep, data_dict, res_list)

        try:
            i = int(choice) - 1
            name = list_dir[i]
        except Exception as e:
            print(e)
        else:
            new_path = os.path.join(path, name)
            new_deep = deep + 1
            # 构建新数据
            data_dict[str(new_deep)] = name
            print('更深一层，当前深度%s当前状态%s' % (new_deep, data_dict))
            select_dir_or_file(new_path, new_deep, data_dict, res_list)
    # 如果是文件，则操作有限
    else:
        print('当前深度%s当前状态%s' % (deep, data_dict))

    # 如果是文件，只能够向上返回或者退出

    # 判断dirpath是不是目录
    # if os.path.isdir(dir_path):
    #     # 获取内容列表
    #     dir_list = os.listdir(dir_path)
    #     # 打印显示
    #     for idx, item in enumerate(dir_list):
    #         print(idx, item)
    #     # 用户选择
    #     ipt = input("请选择：》")
    #     # 验证
    #     try:
    #         ipt = int(ipt)-1  # 转整数
    #         item_name = dir_list[ipt]  # 名称
    #     except:
    #
    #     else:
    #         item_path = os.path.join(dir_path, item_name)  #路径
    #         deep += 1
    #         data_dict[str(deep)] = item_name
    #         select_dir_or_file(item_path, deep,)
    #
    #         new_path = os.path.join(dir_path, item)
    #
    # # 目录情况，选择一个操作，进入下一轮递归
    # # 如果是文件，直接返回


class SelectTarget:
    def __init__(self, source_dir):
        self.res_list = list()  # 已选择的内容
        self.current_path = source_dir  # 资源夹的路径
        self.source = source_dir
        self.deep = 0  # 深度
        self.selected_path_list = list()  # 已选择的项目列表
        self.selected_deep_dict_list = list()  # 已选择的深度列表
        self.deep_dict = dict()  # 深度字典

    def start(self):
        while True:
            print('循环开始，当前深度%s，当前字典%s,当前路径%s' % (self.deep, self.deep_dict, self.current_path))
            if os.path.isdir(self.current_path):
                choice_num = self.dir_fun()
            else:
                self.file_fun()

            if choice_num.lower() == "q":
                return self.selected_deep_dict_list
            print('循环到底，当前深度%s，当前字典%s,当前路径%s' % (self.deep, self.deep_dict, self.current_path))

    def dir_fun(self):
        """路径为目录时的操作"""
        # 去重显示菜单
        item_list = self.show_menu()
        # 用户选择
        choice_num = self.user_choice(item_list)
        return choice_num

    def file_fun(self):
        """当前路径为文件时的操作"""
        self.append_data()

    # 零散的功能
    def show_menu(self):
        """ 显示菜单 """
        # 根据目录获取内容列表
        item_list = os.listdir(self.current_path)
        # 遍历内容列表，比对路径，找到需要删除的内容
        remove_list = list()
        for item in item_list:
            # 获取每一个元素的路径
            item_path = os.path.join(self.current_path, item)
            # 如果这个路径在已有列表中，就不显示
            if item_path in self.selected_path_list:
                # item_list.remove(item)
                remove_list.append(item)
        # 移除掉不要的内容
        for re_item in remove_list:
            item_list.remove(re_item)

        # 输出显示的内容
        print('=' * 20)
        print('当前路径', self.current_path)
        print('已添加路径', self.selected_path_list)
        print('已deepdata', self.selected_deep_dict_list)
        for idx, item in enumerate(item_list, 1):
            print("第【%d】项----> %s" % (idx, item))
        return item_list

    def user_choice(self, item_list):
        """ 用户选择"""
        # print('....', self.deep_dict)
        choice_num = input("请输入需要的操作 a-添加，..-向上一级，q-退出：")
        try:
            idx = int(choice_num) - 1  # 转整数，并校正下标
            choice_title = item_list[idx]  # 获取选中的名称
        except:
            if choice_num == "..":
                self.up_dir()
                # self.current_path = os.path.dirname(self.current_path)
                # if str(self.deep) in self.deep_dict:
                #     self.deep_dict.pop(str(self.deep))
                # self.deep -= 1
                # # 深度小于等于0为异常情况
                # if self.deep <= 0:
                #     self.current_path = source_dir
                #     self.deep = 0
                #     self.deep_dict = dict()
                # print("当前路径已更换为：", self.current_path)

            if choice_num == "a":
                self.append_data()
                # self.selected_path_list.append(self.current_path)
                # self.selected_deep_dict_list.append(self.deep_dict)
                # self.up_dir()

            return choice_num
            # print('1908112121非法输入，已自动校正')
            # choice_title = item_list[0]
        else:
            self.current_path = os.path.join(self.current_path, choice_title)
            self.deep += 1
            self.deep_dict[str(self.deep)] = choice_title
            print("当前路径已更换为：", self.current_path)
            print('当前字典', self.deep_dict)
        return choice_num

    def up_dir(self):
        """ 向上一级的情况 """
        self.current_path = os.path.dirname(self.current_path)
        # if str(self.deep) in self.deep_dict:
        #     self.deep_dict.pop(str(self.deep))
        self.deep -= 1
        # 深度小于等于0为异常情况
        if self.deep <= 0:
            self.current_path = self.source
            self.deep = 0
            self.deep_dict = dict()
        # print("当前路径已更换为：", self.current_path)

    def append_data(self):
        self.selected_path_list.append(self.current_path)
        self.selected_deep_dict_list.append(self.deep_dict)
        self.up_dir()


def get_dir_all_file_data(dir_path):
    """
    给我一个目录名，给你解析好的一切结果
    :param dir_path:
    :return:
    [{'ask': ['写出文件名称\n'], 'ans': ['urls.py\n'], 'tips': [], '1': 'django-test', '2': '02-基本使用', '3': '01-路由系统.txt', 'file_path': '文件路径'}
    """
    # 获取目录下全部文件信息
    file_info_dict_list = cd_dir_recursion(dir_path)
    # print(file_path_dict_list)
    # 读取文件中的全部内容
    knowledge_con_list = list()
    for file_info in file_info_dict_list:
        file_path = file_info["file_path"]
        knowledge_data = trans_file_path_to_multi_knowledge(file_path)  # 文件中的全部知识
        for knowledge in knowledge_data:
            knowledge.update(file_info)

        # print(len(knowledge_data), knowledge_data)
        knowledge_con_list.extend(knowledge_data)
    return knowledge_con_list


def select_from_sourceList_by_condDict(sourceList, cond_dict={}):
    """从一个列表包字典中，查找符合条件的字数据，并返回"""
    right_list = list()
    for source_dict in sourceList:
        for k, v in cond_dict.items():
            if not (k in source_dict and source_dict[k] == v):
                break
        else:
            right_list.append(source_dict)
    return right_list


def select_many_from_sourceList_by_condDict(sourceList, cond_list=[]):
    """ 从条件范围列表中选取符合的内容 """
    # 拿数据
    res_list = list()
    for cond_dict in cond_list:
        right_list = select_from_sourceList_by_condDict(sourceList, cond_dict)
        res_list.extend(right_list)

    # 数据去重
    no_repeat_list = list()
    for res in res_list:
        if res not in no_repeat_list:
            no_repeat_list.append(res)

    return no_repeat_list


if __name__ == '__main__':
    # 模块的配置
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_dir = os.path.join(BASE_DIR, "source")
    s = SelectTarget()
    s.start()
