package evogen;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class Vector2dTest {
    @Test
    public void add() {
        Vector2d testVector1 = new Vector2d(3, 7);
        Vector2d testVector2 = new Vector2d(-5, 2);
        Vector2d testVector3 = new Vector2d(1, 23);

        assertEquals(testVector1.add(testVector2), new Vector2d(-2, 9));
        assertEquals(testVector3.add(testVector1), new Vector2d(4, 30));
    }

    @Test
    public void isInsideTest() {
        Vector2d testVector1 = new Vector2d(5, 8);
        Vector2d testVector2 = new Vector2d(1,1);

        assertTrue(testVector1.isInside(4,7,6,9));
        assertFalse(testVector1.isInside(3,5,5,9));
        assertTrue(testVector2.isInside( 0, 3, 1, 4));
    }
}
