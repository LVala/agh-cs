package agh.ics.oop;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class AnimalTest {

    @Test
    public void orientationTest() {
        Animal animal_1 = new Animal();
        for (int i=0; i < 4; i++) {
            animal_1.move(MoveDirection.LEFT);
            switch(i) {
                case 0 -> assertEquals(animal_1.getOrientation(), MapDirection.WEST);
                case 1 -> assertEquals(animal_1.getOrientation(), MapDirection.SOUTH);
                case 2 -> assertEquals(animal_1.getOrientation(), MapDirection.EAST);
                case 3 -> assertEquals(animal_1.getOrientation(), MapDirection.NORTH);
            }
        }
        for (int i=0; i < 4; i++) {
            animal_1.move(MoveDirection.RIGHT);
            switch(i) {
                case 0 -> assertEquals(animal_1.getOrientation(), MapDirection.EAST);
                case 1 -> assertEquals(animal_1.getOrientation(), MapDirection.SOUTH);
                case 2 -> assertEquals(animal_1.getOrientation(), MapDirection.WEST);
                case 3 -> assertEquals(animal_1.getOrientation(), MapDirection.NORTH);
            }
        }
        assertTrue(animal_1.isAt(new Vector2d(2, 2)));
    }

    @Test
    public void positionTest() {
        Animal animal_1 = new Animal();
        animal_1.move(MoveDirection.FORWARD);
        assertTrue(animal_1.isAt(new Vector2d(2,3)));
        animal_1.move(MoveDirection.BACKWARD);
        assertTrue(animal_1.isAt(new Vector2d(2,2)));

        animal_1.move(MoveDirection.LEFT);
        animal_1.move(MoveDirection.FORWARD);
        assertTrue(animal_1.isAt(new Vector2d(1,2)));
        animal_1.move(MoveDirection.BACKWARD);
        assertTrue(animal_1.isAt(new Vector2d(2,2)));

        animal_1.move(MoveDirection.LEFT);
        animal_1.move(MoveDirection.FORWARD);
        assertTrue(animal_1.isAt(new Vector2d(2,1)));
        animal_1.move(MoveDirection.BACKWARD);
        assertTrue(animal_1.isAt(new Vector2d(2,2)));

        animal_1.move(MoveDirection.LEFT);
        animal_1.move(MoveDirection.FORWARD);
        assertTrue(animal_1.isAt(new Vector2d(3,2)));
        animal_1.move(MoveDirection.BACKWARD);
        assertTrue(animal_1.isAt(new Vector2d(2,2)));
    }

    @Test
    public void outofboundsTest() {
        Animal animal_1 = new Animal();

        for (int i=0; i < 20; i++)
            animal_1.move(MoveDirection.FORWARD);
        assertTrue(animal_1.isAt(new Vector2d(2, 4)));

        for (int i=0; i < 20; i++)
            animal_1.move(MoveDirection.BACKWARD);
        assertTrue(animal_1.isAt(new Vector2d(2, 0)));

        animal_1.move(MoveDirection.LEFT);
        for (int i=0; i < 20; i++)
            animal_1.move(MoveDirection.FORWARD);
        assertTrue(animal_1.isAt(new Vector2d(0, 0)));

        for (int i=0; i < 20; i++)
            animal_1.move(MoveDirection.BACKWARD);
        assertTrue(animal_1.isAt(new Vector2d(4, 0)));
    }

    @Test
    public void parsingTest() {
        OptionsParser parser = new OptionsParser();

        String[] str_arr_1 = {"f", "forward", "l", "left", "r", "right", "b", "backward"};
        MoveDirection[] md_arr_1 = {MoveDirection.FORWARD, MoveDirection.FORWARD, MoveDirection.LEFT,
                MoveDirection.LEFT, MoveDirection.RIGHT, MoveDirection.RIGHT, MoveDirection.BACKWARD, MoveDirection.BACKWARD};
        assertArrayEquals(parser.parse(str_arr_1), md_arr_1);

//        String[] str_arr_2 = {"f", "asd", "l", "zxc", "r"};
//        MoveDirection[] md_arr_2 = {MoveDirection.FORWARD, MoveDirection.LEFT, MoveDirection.RIGHT};
//        assertArrayEquals(parser.parse(str_arr_2), md_arr_2); //wyjątki

    }

    @Test
    public void parseandmoveTest() {
        Animal animal_1 = new Animal();
        OptionsParser parser = new OptionsParser();

        String[] input = {"f", "r", "f", "as", "backward", "forward", "f", "r", "b"};

        for (MoveDirection elem: parser.parse(input)) {
            animal_1.move(elem);
        }

        assertTrue(animal_1.isAt(new Vector2d(4, 4)));
    }
}
