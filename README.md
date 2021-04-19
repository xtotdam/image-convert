# image-convert

Converts image files into sequence of escape codes, ready to be inserted into a C program.
Was created with easter eggs in mind.
You can also add joke comments inside the code - see the code of the script.

* Be aware that `#define` directives are global for a [single compilation unit](https://en.wikipedia.org/wiki/Single_Compilation_Unit).


```sh
usage: image_convert.py [-h] [-r ROUNDS] [-w LINEWRAP] [-f FUNCTION] [-o OUTFILE] [-s] image

Convert image to pixelated C code

positional arguments:
  image

optional arguments:
  -h, --help            show this help message and exit
  -r ROUNDS, --rounds ROUNDS
                        Number of compression rounds
  -w LINEWRAP, --linewrap LINEWRAP
                        Final text width
  -f FUNCTION, --function FUNCTION
                        Name of function
  -o OUTFILE, --outfile OUTFILE
                        Name of output file
  -s, --shuffle         Shuffle letters or not
```

## Example C code

```c
#include <stdio.h>

#define A "[48;5;"
#define B "m  [0m"
#define C "  "
#define D "\n"
#define E "102"
#define F "231"
#define G "202"
#define H "46"
#define I "16"
#define J "210"
#define K "59"
#define L C C C C
#define M B A F B
#define N M A F
#define O B A
#define P C C C
#define Q G O G
#define R N M A
#define S L C L
#define T D L A E
#define U T N O E
#define V C A Q B
#define W D P A
#define X M A
#define Y A G B
#define Z I M

void main(void) { printf(
C S C S P C W E B P A E B S C L C C W E O E X E O E B S P V C W F R F B S C C A
Q O Q O G B W F O H X H M S V L W F X J R F N B L C C Y L C D L A F R I O I O I
N B L V L D L A F N O G N O G O I O Z L C Y L D L A F N O G N O Q X Z L A Q B P
T R F O Q N O G O Z L Y P U R F O Q O Z L Y P U R G R Z P Y P U N O Q O E O E X // <--
Z C V P U R F X E X Z V L U R F X E X Q O Q B L C U R F X E N B L P C W K O K N // magic
O E R F O I N B S D L C C A K O K R Z S C C D L C C A F X K O K O Z S P D
);}
```

## How it looks like

![cat8x](https://user-images.githubusercontent.com/5108025/115274056-f1b7bd80-a148-11eb-8e27-c285ace6bfc0.png)
(8x)   :arrow_right:
![Screenshot_20210419_151931](https://user-images.githubusercontent.com/5108025/115235504-f23d5d80-a122-11eb-9f4b-7ab0655642cd.png)
