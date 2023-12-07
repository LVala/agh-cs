package evogen;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class MapTest {
    @Test
    public void placeAnimalTest() {
        AbstractWorldMap testFoldedMap = new FoldedMap(30,30,100,15,50,0.2,0);
        Animal testAnimal1 = new Animal(new Vector2d(2,2), 100, Genotype.generateRandomGenotype(), testFoldedMap, 0);
        Animal testAnimal2 = new Animal(new Vector2d(4,4), 100, Genotype.generateRandomGenotype(), testFoldedMap, 1);

        testFoldedMap.placeAnimal(testAnimal1, true);
        testFoldedMap.placeAnimal(testAnimal2, true);
        assertEquals(testFoldedMap.getAnimals().get(new Vector2d(2,2)).get(0), testAnimal1);
        assertEquals(testFoldedMap.getAnimals().get(new Vector2d(4,4)).get(0), testAnimal2);
    }

    @Test
    public void removeDeadAnimalTest() {
        AbstractWorldMap testFoldedMap = new FoldedMap(30,30,100,15,50,0.2,0);
        Animal testAnimal1 = new Animal(new Vector2d(2,2), 100, Genotype.generateRandomGenotype(), testFoldedMap, 0);

        testFoldedMap.placeAnimal(testAnimal1, true);
        testFoldedMap.removeDeadAnimal(testAnimal1, 3);
        assertNull(testFoldedMap.getAnimals().get(new Vector2d(2, 2)));
    }

    @Test
    public void getTwoStrongestAnimalsAtTest() {
        AbstractWorldMap testBoundedMap = new BoundedMap(30,30,100,15,50,0.2,0);
        Animal testAnimal3 = new Animal(new Vector2d(2,2), 100, Genotype.generateRandomGenotype(), testBoundedMap, 0);
        Animal testAnimal4 = new Animal(new Vector2d(2,2), 110, Genotype.generateRandomGenotype(), testBoundedMap, 1);

        testBoundedMap.placeAnimal(testAnimal3, true);
        testBoundedMap.placeAnimal(testAnimal4, true);
        Animal[] animals = testBoundedMap.getTwoStrongestAnimalsAt(new Vector2d(2,2));
        assertEquals(animals[0], testAnimal4);
        assertEquals(animals[1], testAnimal3);
    }

    @Test
    public void getStrongestAnimalsAtTest() {
        AbstractWorldMap testBoundedMap = new BoundedMap(30,30,100,15,50,0.2,0);
        Animal testAnimal3 = new Animal(new Vector2d(2,2), 100, Genotype.generateRandomGenotype(), testBoundedMap, 0);
        Animal testAnimal4 = new Animal(new Vector2d(2,2), 110, Genotype.generateRandomGenotype(), testBoundedMap, 1);

        testBoundedMap.placeAnimal(testAnimal3, true);
        testBoundedMap.placeAnimal(testAnimal4, true);
        List<Animal> animals = testBoundedMap.getStrongestAnimalsAt(new Vector2d(2,2));
        assertEquals(1, animals.size());
        assertEquals(animals.get(0), testAnimal4);
    }

    @Test
    public void getStrongestAnimalAtTest() {
        AbstractWorldMap testBoundedMap = new BoundedMap(30,30,100,15,50,0.2,0);
        Animal testAnimal3 = new Animal(new Vector2d(2,2), 100, Genotype.generateRandomGenotype(), testBoundedMap, 0);
        Animal testAnimal4 = new Animal(new Vector2d(2,2), 110, Genotype.generateRandomGenotype(), testBoundedMap, 1);

        testBoundedMap.placeAnimal(testAnimal3, true);
        testBoundedMap.placeAnimal(testAnimal4, true);
        assertEquals(testBoundedMap.getStrongestAnimalAt(new Vector2d(2,2)), testAnimal4);
    }

    @Test
    public void getMovePositionFoldedTest() {
        AbstractWorldMap testFoldedMap = new FoldedMap(30,30,100,15,50,0.2,0);

        assertEquals(testFoldedMap.getMovePosition(new Vector2d(0,0), MapDirection.SOUTH_WEST), new Vector2d(29,29));
        assertEquals(testFoldedMap.getMovePosition(new Vector2d(25, 0), MapDirection.SOUTH_EAST), new Vector2d(26, 29));
        assertEquals(testFoldedMap.getMovePosition(new Vector2d(29, 10), MapDirection.NORTH_EAST), new Vector2d(0, 11));
    }

    @Test
    public void getMovePositionBoundedMap() {
        AbstractWorldMap testBoundedMap = new BoundedMap(30,30,100,15,50,0.2,0);

        assertEquals(testBoundedMap.getMovePosition(new Vector2d(0,0), MapDirection.SOUTH_WEST), new Vector2d(0,0));
        assertEquals(testBoundedMap.getMovePosition(new Vector2d(25, 0), MapDirection.SOUTH_EAST), new Vector2d(25, 0));
        assertEquals(testBoundedMap.getMovePosition(new Vector2d(29, 10), MapDirection.NORTH_WEST), new Vector2d(28, 11));
    }
}
