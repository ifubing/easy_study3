from bin import source
from bin import student


def main_menu():
    """ 程序主菜单 """
    menu_list = [
        {"1", student}
    ]
    return menu_list


class EasyStudy:
    """ 易学习系统类 """
    def __init__(self):
        pass

    def show_menu(self):
        print('欢迎菜单的展现')

    def select_func(self):
        """用户输入数字编号，执行对应的功能"""
        pass

    def start(self):
        # 显示一个欢迎菜单插入学生的成绩成功
        self.menu = self.show_menu()

        # 用户输入数字编号，执行对应的功能
        self.select_func()

# 实例化生成学习系统对象
# es = EasyStudy()
# es.start()

# 更新课程
source.Source()

def start():
    strNum = input("输入要的操作：1-生成考试；2-打分；3-个人测试")
    if strNum == "1":
        student.all_test()
    elif strNum == "2":
        student.score()
    elif strNum == "3":
        lihui = student.Student("td68")
        lihui.have_a_test(10)
    else:
        print("非法输出，程序结束")

start()