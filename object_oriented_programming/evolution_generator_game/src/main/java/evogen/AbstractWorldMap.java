package evogen;

import java.util.*;

abstract public class AbstractWorldMap implements IMapActionObserver {
    protected final Map<Vector2d, List<Animal>> animals = new HashMap<>();
    protected final Map<Vector2d, Plant> plants = new HashMap<>();

    public final int width;
    public final int height;

    public final int startEnergy;
    public final int moveEnergy;
    public final int plantEnergy;

    protected final int jungleSide;
    protected final Vector2d jungleCorner;  // lower left jungle corner, inclusive

    protected final Map<Genotype, Integer> genotypeCounter = new HashMap<>();
    protected int deadAnimalsNumber = 0;
    protected int plantNumber = 0;
    protected int animalNumber = 0;
    protected int sumEnergy = 0;
    protected int sumLifespan = 0;
    protected int sumChildrenNumber = 0;

    // CONSTRUCTOR

    public AbstractWorldMap(int width, int height, int startEnergy, int moveEnergy, int plantEnergy, double jungleRatio,
                            int initialAnimals) {
        this.width = width;
        this.height = height;
        this.startEnergy = startEnergy;
        this.moveEnergy = moveEnergy;
        this.plantEnergy = plantEnergy;
        // jungle always wants to be square, so with some ration and size parameters it may not fit on map, then only it's part is visible in GUI
        this.jungleSide = (int) Math.round(Math.sqrt((jungleRatio / (1 + jungleRatio)) * (this.width * this.height)));
        this.jungleCorner = new Vector2d(((this.width - this.jungleSide)/2), ((this.height - this.jungleSide)/2));

        initializeAnimals(initialAnimals);
    }

    private void initializeAnimals(int initialAnimals) {
        int i = 0;
        int iterator = 0;
        // trying to get unoccupied spot until success or to (2 * map area) failures (probably filled up map)
        while (i < initialAnimals && iterator < 2 * this.height*this.width) {
            Vector2d rndVector = Vector2d.getRandomVector(this.width, this.height);
            if (this.isOccupiedByAnimal(rndVector, 1)) {
                iterator++;
                continue;
            }
            Genotype rndGenotype = Genotype.generateRandomGenotype();
            Animal rndAnimal = new Animal(rndVector, startEnergy, rndGenotype, this, 0);
            placeAnimal(rndAnimal, true);
            i++;
        }
        // if above loop was not able to find free position, this one fills map up with the remaining animals
        // so always there is initialAnimals number of animals on map at the beginning
        if (i < initialAnimals) {
            for (int k = 0; k < this.width; k++) {
                for (int m = 0; m < this.height; m++) {
                    if (i == initialAnimals) return;
                    Vector2d newPosition = new Vector2d(k, m);
                    if (!isOccupiedByAnimal(newPosition, 1)) {
                        Genotype rndGenotype = Genotype.generateRandomGenotype();
                        Animal rndAnimal = new Animal(newPosition, startEnergy, rndGenotype, this, 0);
                        placeAnimal(rndAnimal, true);
                        i++;
                    }
                }
            }
        }
    }

    // GETTERS AND SETTERS

    public abstract Vector2d getMovePosition(Vector2d animalPosition, MapDirection direction);

    public abstract String getMapName();

    public Map<Vector2d, List<Animal>> getAnimals() {
        return this.animals;
    }

    public Plant getPlantAt(Vector2d position) {
        return this.plants.get(position);
    }

    public double getAverageLifespan() {
        if (this.deadAnimalsNumber == 0) return -1;
        return (double) this.sumLifespan/this.deadAnimalsNumber;
    }

    public double getAverageEnergy() {
        if (this.animalNumber == 0) return -1;
        return (double) this.sumEnergy/this.animalNumber;
    }

    public double getAverageChildrenNumber() {
        if (this.animalNumber == 0) return -1;
        return (double) this.sumChildrenNumber/this.animalNumber;
    }

    public double getAnimalNumber() {
        return this.animalNumber;
    }

    public double getPlantNumber() {
        return this.plantNumber;
    }

    public List<Genotype> getMostCommonGenotypes() {
        List<Genotype> mostCommonGenotypes = new ArrayList<>();
        int frequency = 0;
        for (var entry: this.genotypeCounter.entrySet()) {
            if ( entry.getValue() > frequency || mostCommonGenotypes.size() == 0) {
                mostCommonGenotypes.clear();
                mostCommonGenotypes.add(entry.getKey());
                frequency = entry.getValue();
            }
            else if (entry.getValue() == frequency) {
                mostCommonGenotypes.add(entry.getKey());
            }
        }
        return mostCommonGenotypes;
    }

    public Animal getStrongestAnimalAt(Vector2d position) {
        // get ONE of the strongest (most energy) animals on this field
        if (!this.isOccupiedByAnimal(position, 1)) throw new IllegalArgumentException("No animals on this field");
        Animal strongestAnimal = null;

        for (Animal animal : this.animals.get(position)) {
            if (strongestAnimal == null || animal.getEnergy() > strongestAnimal.getEnergy()) {
                strongestAnimal = animal;
            }
        }
        return strongestAnimal;
    }

    public List<Animal> getStrongestAnimalsAt(Vector2d position) {
        // get All the strongest (most energy) animals on this field
        if (!this.isOccupiedByAnimal(position, 1)) throw new IllegalArgumentException("No animals on this field");

        List<Animal> strongestAnimals = new ArrayList<>();

        for (Animal animal : this.animals.get(position)) {
            if (strongestAnimals.size() == 0 || animal.getEnergy() > strongestAnimals.get(0).getEnergy()) {
                strongestAnimals.clear();
                strongestAnimals.add(animal);
            }
            else if (animal.getEnergy() == strongestAnimals.get(0).getEnergy()) {
                strongestAnimals.add(animal);
            }
        }

         return strongestAnimals;
    }

