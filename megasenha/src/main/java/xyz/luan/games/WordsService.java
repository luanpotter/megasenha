package xyz.luan.games;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class WordsService {

    private static final Map<String, List<String>> words = new HashMap<>();
    private static final Random RANDOM = new Random();

    static {
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(WordsService.class.getResourceAsStream("/words.db")))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(" ");
                String word = parts[0];
                String kind = parts[1];
                if (!words.containsKey(kind)) {
                    words.put(kind, new ArrayList<String>());
                }
                words.get(kind).add(word);
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static String getRandom(String kind) {
        return random(words.get(kind));
    }

    private static <T> T random(List<T> ts) {
        return ts.get(RANDOM.nextInt(ts.size()));
    }
}
