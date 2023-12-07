package agh.ics.oop;

import agh.ics.oop.gui.App;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class EngineTest {

    @Test
    public void runTest1() {
        MoveDirection[] directions = new OptionsParser().parse("f b r l f f r r f f f f f f f f".split(" "));
        IWorldMap map = new RectangularMap(10, 5);
        Vector2d[] positions = { new Vector2d(2,2), new Vector2d(3,4) };
        IEngine engine = new SimulationEngine(directions, map, positions, new App());
        engine.run();

        Animal[] animals = map.getAnimals().values().toArray(new Animal[0]);
        assertEquals(animals[0].getPosition(), new Vector2d(2, 0));
        assertEquals(animals[0].getOrientation(), MapDirection.SOUTH);
        assertEquals(animals[1].getPosition(), new Vector2d(3, 4));
        assertEquals(animals[1].getOrientation(), MapDirection.NORTH);
    }

    @Test
    public void runTest2() {
        MoveDirection[] directions = new OptionsParser().parse("r l f f f f f f f f f f f f f f f".split(" "));
        IWorldMap map = new GrassField(10);
        Vector2d[] positions = {new Vector2d(2, 2), new Vector2d(3, 4), new Vector2d(5, 7)};
        IEngine engine = new SimulationEngine(directions, map, positions, new App());
        engine.run();

        Animal[] animals = map.getAnimals().values().toArray(new Animal[0]);
        assertEquals(animals[0].getPosition(), new Vector2d(5, 12));
        assertEquals(animals[0].getOrientation(), MapDirection.NORTH);
        assertEquals(animals[1].getPosition(), new Vector2d(7, 2));
        assertEquals(animals[1].getOrientation(), MapDirection.EAST);
        assertEquals(animals[2].getPosition(), new Vector2d(-2, 4));
        assertEquals(animals[2].getOrientation(), MapDirection.WEST);
    }
}
