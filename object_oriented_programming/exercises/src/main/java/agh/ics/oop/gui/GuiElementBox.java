package agh.ics.oop.gui;

import agh.ics.oop.Grass;
import agh.ics.oop.IMapObject;

import javafx.geometry.Pos;
import javafx.scene.control.Label;
import javafx.scene.image.ImageView;
import javafx.scene.image.Image;
import javafx.scene.layout.VBox;

import java.io.FileInputStream;
import java.io.FileNotFoundException;

public class GuiElementBox {
    VBox vbox = new VBox(3);

    public GuiElementBox(IMapObject object) {
        setImage(object);
    }

    private void setImage(IMapObject object) {
        String filePath = object.getImageFilePath();
        Label label;

       if (object instanceof Grass) {
           label = new Label("Trawa");
       }
       else {
           label = new Label("Z: " + object.getPosition());
       }
        Image image;
       try {
           image = new Image(new FileInputStream(filePath));
       } catch (FileNotFoundException ex) {
           throw new RuntimeException("File was not found");
       }
        ImageView imageView = new ImageView(image);
        imageView.setFitWidth(20);
        imageView.setFitHeight(20);

        this.vbox.getChildren().addAll(imageView, label);
        this.vbox.setAlignment(Pos.CENTER);
    }

    public VBox getVbox() {
        return this.vbox;
    }
}
