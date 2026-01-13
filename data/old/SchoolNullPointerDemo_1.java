// Source - https://codereview.stackexchange.com/q
// Posted by javid piprani, modified by community. See post 'Timeline' for change history
// Retrieved 2025-11-28, License - CC BY-SA 4.0

public class SchoolNullPointerDemo_1 {

    // Simple Student class inside for demo
    static class Student {
        private int id;
        public int getId() { return id; }
        public void setId(int id) { this.id = id; }
    }

    Student student;

    public SchoolNullPointerDemo_1() {
        try {
            // old version: student is uninitialized → triggers NullPointerException
            student.getId();
        } catch(Exception e) {
            System.out.println("Null pointer exception");
        }
    }

    public static void main(String[] args) {
        new SchoolNullPointerDemo_1();
    }
}
