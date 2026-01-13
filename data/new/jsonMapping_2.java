public class jsonMapping_2 {

    public int orangeCount = 3;
    private String orange;

    public static void main(String[] args) {
        jsonMapping_2 obj = new jsonMapping_2();
        if (obj.orangeCount == 3) {System.out.println("I have 3 oranges!");}
        obj.setOrange("hello");
    }
    
    private void setOrange(String orange) { this.orange = orange; }

    public String getOrange() { return this.orange; }
}