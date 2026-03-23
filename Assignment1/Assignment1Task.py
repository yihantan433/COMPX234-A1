import threading
import time
import random

# 导入自定义打印文档类和打印队列类
from printDoc import printDoc
from printList import printList

class Assignment1:
    # ===================== 仿真初始化参数 =====================
    NUM_MACHINES = 50        # 发出打印请求的机器数量
    NUM_PRINTERS = 5         # 系统中的打印机数量
    SIMULATION_TIME = 10     # 仿真持续时间（秒），10秒后停止
    MAX_PRINTER_SLEEP = 3    # 打印机最大休眠时间（秒）
    MAX_MACHINE_SLEEP = 5    # 机器最大休眠时间（秒）
    QUEUE_MAX_SIZE = 5       # 打印队列固定容量（任务2要求）

    # ===================== 初始化仿真变量 =====================
    def __init__(self):
        self.sim_active = True  # 仿真运行标志，True=运行中，False=停止
        
        self.print_list = printList()  # 创建打印队列，存储打印请求
        self.mThreads = []             # 存储所有机器线程的列表
        self.pThreads = []             # 存储所有打印机线程的列表
        
        # ===================== 线程同步核心工具 =====================
        self.queue_lock = threading.Lock()  # 互斥锁：保证同一时间只有一个线程操作队列
        
        # 条件变量：队列未满 → 机器可以提交打印任务
        self.queue_not_full = threading.Condition(self.queue_lock)
        # 条件变量：队列非空 → 打印机可以获取打印任务
        self.queue_not_empty = threading.Condition(self.queue_lock)
        
        self.queue_size = 0  # 队列实时长度，用于判断满/空

    # ===================== 启动仿真（主控制方法） =====================
    def startSimulation(self):
        # ---------- 1. 创建所有机器线程和打印机线程 ----------
        # 创建机器线程（生产者）
        for i in range(1, self.NUM_MACHINES + 1):
            machine = self.machineThread(i, self)
            self.mThreads.append(machine)
        
        # 创建打印机线程（消费者）
        for i in range(1, self.NUM_PRINTERS + 1):
            printer = self.printerThread(i, self)
            self.pThreads.append(printer)
        
        # ---------- 2. 启动所有线程 ----------
        # 启动所有机器线程
        for machine in self.mThreads:
            machine.start()
        
        # 启动所有打印机线程
        for printer in self.pThreads:
            printer.start()
        
        # ---------- 3. 仿真运行指定时间 ----------
        time.sleep(self.SIMULATION_TIME)
        
        # ---------- 4. 停止仿真 ----------
        self.sim_active = False  # 设置停止标志，所有线程检测到后退出循环
        
        # 唤醒所有阻塞的线程，避免停止时发生死锁
        with self.queue_lock:
            self.queue_not_full.notify_all()
            self.queue_not_empty.notify_all()
        
        # ---------- 5. 等待所有线程执行完毕（优雅退出） ----------
        # 等待所有打印机线程结束
        for printer in self.pThreads:
            printer.join()
        
        # 等待所有机器线程结束
        for machine in self.mThreads:
            machine.join()
        
        print("=== 仿真结束（已运行10秒）===")

    # ===================== 打印机线程类（消费者） =====================
    class printerThread(threading.Thread):
        def __init__(self, printerID, outer):
            threading.Thread.__init__(self)
            self.printerID = printerID  # 打印机编号
            self.outer = outer          # 外部类引用，访问主程序变量

        def run(self):
            # 只要仿真在运行，就持续循环
            while self.outer.sim_active:
                # 模拟打印机打印耗时
                self.printerSleep()
                
                # 休眠后检查：如果仿真已停止，直接退出线程
                if not self.outer.sim_active:
                    break
                
                # 从队列获取任务并打印
                self.printDox(self.printerID)

        # 打印机随机休眠，模拟工作间隔
        def printerSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_PRINTER_SLEEP)
            time.sleep(sleepSeconds)

        # 打印任务核心方法（线程安全）
        def printDox(self, printerID):
            # 使用条件变量加锁，独占访问队列
            with self.outer.queue_not_empty:
                # 如果队列为空 且 仿真未停止 → 线程阻塞等待
                while self.outer.queue_size == 0 and self.outer.sim_active:
                    self.outer.queue_not_empty.wait()
                
                # 如果仿真已停止，直接返回
                if not self.outer.sim_active:
                    return
                
                print(f"打印机 ID: {printerID} : 现在空闲，开始打印")
                # 从队列取出任务并打印
                self.outer.print_list.queuePrint(printerID)
                
                # 取出任务后，队列长度-1
                self.outer.queue_size -= 1
                # 唤醒一个等待的机器线程（队列已有空位，可以提交任务）
                self.outer.queue_not_full.notify()

    # ===================== 机器线程类（生产者） =====================
    class machineThread(threading.Thread):
        def __init__(self, machineID, outer):
            threading.Thread.__init__(self)
            self.machineID = machineID  # 机器编号
            self.outer = outer          # 外部类引用，访问主程序变量

        def run(self):
            # 只要仿真在运行，就持续循环
            while self.outer.sim_active:
                # 机器随机休眠，模拟工作间隔
                self.machineSleep()
                
                # 休眠后检查：如果仿真已停止，直接退出线程
                if not self.outer.sim_active:
                    break
                
                # 发送打印请求到队列
                self.printRequest(self.machineID)

        # 机器随机休眠
        def machineSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleepSeconds)

        # 提交打印请求核心方法（线程安全）
        def printRequest(self, id):
            # 使用条件变量加锁，独占访问队列
            with self.outer.queue_not_full:
                # 如果队列已满 且 仿真未停止 → 线程阻塞等待
                while self.outer.queue_size >= self.outer.QUEUE_MAX_SIZE and self.outer.sim_active:
                    self.outer.queue_not_full.wait()
                
                # 如果仿真已停止，直接返回
                if not self.outer.sim_active:
                    return
                
                print(f"机器 {id} 发送了一个打印请求")
                # 创建打印文档对象
                doc = printDoc(f"我是机器 {id}", id)
                # 将打印任务插入队列
                self.outer.print_list.queueInsert(doc)
                
                # 插入任务后，队列长度+1
                self.outer.queue_size += 1
                # 唤醒一个等待的打印机线程（队列已有任务，可以打印）
                self.outer.queue_not_empty.notify()