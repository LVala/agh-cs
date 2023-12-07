package evogen;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class AnimalTest {
    @Test
    public void eatPlantTest() {
        AbstractWorldMap map = new FoldedMap(30,30,100,15,50,0.2,10);
        Animal testAnimal1 = new Animal(new Vector2d(2,2), 100, Genotype.generateRandomGenotype(), map, 0);
        Animal testAnimal2 = new Animal(new Vector2d(4,4), 100, Genotype.generateRandomGenotype(), map, 1);
        map.plants.put(new Vector2d(1,1), new Plant(new Vector2d(1,1)));
        map.plants.put(new Vector2d(3,3), new Plant(new Vector2d(3,3)));

        testAnimal1.eatPlant(new Vector2d(1,1), 50, 2);
        assertEquals(testAnimal1.getEnergy(), 125);
        testAnimal2.eatPlant(new Vector2d(3,3), 100, 1);
        assertEquals(testAnimal2.getEnergy(), 200);
    }

    @Test
    public void reproduceTest() {
        AbstractWorldMap map = new FoldedMap(30,30,100,15,50,0.2,10);
        Animal testAnimal1 = new Animal(new Vector2d(2,2), 100, Genotype.generateRandomGenotype(), map, 0);
        Animal testAnimal2 = new Animal(new Vector2d(4,4), 100, Genotype.generateRandomGenotype(), map, 1);

        Animal testAnimal3 = testAnimal1.reproduce(testAnimal2, 1);
        assertEquals(testAnimal1.getEnergy(), 75);
        assertEquals(testAnimal2.getEnergy(), 75);
        assertEquals(testAnimal3.getEnergy(), 50);
        assertEquals(testAnimal3.getPosition(), new Vector2d(2,2));
    }
}
