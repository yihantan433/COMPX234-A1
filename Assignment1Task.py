import threading
import time
import random

from printDoc import printDoc
from printList import printList

class Assignment1:
    # Simulation Initialisation parameters
    NUM_MACHINES = 50        # Number of machines that issue print requests
    NUM_PRINTERS = 5         # Number of printers in the system
    SIMULATION_TIME = 10     # Simulation duration in seconds (set to 10s stop)
    MAX_PRINTER_SLEEP = 3    # Maximum sleep time for printers (in seconds)
    MAX_MACHINE_SLEEP = 5    # Maximum sleep time for machines (in seconds)
    QUEUE_MAX_SIZE = 5       # Task 2 Requirement: Fixed print queue capacity

    # Initialise simulation variables
    def __init__(self):
        self.sim_active = True
        self.print_list = printList()  # Create an empty list to store print requests
        self.mThreads = []             # List to store machine threads
        self.pThreads = []             # List to store printer threads
        
        # Task 2 Core: Synchronization primitives (Mutex + Condition Variables)
        self.queue_lock = threading.Lock()  # Ensure only one device accesses queue at a time
        self.queue_not_full = threading.Condition(self.queue_lock)  # Condition: Queue is not full (machine can submit)
        self.queue_not_empty = threading.Condition(self.queue_lock) # Condition: Queue is not empty (printer can retrieve)
        self.queue_size = 0  # Real-time queue length for full/empty judgment

    def startSimulation(self):
        # Create Machine and Printer threads
        # Write code here
        # Create machine threads
        for i in range(1, self.NUM_MACHINES + 1):
            machine = self.machineThread(i, self)
            self.mThreads.append(machine)
        
        # Create printer threads
        for i in range(1, self.NUM_PRINTERS + 1):
            printer = self.printerThread(i, self)
            self.pThreads.append(printer)
        
        # Start all the threads
        # Write code here
        # Start all machine threads
        for machine in self.mThreads:
            machine.start()
        
        # Start all printer threads
        for printer in self.pThreads:
            printer.start()
        
        # Let the simulation run for the specified duration
        time.sleep(self.SIMULATION_TIME)
        
        # Finish simulation
        self.sim_active = False
        
        # Wake up all blocked threads to avoid deadlock when stopping
        with self.queue_lock:
            self.queue_not_full.notify_all()
            self.queue_not_empty.notify_all()
        
        # Wait until all printer threads finish by joining them
        # Write code here
        # Wait for all printer threads to complete
        for printer in self.pThreads:
            printer.join()
        
        # Wait for all machine threads to complete (ensure full stop after 10s)
        for machine in self.mThreads:
            machine.join()
        
        print("=== Simulation Ended (10 seconds elapsed) ===")

    # Printer class
    class printerThread(threading.Thread):
        def __init__(self, printerID, outer):
            threading.Thread.__init__(self)
            self.printerID = printerID
            self.outer = outer  # Reference to the parent Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Simulate printer taking some time to print the document
                self.printerSleep()
                
                # Check if simulation has stopped after waking up to avoid invalid operations
                if not self.outer.sim_active:
                    break
                
                # Grab the request at the head of the queue and print it
                # Write code here
                self.printDox(self.printerID)

        def printerSleep(self):
            # Generate random sleep time for printer
            sleepSeconds = random.randint(1, self.outer.MAX_PRINTER_SLEEP)
            time.sleep(sleepSeconds)

        def printDox(self, printerID):
            # Task 2: Mutually exclusive access to queue, only retrieve when queue is not empty
            with self.outer.queue_not_empty:
                # Block and wait if queue is empty and simulation is still active
                while self.outer.queue_size == 0 and self.outer.sim_active:
                    self.outer.queue_not_empty.wait()
                
                # Exit directly if simulation has stopped
                if not self.outer.sim_active:
                    return
                
                print(f"Printer ID: {printerID} : now available")
                # Retrieve and print request from queue
                self.outer.print_list.queuePrint(printerID)
                
                # Decrease queue size after retrieving task, wake up blocked machines (queue has space)
                self.outer.queue_size -= 1
                self.outer.queue_not_full.notify()

    # Machine class
    class machineThread(threading.Thread):
        def __init__(self, machineID, outer):
            threading.Thread.__init__(self)
            self.machineID = machineID
            self.outer = outer  # Reference to the parent Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Machine sleeps for a random amount of time
                self.machineSleep()
                
                # Check if simulation has stopped after waking up to avoid invalid operations
                if not self.outer.sim_active:
                    break
                
                # Machine wakes up and sends a print request
                # Write code here
                self.printRequest(self.machineID)

        def machineSleep(self):
            # Generate random sleep time for machine
            sleepSeconds = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleepSeconds)

        def printRequest(self, id):
            # Task 2: Mutually exclusive access to queue, only submit when queue is not full (no overwrite)
            with self.outer.queue_not_full:
                # Block and wait if queue is full and simulation is still active (completely avoid overwrite)
                while self.outer.queue_size >= self.outer.QUEUE_MAX_SIZE and self.outer.sim_active:
                    self.outer.queue_not_full.wait()
                
                # Exit directly if simulation has stopped
                if not self.outer.sim_active:
                    return
                
                print(f"Machine {id} Sent a print request")
                # Create a print document object
                doc = printDoc(f"My name is machine {id}", id)
                # Insert print request into queue
                self.outer.print_list.queueInsert(doc)
                
                # Increase queue size after submitting task, wake up blocked printers (queue has tasks)
                self.outer.queue_size += 1
                self.outer.queue_not_empty.notify()