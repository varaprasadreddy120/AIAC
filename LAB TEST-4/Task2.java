// Task2.java
// Program to sort an array in ascending order and display the result

import java.util.Arrays;

public class Task2 {
    public static void main(String[] args) {
        int[] arr = {45, 12, 78, 34, 23, 89, 5};

        // Sort the array
        Arrays.sort(arr);

        // Display the sorted array
        System.out.println("Sorted Array in Java:");
        for (int i = 0; i < arr.length; i++) {
            if (i > 0) System.out.print(" ");
            System.out.print(arr[i]);
        }
        System.out.println();
    }
}
