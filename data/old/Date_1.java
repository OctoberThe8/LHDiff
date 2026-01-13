public class Date_1 {
    private int year;
    private int month;
    private int day;

    public Date_1(int year, int month, int day) {
        this.year = year;
        this.month = checkMonth(month);
        this.day = checkDay(day);

    }
    public Date_1 (Date_1 d) {
        this.year = d.year;
        this.month = d.month;
        this.day = d.day;
    }

    private int checkMonth(int month) {
        if (month >= 1 && month <= 12) {
            return month;
        }
        else throw new IllegalArgumentException("invalid month"); //whatever inn message will be printed.



    }

    public String toString() {
        return String.format("%d/%d/%d", year,month,day);

    }

    private int checkDay(int day) {
        if (day >= 1 && day <= 31) {
            return day;
        }
        else throw new IllegalArgumentException("invalid day"); //whatever inn message will be printed.



    }



    public static void main(String[] args) {

    }
}