    public Animal[] getTwoStrongestAnimalsAt(Vector2d position) {
        // get TWO strongest animals (most energy) on this field
        if (!this.isOccupiedByAnimal(position, 2)) throw new IllegalArgumentException("Less than 2 animals on this field");

        Animal fstStrongest = null;
        Animal sndStrongest = null;

        for (Animal animal : this.animals.get(position)) {
            if (fstStrongest == null || animal.getEnergy() > fstStrongest.getEnergy()) {
                sndStrongest = fstStrongest;
                fstStrongest = animal;
            }
            else if (sndStrongest == null || animal.getEnergy() > sndStrongest.getEnergy()) {
                sndStrongest = animal;
            }
        }

        return new Animal[]{fstStrongest, sndStrongest};
    }

    public void changeSumEnergy(int energy) {
        this.sumEnergy += energy;
    }

    public void changeSumChildrenNumber(int children) {
        this.sumChildrenNumber += children;
    }

    // IS OCCUPIED, MISCELLANEOUS

    public boolean isOccupiedByPlant(Vector2d position) {
        return this.plants.containsKey(position);
    }

    public boolean isOccupiedByAnimal(Vector2d position, int size) {
        return (this.animals.containsKey(position) && this.animals.get(position).size() >= size);
    }

    public boolean isOccupied(Vector2d position) {
        return isOccupiedByAnimal(position, 1) || isOccupiedByPlant(position);
    }

    public boolean isInJungle(Vector2d position) {
        return position.isInside(this.jungleCorner.x, this.jungleCorner.x + this.jungleSide,
                this.jungleCorner.y, this.jungleCorner.y + this.jungleSide);
    }

    // PLACE AND REMOVE OBJECT FROM MAP METHODS

    public void placeAnimal(Animal animal, boolean firstTime) {
        if (!isOccupiedByAnimal(animal.getPosition(), 1)) {
            this.animals.put(animal.getPosition(), new LinkedList<>());
        }
        this.animals.get(animal.getPosition()).add(animal);

        // stats tracking, only when initially placed, not when moving
        if (firstTime) {
            this.animalNumber++;
            this.sumEnergy += animal.getEnergy();

            if (this.genotypeCounter.get(animal.getGenotype()) == null) {
                this.genotypeCounter.put(animal.getGenotype(), 1);
            } else {
                this.genotypeCounter.merge(animal.getGenotype(), 1, Integer::sum);
            }
        }
    }

    public void placePlants() {
        // trying to get unoccupied spot until success or to (2 * area) failures (probably filled up area: steppe or jungle)
        // otherwise no plant is spawned, could be solved in similar way initializeMap is, but I don't think there's need to
        if (this.jungleSide > 0) {
            int iterations = 0;
            Vector2d rndPositionJungle = Vector2d.getRandomVector(jungleSide, jungleSide).add(this.jungleCorner);
            while (this.isOccupied(rndPositionJungle) && iterations < 2 * this.jungleSide * this.jungleSide) {
                rndPositionJungle = Vector2d.getRandomVector(jungleSide, jungleSide).add(this.jungleCorner);
                iterations++;
            }
            if (iterations < this.jungleSide * this.jungleSide) {
                Plant newPlant = new Plant(rndPositionJungle);
                this.plants.put(rndPositionJungle, newPlant);
                this.plantNumber++;
            }
        }

        int iterations = 0;
        Vector2d rndPositionSteppe = Vector2d.getRandomVector(width, height);
        while ((this.isOccupied(rndPositionSteppe) || isInJungle(rndPositionSteppe)) && iterations < 2 * this.width * this.height) {
            rndPositionSteppe = Vector2d.getRandomVector(width, height);
            iterations++;
        }
        if (iterations < this.width * this.height) {
            Plant newPlant = new Plant(rndPositionSteppe);
            this.plants.put(rndPositionSteppe, newPlant);
            this.plantNumber++;
        }
    }

    public void removeDeadAnimal(Animal animal, int era) {
        if (!this.animals.get(animal.getPosition()).contains(animal)) throw new IllegalArgumentException("Animal to remove already removed or missing from it's field");

        this.animals.get(animal.getPosition()).remove(animal);
        if (this.animals.get(animal.getPosition()).isEmpty()) this.animals.remove(animal.getPosition());
        animal.setDeathEra(era);

        // stats tracking
        this.deadAnimalsNumber++;
        this.sumLifespan += animal.getDeathEra() - animal.getBornEra();
        this.sumChildrenNumber -= animal.getChildrenNumber();
        this.animalNumber--;
        this.genotypeCounter.merge(animal.getGenotype(), 1, (a, b) -> a - b);
        if (this.genotypeCounter.get(animal.getGenotype()) == 0) this.genotypeCounter.remove(animal.getGenotype());
    }

    // OBSERVER

    public void animalPositionChanged(Animal animal, Vector2d oldPosition) {
        this.animals.get(oldPosition).remove(animal);
        if (this.animals.get(oldPosition).isEmpty()) this.animals.remove(oldPosition);
        this.placeAnimal(animal, false);
    }

    public void plantEaten(Vector2d position) {
        if (plants.containsKey(position)) {
        this.plants.remove(position);
        this.plantNumber--;
        }
    }
}