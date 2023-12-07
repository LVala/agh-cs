package game;

public enum Players {
    RED_PLAYER,
    BLUE_PLAYER;

    public Players getOther() {
        if (this.equals(RED_PLAYER)) return BLUE_PLAYER;
        else return RED_PLAYER;
    }

    public String getColor() {
        return switch(this) {
            case RED_PLAYER -> "#a83232";
            case BLUE_PLAYER -> "#3c32a8";
        };
    }

    public String getName() {
        return switch(this) {
            case RED_PLAYER -> "Red";
            case BLUE_PLAYER -> "Blue";
        };
    }
}
