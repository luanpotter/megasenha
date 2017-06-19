package xyz.luan.games;

import io.yawp.commons.http.annotation.GET;
import io.yawp.repository.actions.Action;

import java.util.*;

public class GamesAction extends Action<Game> {

    @GET("balotar")
    public List<String> balotar() {
        return Collections.singletonList(WordsService.getRandom("v."));
    }

    private static final List<Map.Entry<String, Integer>> probs = new ArrayList<>();

    static {
        probs.add(new AbstractMap.SimpleEntry<>("s.", 14));
        probs.add(new AbstractMap.SimpleEntry<>("v.", 8));
        probs.add(new AbstractMap.SimpleEntry<>("adj.", 7));
        probs.add(new AbstractMap.SimpleEntry<>("adv.", 4));
        probs.add(new AbstractMap.SimpleEntry<>("pron.", 3));
        probs.add(new AbstractMap.SimpleEntry<>("num.", 2));
    }

    private static final Integer SUM;

    static {
        int sum = 0;
        for (Map.Entry<String, Integer> i : probs) {
            sum += i.getValue();
        }
        SUM = sum;
    }

    private static String randomKind() {
        double rand = Math.random();
        for (Map.Entry<String, Integer> entry : probs) {
            double prob = (double) entry.getValue() / SUM;
            if (rand <= prob) {
                return entry.getKey();
            }
            rand -= prob;
        }
        return probs.get(probs.size() - 1).getKey();
    }

    @GET("megasenha")
    public Set<String> megasenha(Map<String, String> params) {
        int amount = Integer.parseInt(params.get("amount"));
        Set<String> results = new HashSet<>();
        while (results.size() < amount) {
            String kind = randomKind();
            results.add(WordsService.getRandom(kind));
        }
        return results;
    }
}
