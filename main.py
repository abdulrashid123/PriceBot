from BaseSite import Base
import sys

if __name__ == '__main__':
    cache = None
    script_name = sys.argv[0]
    print("Script name:", script_name)

    # Additional command-line arguments can be accessed using indices
    # sys.argv[1] corresponds to the first argument after the script name
    # sys.argv[2] corresponds to the second argument, and so on.
    if len(sys.argv) > 1:
        # Print all additional arguments
        print("Additional arguments:")
        for arg in sys.argv[1:]:
            if arg == "--cache":
                cache = arg
                print(cache)
    else:
        print("No additional arguments provided.")
    obj = Base()
    if cache:
        obj.run_bot(cache=True)
    else:
        obj.run_bot()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
