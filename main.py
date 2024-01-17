import socket
import time
import serial
import math
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk
import sys

class RobotProgramGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Program")

        # Load the image
        image_path = "fugro-logo.jpg"
        img = Image.open(image_path)
        img = img.resize((700, 300))
        self.logo_image = ImageTk.PhotoImage(img)

        # Create an image label (1. Logo)
        self.image_label = tk.Label(root, image=self.logo_image)
        self.image_label.pack(pady=10)

        # Create entry boxes for sample depth and total drill depth (2. Input Boxes)
        self.sample_depth_label = tk.Label(root, text="Sample Depth:")
        self.sample_depth_label.pack()
        self.sample_depth_entry = tk.Entry(root)
        self.sample_depth_entry.pack(pady=5)

        self.total_depth_label = tk.Label(root, text="Total Drill Depth:")
        self.total_depth_label.pack()
        self.total_depth_entry = tk.Entry(root)
        self.total_depth_entry.pack(pady=5)

        # Create a "Run Program" button (3. Run Program Button)
        self.run_button = tk.Button(root, text="Run Program", command=self.run_program)
        self.run_button.pack(pady=10)

    def run_program(self):
        # Retrieve values from the entry boxes
        sample_depth = int(self.sample_depth_entry.get())
        total_depth = int(self.total_depth_entry.get())

        # Hide the initial window
        self.root.withdraw()

        # Create a thread to execute the program
        thread = Thread(target=self.execute_program, args=(sample_depth, total_depth))
        thread.start()

        # Create a new window
        self.new_root = tk.Tk()
        self.new_root.title("Robot Program Running")

        # Create a label indicating the program is running
        running_label = tk.Label(self.new_root, text="Running the Robot Program...")
        running_label.pack(pady=10)

        # Create a canvas for drawing
        canvas = tk.Canvas(self.new_root, width=400, height=300, bg="white")
        canvas.pack(pady=10)

        # Draw three red circles on the canvas
        circle1 = canvas.create_oval(50, 50, 100, 100, fill="red")
        circle2 = canvas.create_oval(150, 50, 200, 100, fill="red")
        circle3 = canvas.create_oval(250, 50, 300, 100, fill="red")

        # Store the circle IDs in a list for later reference
        self.circle_ids = [circle1, circle2, circle3]

        # Create a "Close" button below the canvas
        close_button = tk.Button(self.new_root, text="Close", command=self.close_program)
        close_button.pack(pady=10)

        # Change the color of the first circle to green after a certain robot movement
        for i in range(3):
            self.change_circle_color(canvas, self.circle_ids[i], "green")

    def execute_program(self, sample_depth, total_depth):
        print(f"Sample Depth: {sample_depth}")
        print(f"Total Drill Depth: {total_depth}")

        # Simulating a long-running process
        # time.sleep(10)
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the robot is listening
        robot_address = ('192.168.0.5', 9225)
        sock.connect(robot_address)
        
        # arduino shit
        arduino_port = 'COM3'
        ser = serial.Serial(arduino_port, 9600, timeout=1)

        time.sleep(2)

        try:
            print("hello")

            # Switch ON I/O at the beginning of the execution
            sock.sendall(b"set_digital_output(9, ON)")
            time.sleep(1)
            sock.sendall(b"set_digital_output(6, ON)")
            time.sleep(1)
            sock.sendall(b"set_digital_output(1, ON)")
            time.sleep(1)

            #sample_depth = int(input("How deep till sample depth? "))
            #total_depth = int(input("How deep is the total drill depth (Including depth till sample)? "))

            # Total pipes till sample depth    
            total_till_sample = math.ceil((sample_depth)/3)

            # Total needed standard pipes needed till sample Depth
            standard_till_sample = total_till_sample - 1
            if sample_depth == 0:
                standard_till_sample = total_till_sample

            # Determine how much pipes are needed and round up the number
            Total_samples = math.ceil((total_depth-sample_depth)/3)

            # Set the list with the different types of pipes
            list_drillpipes     =      list(range(1,(1)+1))
            list_standardpipes  =      list(range(2,(6)+1))
            list_samplepipes    =      list(range(7,(9)+1))

            total_standard_pipes =  len(list_standardpipes)
            total_standerd_operation = (standard_till_sample + Total_samples)

            #Determine if there are enough pipes in the system for the operation
            if total_standard_pipes < total_standerd_operation:
                print("Not enough standerd pipes for this operation")
                sys.exit()

            # GANTRY

            drilling_pipe = 1

            while True:
                ser.write((str(drilling_pipe) + '\n').encode('utf-8'))

                # Read and print responses until "Done" is received
                while True:
                    if ser.in_waiting > 0:
                        response = ser.readline().decode('utf-8').strip()
                        print(f"Received response: {response}")
                        if response == "pipe is picked":
                            break

                if response == "pipe is picked":
                    break

            # Next to feeding point
            sock.sendall(b"movel(posx(-476.7, 360.5, 112.2, 178.0, 93.1, -178.9), v=100, a=100)")
            time.sleep(7)

            # Feeding point
            sock.sendall(b"movel(posx(-673.8, 355.7, 129.4, 178.0, 93.1, -178.9), v=70, a=100)")
            time.sleep(7)

            sock.sendall(b"set_digital_output(1, OFF)")
            time.sleep(1)

            # Above feeding point
            sock.sendall(b"movel(posx(-673.8, 355.7, 203.7, 178.0, 93.1, -178.9), v=70, a=100)")
            time.sleep(5)

            # Above rooster box
            sock.sendall(b"movel(posx(32.35, 635, 203.7, 91.56, 89.42, -179.15), v=70, a=100)")
            time.sleep(7)

            # Rooster box
            sock.sendall(b"movel(posx(32.35, 635, 125, 91.56, 89.42, -179.15), v=70, a=100)")
            time.sleep(7)

            sock.sendall(b"set_digital_output(1, ON)")
            time.sleep(1)

            # Next to rooster box
            sock.sendall(b"movel(posx(31.2, 580.1, 96.5, 91.6, 89.4, -179.3), v=100, a=100)")
            time.sleep(5)

            for stp in range(standard_till_sample):
                try:
                    ser.write((str(list_standardpipes[stp]) + '\n').encode('utf-8'))

                    # Read and print responses until "Done" is received
                    while True:
                        if ser.in_waiting > 0:
                            response = ser.readline().decode('utf-8').strip()
                            print(f"Received response: {response}")
                            if response == "pipe is picked":
                                break

                except KeyboardInterrupt:
                    print("Program terminated by user.")
                    ser.close()

                # Next to feeding point
                sock.sendall(b"movel(posx(-476.7, 360.5, 112.2, 178.0, 93.1, -178.9), v=100, a=100)")
                time.sleep(7)

                # Feeding point
                sock.sendall(b"movel(posx(-673.8, 355.7, 129.4, 178.0, 93.1, -178.9), v=70, a=100)")
                time.sleep(7)

                sock.sendall(b"set_digital_output(1, OFF)")
                time.sleep(1)

                # Above feeding point
                sock.sendall(b"movel(posx(-673.8, 355.7, 203.7, 178.0, 93.1, -178.9), v=70, a=100)")
                time.sleep(5)

                # Above rooster box
                sock.sendall(b"movel(posx(32.35, 635, 203.7, 91.56, 89.42, -179.15), v=70, a=100)")
                time.sleep(7)

                # Rooster box
                sock.sendall(b"movel(posx(32.35, 635, 125, 91.56, 89.42, -179.15), v=70, a=100)")
                time.sleep(7)

                sock.sendall(b"set_digital_output(1, ON)")
                time.sleep(1)

                # Next to rooster box
                sock.sendall(b"movel(posx(31.2, 580.1, 96.5, 91.6, 89.4, -179.3), v=100, a=100)")
                time.sleep(5)

            for sap in range(Total_samples):
                try:
                    ser.write((str(list_standardpipes[standard_till_sample + sap]) + '\n').encode('utf-8'))

                    # Read and print responses until "Done" is received
                    while True:
                        if ser.in_waiting > 0:
                            response = ser.readline().decode('utf-8').strip()
                            print(f"Received response: {response}")
                            if response == "pipe is picked":
                                break

                except KeyboardInterrupt:
                    print("Program terminated by user.")
                    ser.close()

                # Next to feeding point
                sock.sendall(b"movel(posx(-476.7, 360.5, 112.2, 178.0, 93.1, -178.9), v=100, a=100)")
                time.sleep(7)

                # Feeding point
                sock.sendall(b"movel(posx(-673.8, 355.7, 129.4, 178.0, 93.1, -178.9), v=70, a=100)")
                time.sleep(7)

                sock.sendall(b"set_digital_output(1, OFF)")
                time.sleep(1)

                # Above feeding point
                sock.sendall(b"movel(posx(-673.8, 355.7, 203.7, 178.0, 93.1, -178.9), v=70, a=100)")
                time.sleep(5)

                # Above rooster box
                sock.sendall(b"movel(posx(32.35, 635, 203.7, 91.56, 89.42, -179.15), v=70, a=100)")
                time.sleep(7)

                # Rooster box
                sock.sendall(b"movel(posx(32.35, 635, 125, 91.56, 89.42, -179.15), v=70, a=100)")
                time.sleep(7)

                sock.sendall(b"set_digital_output(1, ON)")
                time.sleep(1)

                # Next to rooster box
                sock.sendall(b"movel(posx(31.2, 580.1, 96.5, 91.6, 89.4, -179.3), v=100, a=100)")
                time.sleep(5)

                try:
                    ser.write((str(list_samplepipes[sap]) + '\n').encode('utf-8'))

                    # Read and print responses until "Done" is received
                    while True:
                        if ser.in_waiting > 0:
                            response = ser.readline().decode('utf-8').strip()
                            print(f"Received response: {response}")
                            if response == "pipe is picked":
                                break

                except KeyboardInterrupt:
                    print("Program terminated by user.")
                    ser.close()

                # Next to feeding point
                sock.sendall(b"movel(posx(-476.7, 360.5, 112.2, 178.0, 93.1, -178.9), v=100, a=100)")
                time.sleep(7)

                # Feeding point
                sock.sendall(b"movel(posx(-673.8, 355.7, 129.4, 178.0, 93.1, -178.9), v=70, a=100)")
                time.sleep(7)

                sock.sendall(b"set_digital_output(1, OFF)")
                time.sleep(1)

                # Above feeding point
                sock.sendall(b"movel(posx(-673.8, 355.7, 203.7, 178.0, 93.1, -178.9), v=70, a=100)")
                time.sleep(5)

                # Above rooster box
                sock.sendall(b"movel(posx(32.35, 635, 203.7, 91.56, 89.42, -179.15), v=70, a=100)")
                time.sleep(7)

                # Rooster box
                sock.sendall(b"movel(posx(32.35, 635, 125, 91.56, 89.42, -179.15), v=70, a=100)")
                time.sleep(7)

                sock.sendall(b"set_digital_output(1, ON)")
                time.sleep(1)

                # Next to rooster box
                sock.sendall(b"movel(posx(31.2, 580.1, 96.5, 91.6, 89.4, -179.3), v=100, a=100)")
                time.sleep(5)

                # FIRST
                if sap == 0:
                    # Rooster box
                    sock.sendall(b"movel(posx(32.35, 643.31, 104.45, 91.56, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    sock.sendall(b"set_digital_output(1, OFF)")
                    time.sleep(1)

                    # Above rooster box
                    sock.sendall(b"movel(posx(31.3, 642.3, 170, 91.56, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    # Above next to sample
                    sock.sendall(b"movel(posx(370, 465, 170, 3.7, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    # Above sample
                    sock.sendall(b"movel(posx(438, 465, 170, 3.7, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    # Sample
                    sock.sendall(b"movel(posx(438, 465, 100, 3.7, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    sock.sendall(b"set_digital_output(1, ON)")
                    time.sleep(1)

                    # Next to sample
                    sock.sendall(b"movel(posx(370, 465, 100, 3.7, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                # SECOND
                if sap == 1:
                    # Next to rooster box
                    sock.sendall(b"movel(posx(31.2, 580.1, 96.5, 91.56, 89.42, -179.15), v=100, a=100)")
                    time.sleep(5)

                    # Rooster box
                    sock.sendall(b"movel(posx(32.35, 643.31, 104.45, 91.56, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    sock.sendall(b"set_digital_output(1, OFF)")
                    time.sleep(1)

                    # Above rooster box
                    sock.sendall(b"movel(posx(31.3, 642.3, 170, 91.56, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    # Above next to sample
                    sock.sendall(b"movel(posx(370, 382, 170, 3.7, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    # Above sample
                    sock.sendall(b"movel(posx(438, 382, 170, 3.7, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    # Sample
                    sock.sendall(b"movel(posx(438, 382, 100, 3.7, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    sock.sendall(b"set_digital_output(1, ON)")
                    time.sleep(1)

                    # Next to sample
                    sock.sendall(b"movel(posx(250, 382, 100, 3.7, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                # THIRD
                if sap == 2:
                    # Next to rooster box
                    sock.sendall(b"movel(posx(31.2, 580.1, 96.5, 91.56, 89.42, -179.15), v=100, a=100)")
                    time.sleep(5)

                    # Rooster box
                    sock.sendall(b"movel(posx(32.35, 643.31, 104.45, 91.56, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    sock.sendall(b"set_digital_output(1, OFF)")
                    time.sleep(1)

                    # Above rooster box
                    sock.sendall(b"movel(posx(31.3, 642.3, 170, 91.56, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    # Above next to sample
                    sock.sendall(b"movel(posx(338, 298, 170, 3.7, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    # Above sample
                    sock.sendall(b"movel(posx(438, 298, 170, 3.7, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    # Sample
                    sock.sendall(b"movel(posx(438, 298, 100, 3.7, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

                    sock.sendall(b"set_digital_output(1, ON)")
                    time.sleep(1)

                    # Next to sample
                    sock.sendall(b"movel(posx(250, 298, 100, 3.7, 89.42, -179.15), v=70, a=100)")
                    time.sleep(5)

            for put in reversed(range(total_standerd_operation)):
                # Next to rooster box
                sock.sendall(b"movel(posx(31.2, 580.1, 96.5, 91.56, 89.42, -179.15), v=100, a=100)")
                time.sleep(5)

                # Rooster box
                sock.sendall(b"movel(posx(32.35, 643.31, 104.45, 91.56, 89.42, -179.15), v=70, a=100)")
                time.sleep(5)

                sock.sendall(b"set_digital_output(1, OFF)")
                time.sleep(1)

                # Above rooster box
                sock.sendall(b"movel(posx(31.3, 642.3, 170, 91.56, 89.42, -179.15), v=70, a=100)")
                time.sleep(5)

                # Next to feeding point
                sock.sendall(b"movel(posx(-476.7, 360.5, 112.2, 178.0, 93.1, -178.9), v=100, a=100)")
                time.sleep(7)

                # Above feeding point
                sock.sendall(b"movel(posx(-673.8, 355.7, 203.7, 178.0, 93.1, -178.9), v=70, a=100)")
                time.sleep(5)

                # Feeding point
                sock.sendall(b"movel(posx(-673.8, 355.7, 129.4, 178.0, 93.1, -178.9), v=70, a=100)")
                time.sleep(7)

                sock.sendall(b"set_digital_output(1, ON)")
                time.sleep(1)

                # Next to feeding point
                sock.sendall(b"movel(posx(-476.7, 360.5, 112.2, 178.0, 93.1, -178.9), v=100, a=100)")
                time.sleep(7)

                # Next to rooster box
                sock.sendall(b"movel(posx(31.2, 580.1, 96.5, 91.56, 89.42, -179.15), v=100, a=100)")
                time.sleep(5)

                try:
                    ser.write((str(list_standardpipes[put]) + 'B' + '\n').encode('utf-8'))

                    # Read and print responses until "Done" is received
                    while True:
                        if ser.in_waiting > 0:
                            response = ser.readline().decode('utf-8').strip()
                            print(f"Received response: {response}")
                            if response == "pipe is picked":
                                break

                except KeyboardInterrupt:
                    print("Program terminated by user.")
                    ser.close()
                
            # Rooster box
            sock.sendall(b"movel(posx(32.35, 643.31, 104.45, 91.56, 89.42, -179.15), v=70, a=100)")
            time.sleep(5)

            sock.sendall(b"set_digital_output(1, OFF)")
            time.sleep(1)

            # Above rooster box
            sock.sendall(b"movel(posx(31.3, 642.3, 170, 91.56, 89.42, -179.15), v=70, a=100)")
            time.sleep(5)

            # Next to feeding point
            sock.sendall(b"movel(posx(-476.7, 360.5, 112.2, 178.0, 93.1, -178.9), v=100, a=100)")
            time.sleep(7)

            # Above feeding point
            sock.sendall(b"movel(posx(-673.8, 355.7, 203.7, 178.0, 93.1, -178.9), v=70, a=100)")
            time.sleep(5)

            # Feeding point
            sock.sendall(b"movel(posx(-673.8, 355.7, 129.4, 178.0, 93.1, -178.9), v=70, a=100)")
            time.sleep(7)

            sock.sendall(b"set_digital_output(1, ON)")
            time.sleep(1)

            # Next to feeding point
            sock.sendall(b"movel(posx(-476.7, 360.5, 112.2, 178.0, 93.1, -178.9), v=100, a=100)")
            time.sleep(7)
            print("put pipe back drilling pipe 1") 

            # Home position
            sock.sendall(b"movej(posj(-94.3, 28.6, -126.4, 180.4, 9.6, -180.9), v=80, a=100)")
            time.sleep(5)

            drilling_pipe = '1B'

            while True:
                ser.write((str(drilling_pipe) + '\n').encode('utf-8'))

                # Read and print responses until "Done" is received
                while True:
                    if ser.in_waiting > 0:
                        response = ser.readline().decode('utf-8').strip()
                        print(f"Received response: {response}")
                        if response == "pipe is picked":
                            break

                if response == "pipe is picked":
                    break

        finally:
            # Close the socket
            sock.close()
            print("bye")

    def change_circle_color(self, canvas, circle_id, new_color):
        # Function to change the color of a circle on the canvas
        canvas.itemconfig(circle_id, fill=new_color)

    def close_program(self):
        # Destroy the new window
        self.new_root.destroy()

        # Terminate the entire program
        sys.exit()

def main():
    root = tk.Tk()
    gui = RobotProgramGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
