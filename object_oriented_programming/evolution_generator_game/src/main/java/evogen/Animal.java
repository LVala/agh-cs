package evogen;

import java.util.Arrays;
import java.util.Random;

public class Animal implements IMapObject {
    private Vector2d position;
    private MapDirection orientation = MapDirection.getRandomDirection();
    private int energy;
    private final Genotype genotype;
    private final AbstractWorldMap map;

    private final int bornEra;
    private int deathEra = -1;

    private int childrenNumber = 0;

    private int trackedChildrenNumber = 0;  // used when animal is clicked on in gui
    private int trackedDescendantsNumber = 0;
    private boolean ifTracked = false;
    private Animal trackedAncestor = null;

    // CONSTRUCTOR

    public Animal(Vector2d position, int energy, Genotype genotype, AbstractWorldMap map, int bornEra) {
        this.position = position;
        this.energy = energy;
        this.genotype = genotype;
        this.map = map;
        this.bornEra = bornEra;
    }

    // GETTERS AND SETTERS

    public void setIfTracked(boolean ifTracked) {
        this.ifTracked = ifTracked;
        this.trackedChildrenNumber = 0;  // reset when clicked on, even if it's the same animal
        this.trackedDescendantsNumber = 0;
    }

    public void setDeathEra(int era) {
        this.deathEra = era;
    }

    public Vector2d getPosition() {
        return this.position;
    }

    public int getEnergy() {
        return this.energy;
    }

    public Genotype getGenotype() {
        return this.genotype;
    }

    public int getBornEra() {
        return this.bornEra;
    }

    public int getDeathEra() {
        return this.deathEra;
    }

    public int getTrackedChildrenNumber() {
        return this.trackedChildrenNumber;
    }

    public int getTrackedDescendantsNumber() {
        return this.trackedDescendantsNumber;
    }

    public int getChildrenNumber() {
        return this.childrenNumber;
    }

    // MAP ACTION METHODS

    public void eatPlant(Vector2d position, int plantEnergy, int splitBetween) {
        this.energy += (plantEnergy/splitBetween);

        map.plantEaten(position); // observer
        this.map.changeSumEnergy(plantEnergy);  // for stats tracking
    }

    public Animal reproduce(Animal other, int bornEra) {
        if (this.energy < 0.5  * this.map.moveEnergy || other.energy < 0.5  * this.map.moveEnergy)
            throw new IllegalArgumentException("Not enough energy to reproduce");

        boolean biggerTakesLeft = new Random().nextBoolean();

        Animal bigger = (this.energy >= other.energy) ? this : other;
        Animal smaller = (this.energy < other.energy) ? this : other;

        int[] leftGenes, rightGenes;
        double splitAt;
        if (biggerTakesLeft) {
            splitAt = (double) bigger.energy/(bigger.energy + smaller.energy);
            leftGenes = bigger.genotype.getPartOfGenotype(splitAt, true);
            rightGenes = smaller.genotype.getPartOfGenotype(splitAt, false);
        }
        else {
            splitAt = (double) smaller.energy/(bigger.energy + smaller.energy);
            leftGenes = smaller.genotype.getPartOfGenotype(splitAt, true);
            rightGenes = bigger.genotype.getPartOfGenotype(splitAt, false);
        }

        int[] newGenes = Arrays.copyOf(leftGenes, leftGenes.length + rightGenes.length);
        System.arraycopy(rightGenes, 0, newGenes, leftGenes.length, rightGenes.length);
        Genotype newGenotype = new Genotype(newGenes);

        int newEnergy = (int) (0.25 * this.energy) + (int) (0.25 * other.energy);
        this.energy -= (int) (0.25 * this.energy);
        other.energy -= (int) (0.25 * other.energy);

        Animal newAnimal = new Animal(this.position, newEnergy, newGenotype, this.map, bornEra);

        // stats tracking

        this.childrenNumber++;
        other.childrenNumber++;

        if (this.ifTracked) {
            this.trackedChildrenNumber++;
            this.trackedDescendantsNumber++;
        }
        else if (other.ifTracked) {
            other.trackedChildrenNumber++;
            other.trackedDescendantsNumber++;
        }
        if (this.trackedAncestor != null && this.trackedAncestor.ifTracked) {
            this.trackedAncestor.trackedDescendantsNumber++;
            newAnimal.trackedAncestor = this.trackedAncestor;
        }
        else if (other.trackedAncestor != null && other.trackedAncestor.ifTracked) {
            other.trackedAncestor.trackedDescendantsNumber++;
            newAnimal.trackedAncestor = other.trackedAncestor;
        }

        this.map.changeSumEnergy((-1) * (newAnimal.energy));
        this.map.changeSumChildrenNumber(2);

        return newAnimal;
    }

    public void move(int moveEnergy) {
        if (!this.map.getAnimals().get(this.position).contains(this)) throw new IllegalStateException("Animals position and it's place on map does not match");

        Vector2d oldPosition = this.position;
        int rndGene = this.genotype.getRandomGene();

        if (rndGene == 0) {
            this.position = this.map.getMovePosition(this.position, this.orientation);
            map.animalPositionChanged(this, oldPosition); // observer
        }
        else if (rndGene == 4) {
            this.position = this.map.getMovePosition(this.position, this.orientation.opposite());
            map.animalPositionChanged(this, oldPosition); // observer
        }
        else {
            this.orientation = this.orientation.next(rndGene);
        }

        this.map.changeSumEnergy((-1) * Math.min(moveEnergy, this.energy)); // stats tracking
        this.energy = Math.max(this.energy - moveEnergy, 0);
    }
}