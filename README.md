**Overview**

The Karplus-Strong algorithm can simulate the sound of a plucked string by using a ring buffer of displacement values to simulate a string tied down at both ends, similar to a guitar string.
A ring buffer (also known as a circular buffer) is a fixed-length buffer (just an array of values) that wraps around itself. 
In other words, when you reach the end of the buffer, the next element you access will be the first element in the buffer. 

The length (N) of the ring buffer is related to the fundamental frequency of vibration according to the equation N = S/f, where S is the sampling rate and f is the frequency.
At the start of the simulation, the buffer is filled with random values in the range [−0.5, 0.5], which you might think of as representing the random displacement of a plucked string as it vibrates.
In addition to the ring buffer, you use a samples buffer to store the intensity of the sound at any particular time. 
The length of this buffer and the sampling rate determine the length of the sound clip.

**Usage**

`git clone https://github.com/the-inevitable/karplus-strong-algorithm.git`

`cd karplus-strong-algorithm`

`python karplus_strong.py [-h] [--replay] [--play]`

Passing `--replay` will make the script recreate and play all the notes even if they are already in `./media/`

Passing `--play` will make the script play random notes with random delay.

Sound on!

The script is written Python3.8.