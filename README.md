# LSystem Generator

This project is a compiler from _LSystem Definition Language_ (LSDL) and 3D models.

**LSDL** is a language that we define for the compilation based on examples from the book _"The Algorithmic Beauty of Plants"_ written by Przemyslaw Prusinkiewicz and Aristid Lindenmayer in 1996.

## LSystem Definition Language

The **LSDL** is a language that defines a set of rules needed to generate a L-System fractal 3D model.

A simple LSDL program and its output equivalent string.
```
#iterate 3
begin: F-F
rule: F ::= F+F
```
```
F+F+F+F+F+F+F+F-F+F+F+F+F+F+F+F
```
### Syntax
* **Numbers:** `<NUM>`

  LSDL accepts Integer and floating point values.

  >**Examples:**
  ```
  2 345 2.453 0.90 .89
  ```
* **Symbols:** `<SYM>`

  Symbols are LSDL variables. All symbols must start with a character and can only contain lower case characters and numbers.

  >**Examples:**
  ```
  a l w width h1s
  ```
* **Numeric expression:** `<NUMEXPR>`

  Numeric operations between numbers and symbols.

  Supports addition, subtraction, multiplication, division and power.

  >**Examples:**
  ```
  34 l s+w 2-3 2*s 4.0/2 2^3 -k
  ```
* **Rule names:** `<FUN>`

  Rules are LSDL functions. All rule names must start with a major case character and can be followed only by a combination of lower case characters and numbers.

  The only exceptions are the **special rules**.

  >**Examples:**
  ```
  F Leaf Trunk1
  ```
* **Special Rules:** `<FUN> (<ARG>)`

  These rules have a special meaning for the interpretation of the resulting model.

  The following rules can receive one or two arguments.
  * `F` : Move forward and draw a line.
  * `f` : Move forward without drawing.
  * `G` : Move forward and draw a line. Do not record a vertex in the current polygon.
  * `+` : Turn left.
  * `-` : Turn right.
  * `^` : Pitch up.
  * `&` : Pitch down.
  * `\` : Roll left.
  * `/` : Roll right.
  * `!` : Decrement the diameter of segments.
  * `%` : Cut out the remainder of the branch.

  The following rules do not support arguments.
  * `|` : Turn around.
  * `$` : Rotate turtle to vertical.
  * `[` : Start a branch.
  * `]` : Complete a branch.
  * `{` : Start a polygon.
  * `.` : Record a vertex in the current polygon.
  * `}` : Complete a polygon.
  * `~` : Incorporate a predefined surface.
  * `'` : Increment the current color index.
* **Application of rule:** `<FUN> (<NUMEXPR>,...)`

  Makes a call to the corresponding rule.

  The arguments can be symbols, numbers or numeric expressions.

  >**Examples:**
  ```
  F F(l) B(l,w) A(0.876) B(5*l,0.2)
  ```
* **Initiator clause:** `begin: <APP> ...`

  A series of applications that define the initial state of the system.

  The argument must be a series of one or more application of Rules.
  >**Examples:**
  ```
  begin: F
  begin: FFF
  begin: F G
  begin: Leaf
  ```
* **Rule definition:** `#rule: <FUN> (<SYM>,...) ::= <APP> ...`

  Production rules define the way variables can be replaced with combinations of constants and other rules.

  A Rule consists of a predecessor and a successor. A predecessor defines the name and number of arguments of the rule and the successor is a series of applications. The successor cannot be empty.

  Rules can have any number of arguments. The arguments must be symbols.

  >**Examples:**
  ```
  rule: F ::= F-f
  rule: A(l) ::= FA(l-1)
  rule: B(l,w) ::= A(l)B(w*l,0.2)
  rule: C(wa2) ::= C(0.2*wa2)
  ```

  **Special rules** can be redefined, but the number of arguments must be maintained.
* **Number of iterations:** `#iterate <INT>`

  Sets the number of iterations needed to generate the model.

  If no `#iterate` is written, the program iterates 0 times.

  The argument must be a positive integer.

  >**Example:**
  ```
  #iterate 3
  ```
* **Symbol definition:** `#define <SYM> <NUM>`

  A symbol definition lets you set a value to a symbol. This symbol can then be used in the application of rules as arguments.

  >**Example:**
  ```
  #define r 2
  #define r0 -3.87
  #define width 0.5
  ```
* **Set the rotation angle:** `#delta <NUMEXPR>`

  Sets the default angle (in degrees) for the argument-less rotation rules like: `+`, `-`, `/`, `\`, `^` and `&`.

  >**Example:**
  ```
  #delta 180
  #delta 33.33
  #delta -45*s
  ```
* **Set a tropism:** `#tropism <NUMEXPR> <NUMEXPR> <NUMEXPR>`

  The branches of trees are bent by wind, gravity and phototropism. The direction of these changes can be represented by a 3 component vector named Tropism.

  The Tropism vector is not normalized before applying.

  >**Example:**
  ```
  #tropism 0 0 -1 // A tropism down, maybe by gravity
  #tropism 2 4 1
  #tropism -0.1 1.3 -4
  ```
* **Asign value to a symbol:** `<SYM> = <NUMEXPR>`

  Set a value to a symbol. The value can be computed as a numeric expression.
  This symbol can then be used in the application of rules as arguments.

  >**Example:**
  ```
  r = 2
  l = 2*r
  k = 2+2*x
  ```

## To Do:
1. Incorporate Turtle 3D and export first **OpenSCAD** models.
2. Modify RULE to handle conditions.
3. Modify the environment lookup to handle conditions.
4. Modify RULE to handle multiple probabilities.
5. Modify the environment lookup to handle multiple probabilities.
6. Add `#ignore` keyword.
7. Add `#constant` keyword.
8. Generate **Constructive Solid Geometry** directly.
9. Export models to a common used file format.
10. Fix NUMVAR regex so it throws a Syntax Error for numbers ending in -.
11. Fix argument regex to support only lower case letters followed by numbers.
12. Cleanup regex definitions.
15. Check syntax definitions are met.
