"""非关系型数据库的功能模拟"""
import json
import logging
import os
import time

# 数据库里的所有的提示，不允许使用print语句担示。用logging模块。菜单用print语句输出

db_file_dir = os.path.dirname(os.path.abspath(__file__))

databases_dir = os.path.join(db_file_dir, "databases")



class Database:
    """数据库的类"""

    def __init__(self):
        self.database = None  # 数据库的名称
        self.database_path = None  # 数据库的地址
        self.table = None  # 表名称
        self.table_path = None  # 表的路径

    # 库操作 ##########
    # 增删改查
    def create_database(self, database_name):
        """
        创建数据库
        数据库创建好以后，自动切换到新建好的数据库
        需要做一个判断，如果这个数据库已经存在，就不创建

        :param database_name: 数据库的名称
        :return:
        """
        temp_database_path = os.path.join(databases_dir, database_name)
        # todo 1 验证，目录存在就不创建。 2 创建好后自动切换到新目录
        os.mkdir(temp_database_path)
        print("数据库创建成功：%s" %database_name)


    def show_databases(self):
        """查看所有的数据库有哪些"""
        # 用print语句来输出结果
        for database_name in os.listdir(databases_dir):
            print(database_name)

    def use_database(self, database_name):  # user_database = check(use_database)
        """
        切换数据库
        :param database_name: 数据库名称
        :return:
        """
        path = self.get_database_path_by_name(database_name)
        # G:\易二\dbsql\databases\python
        self.database = database_name  # 记录数扭库的名称
        self.database_path = path  # 记录数据库的路径
        print("数据库切换成功：%s" % database_name)

    def select_database(self):
        """显示当前选中的数据库"""
        print(self.database)

    def rename_database(self, old_name, new_name):
        """
        修改数据库的名称
        :param old_name: 旧名字
        :param new_name: 新名字
        :return:
        """
        # 提示更名成功
        # 根据老数据库名，得到一个路径
        old_database_path = self.get_database_path_by_name(old_name)
        # 根据新的数据库名，得到另一个路径
        new_database_path = self.get_database_path_by_name(new_name)
        os.rename(old_database_path, new_database_path)


    def drop_database(self, database_name):
        """
        删除数据库
        先验证数据库是否存在，存在就删，不存在就提示
        :param database_name: 数据库名称
        :return:
        """
        # 拿数据库目录的路径
        path = self.get_database_path_by_name(database_name)
        # 删除目录下的全部文件名称列表
        file_name_list = os.listdir(path)  # ["stuinfo.db", "tearch.db"]   []
        for file_name in file_name_list:
            file_path = os.path.join(path, file_name)
            os.remove(file_path)
        os.rmdir(path)


    # 表操作  ##########
    def show_tables(self):
        """查看有哪些数据表"""
        pass
        # print打印输出菜单

    def create_table(self, table_name):
        """创建数据表"""
        path = self.get_table_path_by_name(table_name)
        # todo 验证，如果表已经存在就不要再创建了
        with open(path, "w", encoding="utf8") as f:
            f.write(str([]))
        print("数据表创建成功：%s" % table_name)

    def drop_table(self, table_name):
        """删除数据表"""
        pass

    def truncate_table(self, table_name):
        """ 清空数据表 """
        path = self.get_table_path_by_name(table_name)

        with open(path, "w", encoding="utf8") as f:
            f.write("[]")

    def rename_table(self, table_name):
        """修改表名"""
        pass

    def alter_table_change(self, table_name, old_key_name, new_key_name):
        """修改表中的字段名称"""
        # 根据表名称获得表的文件路径
        # 读取文件的内容
        # 遍历，依次拿到每一个字典
        # {"name": "李辉", "sid": "us65"}

        # [{"name": "李辉", "sid": "us65"}，{}] - 把name字段更名为n
        # []{"n": "李辉", "sid": "us65"}

    # 数据的增删改查
    def write_into_table(self, table_name, write_data):
        """写入到数据库中"""
        # todo 确保表一定存在 check，如果不存在，提示
        table_path = self.get_table_path_by_name(table_name)
        with open(table_path, "w", encoding="utf8") as f:
            f.write(json.dumps(write_data, ensure_ascii=False))

    def read_from_table(self, table_name):
        """
        从表中读取所有数据
        :param table_name:
        :return: 表格中的数据,[{},{}]
        """
        path = self.get_table_path_by_name(table_name)
        with open(path, "r", encoding="utf8") as f:
            table_data = json.load(f)
        # print("读取表格成功，从%s表中读取了%s条数据" %(table_name, len(table_data)))
        return table_data

    # 数据行操作  ##########
    def insert_into_table(self, table_name, insert_data_dict):
        """插入一行数据"""
        # 读取数据文件的全部内容  列表包字典
        table_data = self.read_from_table(table_name)
        # 在列表中添加insert_data
        table_data.append(insert_data_dict)
        # 保存最新的数据到数据文件（重写保存）
        self.write_into_table(table_name, table_data)
        # print("往%s表中插入数据%s成功" %(table_name, insert_data_dict) )

    def insert_many_into_table(self, table_name, data_list):
        # data_list = [{},{},{}]
        """插入多行数据"""
        for data in data_list:
            self.insert_into_table(table_name, data)
        print("插入多行数据成功：往%s表中插入了%s行数据" %(table_name, len(data_list)))

    def update_table_set(self, table_name, cond, up_dict={}):
        # update student set score=80 where id=2

        """更新一行数据"""
        # 读取全部表内容
        table_data = self.read_from_table(table_name) # [张三，新李四，王五]
        # 查找符合条件的数据
        data_list = self.select_from_table(table_name, cond)  # [{李四age18}, {王五}]
        # 遍历并更新数据
        for data in data_list:  # data = {李四}
            idx = self.get_data_index_at_table(table_name, data)  # 1
            data.update(up_dict)  # 李四字典.update({"age":22})   {李四age22}
            table_data[idx] = data  # 列表[李四的索引] = 新的李四字典
        # 保存数据
        self.write_into_table(table_name, table_data)


    def delete_from_table(self, table_name, cond):
        """
        删除符合条件的数据
        :param table_name:
        :param cond:{"age":20, "gender":0}
        :return:
        """
        # 读文件内容
        # 找到要删的数据们
        # 删除数据
        # 保存文件
        table_data = self.read_from_table(table_name)
        data_list = self.select_from_table(table_name, cond)
        for data in data_list:
            table_data.remove(data)
        self.write_into_table(table_name, table_data)

    def delete_many_from_table(self, table_name, cond_list):
        """ 删除多个数据 """
        for cond in cond_list:
            self.delete_from_table(table_name, cond)
        print("删除多条记录完成，删除了%d条" % len(cond_list))


    def select_from_table(self, table_name, cond={}):
        """
        挑选出符合条件的数据
        :param table_name:
        :param cond: {"gender":1, "class":"python"}
        :return:[{},{}]
        """
        # path = self.get_table_path_by_name(table_name)
        table_data = self.read_from_table(table_name)
        data_container = list()
        cond_len = len(cond)  # 条件个数
        for data in table_data:
            n = 0  # 符合条件数，计数
            for k, v in cond.items():
                if k in data and data[k] == v:
                    n += 1
            if n == cond_len:
                data_container.append(data)
        return data_container

    # 通用操作  ##########
    def get_table_path_by_name(self, table_name):
        """获取表的路径"""
        # todo 需验证，database得先选中才行，装饰器
        return os.path.join(self.database_path, table_name)

    def get_database_path_by_name(self, database_name):
        # 比如 "python"
        # G:\易二\dbsql\databases\
        # python
        return os.path.join(databases_dir, database_name)

    def check_database_exists(self, database_name):
        """
        检测数据库是否存在
        :param database_name:
        :return:
        """
        pass
        # 日志显示是否存在
        # return {"path":数据库路径, "is_exist":布尔值}

    def check_table_exists(self, table_name):
        """
        检测数据库是否存在
        :param database_name:
        :return:
        """
        print("464646")
        pass
        # return {"path":数据库路径, "is_exist":布尔值}

    def ensure_table_exists(self, table_name):
        path = self.get_table_path_by_name(table_name)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf8") as f:
                f.write("[]")

    def get_data_index_at_table(self, table_name, row_data):
        """获取数据在表中的索引位置"""
        table_data = self.read_from_table(table_name)
        data_index = table_data.index(row_data)
        return data_index

    def test_clear_score_data(self, db_name):
        db_path = os.path.join(databases_dir, db_name)
        stu_score_path = os.path.join(db_path, "stu_score")
        exam_data_path = os.path.join(db_path, "exam_data")

        self.truncate_table(stu_score_path)
        self.truncate_table(exam_data_path)
        print('llll')

# 针对当前项目的个性化设置
db = Database()
db.use_database("python")


if __name__ == '__main__':

    # db.test_clear_score_data("python")
    res = db.read_from_table("stu_score")
    print(len(res))

    # db = Database()
    # db.create_table("exam_data")  # 创建表
    # db.create_database("python2")
    # db.use_database("python")