package evogen;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class GenotypeTest {
    @Test
    public void getPartOfGenotypeTest() {
        Genotype testGenotype = new Genotype(new int[]{0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7});

        int[] genotypePart = testGenotype.getPartOfGenotype(0.25, true);
        assertArrayEquals(genotypePart, new int[]{0,0,0,0,1,1,1,1});
    }
}
