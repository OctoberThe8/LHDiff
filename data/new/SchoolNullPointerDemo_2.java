// Source - https://codereview.stackexchange.com/q
// Posted by javid piprani, modified by community. See post 'Timeline' for change history
// Retrieved 2025-11-29, License - CC BY-SA 4.0

public class SchoolNullPointerDemo_2 {

    // Simple Student class inside for demo
    static class Student {
        private int id;
        public int getId() { return id; }
        public void setId(int id) { this.id = id; }
    }

    Student student;

    public SchoolNullPointerDemo_2() {
        try {
            // new version: student initialized → no NullPointerException
            student = new Student();
            student.setId(12);
            int studentId = student.getId();
            System.out.println("Student ID: " + studentId);
        } catch(Exception e) {
            System.out.println("Null pointer exception");
        }
    }

    public static void main(String[] args) {
        new SchoolNullPointerDemo_2();
    }
}
