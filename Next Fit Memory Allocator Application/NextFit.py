import tkinter as tk
from tkinter import messagebox

# Memory Block Class
class MemoryBlock:
    def __init__(self, size):
        self.size = size
        self.is_allocated = False
        self.allocated_to = None

# Process Class
class Process:
    def __init__(self, size, process_id):
        self.size = size
        self.process_id = process_id

# Next Fit Class
class NextFitAllocator:
    def __init__(self, memory_blocks):
        self.memory_blocks = [MemoryBlock(size) for size in memory_blocks]
        self.last_allocated_index = -1
        self.allocations = []

    def allocate(self, process, output_text):
        n = len(self.memory_blocks)
        start_index = (self.last_allocated_index + 1) % n
        index = start_index

        while True:
            block = self.memory_blocks[index]

            if block.size >= process.size:  # Check if block size is greater than or equal to process size
                block.is_allocated = True
                block.size -= process.size
                block.allocated_to = process.process_id
                self.last_allocated_index = index
                self.allocations.append((process.process_id, process.size, index + 1))
                output_text.insert(tk.END, f"\nProcess {process.process_id} requiring {process.size} KB allocated to Block {index + 1}\n")
                return True

            index = (index + 1) % n
            if index == start_index:
                break

        output_text.insert(tk.END, f"\nProcess {process.process_id} requiring {process.size} KB could not be allocated.\n")
        return False

    def print_memory_state(self, output_text):
        output_text.insert(tk.END, "\nCurrent Memory State:\n")
        for i, block in enumerate(self.memory_blocks):
            if block.is_allocated:  # Check Block is allocated
                if block.size == 0:
                    output_text.insert(tk.END, f"\tBlock {i + 1}: Allocated to Process {block.allocated_to}\n")
                else:
                    output_text.insert(tk.END, f"\tBlock {i + 1}: {block.size} KB (free, remaining after allocation to Process {block.allocated_to})\n")
            else:  # Check Block is not allocated
                output_text.insert(tk.END, f"\tBlock {i + 1}: {block.size} KB (free)\n")

    def print_final_allocation(self, output_text):
        output_text.insert(tk.END, "\nFinal Memory Allocation:\n")
        for allocation in self.allocations:
            process_id, size, block_number = allocation
            output_text.insert(tk.END, f"\tProcess {process_id}: Allocated {size} KB in Block {block_number}.\n")

# GUI Implementation
def run_allocator():
    def allocate_processes():
        try:
            TOTAL_MAIN_MEMORY = 5120  # Fixed total main memory size is 5 MB
            memory_sizes = list(map(int, block_sizes_entry.get().split(',')))
            if sum(memory_sizes) > TOTAL_MAIN_MEMORY:
                messagebox.showerror("Error", "Total memory block sizes exceed the main memory size of 5120 KB.")
                return

            processes = list(map(int, process_sizes_entry.get().split(',')))

            allocator = NextFitAllocator(memory_sizes)
            output_text.delete(1.0, tk.END)
            for i, size in enumerate(processes):
                process = Process(size, i + 1)
                allocator.allocate(process, output_text)
                allocator.print_memory_state(output_text)

            allocator.print_final_allocation(output_text)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers separated by commas.")

    def clear_output():
        output_text.delete(1.0, tk.END)
        block_sizes_entry.delete(0, tk.END)
        process_sizes_entry.delete(0, tk.END)

    # Create GUI window
    window = tk.Tk()
    window.title("Next Fit Memory Allocator")

    tk.Label(window, text="Enter memory block sizes (in KB, separated by commas):").pack()
    block_sizes_entry = tk.Entry(window, width=50)
    block_sizes_entry.pack()

    tk.Label(window, text="Enter process sizes (in KB, separated by commas):").pack()
    process_sizes_entry = tk.Entry(window, width=50)
    process_sizes_entry.pack()

    # Buttons Frame
    buttons_frame = tk.Frame(window)
    buttons_frame.pack(pady=10)

    allocate_button = tk.Button(buttons_frame, text="Allocate Memory", command=allocate_processes)
    allocate_button.pack(side=tk.LEFT, padx=5)

    clear_button = tk.Button(buttons_frame, text="Clear", command=clear_output)
    clear_button.pack(side=tk.LEFT, padx=5)

    # Add scrollable output
    output_frame = tk.Frame(window)
    output_frame.pack()
    output_scrollbar = tk.Scrollbar(output_frame)
    output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    output_text = tk.Text(output_frame, width=80, height=20, yscrollcommand=output_scrollbar.set)
    output_text.pack(side=tk.LEFT)
    output_scrollbar.config(command=output_text.yview)

    window.mainloop()

# Run the GUI application
run_allocator()
