# Xenakis <font size="3" >_by Carlos Mauro_ </font>

## _A graphic music notation handler_


_October, 2022_

## Alpha 1.5 update:

### This update achieved:

- Simplification of code:
  - This version only contains the png to score generator module to simplify the development.
  - The other functionalities will be developed once the main one is ready.
- User Defined Pitch Mapping:
  - Now the algorithm will map pitches to a user defined range (in midicents).
- LARGE files now supported
  - If output is LARGE, it will be splited into batches of a maximun of 9999 events per batch
  - This allows MAX 8 to read and load the data without crashing.
- Preview Combined layers function fixed.
  - It now shows a preview in a separate window.
- Now each layer is stored independentely in a subarray.
  - This was done to organize large amounts of data more efficiently.
- Lenght Inquiry Function added.
  - Now the user can check the lenght of the output file without having to run the algorithm by pressing the boton "How Long?".
  - Outputs the duration in console.
- Xenakis now stores stores the data array as a .csv file in the Output folder.
  - Debugging purposes.
  - A header is included that contains the following information:
    - int(start_flag), int(total_voices), int(total_events), int(multiplier factor)
- Xenakis now automatically organizes the voice order from high to low (pitch-wise).
  - Xenakis calculates the average midicent value for every voice and reorders the data accordingly.
- Fixed bugs in .BachScroll syntax creation.
- Keyboard Binds added:
  - [space] Preview layer.
  - [a] Preview combined layers.

### In the future:

- Add scrolling bar single and combined layer preview.
- Direct output as MIDI will be availble in the upcoming months.

_Feb, 2022_

## Alpha 1.4 update:

### This update achieved:

- Overhaul of score generator function:

  - In **general:**
    - Now possible to **add and delete voices** on demand.
    - Huge Improvement of GUI.
    - Improvement on code of the containing class.
    - Enhanced comments.
  - In **Parameters Window:**
    - **Elimination** of **number of voices input.** (Became Redundant)
  - In **Path List:**
    - "Path move up" and "Path move down" fixed:
      - Keeps selection.
    - Added **Add Voice** method.
    - **Voice Preview-on demand** by presing **>space<**.
    - **Cycle Elements** using **>arrows<**
    - Elimination of **Update Filepath** button:
      - Now **Start** button updates variables with current state of window.
    - Added **Matrix-like Theme** to text output.
      - Just because I can.

### Coming up soon:

- In **general:**
  - **Split clases** into **different files** to make it more managable.
- **Score Generation:**
  - Create **summed voice preview** option in external window.
    - Add everything into an multidimensinal array where z depth = number of voices
    - Split into n 2 dimensional arrays
    - Add 0s and 1s
    - create (.png?) based on output sum.
  - Implement **picture height scaling.**
    - Make Xenakis algorithm recognize boundary lines and scale based on that.
- **Graphic Editor:**
  - Figure out:
    - **Infinite Canvas**
    - **Layers**
  - Improve Drawing modes
  - Save as local project
  - Export to .png
  - Direct generation of bach.roll.
  - Octave grids with Labels.

### Eventually:

- Overhaul colors on GUI.
- Realtime connection between graphical editor and Max Msp Software.

