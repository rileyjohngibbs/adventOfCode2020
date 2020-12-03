In `solve3.py`, the `reduce` function is rewritten in a `lambda` as:

```python
lambda f, i, b: (lambda r, a: r(r, *a))(lambda r, f, i, b: (r(r, f, i[1:], f(b, i[0])) if i else b), (f, i, b))
```

More readably, if marginally:

```python
lambda f, i, b: \
  (lambda r, a: r(r, *a))(
    lambda r, f, i, b: (
      r(r, f, i[1:], f(b, i[0]))
      if i
      else b
    ),
    (f, i, b)
  )
```

This version of `reduce` only works with indexable iterables, and won't work with generators such as `map` and `filter` objects, which must be made into `list` objects before being supplied to the `lambda`, as is done in `solve3.py`.
