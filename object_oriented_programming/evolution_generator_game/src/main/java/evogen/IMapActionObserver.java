package evogen;

public interface IMapActionObserver {

    void animalPositionChanged(Animal animal, Vector2d oldPosition);

    void plantEaten(Vector2d position);
}
