package gui;

import game.GameBoard;
import javafx.application.Application;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.stage.Popup;
import javafx.stage.Stage;

public class MainGameStage extends Application {
    public static final String FONT_NAME = "Tahoma";
    public static final int FONT_SIZE = 15;

    private VBox createMainBox(GameBoard gameBoard, Stage primaryStage) {
        VBox vBox = new VBox(20);

        GameGrid gameGrid = new GameGrid(gameBoard);
        gameGrid.updateGrid();
        gameGrid.grid.setAlignment(Pos.CENTER);
        vBox.getChildren().add(gameGrid.grid);

        HBox hBox = new HBox(10);
        Circle turnCircle = new Circle();
        turnCircle.setRadius(10);
        turnCircle.setFill(Color.web(gameBoard.turn.getColor()));
        turnCircle.setStroke(Color.web(gameBoard.turn.getColor()));
        Label turnLabel = new Label("Turn of: ");
        turnLabel.setFont(Font.font(FONT_NAME, FontWeight.NORMAL, FONT_SIZE));
        hBox.getChildren().add(turnLabel);
        hBox.getChildren().add(turnCircle);

        hBox.setAlignment(Pos.CENTER);
        vBox.getChildren().add(hBox);

        HBox inputHBox = new HBox(20);

        TextField inputTextField = new TextField("Moves here");
        Button btn = new Button("Move");
        btn.setFont(Font.font(FONT_NAME, FontWeight.NORMAL, 22));
        btn.setPrefSize(100,40);

        btn.setOnAction(event -> {
            try {
                if (gameBoard.ifChosen) {
                    inputTextField.setStyle(null);
                    gameBoard.move(inputTextField.getText());
                    gameGrid.updateGrid();
                    turnCircle.setFill(Color.web(gameBoard.turn.getColor()));
                    turnCircle.setStroke(Color.web(gameBoard.turn.getColor()));
                    if (gameBoard.checkIfWon()) {
                        showPopup(gameBoard, primaryStage);
                    }
                    inputTextField.setText("");
                }
            }
            catch (IllegalArgumentException ex) {
                inputTextField.setStyle("-fx-text-box-border: #B22222; -fx-focus-color: #B22222;");
                inputTextField.setText("Invalid input or pawn");
            }
        });

        inputHBox.getChildren().add(inputTextField);
        inputHBox.getChildren().add(btn);
        inputHBox.setAlignment(Pos.CENTER);
        vBox.getChildren().add(inputHBox);

        return vBox;
    }

    private void showPopup(GameBoard gameBoard, Stage parentStage) {
        Popup popup = new Popup();
        Label label = new Label(String.format("%s Player Won!", gameBoard.turn.getOther().getName()));
        label.setFont(Font.font(FONT_NAME, FontWeight.NORMAL, 30));
        label.setStyle(" -fx-background-color: white; -fx-border-color: black");
        popup.getContent().add(label);
        popup.show(parentStage);
    }

    public void start(Stage primaryStage) {

        GameBoard gameBoard = new GameBoard();

        primaryStage.setTitle("Jumpers");
        VBox vBox = createMainBox(gameBoard, primaryStage);
        Scene scene = new Scene(vBox, 450, 500);
        primaryStage.setScene(scene);

        primaryStage.show();
    }

    public static void startGui(String[] args) {
        launch(args);
    }
}
