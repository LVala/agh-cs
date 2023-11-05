package agh.ics.oop;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class Vector2dTest {

    @Test
    public void equalsTest() {
        Vector2d test_vector_1 = new Vector2d(1, 1);
        Vector2d test_vector_2 = new Vector2d(1, 1);
        Vector2d test_vector_3 = new Vector2d(1, 4);
        int[] test_not_vector_object = new int[10];

        assertTrue(test_vector_1.equals(test_vector_2));
        assertFalse(test_vector_1.equals(test_vector_3));
        assertFalse(test_vector_1.equals(test_not_vector_object));
    }

    @Test
    public void toStringTest() {
        Vector2d test_vector = new Vector2d(3, 67);
        assertEquals(test_vector.toString(), "(3, 67)");
    }

    @Test
    public void precedesTest() {
        Vector2d test_vector_1 = new Vector2d(1, 1);
        Vector2d test_vector_2 = new Vector2d(0, 1);
        Vector2d test_vector_3 = new Vector2d(1, 4);
        assertFalse(test_vector_3.precedes(test_vector_1));
        assertTrue(test_vector_2.precedes(test_vector_1));
    }

    @Test
    public void followsTest() {
        Vector2d test_vector_1 = new Vector2d(1, 1);
        Vector2d test_vector_2 = new Vector2d(0, 1);
        Vector2d test_vector_3 = new Vector2d(1, 4);
        assertTrue(test_vector_3.follows(test_vector_1));
        assertFalse(test_vector_2.follows(test_vector_1));
    }

    @Test
    public void upperRightTest() {
        Vector2d test_vector_1 = new Vector2d(3, 7);
        Vector2d test_vector_2 = new Vector2d(-5, 2);
        Vector2d test_vector_3 = new Vector2d(5, 23);
        assertEquals(test_vector_1.upperRight(test_vector_2), new Vector2d(3, 7));
        assertEquals(test_vector_3.upperRight(test_vector_2), new Vector2d(5, 23));
    }

    @Test
    public void lowerLeftTest() {
        Vector2d test_vector_1 = new Vector2d(3, 7);
        Vector2d test_vector_2 = new Vector2d(-5, 2);
        Vector2d test_vector_3 = new Vector2d(1, 23);
        assertEquals(test_vector_1.lowerLeft(test_vector_2), new Vector2d(-5, 2));
        assertEquals(test_vector_3.lowerLeft(test_vector_1), new Vector2d(1, 7));
    }

    @Test
    public void add() {
        Vector2d test_vector_1 = new Vector2d(3, 7);
        Vector2d test_vector_2 = new Vector2d(-5, 2);
        Vector2d test_vector_3 = new Vector2d(1, 23);
        assertEquals(test_vector_1.add(test_vector_2), new Vector2d(-2, 9));
        assertEquals(test_vector_3.add(test_vector_1), new Vector2d(4, 30));
    }

    @Test
    public void subtract() {
        Vector2d test_vector_1 = new Vector2d(3, 7);
        Vector2d test_vector_2 = new Vector2d(-5, 2);
        Vector2d test_vector_3 = new Vector2d(1, 23);
        assertEquals(test_vector_1.subtract(test_vector_2), new Vector2d(8, 5));
        assertEquals(test_vector_3.subtract(test_vector_1), new Vector2d(-2, 16));
    }

    @Test
    public void opposite() {
        Vector2d test_vector_1 = new Vector2d(-5, 2);
        Vector2d test_vector_2 = new Vector2d(1, 23);
        assertEquals(test_vector_1.opposite(), new Vector2d(5, -2));
        assertEquals(test_vector_2.opposite(), new Vector2d(-1, -23));
    }
}
