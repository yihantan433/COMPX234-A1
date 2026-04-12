## Design
This is a monitor-style solution to the Readers-Writers problem.
Multiple readers can read concurrently when no writer is active.
Writers are guaranteed exclusive access to the shared resource.
Synchronization uses Python threading.Condition for safe waiting and notification.

## How to Run
1. Make sure you have Python installed
2. Run the command/click the run button
   python readers_writers.py

sample output：
Reader 2 wants to read
Reader 2 starts reading (active readers: 1)
Reader 2 is READING
Reader 3 wants to read
Reader 3 starts reading (active readers: 2)
Reader 3 is READING
Writer 1 wants to write
Reader 1 wants to read
Reader 1 starts reading (active readers: 3)
Reader 1 is READING
Writer 2 wants to write
Reader 2 finished reading (active readers: 2)
Reader 2 finished reading
Reader 1 finished reading (active readers: 1)
Reader 1 finished reading
Reader 1 wants to read
Reader 1 starts reading (active readers: 2)
Reader 1 is READING
Reader 3 finished reading (active readers: 1)
Reader 3 finished reading
Reader 2 wants to read
Reader 2 starts reading (active readers: 2)
Reader 2 is READING
Reader 1 finished reading (active readers: 1)
Reader 1 finished reading
Reader 3 wants to read
Reader 3 starts reading (active readers: 2)
Reader 3 is READING
Reader 2 finished reading (active readers: 1)
Reader 2 finished reading
Reader 1 wants to read
Reader 1 starts reading (active readers: 2)
Reader 1 is READING
Reader 2 wants to read
Reader 2 starts reading (active readers: 3)
Reader 2 is READING
Reader 1 finished reading (active readers: 2)
Reader 1 finished reading
Reader 3 finished reading (active readers: 1)
Reader 3 finished reading
Reader 2 finished reading (active readers: 0)
Reader 2 finished reading
Writer 1 starts writing (waiting writers: 1)
Writer 1 is WRITING
Reader 3 wants to read
Writer 1 finished writing
Writer 1 finished writing
Reader 3 starts reading (active readers: 1)
Reader 3 is READING
Reader 3 finished reading (active readers: 0)
Reader 3 finished reading
Writer 2 starts writing (waiting writers: 0)
Writer 2 is WRITING
Writer 1 wants to write
Writer 2 finished writing
Writer 2 finished writing
Writer 1 starts writing (waiting writers: 0)
Writer 1 is WRITING
Writer 2 wants to write
Writer 1 finished writing
Writer 1 finished writing
Writer 2 starts writing (waiting writers: 0)
Writer 2 is WRITING
Writer 2 finished writing
Writer 2 finished writing
Simulation completed