#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 07:53:07 2024

@author: Halogene

Description: WIP Takes a sound from the microphone (mac) and plots the wave on a graph. Then 
             it decomposes the wave with fourier analysis and prints the constituent waves
             in a new graph. Ultimately I want to play chords on a piano and then be able
             to show which notes are being played. I have coded it to recognize (based on my phone piano app so innacurate lmao) C7 D7 E7 and D8. 
             Because of backround sounds (my guess I am probably wrong) with background noise things can get a bit messy. With my app it seems at the start
             there is a bunch but if u hold it down the code is able to find it. 
             I'll say what frequency my piano app plays the notes at for funz:

             C7 = 2110.253 Hz
             D7 = 2368.652 Hz
             E7 = 2670.117 HZ
             C8 = 4220.5078 Hz
             
updates: created plot
"""
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import threading # this will allow me to make an input at any given time in the code (remember you still have to enter the s for the input)
                 # Threading typically allows you to compute multiple tasks simultaneously, here im handeling the user_input(Designed to terminate the running while loop) and the peak frequency

Information = input("Do you want information of bit arrays, buffer-like-objects, numpy stuff? (y/n)")



if Information == "y": 
    print("Bit Arrays: https://en.wikipedia.org/wiki/Bit_array")
    print("Buffers: https://docs.python.org/3/c-api/buffer.html")
    print("np.frombuffer: https://numpy.org/doc/stable/reference/generated/numpy.frombuffer.html")
    print("Example of what I want to do ultimately: https://www.physics.wisc.edu/ingersollmuseum/exhibits/waves/fourier/sound-analyzer/")
    print("ARRAYS: https://www.simplilearn.com/tutorials/python-tutorial/python-arrays")
    print("Fast Fourier Transforms")
    print("Channel Explination: https://stackoverflow.com/questions/58613948/what-does-the-number-of-channels-mean-in-pyaudio")

    


CHUNK = 1024  # the number of frames in the buffer

FORMAT = pyaudio.paInt16 # paInt16 is a 16-bit binary string -> 15 bits for the number 1 for the sign (this is a common method of storage for audio)

CHANNELS = 1 # each frame will have 1 channel

RATE = 44100 # number of samples collected per second

p = pyaudio.PyAudio() # initializes PyAudio / acquires system resources for PortAudio 
 
# p.open() creates audio object "p" which initializes an audio stream for input  
stream = p.open(
    format = FORMAT, 
    channels = CHANNELS,
    rate = RATE,
    input = True,
    frames_per_buffer = CHUNK)


plt.ion() # Allows me to update the graph live ---> move back up if it changes things


# Initializing variables: 
data = stream.read(CHUNK, exception_on_overflow=False) # reads each chunk and stores it in an (binary) array called "data"
audio_data = np.frombuffer(data, dtype=np.int16) # [np.frombuffer()] Interprets a buffer as a 1 dimensional array) creates a 1-D numpy array from the raw binary info stored in "data". it interprets it as a 16-bit signed integer. Remember we are using paINT16
time = np.arange(len(audio_data)) / RATE
 

 # In the future I will use this code to terminate things in a similar fashion
def input_thread(): # you put the code you want to thread inside here
    global running
    while True:
        user_input = input()
        if user_input == "s":
            running = False
            break # this stops the thread 

input_thread = threading.Thread(target=input_thread) # creates a thread object "threading.Thread". Further the target is input_thread() so it will execute the code in that function
input_thread.daemon = True # setting a thread as daemon will mean it automatically terminates when the over-arching progam ends
input_thread.start() # initializes the thread


# Setting up my graphs to be updated by an update_plots() function
fig, (ax1, ax2, ax3) = plt.subplots(3,1)  # I'll j
x_freq = np.abs(np.fft.fftfreq(CHUNK, 1 / RATE)) # the "np.fft.fftfreq()" is a discrete fourier transformation that computes the one-dimensional FFT of a signal. Input is time domain signal output is frequency domain signal --> The input parameters to np.fft.fftfreq are the length of the input signal and the sampling interval (inverse of the sampling rate). x_freq here sets up the x axis frequency and doesn't need to be updated
fig.subplots_adjust(hspace=1) # separates the subplots

line, = ax1.plot(x_freq[:CHUNK // 2], np.zeros(CHUNK // 2), lw = 2, color = 'blue') 
# "line,"" is a variable that stores the reference information to plot() which can be updated later
# "x_freq[:CHUNK // 2]" Slices the x_freq array starting at 0 
# "np.zeros(CHUNK // 2)" creates an array the size of CHUNK // 2 of zeros. this will be 
ax1.set_title("Frequency and magnitude")
ax1.set_ylim(0, 7)
ax1.set_xlim(0, 6000) # here we are just showing that only frequency up to the Nyquist freq are displayed --> The Nyquist theorem states that the highest frequency that can be represented accurately in a digital signal is half of the sampling rate.
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Magnitude (log10)')


peak_line, = ax2.plot([], [], lw = 3, color = 'red') # "," designated line status
ax2.set_title("Peak Frequency")
ax2.set_ylim(0, 5000)
ax2.set_xlim(0, 1)
ax2.set_xlabel('Time in seconds')
ax2.set_ylabel('Peak Frequency (Hz)')




wave_line, = ax3.plot([], [], lw = 2, color = 'green') # "," designated line status
daeta = stream.read(CHUNK, exception_on_overflow=False)
ax3.set_title("Waveform")
ax3.set_ylim(-7000, 7000)
ax3.set_xlim(0, time[-1])
ax3.set_xlabel('Time in seconds')
ax3.set_ylabel("Amplitude")

def find_pitch(): 
    data = stream.read(CHUNK, exception_on_overflow=False)
    audio_data = np.frombuffer(data, dtype=np.int16)
    y_freq = np.abs(np.fft.fft(audio_data))
    freqs = np.fft.fftfreq(len(audio_data), d=1/RATE)
    peak_freq_index = np.argmax(y_freq)
    peak_freq = np.abs(freqs[peak_freq_index])

    """--- CLEARING THINGS UP ABOUT THE FREQS 
    
     y_freqs is  a 1-dimensional array that holds the magnitudes of the fast foureir transformation coefficients corresponding 
    to each frequency bin which were defined by x_freq. Each element in y_freqs corresponds to the magnitude of the FFT result at 
    the corresponding frequency in x_freq. This is why I don't update x_freq
    
    """
   
    # I want to replace this with an algorithm
    if 4000 < peak_freq < 4300:
        print("C8")
        return "C8"
    if 2090 < peak_freq <= 2111: 
        print("C7")
        return "C7"
    if 2366 < peak_freq <= 2369: 
        print("D7")
        return "D7"
    if 2660 < peak_freq <= 2671: 
        print("E7")
        return "E7"

def update_plots():
    global running
    data = stream.read(CHUNK, exception_on_overflow=False)
    audio_data = np.frombuffer(data, dtype=np.int16)
    y_freq = np.abs(np.fft.fft(audio_data))
    freqs = np.fft.fftfreq(len(audio_data), d=1/RATE) # "d=1/RATE"  specifies the spacing between frequency bins ->  a frequency bin is a frequency range or interval in the frequency domain
    line.set_ydata(np.log10(y_freq[:CHUNK // 2]))
   
    peak_freq_index = np.argmax(y_freq)
    peak_freq = np.abs(freqs[peak_freq_index])
    
    print("Peak Frequency:", peak_freq, "Hz and pitch:", find_pitch())
    peak_line.set_xdata(np.arange(len(audio_data)))
    peak_line.set_ydata([np.repeat(peak_freq, len(audio_data))])
   

    
    wave_line.set_xdata(time)
    wave_line.set_ydata(audio_data)
   
    fig.canvas.draw()
    fig.canvas.flush_events()

  

running = True

while running:
         update_plots()     
         
         
# Essentially used threading to do this by stopping the program with an input of "s"

"""
stream.stop_stream()
stream.close()
p.terminate()
"""

