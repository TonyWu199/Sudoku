#coding:utf-8
from stack import ArrayStack
import time
import sys
sys.setrecursionlimit(5000) # set the maximum depth as 1500


class Transfer:
    def __init__(self,str):
        self.str = str
        self.matrix = [[0 for col in range(9)] for row in range(9)]
        self.possible_cell = {i: [1, 2, 3, 4, 5, 6, 7, 8, 9] for i in range(81)}
        self.init_check = {i: 0 for i in range(81)}          #判别该格数值是否能改
        self.count = 0
        self.stack = ArrayStack()

    def get_matrix(self):
        shudu = open(self.str, "r").readline()
        shudu = shudu.replace(",", "")
        (i,j,m) = (0,0,0)
        for i in range(9):
            for j in range(9):
                self.matrix[i][j] = int(shudu[m])
                m = m + 1
        return self.matrix

    def update(self):

        #每一格做行、列排除，选出每一格可能的值
        count = 0
        for row in range(9):
            for col in range(9):
                if self.matrix[row][col] == 0:
                    list_temp_row = []
                    list_temp_col = []
                    for col_temp in range(9):
                        list_temp_row.append(self.matrix[row][col_temp])
                        list_temp_col.append(self.matrix[col_temp][col])
                    #注意remove函数没有返回值,这里先去0的重复，再删除0
                    list_temp_row = list(set(list_temp_row))
                    list_temp_col = list(set(list_temp_col))
                    list_temp_row.remove(0)
                    list_temp_col.remove(0)
                    self.possible_cell[count] = list(set(self.possible_cell[count]) - (set(list_temp_col) | set(list_temp_row)))
                else:
                    self.possible_cell[count] = [self.matrix[row][col]]
                count += 1

        #每一格做宫排除
        gong_1 = []   #保存每个小九宫格
        gong = []   #整个数独的小九宫格储存，左→右，上→下
        for num_row in range(3):
            for num_col in range(3):
                gong_temp = []
                gong_temp.append(self.matrix[num_col * 3 + 0][num_row * 3:num_row * 3 + 3])
                gong_temp.append(self.matrix[num_col * 3 + 1][num_row * 3:num_row * 3 + 3])
                gong_temp.append(self.matrix[num_col * 3 + 2][num_row * 3:num_row * 3 + 3])
                temp = list(set(gong_temp[0]) | set(gong_temp[1]) | set(gong_temp[2]))
                if 0 in temp:
                    temp.remove(0)
                gong_1.append(temp)
        gong.append(gong_1[0])
        gong.append(gong_1[3])
        gong.append(gong_1[6])
        gong.append(gong_1[1])
        gong.append(gong_1[4])
        gong.append(gong_1[7])
        gong.append(gong_1[2])
        gong.append(gong_1[5])
        gong.append(gong_1[8])
        #print gong

        count = 0
        for row in range(9):
            for col in range(9):
                if self.matrix[row][col] == 0:
                    if row <= 2 and col <= 2:
                        self.possible_cell[count] = list(set(self.possible_cell[count]) - set(gong[0]))
                    elif row <= 2 and 3 <= col <= 5:
                        self.possible_cell[count] = list(set(self.possible_cell[count]) - set(gong[1]))
                    elif row <= 2 and 6 <= col <= 8:
                        self.possible_cell[count] = list(set(self.possible_cell[count]) - set(gong[2]))
                    elif 3 <= row <= 5 and col <= 2:
                        self.possible_cell[count] = list(set(self.possible_cell[count]) - set(gong[3]))
                    elif 3 <= row <= 5 and 3 <= col <= 5:
                        self.possible_cell[count] = list(set(self.possible_cell[count]) - set(gong[4]))
                    elif 3 <= row <= 5 and 6 <= col <= 8:
                        self.possible_cell[count] = list(set(self.possible_cell[count]) - set(gong[5]))
                    elif 6 <= row <= 8 and col <= 2:
                        self.possible_cell[count] = list(set(self.possible_cell[count]) - set(gong[6]))
                    elif 6 <= row <= 8 and 3 <= col <= 5:
                        self.possible_cell[count] = list(set(self.possible_cell[count]) - set(gong[7]))
                    else:
                        self.possible_cell[count] = list(set(self.possible_cell[count]) - set(gong[8]))
                else:
                    pass
                count += 1

    def insert_first(self):
        #迭代将所有只有一种结果的格子填入
        def insert_one():
            count = 0
            self.update()
            #print self.possible_cell
            for row in range(9):
                for col in range(9):
                    #print self.possible_cell[count]
                    if self.matrix[row][col] == 0:
                        #只有一种情况
                        if len(self.possible_cell[count]) == 1:
                            self.matrix[row][col] = self.possible_cell[count][0]
                            self.init_check[count] = 1
                            #print self.matrix
                            insert_one()
                        else:
                            pass
                    else:
                        self.init_check[count] = 1
                        pass
                    count += 1
        insert_one()

    def insert_main(self):
        #先将原始可能列表入栈，注意，序号为count执行时，堆栈顶储存的是count格未填入的状态
        temp = self.possible_cell.copy()
        self.stack.push(temp)

        def insert():
            if self.init_check[self.count] == 0: #待填入的格
                possible_save = self.possible_cell.copy()    #当前可能状况
                for item in self.possible_cell[self.count]:
                    self.matrix[self.count / 9][self.count % 9] = item    #尝试填入
                    self.update()   #更新可能列表
                    #check部分
                    flag = False
                    for num in range(81):
                        if self.possible_cell[num] == []:      #列表中出现[]表明填写错误
                            self.possible_cell = possible_save   #更新失效，回复原列表
                            flag = True
                            break
                    if flag == True:
                        continue
                    #字典无[]，压入可能值列表，进行下面的递归
                    temp = self.possible_cell.copy()
                    self.stack.push(temp)   #存入更新
                    if self.count < 80:
                        self.count += 1
                    elif self.count == 80:
                        return
                    insert()
                    #迭代完成
                    if self.count == 80:
                        return
                #无论怎么填下一步都无解，上一步填写有问题
                self.matrix[self.count / 9][self.count % 9] = 0   #修改赋值
                self.stack.pop()   #弹出上一步假设的可能情况
                self.count -= 1   #序号上回到上步
                temp = self.stack.top()  #可能情况表为栈顶
                self.possible_cell = temp.copy()
                return

            else:   #已确定的格
                if self.count < 80:
                    self.count += 1
                insert()
                #迭代完成
                if self.count == 80:
                    return
                self.count -= 1
                return

        insert()

    def out_put(self):
        for i in self.matrix:
            print i

if __name__ == "__main__":
    time_start = time.time()
    g = Transfer("Matrix.txt")
    g.get_matrix()
    g.insert_first()
    g.insert_main()
    g.out_put()
    time_end = time.time()
    print time_end-time_start
