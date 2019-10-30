"""
学生模块
初始化时做的事：
读取数据库中的知识
读取自己的知识
构建成一个全新的知识内容


相关表名称：
stu_info.json，学生基本信息表。
stu_score，学生成绩表
exam_data，考试题目源表（打分后就删除掉）

考试相关格式
题目源表中拿到的考题格式为：
{'ask': ['问题行1..\n', '问题行2\n'], 'ans': ['答案行1\n', '答案行2\n'], 'tips': ['补充行1\n', '补允行2\n'], '1': 'django-test', '2': '02-基本使用', '3': '01-基本.txt', 'file_path': 'G:\\易三\\source\\django-test\\02-基本使用\\01-基本.txt', 'test_id': 'nx80719558'}
学生成绩表中新增加以下字段
level-级别,根据熟练度估算出的知识点的熟悉程度1-4分
score-总分，答题总得分，排序参照
strength_list-熟练度列表，自我评测熟练度打分收录
exam_id-考试编号

生成考题后，考题存在数据表中的格式
[{"ask": ["从组的配置文件中查找 某某 \n", "显示 某某 那一行的信息\n"], "ans": ["grep 某某 /etc/group\n"], "tips": [], "1": "linux", "2": "01-用户与组", "3": "01-基本操作-格式.txt", "file_path": "G:\\易三\\source\\linux\\01-用户与组\\01-基本操作-格式.txt", "test_id": "ym35393043", "exam_id": "tsk804", "stu_id": "ie40"}]
如果要获取考题，可以根据考试id与学生姓名来获取

当前进度，可以选择考试范围了。可以全域考试，也可以指定范围考试。
解析成绩，让成绩与记分对应上


需要解决的问题
分数录入成功后，需要删掉打分文件，需要删掉考试源文件

当前：
出题时，出一个新题，出一个低分题。

出题功能完成，打分完成，阅卷完成，一切完成
等待测试

"""
import os
import time
import random
import copy
# from lib import randomhandle
from lib.dbsql.dbfile import db
from lib import randomhandle
from lib import filehandle
import test_setting

# 配置
# 模块的配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
exam_dir = os.path.join(BASE_DIR, "exam")  # 试题dir
exam_score_dir = os.path.join(BASE_DIR, "exam_score")  # 打分目录
source_dir = os.path.join(BASE_DIR, "source")  # 题目源目录
error_dir = os.path.join(BASE_DIR, "error") # 错误路径


# 表名称
table_name_stu_score = "stu_score"
table_name_stu_base_info = "stu_base_info"
table_name_exam_data = "exam_data"
table_name_source = "source"
# 知识源
# source_data = filehandle.get_dir_all_file_data(source_dir)
source_data = db.read_from_table("source")


# 考题范围
g_test_num = test_setting.test_num  # 试题数量
# g_test_type = "0"

# g_test_type = input("希望如何考试？0-全能测试；1-局部测试；给我答案吧：")
g_test_type = "0"
if g_test_type == "1":
    st_obj = filehandle.SelectTarget(source_dir)
    cond_dict_list = st_obj.start()
    print(cond_dict_list, '*' * 20)


class Manage:
    def del_die_score(self):
        """
        删除已经不存在的得分数据
        :return:
        """
        # 学生成绩列表
        score_dict_list = db.read_from_table(table_name_stu_score)
        # 知识题库列表
        source_dict_list = db.read_from_table(table_name_source)
        # print('学生成绩',score_dict_list)
        #
        # print('知识题库', source_dict_list)


        # score_test_id_list = [score_dict["test_id"] for score_dict in score_dict_list]
        # score_test_id_list = list(set(score_test_id_list))
        source_test_id_list = [source_dict["test_id"] for source_dict in source_dict_list]

        del_dict_list = list()
        for score_dict in score_dict_list:
            if "test_id" in score_dict and score_dict["test_id"] not in source_test_id_list:
                del_dict_list.append(score_dict)
        # for source_dict in source_test_id_list:
            # # source_dict，考题源的一个字典
            # print('next1234')
            # for score_dict in score_dict_list:
            #     # scroe_dict，得分字典
            #     if "test_id" in score_dict and source_dict == score_dict["test_id"]:
            #         # 如果试题源id在分数字典中
            #         # del_dict_list.append(score_dict)
            #         print('continue1234')
            #         continue
            # else:
            #     # 找遍了所有的都没有，就是要删的
            #     if score_dict not in del_dict_list:
            #         del_dict_list.append(score_dict)


        print('要删除的学生成绩有{}个,详情：{}'.format(len(del_dict_list), del_dict_list))

        db.delete_many_from_table(table_name_stu_score, del_dict_list)
        print('删多出的学生成绩成功')



        return score_dict_list



