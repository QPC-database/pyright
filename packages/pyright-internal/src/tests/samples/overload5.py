# This sample tests the type checker's detection of overlapping
# overload declarations.

from typing import (
    Any,
    Generic,
    Literal,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)


@overload
def func1(a: float, b: Optional[float], c: Optional[bool] = None) -> int:
    return 1


# This should generate an error because the overload is obscured.
@overload
def func1(a: int, b: int) -> int:
    return 1


@overload
def func1(a: int, b: int, *, named: int = 3) -> int:
    return 1


# This should generate an error because the overload is obscured.
@overload
def func1(a: int, b: int, *, named: int) -> int:
    return 1


@overload
def func1(a: complex, b: int) -> int:
    return 1


@overload
def func2(a: int, b: Any) -> int:
    return 1


# This should generate an error because the overload is obscured.
@overload
def func2(a: int, b: int) -> int:
    return 1


@overload
def func3(a: int, b: int) -> int:
    return 1


@overload
def func3(a: int, b: int, **c: Any) -> int:
    return 1


@overload
def func3(a: int, b: Any) -> int:
    return 1


@overload
def func4(a: int, *, c: int, b: int) -> int:
    return 1


# This should generate an error because the overload is obscured.
@overload
def func4(a: int, *, b: int, c: int) -> int:
    return 1


# This should generate an error because the overload is overlapping
# in an unsafe way (i.e. returns an incompatible type).
@overload
def func5(a: int, b: int) -> int:
    return 3


@overload
def func5(a: float, b: float = 3.4, *c: int, d: float = 4.5) -> str:
    return ""


_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")


class GenericClass(Generic[_T1, _T2]):
    @overload
    def method1(a: _T1, b: Tuple[_T2, ...]) -> int:
        return 1

    @overload
    def method1(a: _T1, b: Tuple[Any, ...]) -> int:
        return 1

    @overload
    def method2(a: _T2, b: int) -> int:
        return 1

    @overload
    def method2(a: _T1, b: _T2) -> int:
        return 1


class Parent:
    ...


class Child(Parent):
    ...


# Test 1: Literal subtype
@overload
def func10(x: Literal[3]) -> int:
    ...


@overload
def func10(x: int) -> str:
    ...


# Test 2: Subclass subtype
@overload
def func11(x: Child) -> str:
    ...


@overload
def func11(x: Parent) -> int:
    ...


# Test 3: Implicit subtype
@overload
def func12(x: int) -> str:
    ...  # Mypy does not report error here


@overload
def func12(x: float) -> int:
    ...


# Test 4: Union subtype
@overload
def func13(x: int) -> str:
    ...


@overload
def func13(x: Union[int, str]) -> int:
    ...


# Test 5: non-matching keyword argument (shouldn't generate error)
@overload
def func14(x: int, *, cls: str, **kwargs: Any) -> int:
    ...


@overload
def func14(x: int, **kwargs: Any) -> str:
    ...


# Test 6: non-matching keyword argument (shouldn't generate error)
@overload
def func15(cls: str, **kwargs: Any) -> int:
    ...


@overload
def func15(**kwargs: Any) -> str:
    ...
