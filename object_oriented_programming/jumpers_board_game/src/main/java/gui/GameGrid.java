package gui;

import game.GameBoard;
import game.Vector2d;
import javafx.geometry.HPos;
import javafx.scene.control.Label;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;

public class GameGrid {
    public static final String FONT_NAME = "Tahoma";
    public static final int FONT_SIZE = 15;

    public final GridPane grid = new GridPane();
    private final GameBoard gameBoard;

    public GameGrid(GameBoard gameBoard) {
        this.gameBoard = gameBoard;

        Label label = new Label("y\\x");
        label.setFont(Font.font(FONT_NAME, FontWeight.NORMAL, FONT_SIZE));
        StackPane xy_stack = new StackPane();
        xy_stack.setBorder(new Border(new BorderStroke(Color.web("0x000000"),
                BorderStrokeStyle.SOLID, CornerRadii.EMPTY, new BorderWidths(0.4))));
        xy_stack.getChildren().add(label);
        grid.add(xy_stack, 0,0,1,1);
        grid.getColumnConstraints().add(new ColumnConstraints(40));
        grid.getRowConstraints().add(new RowConstraints(40));
        GridPane.setHalignment(xy_stack, HPos.CENTER);

        for (int i=1; i <= GameBoard.BOARD_SIZE; i++) {
            grid.getColumnConstraints().add(new ColumnConstraints(40));

            label = new Label(String.format("%d", i-1));
            label.setFont(Font.font(FONT_NAME, FontWeight.NORMAL, FONT_SIZE));
            StackPane stack = new StackPane();
            stack.setBorder(new Border(new BorderStroke(Color.web("0x000000"),
                    BorderStrokeStyle.SOLID, CornerRadii.EMPTY, new BorderWidths(0.4))));
            stack.getChildren().add(label);

            GridPane.setHalignment(stack, HPos.CENTER);

            grid.add(stack, i, 0,1,1);
        }

        for (int i=1; i <= GameBoard.BOARD_SIZE; i++) {
            grid.getRowConstraints().add(new RowConstraints(40));

            label = new Label(String.format("%d", GameBoard.BOARD_SIZE-i));
            label.setFont(Font.font(FONT_NAME, FontWeight.NORMAL, FONT_SIZE));
            StackPane stack = new StackPane();
            stack.setBorder(new Border(new BorderStroke(Color.web("0x000000"),
                    BorderStrokeStyle.SOLID, CornerRadii.EMPTY, new BorderWidths(0.4))));
            stack.getChildren().add(label);

            GridPane.setHalignment(label, HPos.CENTER);

            grid.add(stack, 0, i,1,1);
        }
    }

    private void createPawn(int i, int j) {
        int finalJ = i+1;
        int finalI = GameBoard.BOARD_SIZE-j;
        this.grid.getChildren().removeIf(node -> GridPane.getRowIndex(node) == finalI && GridPane.getColumnIndex(node) == finalJ);

        StackPane stack = new StackPane();
        stack.setBorder(new Border(new BorderStroke(Color.web("0x000000"),
                BorderStrokeStyle.SOLID, CornerRadii.EMPTY, new BorderWidths(0.4))));

        if (gameBoard.board.containsKey(new Vector2d(i, j))) {
            Circle circle = new Circle();
            circle.setRadius(17);
            String color = gameBoard.board.get(new Vector2d(i, j)).ownedBy.getColor();
            circle.setFill(Color.web(color));
            circle.setStroke(Color.web(color));
            stack.getChildren().add(circle);
        }

        stack.setOnMouseClicked(event -> {
            if (gameBoard.board.containsKey(new Vector2d(i, j))) {
                Vector2d oldChosen = this.gameBoard.chosenPosition;

                if (oldChosen != null && gameBoard.board.containsKey(oldChosen)) {
                    createPawn(oldChosen.x, oldChosen.y);
                }

                this.gameBoard.ifChosen = true;
                this.gameBoard.chosenPosition = new Vector2d(i, j);

                Circle innerCircle = new Circle();
                innerCircle.setRadius(10);
                innerCircle.setFill(Color.web("#39e609"));
                innerCircle.setStroke(Color.web("#39e609"));
                stack.getChildren().add(innerCircle);
            }
        });

        GridPane.setHalignment(stack, HPos.CENTER);
        grid.add(stack, i+1, GameBoard.BOARD_SIZE-j,1,1);
    }

    public void updateGrid() {
        for (int i=0; i < GameBoard.BOARD_SIZE; i++) {
            for (int j=0; j < GameBoard.BOARD_SIZE; j++) {
                createPawn(i, j);
            }
        }
    }
}
