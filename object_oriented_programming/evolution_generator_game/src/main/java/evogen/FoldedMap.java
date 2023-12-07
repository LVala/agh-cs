package evogen;

public class FoldedMap extends AbstractWorldMap{

    public FoldedMap(int width, int height, int startEnergy, int moveEnergy, int plantEnergy, double jungleRatio,
                      int initialAnimals) {
        super(width, height, startEnergy, moveEnergy, plantEnergy, jungleRatio, initialAnimals);
    }

    public Vector2d getMovePosition(Vector2d animalPosition, MapDirection direction) {
        Vector2d moveVec = direction.getDirectionVector();
        Vector2d newPos = animalPosition.add(moveVec);
        if (newPos.x >= 0 && newPos.x < this.width && newPos.y >= 0 && newPos.y < this.height) {
            return newPos;
        }
        int newX = ((newPos.x + this.width)%this.width);
        int newY = ((newPos.y + this.height)%this.height);

        return new Vector2d(newX, newY);
    }

    public String getMapName() {
        return "Folded Map";
    }
}
