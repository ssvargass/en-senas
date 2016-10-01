import Tkinter as tk
from PIL import ImageTk, Image
import io
import socket
import struct
import time
import picamera
import ast
import os.path
import sys
from six.moves import urllib

root = tk.Tk()

panel = tk.Label(root)
panel.pack(side = "bottom", fill = "both", expand = "yes")
titleWord = tk.StringVar()
titlePanel = tk.Label(root, textvariable=titleWord, font=("Helvetica", 24))
titleWord.set("Wellcome!")
titlePanel.pack()


def print_cam_preview():
    photo = tk.PhotoImage(file = 'imagen.gif')
    panel.configure(image = photo)
    panel.image = photo

    
def captura():
    try:
        with picamera.PiCamera() as camera:
            client_socket = socket.socket()
            client_socket.connect(('192.168.0.12', 8080))
            connection = client_socket.makefile('wb')


            camera.resolution = (640, 480)
            # Start a preview and let the camera warm up for 2 seconds
            camera.start_preview()
            time.sleep(1)

            # Note the start time and construct a stream to hold image data
            # temporarily (we could write it directly to connection but in this
            # case we want to find out the size of each capture first to keep
            # our protocol simple)
            start = time.time()
            stream = io.BytesIO()
            camera.capture(stream, 'jpeg')
            camera.capture('imagen.gif')
            print_cam_preview()
            #for foo in camera.capture_continuous(stream, 'jpeg'):
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
            connection.write(struct.pack('<L', stream.tell()))

            connection.flush()
                # Rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(stream.read())
                # If we've been capturing for more than 30 seconds, quit
            #    if time.time() - start > 30:
            #        break
                # Reset the stream for the next capture
            #    stream.seek(0)
            stream.truncate()
            # Write a length of zero to the stream to signal we're done
            connection.write(struct.pack('<L', 0))
            
    finally:
        data = client_socket.recv(1024)
        dictionary = ast.literal_eval(data)
        if()
        title = dictionary['title']
        img_url = dictionary['image']

        titleWord.set(title)
        dest_directory = 'sign'
        sign_img = dest_directory + '/' + title.lower() + '.gif'
        if not os.path.exists(sign_img):
            def _progress(count, block_size, total_size):
                sys.stdout.write('\r>> Downloading %s %.1f%%' % (
                    filename, float(count * block_size) / float(total_size) * 100.0))
                sys.stdout.flush()
            
            filepath, _ = urllib.request.urlretrieve(img_url, sign_img, _progress)
                
        sign = Image.open(sign_img)
        print(sign)
        
        connection.close()
        client_socket.close()    


# root.title("APRENDE VIENDO")
# root.configure(background='black')
#
# w, h = root.winfo_screenwidth(), root.winfo_screenheight()
# root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (1000,600))

camara = tk.PhotoImage(file="Camara.gif")

 
boton = tk.Button(root,image=camara,command=captura).place(x=0,y=0)
# botonClose = Button(ventana,image=imagen2,command=ventana.destroy).place(x=850,y=50)


root.mainloop()
