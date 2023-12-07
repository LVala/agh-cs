package gui;

public class Main {

    // Projekt nr2 na Programowanie Obiektowe - Skoczki
    // informatyka WIET AGH 2021/22
    // autor: Lukasz Wala

    // made using Gradle 7.3.1 and Java 17

    // without this artificial main class JavaFX
    // always produces "runtime components are missing" error
    // covered on https://github.com/javafxports/openjdk-jfx/issues/236

    public static void main(String[] args) {
        MainGameStage.startGui(args);
    }
}
