package agh.ics.oop;

public interface IPositionChangeObserver {

    void positionChanged(IMapObject map_object, Vector2d oldPosition, Vector2d newPosition);
}
