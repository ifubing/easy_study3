"""
资源模块

初始化时做以下操作
读取资源目录下全部文件，并把文件转换为列表包字典
读取数据库中存放的数据
比对两种数据，一切以资源目录下最新数据为准。数据库中会保存新添加的，删掉修改或删除掉的

数据重点
插入数据时，确保数据具备 “test_id” 字段，格式为2个英文8个数字
"""
import os

from lib import filehandle
from lib.dbsql.dbfile import db
from lib import randomhandle

# 模块的配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source_dir = os.path.join(BASE_DIR, "source")
# 存放知识源的数据表名称
table_name_source = "source"


class Source:
    def __init__(self):
        self.update_source_data()

    def update_source_data(self):
        """ 更新资源数据 """
        # 把内容转变为数据

        # 获取最新的内容-从知识文本中提取出来的内容
        source_data = self.load_source_data()

        # 获取数据库中保存的内容-存在数据库中的内容
        read_data = self.read_source_data_from_db()

        # 比对这两个内容，得到需要添加的与需要删除的数据
        del_data_list, insert_data_list = self.compare_two_knowledge_data(source_data, read_data)
        print("要删除的数据有%d条，详情为%s" %(len(del_data_list), del_data_list))
        print("要添加的数据有%d条，详情为%s" %(len(insert_data_list), insert_data_list))

        # 数据库的操作，添加与删除
        # 删除
        self.del_many_from_table(del_data_list)
        # 添加
        self.insert_many_in2_table(insert_data_list)


        # 把数据存放到数据库中,去重与更新形式的转换
        # 存数据
        # db.truncate_table(table_name_source)  # 清空列表
        # db.insert_many_into_table(table_name_source, source_data)



    # 辅助功能
    def load_source_data(self):
        """
        获取所有的数据
        最新最新的数据
        从资源目录中读取题目，并返回
        :return: 题目资源
        {'ask': ['问题行1\n', '问题行2\n'], 'ans': ['答案行1\n', '答案行2\n'], 'tips': ['补充行1\n', '补允行2'], '1': 'django-test', '2': '02-基本使用', '3': '01-基本.txt', 'file_path': 'G:\\易三\\source\\django-test\\02-基本使用\\01-基本.txt'}
        """
        source_data = filehandle.get_dir_all_file_data(source_dir)

        # 调试，显示
        print("定位：1908110553加载到了%s题" % len(source_data))
        # for s in source_data:
        #     print(s)

        return source_data


    def read_source_data_from_db(self):
        """ 从数据库中读存好的数据 """
        read_data = db.read_from_table(table_name_source)
        # print(read_data)
        return read_data

    def del_many_from_table(self, del_data_list):
        db.delete_many_from_table(table_name_source, del_data_list)

        # 删除学生数据表


    def insert_many_in2_table(self, insert_data_list):
        """插入多条"""
        # 先给需要插入的数据添加一个test_id
        for insert_data in insert_data_list:
            test_id = randomhandle.create_code(2, 8)
            insert_data.update({
                "test_id": test_id
            })
        db.insert_many_into_table(table_name_source, insert_data_list)
        print("插入数据成功，插入了%d条" % len(insert_data_list))

# del_data_list, insert_data_list = self.compare_two_knowledge_data(source_data, read_data)
    def compare_two_knowledge_data(self, source_data, read_data):
        """ 比较两种数据，返回需要删除的数据瑟需要添加的数据"""
        # 把两者的数据进行格式同步化
        for tmp in read_data:
            if "test_id" in tmp:
                tmp.pop("test_id")

        del_data_list = list()  # 要删除的
        insert_data_list = list()  # 要插入的

        # 以最新的源为准进行比对
        for source in source_data:
            # 如果题不在数据库中，就需要添加了
            if source not in read_data:
                insert_data_list.append(source)
            # 如果题在数据库中，什么也不做

        # 以旧的数据为源进行比对
        for read in read_data:
            if read not in source_data:
                del_data_list.append(read)

        return del_data_list, insert_data_list





if __name__ == '__main__':
    obj = Source()
    # obj.load_source_data()