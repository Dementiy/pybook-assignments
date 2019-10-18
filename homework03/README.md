Запустить тесты можно так:

```
python -m unittest discover
test_can_create_a_random_grid (test_life.TestGameOfLife) ... ok
test_can_create_an_empty_grid (test_life.TestGameOfLife) ... ok
test_can_update (test_life.TestGameOfLife) ... ok
test_get_neighbours (test_life.TestGameOfLife) ... ok
test_get_neighbours_for_bottom_side (test_life.TestGameOfLife) ... ok
test_get_neighbours_for_left_side (test_life.TestGameOfLife) ... ok
test_get_neighbours_for_lower_left_corner (test_life.TestGameOfLife) ... ok
test_get_neighbours_for_lower_right_corner (test_life.TestGameOfLife) ... ok
test_get_neighbours_for_right_side (test_life.TestGameOfLife) ... ok
test_get_neighbours_for_upper_left_corner (test_life.TestGameOfLife) ... ok
test_get_neighbours_for_upper_right_corner (test_life.TestGameOfLife) ... ok
test_get_neighbours_for_upper_side (test_life.TestGameOfLife) ... ok
test_is_changing (test_life.TestGameOfLife) ... ok
test_is_max_generations_exceed (test_life.TestGameOfLife) ... ok
test_is_not_changing (test_life.TestGameOfLife) ... ok
test_prev_generation_is_correct (test_life.TestGameOfLife) ... ok

----------------------------------------------------------------------
Ran 16 tests in 0.026s

OK

test_can_create_a_random_grid (test_life_proto.TestGameOfLife) ... ok
test_can_create_an_empty_grid (test_life_proto.TestGameOfLife) ... ok
test_can_update (test_life_proto.TestGameOfLife) ... ok
test_get_neighbours (test_life_proto.TestGameOfLife) ... ok
test_get_neighbours_for_bottom_side (test_life_proto.TestGameOfLife) ... ok
test_get_neighbours_for_left_side (test_life_proto.TestGameOfLife) ... ok
test_get_neighbours_for_lower_left_corner (test_life_proto.TestGameOfLife) ... ok
test_get_neighbours_for_lower_right_corner (test_life_proto.TestGameOfLife) ... ok
test_get_neighbours_for_right_side (test_life_proto.TestGameOfLife) ... ok
test_get_neighbours_for_upper_left_corner (test_life_proto.TestGameOfLife) ... ok
test_get_neighbours_for_upper_right_corner (test_life_proto.TestGameOfLife) ... ok
test_get_neighbours_for_upper_side (test_life_proto.TestGameOfLife) ... ok

----------------------------------------------------------------------
Ran 12 tests in 1.015s

OK
............................
----------------------------------------------------------------------
Ran 28 tests in 0.047s

OK
```

