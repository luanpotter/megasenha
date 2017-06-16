package xyz.luan.games;

import io.yawp.commons.http.annotation.GET;
import io.yawp.repository.actions.Action;

import java.util.*;

public class GamesAction extends Action<Game> {

    @GET("balotar")
    public List<String> balotar() {
        return Collections.singletonList(WordsService.getRandom("v."));
    }

    @GET("megasenha")
    public Set<String> megasenha(Map<String, String> params) {
        int amount = Integer.parseInt(params.get("amount"));
        Set<String> results = new HashSet<>();
        while (results.size() < amount) {
            String kind = "s."; // TODO random kind
            results.add(WordsService.getRandom(kind));
        }
        return results;
    }
}
