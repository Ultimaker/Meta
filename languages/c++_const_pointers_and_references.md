# C/C++ const pointers and references
This document describes the principles behind using the const modifier for C and more so C++ when it comes to (class) functions, values to pass or return when using functions.

Setters
=======
Consider the following simplified piece of code:
~~~~~~~~~~~~~~~{.cpp}
class Printer
{
  public:
  void move_head_to_position(Point3D *position);
}
~~~~~~~~~~~~~~~
This looks fine at first, however, one has to consider what consequences this code might have.
What happens after the code has been executed? Would the data pointed to by position still be the same?
That might not be the case.

Consider the next example:
~~~~~~~~~~~~~~~{.cpp}
class Printer
{
  public:
  void move_head_to_position(const Point3D *position);
}
~~~~~~~~~~~~~~~
This now looks a lot better. We're done. Right?
Right now, it only defines that the data pointed to cannot be changed within the function. The pointer itself could be altered still.

So lets try another example:
~~~~~~~~~~~~~~~{.cpp}
class Printer
{
  public:
  void move_head_to_position(const Point3D * const position);
}
~~~~~~~~~~~~~~~
Now neither the value nor the pointer can be changed from within the function.

Using references instead, which are comparable to hidden pointers, the above becomes a bit simpler:
~~~~~~~~~~~~~~~{.cpp}
class Printer
{
  public:
  void move_head_to_position(const Point3D &position);
}
~~~~~~~~~~~~~~~
A reference is a hidden pointer and thus by definition cannot be changed by overriding its value with an address.
It would be possible tho to alter it to point it to different object by reference.

Getters
=======
Consider the following simplefied piece of code:
~~~~~~~~~~~~~~~{.cpp}
class Printer
{
  private:
  Point3D *head_position;
  
  public:
  Point3D *get_head_position()
  {
    return head_position;
  }
}
~~~~~~~~~~~~~~~
This is dangerous code. Return the pointer to the the value inside breaks one of the OOP rules of data hiding (abstraction, encapsulation).
It would allow changing the internals by means outside of the defined interface! Not only that, it would also invalidate the known state of the instance.

Let's improve:
~~~~~~~~~~~~~~~{.cpp}
class Printer
{
  private:
  Point3D *head_position;
  
  public:
  const Point3D *get_head_position()
  {
    return head_position;
  }
}
~~~~~~~~~~~~~~~
Much better. Returning a const pointer solves one issue that this pointer cannot be (directly) used to change the value inside the instance directly.

Contrary to a 'setter' function, a 'getter' normally does not change the state of the instance, so using another const after the function declaration makes this clear:
~~~~~~~~~~~~~~~{.cpp}
class Printer
{
  private:
  Point3D *head_position;
  
  public:
  const Point3D *get_head_position() const
  {
    return head_position;
  }
}
~~~~~~~~~~~~~~~
Most compilers are smart; if a const-function would return a non-const value, it would been marked as a compile time error.
There is a somewhat dealbreaker, which will be explained later. A smaller drawback can be solved in a different way. A const function specifies that the object (state) cannot be safed. This is however, not entirely true. Consider the following code:
~~~~~~~~~~~~~~~{.cpp}
class Printer
{
  private:
  Point3D *head_position;
  mutable int get_head_position_counter;
  
  public:
  const Point3D *get_head_position() const
  {
    ++get_head_position_counter;
    return head_position;
  }
}
~~~~~~~~~~~~~~~
Because of the mutable keyword, the const function is able to change the value of that variable. This example might be trivial, but consider some object where data might be loaded / unloaded (cached) on a requests notice.

Dealbreaker
-----
The dealbreaker that might cause issues is that using const other (older) libraries or code might cause problems.
A const function cannot call non-const functions, nor can const variables passed as non-const arguments.
A non-const can allways be used as a const, but not vice versa.
To this end, there is a special cast, the const_cast.
This cast will either remove a const modifier (if it was a const) or add it (when it was not const).

Advise regarding constness
=======
There are no real drawbacks for not using const all the time. The more code that is implemented using consts, the less dealbreakers will be left. Using the const keyword makes the code intentions very clear and allows a compiler to enforce additional rules which makes programming errors less prone to happen.

References
=======

Basically, references are equal to pointers, however with some very distintcive differences:
* References are treated like a normal object, hence the . scope instead of the ->
* Unlike pointers, references can only be initialized once
* References must also be initialized on declaration (very RAII)
* This also means a reference cannot be NULL
* And, on top of that, a resource cannot created like a pointer nor deleted like one.

These restrictions do give a number of advantages compare to pointers.
Just as pointer, references must hold objects that are still in scope. But contrary to pointers, this is a situation that most of the time the compiler can detect and warn about.

Also, using references make code more readable, especially when it comes to operator overloading.
Consider this piece of code:
~~~~~~~~~~~~~~~{.cpp}
class Matrix
{
  public:
  Matrix::Matrix(const Matrix &matrix_to_clone);
  
  const &Matrix operator::operator*(const Matrix &multiplier);
}

Matrix m1;
Matrix m2;
Matrix m3(m1 * m2);
~~~~~~~~~~~~~~~
versus
~~~~~~~~~~~~~~~{.cpp}
class Matrix
{
  public:
  Matrix::Matrix(const Matrix *matrix_to_clone);
  
  const *Matrix operator::operator*(const Matrix *multiplier);
}

Matrix m1;
Matrix m2;
Matrix m3(m1->operator*(&m2));
~~~~~~~~~~~~~~~
Which one is more natural to read and understand?

Studies have shown that a very large percentage of bugs in C++ are caused by memory leaks. Using references whenever possible will reduce those kinds of bugs.

Nonetheless, there are a number of reasons to keep using pointers:
* old libraries that expect pointers using NULL values
* pointer arithmetic for low level accessing data

Advise regarding references
=======
It's a good idea to use references where and whenever possible and only to use pointers when it's absolutely necessary.
