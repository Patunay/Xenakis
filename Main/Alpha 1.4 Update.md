
# Xenakis <font size="3" >*by Carlos Mauro* </font>

## *A graphic music notation handler*

*Feb, 2022*

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

## On Concepts Ipad app:

### Things to work on:

- Create guides for diferrent intervals( 8ves done)
- Create assets for different intervals
- Togable (See only what you want to see)

### Eventually:
- Figure out a format or create one yourself that allows you to embed all individual layers (voices) of a file in a single one.
- add support for note velocity control on empty space abvove or below maybe even use colors since its fairly easy to completely hide them.
- Try creating files in illustrator.
- Create texture generators using np.arrays!!
- Experiment with harmony.
- Create AI(??) to detect time information in score and expand lenght dynamically.