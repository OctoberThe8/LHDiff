public class Date_2 {
    private int yr;
    private int mon;
    private int dayOfMonth;

    // Constructor
    public Date_2(int yr, int mon, int dayOfMonth) {
        this.yr = 
        yr;
        this.mon = validateMonth(mon);
        this.dayOfMonth = validateDay(dayOfMonth);
    }

    // Copy constructor
    public Date_2(Date_2 other) {
        this.yr = other.yr;
        this.mon = other.mon;
        this.dayOfMonth = other.dayOfMonth;
    }

    // Month validation
    private int validateMonth(int mon) {
        if (mon >= 1 && mon <= 12) {
            return mon;
        } else {
            throw new IllegalArgumentException("Month must be between 1 and 12");
        }
    }

    // Day validation
    private int validateDay(int dayOfMonth) {
        if (dayOfMonth >= 1 && dayOfMonth <= 31) {
            return dayOfMonth;
        } else {
            throw new IllegalArgumentException("Day must be between 1 and 31");
        }
    }

    // String representation
    @Override
    public String toString() {
        return String.format("%d/%d/%d", yr, mon, dayOfMonth);
    }

    // Main method
    public static void main(String[] args) {
        Date_2 today = new Date_2(2025, 11, 30);
        System.out.println(today);

        Date_2 copy = new Date_2(today);
        System.out.println(copy);
    }
}
