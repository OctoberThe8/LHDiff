import java.util.ArrayList;


public class Main_2 {  // trimToSize() adjusts capacity to match size

    public static void main(String[] args) {
        
        // Initialize an ArrayList with capacity 20
        ArrayList<String> tasks = new ArrayList<>(20);
        

        // Display initial size and capacity
        System.out.println("Starting Size: " + tasks.size()); // Size = 0
        System.out.println("Starting Capacity: 20 (unchanged until trim)");
        
        // Add a task
        tasks.add("Learn Java");
        System.out.println("Size after adding task: " + tasks.size()); // Size = 1


        // Remove the task
        tasks.remove("Learn Java");
        System.out.println("Size after removing task: " + tasks.size()); // Size = 0
        
        
        // Trim the capacity to match current size
        tasks.trimToSize();
        System.out.println("Trimmed: capacity now equals size (0)");
        

        // Add another task after trimming
        tasks.add("Practice Algorithms");  // adding another task
        System.out.println("Size after adding new task post-trim: " + tasks.size()); // Size = 1

        System.out.println("Capacity adjusts dynamically now, not directly visible");

    }
    
}
