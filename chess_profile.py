import cProfile
from main import main

def my_func():
    main()

cProfile.run('my_func()', sort='cumulative')