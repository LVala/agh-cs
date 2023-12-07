package agh.ics.oop;

import java.util.Arrays;

public class OptionsParser {
    public MoveDirection[] parse(String[] dir_array) {
        MoveDirection[] return_array = new MoveDirection[dir_array.length];

        int i = 0;
        for (String elem: dir_array) {
            if (elem == null) continue;

            switch(elem) {
                case "f", "forward" -> return_array[i] = MoveDirection.FORWARD;
                case "b", "backward" -> return_array[i] = MoveDirection.BACKWARD;
                case "l", "left" -> return_array[i] = MoveDirection.LEFT;
                case "r", "right" -> return_array[i] = MoveDirection.RIGHT;
                default -> throw new IllegalArgumentException(elem + " is not legal move specification");
            }
            i++;

        }
        return return_array;
    }
}
