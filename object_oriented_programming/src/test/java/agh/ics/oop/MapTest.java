package agh.ics.oop;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class MapTest {

    @Test
    public void isOccupiedTest() {
        IWorldMap map = new RectangularMap(4, 4);
        map.place(new Animal(map, new Vector2d(2,2)));

        assertTrue(map.isOccupied(new Vector2d(2,2)));
        assertFalse(map.isOccupied(new Vector2d(2,3)));
    }

    @Test
    public void canMoveToTest() {
        IWorldMap map = new RectangularMap(4, 4);
        map.place(new Animal(map, new Vector2d(2,2)));

        assertFalse(map.canMoveTo(new Vector2d(2,2)));
        assertFalse(map.canMoveTo(new Vector2d(4,0)));
        assertTrue(map.canMoveTo(new Vector2d(1,2)));
    }

    @Test
    public void placeTest() {
        IWorldMap map = new RectangularMap(10, 10);

        assertEquals(map.getAnimals().size(), 0);

        map.place(new Animal(map, new Vector2d(2,2)));
        assertTrue(map.isOccupied(new Vector2d(2,2)));
//        map.place(new Animal(map, new Vector2d(2,2))); // wyjątki
        assertEquals(map.getAnimals().size(), 1);
        map.place(new Animal(map, new Vector2d(4,2)));
        assertEquals(map.getAnimals().size(), 2);
    }

    @Test
    public void isOccupiedGrassTest() {
        IWorldMap map = new GrassField(10);
        assertTrue(map.place(new Animal(map, new Vector2d(2,2))));

        assertTrue(map.isOccupied(new Vector2d(2,2)));
        assertFalse(map.isOccupied(new Vector2d(2,3)));
    }

    @Test
    public void canMoveToGrassTest() {
        IWorldMap map = new GrassField(10);
        assertTrue(map.place(new Animal(map, new Vector2d(2,2))));

        assertFalse(map.canMoveTo(new Vector2d(2,2)));
        assertTrue(map.canMoveTo(new Vector2d(4,0)));
        assertTrue(map.canMoveTo(new Vector2d(1,2)));
    }

    @Test
    public void placeGrassTest() {
        IWorldMap map = new GrassField(10);

        assertEquals(map.getAnimals().size(), 0);

        map.place(new Animal(map, new Vector2d(2,2)));
        assertTrue(map.isOccupied(new Vector2d(2,2)));
        map.place(new Animal(map, new Vector2d(2,2)));
        assertEquals(map.getAnimals().size(), 1);
        map.place(new Animal(map, new Vector2d(4,2)));
        assertEquals(map.getAnimals().size(), 2);
    }
}
