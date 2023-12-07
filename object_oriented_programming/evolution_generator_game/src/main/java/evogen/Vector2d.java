package evogen;

import java.util.Objects;
import java.util.Random;

public class Vector2d {
    public final int x;
    public final int y;

    public Vector2d(int x, int y) {
        this.x = x;
        this.y = y;
    }

    // static method
    public static Vector2d getRandomVector(int width, int height) {
        // returns random Vector2d with coords [0-width), [0-height)

        int rnd_height = new Random().nextInt(height);
        int rnd_width = new Random().nextInt(width);
        return new Vector2d(rnd_width, rnd_height);
    }

    public Vector2d add(Vector2d other) {
        int newX = this.x + other.x;
        int newY = this.y + other.y;
        return new Vector2d(newX, newY);
    }

    public boolean isInside(int startWidth, int endWidth, int startHeight, int endHeight) {
        if (startWidth > endWidth || startHeight > endHeight) throw new IllegalArgumentException("Invalid coordinates to check");
        // checks if Vector2d is inside rectangle with given coords
        return (this.x >= startWidth && this.x < endWidth && this.y >= startHeight && this.y < endHeight);
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) return true;
        if (!(other instanceof Vector2d that)) return false;
        return this.x == that.x && this.y == that.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(this.x, this.y);
    }
}
