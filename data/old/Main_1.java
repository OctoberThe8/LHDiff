import java.util.ArrayList;

public class Main_1 { // method trimToSoze() capacity will match the current size 
    public static void main(String[] args) {
        // Create an ArrayList with an initial capacity of 20
        ArrayList<String> toDo = new ArrayList<>(20);
        
        // Check initial size and capacity
        System.out.println("Initial Size: " + toDo.size()); // Size = 0
        System.out.println("Initial Capacity: 20 (default capacity won't change until trimming)");

        // Add one element
        toDo.add("Learn Java");
        System.out.println("Size after adding one element: " + toDo.size()); // Size = 1

        // Remove the element
        toDo.remove("Learn Java");
        System.out.println("Size after removing the element: " + toDo.size()); // Size = 0

        // Trim the ArrayList to match the current size
        toDo.trimToSize();
        System.out.println("After trimToSize, the capacity matches the size (both = 0)");

        // Demonstrate resizing after trimming
        toDo.add("Practice Algorithms");
        System.out.println("Size after adding one element post-trim: " + toDo.size()); // Size = 1
        System.out.println("Capacity is now increased dynamically, but we don't directly access it");
    }
}

