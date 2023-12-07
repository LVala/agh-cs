package evogen;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class MapDirectionTest {
    @Test
    public void nextTest() {
        assertEquals(MapDirection.NORTH.next(3), MapDirection.SOUTH_EAST);
        assertEquals(MapDirection.WEST.next(9), MapDirection.NORTH_WEST);
    }

    @Test
    public void oppositeTest() {
        assertEquals(MapDirection.NORTH.opposite(), MapDirection.SOUTH);
        assertEquals(MapDirection.SOUTH_WEST.opposite(), MapDirection.NORTH_EAST);
    }
}