m = Manage()
r = m.del_die_score()


def main_menu():
    """ 学生程序主菜单 """
    menu_list = [
        {"1", ("选择考试范围", "ensure_test_target")},
        {"2", ("进行一场笔试", "ensure_test_target")},
    ]
    return menu_list


class Student:
    def __init__(self, id):
        """初始化学生数据"""
        self.id = id  # ID
        self.stu_data_dict = self.get_stu_data_by_id(id)  # 学生字典
        self.score_list = self.get_stu_score_list()  # 学生答题的分数，已按得分score排序
        self.source_all_data = self.get_source_all_data()  # 题目源全部,重复的
        self.new_test_id_list = self.get_new_test_list()  # 当前学生未新增的知识id列表


        """
        学生字典的键名说明
        id，name,level,exp
        """
        self.name = self.get_stu_name()  # 姓名
        self.test_target = self.ensure_test_target()  # 明确学生本次考试的出题范围
        self.test_target_id = self.get_test_target_id()  # 获取考试的题目列表
        self.update_score_list()  # 更新分数情况，只保留考试范围内的分数

        # 根据学生id获取学生的完整个人数据
        self.is_new_test = True  # 出贩时候是否从未出题列表中取值

        # 已出的题目
        self.already_exam = []


    def start(self):
        """
        学生系统启动
        :return:
        """
        print("学生系统开启，%s同学 准备开始考试：" % self.name)
        self.have_a_test(g_test_num)
        # self.current_test(test_num)

    def write_test(self, num):
        """ 笔试 """
        # 确题出题数量
        # 生成一场考试
        # 考试文档生成
        pass

    def current_test(self, num):
        # 一道一道的出题
        # one_test = self.get_one_ask()
        # self.show_ask_to_student()
        # # 等答案
        # self.wait_for_skno()
        # 一道一道的给答案
        # 最终生成问答文档
        # 生成考试数据
        pass

    # 主要的方法
    def have_a_test(self, num):
        """ 进行一场考试"""
        # 生成考试编号
        # 产生若干题目
        # 题目保存，用于未来的打分
        test_dict_list = list()
        exam_id = randomhandle.create_code(3, 3)

        # 修复数据
        # 如果要出的题目5大于现有的题目2，那么就只出2道题
        num = num if (num < len(self.test_target)) else len(self.test_target)
        for i in range(num):
            item_dict = self.get_one_ask()
            item_dict["exam_id"] = exam_id
            item_dict["stu_id"] = self.id
            test_dict_list.append(item_dict)
        # 题目保存到数据库中
        db.insert_many_into_table("exam_data", test_dict_list)
        # 提目生成问答文档
        self.create_ask_ans_file(test_dict_list)
        print("考试创建完毕，有{}题\n".format(len(test_dict_list)))

    def score_all_test(self):
        """
        为每一个考试进行打分
        :return:
        """
        # 获得所有文件列表
        score_file_name_list = os.listdir(exam_score_dir)
        # print(score_list)  # 查题目

        # 遍历每一个文件
        score_file_path_container = list()  # 评分文件路径保存容器，用于后面的删文件
        for score_file_name in score_file_name_list:
            score_file_path_container.append(os.path.join(exam_score_dir, score_file_name))
            # 解析得到相关的数据，然后进行读分操作。可能存在错误。出错记录数据。跳过这一轮。
            score_file_info_dict = self.parse_score_file_name(score_file_name)
            # 解析自我评分
            score_data_list_list = filehandle.trans_file_to_list(score_file_info_dict["path"])
            #     根据考试ID获取考试数据源的内容
            exam_data_dict_list = db.select_from_table(table_name_exam_data, {
                "exam_id": score_file_info_dict["exam_id"],
                "stu_id": score_file_info_dict["stu_id"]
            })
            #     统计工作
            print('评分文件题目条数', len(score_data_list_list), '考试题目条数', len(exam_data_dict_list))
            zip_score_res = zip(exam_data_dict_list, score_data_list_list)
            # 根据配好的组合，解析数据，做好加减法
            self.make_stu_score(zip_score_res)  # 生成学生分数309行
            # 删除考试文件和考试数据
            self.del_exam_data_and_score_file(score_file_name, score_file_info_dict["exam_id"])

    def del_exam_data_and_score_file(self, score_file_name, exam_id):
        """
        删除考试评分文件和考试的数据源
        :param score_file_name:
        :param exam_id:
        :return:
        """
        # 删除评分文件
        score_file_path = os.path.join(exam_score_dir, score_file_name)
        os.remove(score_file_path)
        print('删除评分文件成功：', score_file_name)
        # 删除数据库中的考试题目源
        db.delete_from_table(table_name_exam_data, {"exam_id": exam_id})
        print('删除考试源成功,exam_id', exam_id)

    def make_stu_score(self, zip_data):
        """
        生成学生分数
        :return:
        """
        for data_tuple in zip_data:
            # ({'ask': ['组的配置文件路径\n'], 'ans': ['/etc/group\n'], 'tips': [], '1': 'linux', '2': '01-用户与组', '3': '01-基本操作-格式.txt', 'file_path': 'G:\\易三\\source\\linux\\01-用户与组\\01-基本操作-格式.txt', 'test_id': 'ic45200807', 'exam_id': 'bps528', 'stu_id': 'ie40'}, ['1\n', '第[1]题_linux__01-用户与组__01-基本操作-格式.txt\n', '组的配置文件路径\n'])
            stu_id = data_tuple[0]["stu_id"]  # 学生ID
            test_id = data_tuple[0]["test_id"]  # 测试id
            grade_point = data_tuple[1][0]  # 等级点数 '1/n'
            # 如果评分为9，记录数据
            if grade_point.strip() == "9":
                self.save_error(data_tuple[1])  # 记录错误题
            score_int, grade_point = self.get_score_num_by_grade(grade_point)  # 分数
            cond_dict = {
                "stu_id": stu_id,
                "test_id": test_id
            }
            # 根据学生姓名与考试编号，查询得分数据
            select_list = db.select_from_table(table_name_stu_score, cond_dict)  # 要么查询成功得一条数据，要么是0条数据查询不到

            # 判断数据的长度，如果是0条，那么新增一条数据到数据库中
            if select_list:  # 如果列表不为空，要合并后保存
                select_dict = select_list[0]
                select_dict["score"] += score_int
                select_dict["grade_list"].append(grade_point)
                avg = sum(select_dict["grade_list"]) / len(select_dict["grade_list"])
                select_dict["level"] = round(avg, 2)
                select_dict["last_time"] = int(time.time())
                db.update_table_set(table_name_stu_score, cond_dict, select_dict)
                print("合并数据成功")

            # 如果是0条数据，直接转换后插入
            else:
                select_dict = dict()
                select_dict["stu_id"] = stu_id
                select_dict["test_id"] = test_id
                select_dict["score"] = score_int
                select_dict["level"] = grade_point
                select_dict["grade_list"] = [grade_point]
                select_dict["last_time"] = int(time.time())
                db.insert_into_table(table_name_stu_score, select_dict)
                print('插入学生的成绩成功')

    def save_error(self, error_data):
        """有错误的题目"""
        nt = time.strftime("%Y-%m-%d")
        path = os.path.join(error_dir, nt+".txt")
        print("带9的问题:", error_data)
        with open(path, "a", encoding="utf8") as f:
            f.write(str(error_data))
            f.write("\n")


    def get_score_num_by_grade(self, grade_point):
        """
        根据自我评分获得打分的情况
        :return:
        """
        # 验证grade_point
        try:
            grade_int = int(grade_point.strip())
        except:
            grade_int = 0
        else:
            if grade_int == 9:
                print('自评9分，异常')
                # 记录情况
                # 修正数据
                grade_int = 0
            if grade_int not in [0, 1, 2, 3, 4]:
                grade_int = 0

        # 自我评级转为评分的对应关系
        grade2score = {
            0: -2,
            1: 2,
            2: 4,
            3: 6,
            4: 10
        }

        score_int = grade2score[grade_int]
        return score_int, grade_int

    def parse_score_file_name(self, score_file_name):
        """
        解析信息，根据打分的文件
        :param score_file_name:
        :return: {path:,exam_id:,stu_name:,stu_id}
        """
        score_file_info_dict = dict()
        info_list = score_file_name.split("_")  # 切割后的信息
        score_file_info_dict["path"] = os.path.join(exam_score_dir, score_file_name)
        score_file_info_dict["exam_id"] = info_list[0]
        score_file_info_dict["stu_name"] = info_list[1]
        score_file_info_dict["stu_id"] = info_list[2]
        return score_file_info_dict

    def get_source_all_data(self):
        return db.read_from_table(table_name_source)


    def score_a_test(self, test_id):
        """为一场考试进行评分"""
        # 根据考试ID获取学生的自我评分数据
        # 异常验证。 两个情况是否一致，不一致的记录起来。存在数据库中。
        # 如果一致，才进行解析
        # 根据学生自我评分，为本次考试进行评分（评分的制度需要完成）
        pass


    def get_source_dict_id_list(self):
        """获取题目资源的id"""
        source_dict_list = self.source_all_data
        id_list = [source_dict['test_id'] for source_dict in source_dict_list]
        return id_list

    def get_stu_score_id_list(self):
        """学生已考试列表"""
        id_list = list()
        for score in self.score_list:
            id_list.append(score['test_id'])

        return(id_list)

    def get_new_test_list(self):
        """获取新知识列表"""
        # 拿到学生的已考试id列表
        score_id_list = self.get_stu_score_id_list()
        # 拿到知识源id列表
        source_id_list = self.get_source_dict_id_list()
        # 提取新知识id
        new_test_id_list = list()
        for source_id in source_id_list:
            if source_id not in score_id_list:
                new_test_id_list.append(source_id)
        return new_test_id_list


    def get_source_data_by_exam_id(self,test_id):
        """根据考试id，从考试数据源中提取一个考题的字典"""
        for source_dict in self.source_all_data:
            # data = source_dict['test_id']
            if source_dict['test_id'] == test_id:
                return source_dict
        return None

    def get_one_ask(self):
        """获取低分考题"""
        # 获取一个低分的考题
        # 逻辑：
        # 学生知识点获取，按照分数由低到高排序。
        # 记录当天是否已经考过这个题目，把没有考过的题目，低分的，展现出来

        print('已出题目')
        print(self.already_exam)
        # 先出新题目
        # 如果新题列表非空，从里面取出一题
        if self.new_test_id_list:
            # one_id = self.new_test_id_list.pop()
            # one_id = self.new_test_id_list.pop()
            import random
            one_id = random.choice(self.new_test_id_list)
            self.new_test_id_list.remove(one_id)

        # 根据题目id拿到题目数据
            one_test = self.get_source_data_by_exam_id(one_id)
            self.already_exam.append(one_test)
            return one_test

        # 否则再出老题目
        # 从学生得分中取一题分值低的
        low_score = self.score_list.pop()
        low_test_id = low_score['test_id']
        one_test = self.get_source_data_by_exam_id(low_test_id)
        while one_test in self.already_exam:
            one_test = self.get_source_data_by_exam_id(low_test_id)
        self.already_exam.append(one_test)



        # 数据返回，下面的就都可以不要了



        # one_test = random.choice(self.test_target)
        # while one_test in self.already_exam:
        #     one_test = random.choice(self.test_target)
        # self.already_exam.append(one_test)

        return one_test


    def ensure_test_target(self):
        """
        明确考试的范围
        :param mode: 模式
        :return:
        [{'ask': ['问题行1..\n', '问题行2\n'], 'ans': ['答案行1\n', '答案行2\n'], 'tips': ['补充行1\n', '补允行2\n'], '1': 'django-test', '2': '02-基本使用', '3': '01-基本.txt', 'file_path': 'G:\\易三\\source\\django-test\\02-基本使用\\01-基本.txt'}]
        """
        test_info_dict_list = list()  # 考试信息列表容器
        # num = "1"  # 手动输入考试范围
        num = g_test_type  # 手动输入考试范围

        # 数据验证，要么0全部范围，要么1手动选择范围
        if num not in ["0", "1"]:
            num = "0"

        # 全范围的情况
        if num == "0":
            test_info_dict_list = copy.deepcopy(source_data)
        elif num == "1":
            test_info_dict_list = filehandle.select_many_from_sourceList_by_condDict(source_data, cond_dict_list)
        print('出题范围，一共有%d题，' % len(test_info_dict_list))

        # 已得分的题目里取出id，从全部考试题目中去掉相同id的数据字典
        # 此处的去重功能有逻辑错误
        # new_test_info_dict_list = self.del_repeat_test(test_info_dict_list)


        return test_info_dict_list

    """ 获取一个考题 """

    def get_many_ask(self, num):
        """ 获取多个考题 """
        ask_dict_list = list()  # [{"ask_id":"111","ask":"什么是多线程"}]
        for i in range(num):
            pass
        ask_dict_list.append(self.get_one_ask())
        return ask_dict_list

    def save_one_ask_score(self, ask_id, score):
        # 根据问题id找到问题字典，从数据库中查找。 找到以后，把分数添加进去。再保存
        # 对分数进行验证，如果分数是9分，就另存到一个文件中，同时给这个题目记1分
        # 如果分数是1234分，就记录到数据库中
        print("知识点{}添加了{}分，记录完毕".format(ask_id, score))

    # 根据考试ID获取考试的数据
    """ 给一个知识点打分 """

    def save_many_ask_score(self, ask_id_list, score_list):
        """ 批量保存问题分数"""
        # ["111","112"]
        # [3,2]
        # 使用zip方法
        print("批量打分工作完成，一共完成了{}题的记分".format(len(score_list)))

    # 输助方法
    def get_stu_data_by_id(self, id):
        """ 根据学生的id 获取学生数据"""
        stu_data_dict = dict()
        # 从数据库中读保存好的数据
        stu_data_dict = db.select_from_table(table_name_stu_base_info, {"id": id})
        # 从题目源中去重的处理知识点
        return stu_data_dict[0] if len(stu_data_dict) == 1 else {}

    # 二级辅助方法
    def get_stu_name(self):
        """获取学生的名字"""
        return self.stu_data_dict["name"]

    def get_stu_score_list(self):
        """获取学生技能得分列表"""
        # skill_list = list()
        # 从学生表中查询学生的成绩并返回
        skill_list = db.select_from_table(table_name_stu_score, {"stu_id": self.id})
        print("从%s表中查到了%d条数据，详情%s" % (table_name_stu_score, len(skill_list), skill_list))
        # 对分数进行排序
        skill_list.sort(key=lambda ele: ele["score"],reverse=True)

        return skill_list

    # def get_target_area(self):
    #     """ 获取考试目标 """
    #     st_obj = filehandle.SelectTarget(source_dir)
    #     cond_dict_list = st_obj.start()
    #     return cond_dict_list

    # 生成文档
    def create_ask_ans_file(self, test_dict_list):
        """
        生成考试问答的文档
        :param test_dict_list:
        :return:
        """
        # 通用部分
        ask_con = "\n"  # 问题串
        ans_con = "\n"  # 答案串
        import time
        time_title = time.strftime("%Y%m%d%H")
        print("***********",test_dict_list)
        exam_id = test_dict_list[0]["exam_id"]

        # 创建文件夹
        ask_dir_name = "{time_title}-问题".format(exam_id=exam_id, time_title=time_title)
        # ask_dir_name = "{exam_id}-{time_title}-问题".format(exam_id=exam_id, time_title=time_title)
        ans_dir_name = "{time_title}-答案".format(exam_id=exam_id, time_title=time_title)
        # ans_dir_name = "{exam_id}-{time_title}-答案".format(exam_id=exam_id, time_title=time_title)
        ask_dir_path = os.path.join(exam_dir, ask_dir_name)
        ans_dir_path = os.path.join(exam_dir, ans_dir_name)
        # self.ensure_dir_exists(ask_dir_path)
        self.ensure_dir_exists(ans_dir_path)

        # 出题了
        for idx, test_dict in enumerate(test_dict_list, 1):
            # 问题串
            ask_line = ""
            for ask in test_dict["ask"]:
                ask_line += ask
            # 答案串
            zhanwei = "...\n"+"!\n"*16
            ans_line = zhanwei + "答案：\n"
            for ans in test_dict["ans"]:
                ans_line += ans
            # 提示串
            tips_line = ""
            for tips in test_dict["tips"]:
                tips_line += tips
            # 信息串
            test_info = "第[%s]题_%s__%s\n%s\n...\n" % (idx, test_dict["1"], test_dict["2"], test_dict["3"])

            ask_con += "%s%s\n\n\n\n" % (test_info, ask_line)
            ans_con += "%s%s%s%s\n\n\n" % (test_info, ask_line, ans_line, tips_line)

        # 生成题目文件
        ask_file_title = "{exam_id}_{stu_name}_{stu_id}_{time_title}_问题.txt".format(exam_id=exam_id, stu_name=self.name,
                                                                                    stu_id=self.id,
                                                                                    time_title=time_title)
        ans_file_title = "{exam_id}_{stu_name}_{stu_id}_{time_title}_答案.txt".format(exam_id=exam_id, stu_name=self.name,
                                                                                    stu_id=self.id,
                                                                                    time_title=time_title)
        ask_file_path = os.path.join(ask_dir_path, ask_file_title)
        ans_file_path = os.path.join(ans_dir_path, ans_file_title)

        # with open(ask_file_path, "w", encoding="utf8") as f:
        #
        #     f.write(ask_con)

        with open(ans_file_path, "w", encoding="utf8") as f:

            f.write(ans_con)

    def ensure_dir_exists(self, dir_path):
        """
        :param dir_path:
        :return:
        """
        if not (os.path.isdir(dir_path)):
            os.mkdir(dir_path)
            print("目录创建成功", dir_path)

    def del_repeat_test(self, test_info_dict_list):
        """
        删掉重复的数据
        :param test_info_dict_list:
        :return:
        """
        # 继续这里
        # 去重功能实现，从题目源中删掉已答题目中有的部分
        test_info_id_list = [info_dict["test_id"] for info_dict in test_info_dict_list]  # 考试ID列表
        remove_test_info_dict_list = list()  # 要删除的测试信息字典
        for score_dict in self.score_list:
            if score_dict["test_id"] in test_info_id_list:
                for test_info_dict in test_info_dict_list:
                    if test_info_dict["test_id"] == score_dict["test_id"]:
                        remove_test_info_dict_list.append(test_info_dict)

        print("重复的数据大约有%d条" % len(remove_test_info_dict_list))

        for remove_test in remove_test_info_dict_list:
            test_info_dict_list.remove(remove_test)
        return test_info_dict_list

    def get_test_target_id(self):
        """

        :return:
        """
        id_list = [item["test_id"] for item in self.test_target]
        return id_list

    def update_score_list(self):
        """
        更新分数的情况，按照考试试题列表
        有一个考试范围的题目ID列表，根据此表对分数进行保留
        只留题目ID中存在的分数记录
        :return:
        """

        container = list()
        for target_id in self.test_target_id:
            for score_dict in self.score_list:
                if target_id == score_dict["test_id"]:
                    container.append(score_dict)
                    break
        container.sort(key=lambda e:e["score"], reverse=True)
        self.score_list = container

    def select_test_dict_from_target(self, lowest_test):
        """
        从考试范围中查到低分成绩对应的考试信息
        :param lowest_test: 低分成绩字典
        :return:
        """
        test_id = lowest_test["test_id"]
        for target_dict in self.test_target:
            if test_id == target_dict["test_id"]:
                return target_dict


