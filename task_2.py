def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = left + (right - left) // 2
        mid_value = arr[mid]

        if mid_value < target:
            left = mid + 1
        else:
            upper_bound = mid_value
            right = mid - 1

    if upper_bound is None and left < len(arr):
        upper_bound = arr[left]
    elif upper_bound is None:
        upper_bound = None  # Target is greater than any element in the array

    return (iterations, upper_bound)

def main():
    arr = [0.5, 1.2, 2.8, 3.3, 4.7, 5.5, 6.1, 7.0]
    targets = [3.0, 4.7, 8.0, 0.1]

    print(f"Array: {arr}\n")
    for target in targets:
        result = binary_search(arr, target)
        print("Target:", target)
        print("Number of iterations:", result[0])
        print(f"Upper bound: {result[1]}\n")

if __name__ == "__main__":
    main()
