import java.util.Random;
import static java.lang.Math.*;

public class Main {

    public static float calculateW(int sValue, float xValue) {
        try {
            if (sValue == 11) {
                if (xValue <= 0) return 0; // защита от log(0)
                double temp = cos(cbrt(log(abs(xValue))));
                return (float) asin(temp);
            }
            else if (sValue == 5 || sValue == 7 || sValue == 9 ||
                    sValue == 13 || sValue == 15 || sValue == 17) {
                double cosVal = cos(xValue);
                double denominator = cosVal * cosVal / 3;
                if (denominator <= 0) return 0;
                return (float) log(denominator);
            }
            else {
                double sinVal = sin(xValue);
                if (sinVal == 0) return 0;
                double base = 2 * log(sinVal * sinVal);
                double exponent = cos(pow(xValue, xValue + 1.0/xValue));
                return (float) cos(pow(base, exponent));
            }
        } catch (Exception e) {
            return 0;
        }
    }

    public static void printMatrix(float[][] matrix) {
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                System.out.printf("%8.2f ", matrix[i][j]);
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {
        int[] s = new int[12];
        for (int i = 25, index = 0; i >= 3; i -= 2, index++) {
            s[index] = i;
        }

        float[] x = new float[16];
        Random rand = new Random();
        for (int i = 0; i < 16; i++) {
            x[i] = rand.nextFloat() * 14 - 3;
        }

        float[][] w = new float[12][16];
        for (int i = 0; i < 12; i++) {
            for (int j = 0; j < 16; j++) {
                w[i][j] = calculateW(s[i], x[j]);
            }
        }

        System.out.println("Результат:");
        printMatrix(w);
    }
}