def create_student(sname=None):
    """ 创建一个学生"""
    # 新建一个学生数据
    # 接收用户输入，学生姓名
    if sname is None:
        name = input("请输入学生姓名：")
    else:
        name = sname
    # 随机出一个学生ID
    id = randomhandle.create_code()
    # 把学生的数据存到数据库中

    # 插入学生字典的构建
    insert_stu_dict = generate_stu_data_dict(id, name)

    print(insert_stu_dict)
    db.insert_into_table("stu_info.json", insert_stu_dict)


def generate_stu_data_dict(id, name):
    """初始化学生数据字典，用于新的学生数据的构建"""
    new_stu_data_dict = {
        "id": id,
        "name": name,
        "level": 1,
        "exp": 0
    }
    return new_stu_data_dict


# 对于新录入的知识，默认给0分

# 实例化资源对象
# source_obj = source.Source()


# def create_student(sname=None):

def load_stu_info():
    with open('base_stu_info', 'r', encoding='utf8') as f:
        c = f.read()
    import json
    c = json.loads(c)
    for dic in c:
        create_student(dic["name"])
        print(dic["name"], '创建完毕')


def all_test():
    all_stu_dict_list = db.read_from_table(table_name_stu_base_info)
    for stu_dict in all_stu_dict_list:
        # print(stu_dict)
        sid = stu_dict["id"]
        stuobj = Student(sid)

        stuobj.have_a_test(g_test_num)
        print(stu_dict["name"], '出题完成')
    # 读学生数据
    # 让每一个学生出题
    # 结束


def score():
    stuobj = Student("td68")
    stuobj.score_all_test()


if __name__ == '__main__':

    # score()

    lihui = Student("td68")
    lihui.have_a_test(10)

    # all_test()

    # stu = Student("ie40")
    # res = stu.get_one_ask()
    # print(res)

    # stu.start()
    # stu.score_all_test()
    # stu.get_target_area()

    # load_stu_info()
