package evogen;

public class BoundedMap extends AbstractWorldMap{

    public BoundedMap(int width, int height, int startEnergy, int moveEnergy, int plantEnergy, double jungleRatio,
                      int initialAnimals) {
        super(width, height, startEnergy, moveEnergy, plantEnergy, jungleRatio, initialAnimals);
    }

    public Vector2d getMovePosition(Vector2d animalPosition, MapDirection direction) {
        Vector2d moveVec = direction.getDirectionVector();
        Vector2d newPos = animalPosition.add(moveVec);
        if (newPos.x >= 0 && newPos.x < this.width && newPos.y >= 0 && newPos.y < this.height) {
            return newPos;
        }
        else return animalPosition;
    }

    public String getMapName() {
        return "Bounded Map";
    }
}
