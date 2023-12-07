package game;

import java.util.*;

public class GameBoard {
    public static final int BOARD_SIZE = 8;

    public final Map<Vector2d, Pawn> board = new HashMap<>();
    public Players turn = Players.BLUE_PLAYER;

    public Vector2d chosenPosition;
    public boolean ifChosen = false;

    public GameBoard() {
        for (int i = 0; i < BOARD_SIZE; i++) {
            this.board.put(new Vector2d(i, 0), new Pawn(Players.BLUE_PLAYER));
            this.board.put(new Vector2d(i, 1), new Pawn(Players.BLUE_PLAYER));

            this.board.put(new Vector2d(i, BOARD_SIZE-1), new Pawn(Players.RED_PLAYER));
            this.board.put(new Vector2d(i, BOARD_SIZE-2), new Pawn(Players.RED_PLAYER));
        }
    }

    private List<Vector2d> parsePath(String path) {
        List<Vector2d> returnList = new ArrayList<>();

        String[] pathArray = path.split("\\s+");

        if (pathArray.length % 2 == 1) throw new IllegalArgumentException("Last field's y coordinate is not specified");

        for (int i = 0; i < pathArray.length; i += 2) {
            int x = Integer.parseInt(pathArray[i]);
            int y = Integer.parseInt(pathArray[i+1]);
            if (!((x < BOARD_SIZE && x >= 0) && (y < BOARD_SIZE && y >= 0))) throw new IllegalArgumentException("Value outside of board");
            returnList.add(new Vector2d(x, y));
        }

        return returnList;
    }

    private boolean validateMoves(Vector2d position, List<Vector2d> movesList) {
        if (movesList.size() == 0) return false;
        if (movesList.size() == 1) {
            if (position.x == movesList.get(0).x && Math.abs(position.y - movesList.get(0).y) == 1 && !this.board.containsKey(movesList.get(0))) return true;
            if (position.y == movesList.get(0).y && Math.abs(position.x - movesList.get(0).x) == 1 && !this.board.containsKey(movesList.get(0))) return true;
        }

        if (this.board.containsKey(movesList.get(0))) return false;
        if (!(position.x == movesList.get(0).x && Math.abs(position.y - movesList.get(0).y) == 2
                && this.board.containsKey(new Vector2d(position.x, (position.y + movesList.get(0).y)/2)))
                && !(position.y == movesList.get(0).y && Math.abs(position.x - movesList.get(0).x) == 2
                && this.board.containsKey(new Vector2d((position.y + movesList.get(0).x)/2, position.y)))) return false;

        for (int i = 1; i < movesList.size(); i++) {
            if (this.board.containsKey(movesList.get(i))) return false;
            if (!(movesList.get(i-1).x == movesList.get(i).x && Math.abs(movesList.get(i-1).y - movesList.get(i).y) == 2
                    && this.board.containsKey(new Vector2d(movesList.get(i).x, (movesList.get(i-1).y + movesList.get(i).y)/2)))
                    && !(movesList.get(i-1).y == movesList.get(i).y && Math.abs(movesList.get(i-1).x - movesList.get(i).x) == 2
                    && this.board.containsKey(new Vector2d((movesList.get(i-1).x + movesList.get(i).x)/2, movesList.get(i).y)))) return false;
        }
        return true;
    }

    public void move(String path) throws IllegalArgumentException {
        if (!this.board.containsKey(this.chosenPosition) || !this.board.get(this.chosenPosition).ownedBy.equals(this.turn)) throw new IllegalArgumentException("Invalid chosen field");

        List<Vector2d> movesList = parsePath(path);
        if (!validateMoves(this.chosenPosition, movesList)) throw new IllegalArgumentException("Invalid moves sequence");

        Vector2d newPosition = movesList.get(movesList.size()-1);
        this.board.remove(this.chosenPosition);
        this.board.put(newPosition, new Pawn(this.turn));
        this.turn = this.turn.getOther();
    }

    public boolean checkIfWon() {
        boolean blueWon = true;
        boolean redWon = true;

        for (int i = 0; i < BOARD_SIZE; i++) {
            if (!board.containsKey(new Vector2d(i, 0)) || !board.get(new Vector2d(i, 0)).ownedBy.equals(Players.RED_PLAYER)) redWon = false;
            if (!board.containsKey(new Vector2d(i, 1)) || !board.get(new Vector2d(i, 1)).ownedBy.equals(Players.RED_PLAYER)) redWon = false;

            if (!board.containsKey(new Vector2d(i, BOARD_SIZE-1)) || !board.get(new Vector2d(i, BOARD_SIZE-1)).ownedBy.equals(Players.BLUE_PLAYER)) blueWon = false;
            if (!board.containsKey(new Vector2d(i, BOARD_SIZE-2)) || !board.get(new Vector2d(i, BOARD_SIZE-2)).ownedBy.equals(Players.BLUE_PLAYER)) blueWon = false;
        }

        return blueWon || redWon;
    }
}
